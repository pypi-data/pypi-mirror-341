import asyncio
import json
import uuid
from typing import Any, Literal, cast

import langsmith as ls
from env_setup import TOOLS, TestCase, with_test_case
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langsmith import utils
from pydantic import BaseModel, Field, model_validator
from trustcall import create_extractor
from copy import deepcopy

with open("data.json") as f:
    USERS = json.load(f)["users"]
executor = utils.ContextThreadPoolExecutor(max_workers=1)

simulations = []
with open("scenarios.jsonl") as f:
    for line in f:
        line = line.strip()
        if line == "" or line.startswith("//") or line.startswith("#"):
            continue
        try:
            simulations.append(json.loads(line))
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON: |{line}|")


def ConversationStatus(reason: str, status: Literal["open", "on_hold", "closed"]):
    """Call this function if the support agent has fulfilled your request or if the conversation has gone on way longer than is tolerable.
    If the support team seems to indicate the conversation is over, call this function.
    """
    return status


def get_email(user_id):
    return USERS.get(user_id).get("email")


def get_name(user_id):
    name = USERS.get(user_id).get("name")
    return f"{name['first_name']} {name['last_name']}"


user_llm = ChatOpenAI(model="gpt-4o")
status_extractor = create_extractor(
    ChatOpenAI(model="gpt-4o-mini"),
    tools=[ConversationStatus],
    tool_choice="ConversationStatus",
)
example = {
    "user_id": "user_001",
    "email": "qeypgjka@argolangai",
}


class State(AgentState):
    data: dict
    classification: dict


class CorrectionState(State):
    advice: str


@ls.traceable
async def classify_conversation(messages):
    text = ChatPromptTemplate.from_messages(add_messages([], messages)).pretty_repr()
    uid = uuid.uuid4().hex
    text = f"""Classify the status of conversation {uid}:

<Conversation id={uid}>
{text}
</Conversation id={uid}>
"""
    result = await status_extractor.ainvoke(
        [
            {
                "role": "system",
                "content": "You are a conversation status classifier. If the conversation seems over (e.g., if the user just responds with thanks, etc.), call ConversationStatus with status 'closed'."
                " If the conversation is ongoing but the suport agent has indicated that they created a ticket and are waiting for a response, call ConversationStatus with status 'on_hold'."
                " Otherwise, call ConversationStatus with status 'open'.",
            },
            {"role": "user", "content": text},
        ]
    )
    response = result["responses"][0]
    return {"status": response.status, "reason": response.reason}


@ls.traceable
async def simulation(user_id: str, instructions: str, data: dict):
    email = get_email(user_id)
    name = get_name(user_id)
    support_agent = create_react_agent(
        ChatOpenAI(model="gpt-4o"),
        tools=TOOLS,
        state_schema=State,
        checkpointer=MemorySaver(),
        state_modifier="You are a support agent for LangChain's products. "
        "First, classify the request before doing any actions. Then, use the tools provided to resolve the request.",
    )
    support_agent.name = "Support Agent"
    messages = [
        {
            "role": "system",
            "content": "You are role playing as a user of LangChain's products so that LangChain can help train their new support trainee (aka support agent) and test their quality and performance."
            f" In this simulation, your name is {name}, and your email is {email}."
            "  DO NOT reveal that you are role playing or that you are a simulation to the support agent. This must be a natural conversation between you and the support agent, though you may be requested to be more obstinate or troublesome to help us ensure the quality of our support system."
            " The first message will contain instructions for you to follow, then every response thereafter will be from the support agent. Play the personality and role provided in the first user mesage.",
        },
        {"role": "user", "content": instructions, "name": "simulation_manager"},
    ]
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    ix = 0
    thread_classification = None
    collected_checkpoints = {}
    while True:
        with ls.trace(
            "User",
            inputs={"messages": messages, "step": len(messages)},
            metadata={"which": "user", "step": ix},
        ) as rt:
            user_message = await user_llm.ainvoke(messages)
            rt.add_outputs({"output": user_message})
        user_message.name = name.replace(" ", "_").strip()
        messages.append(user_message)
        if ix > 0:
            classification = await classify_conversation(messages)
            if classification["status"].lower() in {"closed", "on_hold"}:
                break
        run_id = str(uuid.uuid4())
        state = None
        with ls.tracing_context(metadata={"which": "support", "step": ix}):
            try:
                async for chunk in support_agent.astream(
                    {
                        "messages": [{"role": "user", "content": user_message.content}],
                        "data": data,
                        "classification": thread_classification,
                    },
                    config={**config, "run_id": run_id},
                    stream_mode="debug",
                ):
                    if chunk["type"] != "checkpoint":
                        continue
                    chunk_messages = chunk["payload"]["values"]["messages"]
                    if not chunk_messages:
                        continue
                    if chunk_messages[-1].type == "ai":
                        # Just did an AI message. About to execute.
                        # This will potentialy be one to re-simulate
                        msg_id = chunk_messages[-1].id
                        payload = deepcopy(chunk["payload"]["values"])
                        messages = payload["messages"][
                            :-1
                        ]  # Up until that last AI message
                        payload["messages"] = messages
                        if msg_id not in collected_checkpoints:
                            collected_checkpoints[msg_id] = payload
            except Exception as e:
                print(f"Error in simulation {ix}: {e}")
                break

            state = (await support_agent.aget_state(config))[0]
        data = state["data"]
        thread_classification = state["classification"]
        messages.append(
            {
                "role": "user",
                "name": "support_agent",
                "content": state["messages"][-1].content,
            }
        )
        ix += 1
    return messages, collected_checkpoints, state


async def simulate_test_case(test_case: TestCase):
    async with with_test_case(test_case) as test_data:

        with ls.trace("Simulator", project_name="Simulations") as rt:

            def purl():
                print(rt.get_url(), flush=True)

            executor.submit(purl)
            convo_messages, collected_checkpoints, state = await simulation(
                test_case["user_id"],
                test_case["instructions"],
                test_data,
            )
            ideal_states = await detect_and_correct(collected_checkpoints, state)
    return ideal_states


def prepare_messages(state: CorrectionState):
    system = (
        "You are a support agent for LangChain's products. "
        "First, classify the request before doing any actions. Then, use the tools provided to resolve the request."
        " The system will provide additional advice on your next step."
    )
    return [
        {"role": "system", "content": system},
        *state["messages"],
        {"role": "system", "content": "Advice: " + state["advice"]},
    ]


REVISION_AGENT = create_react_agent(
    ChatOpenAI(model="gpt-4o"),
    tools=TOOLS,
    state_schema=CorrectionState,
    state_modifier=prepare_messages,
    interrupt_before=["tools"],
)
REVISION_AGENT.name = "Oracle Agent"


def format_loop(chunks, n):
    def format_msg(msg):
        data = {"content": msg.content}
        if getattr(msg, "tool_calls", None):
            data["tool_calls"] = msg.tool_calls
        status = f' status="{msg.status}"' if getattr(msg, "status", None) else ""
        role = msg.type
        if role == "ai":
            role = "assistant"
        if role == "human":
            role = "user"
        data["role"] = role
        name = f' name="{msg.name}"' if msg.name else ""
        return f"""<{role}{name}{status}>
{json.dumps(data)}
</{role}>"""

    cycle = "\n".join([format_msg(msg) for msg in chunks])
    return f"""<agent_step n={n}>
{cycle}
</agent_step>"""


def format_turn(steps: list[str], ix: int):
    turn = "\n".join(steps)
    return f"""<conversation_turn n={ix}>
{turn}
</conversation_turn>"""


def format_messages(
    messages: list[BaseMessage],
) -> tuple[str, list[int], dict[int, str]]:
    texts = []
    chunks = []
    n = 0
    known_errors = []
    step_map = {}
    turns = []
    turn_ix = 0
    for msg in messages:
        if msg.type == "ai":
            if any([m.type == "ai" for m in chunks]):
                msg_id = next(m for m in chunks if m.type == "ai").id
                texts.append(format_loop(chunks, n))
                step_map[n] = msg_id
                chunks = []
                n += 1
        if getattr(msg, "status", None) == "error":
            known_errors.append(n)
        chunks.append(msg)
        if msg.type == "human" and texts:
            turns.append(format_turn(texts, turn_ix))
            turn_ix += 1

    if chunks:
        msg_id = next(m for m in chunks if m.type == "ai").id
        step_map[n] = msg_id
        texts.append(format_loop(chunks, n))
    if texts:
        turns.append(format_turn(texts, turn_ix))

    txt = "\n".join(turns)
    return (
        f"""<conversation>
{txt}
</conversation>""",
        known_errors,
        step_map,
    )


@ls.traceable
async def detect_and_correct(states: dict[str, dict], final_state: dict):
    messages = final_state["messages"]
    text, known_errors, step_map = format_messages(messages)

    # 2. Evaluate outcome & trajectory.
    # You could only pick the first error, assuming that everything after that is downstream of the error.
    # But we'll actually just get all.
    # 3. Flag each step T that's erroneous.
    # 4. Give advice on how to fix it.
    # 5. Fork step T - 1; update state with the advice. Then re-run step T - 1.
    # 6. Assume the outcome is the correct one now.
    class MarkIncorrect(BaseModel):
        agent_step_index: int = Field(
            description="agent_step index that needs correction."
        )
        reason_for_failure: str = Field(
            description="Provide justification for why the step is incorrect or could be skipped."
            " Cite why (e.g., the tool returned an error or didn't return the desired information; subsequent steps needed to backtrack, etc.)."
            " This should not be behavioral (like 'the agent should have responded here') but factual"
            " (fixing tool errors, or if the agent made a mistake that revealed itself later in the conversation)."
        )
        advice: str = Field(
            description="Provide advice to the agent that would make it fix take the optimal step here."
            " Tell the agent the oracle correct answer, such as the tool(s) to call and with what values and why."
        )

        @model_validator(mode="before")
        @classmethod
        def validate_index(cls, data: Any) -> Any:
            assert data["agent_step_index"] < len(
                step_map
            ), f"Index {data['agent_step_index']} is out of range {len(step_map)}"
            return data

    known_errors_str = (
        f" Known erroneous steps: {', '.join(map(str, known_errors))}."
        if known_errors
        else ""
    )

    class EvaluateTrajectory(BaseModel):
        f"""Submit corrections for any agent steps that were incorrect or sub-optimal, one MarkCorrect per step.{known_errors_str}"""

        failed_steps: list[MarkIncorrect]

        @model_validator(mode="after")
        @classmethod
        def validate_failed_steps(cls, data: Any) -> Any:
            if known_errors:
                marked_steps = {step.agent_step_index for step in data.failed_steps}
                missing = set(known_errors) - marked_steps
                if missing:
                    raise ValueError(f"Missing feedback for known errors: {missing}")
            return data

    detector = create_extractor(
        ChatOpenAI(model="gpt-4o"),
        tools=[EvaluateTrajectory],
        tool_choice="EvaluateTrajectory",
    )
    result = await detector.ainvoke(
        {
            "messages": [
                {
                    "role": "system",
                    "content": "You are working as a process reward model that"
                    " evaluates the trajectory of a conversation to determine if"
                    " any of the agent's actions were incorrect. Focus on"
                    " Note that the agent's first step MUST BE to"
                    " classify the conversation. Actions are incorrect if they result in an error, are obviously wrong, "
                    "or if later actions by the agent show that"
                    " they need to be undone or re-executed in a correct way."
                    " Submit your response via EvaluateTrajectory. If the agents' steps were"
                    f" all correct, simply return an empty list. Do not fill out any advice for steps that are already correct. {known_errors_str}",
                },
                {
                    "role": "user",
                    "content": "Evaluate the trajectory of this conversation:\n\n"
                    + text,
                },
            ],
        }
    )
    evaluation = cast(EvaluateTrajectory, result["responses"][0])
    starting_states = []
    for failed in evaluation.failed_steps:
        try:
            msg_id = step_map[failed.agent_step_index]
            failed_state = states[msg_id]
            print(
                "STEP INDEX ",
                failed.agent_step_index,
                msg_id,
                len(failed_state["messages"]),
            )
            starting_states.append({**failed_state, "advice": failed.advice})
        except KeyError as e:
            print("No state for index", failed.agent_step_index, msg_id, e)
            pass
    if starting_states:
        ideal_states = await REVISION_AGENT.abatch(starting_states)
        generated = [state["messages"][-1] for state in ideal_states]
        return [
            {"inputs": state, "outputs": {"output": generated[i]}}
            for i, state in enumerate(starting_states)
        ]
    return []


async def process_simulation(simulation, ix, ds, semaphore, client):
    async with semaphore:
        try:
            ideal_states = await simulate_test_case(simulation)
            if ideal_states:
                client.create_examples(
                    inputs=[state["inputs"] for state in ideal_states],
                    outputs=[state["outputs"] for state in ideal_states],
                    metadata=[
                        {
                            "scenario": ix,
                            "user_id": simulation["user_id"],
                            "email": simulation["email"],
                            "category": simulation["category"],
                        }
                        for _ in ideal_states
                    ],
                    dataset_id=ds.id,
                )
        except Exception as e:
            print(f"Error in simulation {ix}: {e}")
            return None
    return ideal_states


async def main():
    global simulations
    import argparse

    parser = argparse.ArgumentParser()
    ds = "Simulations-6e9d"
    uid = uuid.uuid4().hex[:4]
    dataset = f"Simulations-{uid}"
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--dataset", default=dataset)

    args = parser.parse_args()
    c = ls.Client()
    if c.has_dataset(dataset_name=args.dataset):
        ds = c.read_dataset(dataset_name=args.dataset)
    else:
        ds = c.create_dataset(dataset_name=args.dataset)

    if args.start:
        simulations = simulations[args.start :]

    print(f"Creating dataset {ds.url}")

    sem = asyncio.Semaphore(5)

    tasks = [
        asyncio.create_task(process_simulation(simulation, ix, ds, sem, c))
        for ix, simulation in enumerate(simulations, start=args.start)
    ]

    ix = 0
    for coro in asyncio.as_completed(tasks):
        await coro
        print(f"Finished {ix}/{len(tasks)}", end="\r")
        ix += 1
        pass

    return []


asyncio.run(main())

# The idea is we're doing a PRM over the steps.
# 2 things: detection & resolution
# Detection is of two types:
# Explicit errors: (look for status=error) in a tool message
# Implicit errors: using an LLM, try to detect inefficiencies in the agen'ts actions.
# - Could they have skipped a step?
# - Should they have used a different tool or different tool arguments?
# - etc....
# The challenging thing is **resolution**. We want to add ground truth to the data.
# For inputs, we want to have the full simulator state.
# For outputs, we want to **correct** the output. I thinkt he easiest way to do this is to
# I think the easiest way to do this is to take the failing state (inputs) and give advice/ instrucitons on what the bot should have done
# Then RE-RUN THAT STEP!!!
# Then check if the state has changed. If it has, the instruction is incorrect.

# So I'im gonna have basically two componenets
# Error finder
# Error adviser
# and then re-runt he step with advice. NEHHHHH?

# So really it's
# 1. Run the simulation
