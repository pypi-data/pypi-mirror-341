import argparse
import asyncio
import json
import statistics

import langsmith as ls
from langchain_core.load import load
from langmem import create_prompt_optimizer
from langmem.prompts.stateless import Prompt, PromptMemoryMultiple

from promptim.__main__ import _load_task
from promptim.types import PromptWrapper


def _score(results):
    all_scores = []
    for result in results:
        for res in result["evaluation_results"]["results"]:
            if res.score is not None:
                all_scores.append(res.score)

    return statistics.mean(all_scores)


def _get_messages(run):
    llm_run = None
    runs = [run]
    while runs:
        run = runs.pop()
        if run.run_type != "llm":
            runs.extend(run.child_runs or [])
        else:
            llm_run = run
            break
    assert llm_run
    start = load(llm_run.inputs["messages"][0])
    try:
        out = load(llm_run.outputs["generations"][0][0]["message"])
    except:
        breakpoint()
        raise
    return [*start, out]


def _get_feedback(result):
    all_fb = {}
    outputs = result["example"].outputs
    for res in result["evaluation_results"]["results"]:
        all_fb[res.key] = f"{res.score} | {res.comment}"
    if outputs:
        all_fb["expected"] = outputs

    return all_fb


def _get_convos(results):
    all_convos = [_get_messages(row["run"]) for row in results]
    feedbacks = [_get_feedback(row) for row in results]
    return list(zip(all_convos, feedbacks))


async def run_method(config_path: str, model: str, epochs: int, algo: str):
    task, config, _ = _load_task(config_path)
    with open(config_path) as f:
        config = json.load(f)
    if algo == "PromptMemory":
        optimizer = PromptMemoryMultiple(model).areflect
    else:
        optimizer = create_prompt_optimizer(model)
    client = ls.Client()
    dataset = config["dataset"]
    if dataset.startswith("http"):
        ds = client.clone_public_dataset(dataset)
        dataset = ds.name
    train = list(client.list_examples(dataset_name=dataset, splits=["train"]))
    dev = list(client.list_examples(dataset_name=dataset, splits=["dev"]))
    test = list(client.list_examples(dataset_name=dataset, splits=["test"]))
    best_prompt_wrapper = PromptWrapper.from_config(task.initial_prompt)
    best_prompt_wrapper.load()
    best_prompt = Prompt(
        name="prompt",
        prompt=best_prompt_wrapper.get_prompt_str(),
        update_instructions="Update only what is necessary.",
        when_to_update="always",
    )
    best_score = -1

    system = task.get_prompt_system(best_prompt_wrapper)

    async def predict(inputs: dict):
        return await system(best_prompt_wrapper._cached, inputs)

    for epoch in range(epochs):
        print(f"Epoch {epoch}")
        # Forward
        results = [
            r
            async for r in (
                await ls.aevaluate(
                    predict,
                    data=train,
                    evaluators=task.evaluators,
                    max_concurrency=None,
                )
            )
        ]
        train_score = _score(results)
        print(f"Training score: {train_score}")

        # "Compute loss"
        # Just format the results
        trajectories = _get_convos(results)

        # "Backward"
        updated = await optimizer(
            trajectories,
            best_prompt,
        )
        candidate = PromptWrapper.from_prior(best_prompt_wrapper, updated)

        # Check performance on dev
        async def predict_candidate(inputs: dict):
            return await system(candidate._cached, inputs)

        dev_results = [
            r
            async for r in (
                await ls.aevaluate(
                    predict_candidate,
                    data=dev,
                    evaluators=task.evaluators,
                    max_concurrency=None,
                )
            )
        ]
        dev_score = _score(dev_results)
        if dev_score > best_score:
            print("New best")
            print(dev_score)
            best_score = dev_score
            best_prompt_wrapper = candidate
            print(best_prompt_wrapper.get_prompt_str_in_context())
        else:
            print("Failed to improve; retaining old best")
            print(dev_score)

    # Check performance on test
    test_results = [
        r
        async for r in await ls.aevaluate(
            predict, data=test, evaluators=task.evaluators, max_concurrency=None
        )
    ]
    test_score = _score(test_results)
    print("Test score: ", test_score)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config.json")
    parser.add_argument("--model", type=str, default="claude-3-5-sonnet-20241022")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--algo", type=str, default="PromptMemory")
    args = parser.parse_args()
    asyncio.run(run_method(args.config, args.model, args.epochs, args.algo))
