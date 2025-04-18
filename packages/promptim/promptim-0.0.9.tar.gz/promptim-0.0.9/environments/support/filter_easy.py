from langchain_core.messages import AIMessage
import asyncio
import langsmith as ls


async def check_tool_call(expected: dict, tool_calls: list) -> dict:
    matching = next((tc for tc in tool_calls if tc["name"] == expected["name"]), None)
    if matching is None:
        return {"comment": "", "score": 0.0}
    args: dict = matching["args"]
    expected_args: dict = expected["args"]
    pf = {}
    for arg_name, arg_value in expected_args.items():
        if arg_name not in args:
            return {"comment": f"missing arg: {arg_name}", "score": 0.0}
        if isinstance(arg_value, str) and len(arg_value.split(" ")) > 5:
            # TODO: Use a judge LLM.
            pf[arg_name] = (
                arg_name in args
                and isinstance(args[arg_name], str)
                and len(args[arg_name].split(" ")) > 5
            )
            continue
        pf[arg_name] = arg_value == args[arg_name]
    score = sum(pf.values()) / len(pf)
    if score < 1.0:
        score_per_arg = ", ".join(
            f"{arg_name}: {score}" for arg_name, score in pf.items()
        )
        comment = f"Score per arg: {score_per_arg}"
    else:
        comment = "ok"
    return {"comment": comment, "score": score}


async def check_output(outputs: dict, reference_outputs: dict) -> dict:
    expected: dict = reference_outputs["output"]
    actual: AIMessage = outputs["output"]
    actual_tcs = actual.tool_calls or []

    coros = []
    for tc in expected.get("tool_calls", []) or []:
        coros.append(check_tool_call(tc, actual_tcs))

    results = await asyncio.gather(*coros)
    if not results:
        return {
            "key": "quality",
            "score": 1.0,
            "comment": "No tool calls found to evaluate.",
        }
    score = sum(r["score"] for r in results) / len(results)
    passed = score == 1.0
    comment = ", ".join(r["comment"] for r in results if r["comment"])
    comment = f"{'Passed' if passed else 'Failed'}: {comment}"

    return {"key": "quality", "score": score, "comment": comment}


client = ls.Client()
chain = client.pull_prompt(
    "langchain-ai/support-tool-use-demo:d6981321", include_model=True
)
dataset_name = "Simulations-6e9d"


async def main():
    # examples = client.list_examples(dataset_name=dataset_name)  # , limit=10)
    # notc = []
    # for e in examples:
    #     output = e.outputs["output"]
    #     if "tool_calls" not in output or len(output["tool_calls"]) == 0:
    #         notc.append(e)
    #         continue
    results = await client.aevaluate(
        chain, data=dataset_name, evaluators=[check_output]
    )



asyncio.run(main())

# async def main():
#     experiment = "kind-cat-98"
#     runs = list(client.list_runs(experiment_name=experiment, is_root=True))
#     print(f"Found {len(runs)} runs")

