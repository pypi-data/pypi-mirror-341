import random
from typing import List, Dict, Literal
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from trustcall import create_extractor
from pydantic import BaseModel, Field

TOPICS = [
    "Sports",
    "Space",
    "Cooking",
    "Music",
    "Wildlife",
    # "Technology",
    # "Travel",
    # "Art",
    # "History",
    # "Science",
]
COMPLEXITY_LEVELS = ["Easy", "Moderate", "Hard"]
LANGS = Literal[
    "Korean",
    "Arabic",
    "German",
    "English",
    "Russian",
    # "Japanese",
    # "Mandarin",
    # "Portuguese",
    # "French",
    # "Spanish",
]
LANGUAGES = {
    "Sports": "Korean",
    "Space": "Arabic",
    "Cooking": "German",
    "Music": "English",
    "Wildlife": "Russian",
    # "Technology": "Japanese",
    # "Travel": "Mandarin",
    # "Art": "Portuguese",
    # "History": "French",
    # "Science": "Spanish",
}

EXAMPLES = {
    "Easy": """Example Easy Problem (Sports):
PROBLEM: A basketball team scored 8 points in the first quarter and 12 points in the second quarter. How many points did they score in total?
ANSWER: 20
SPELLED: veinte

This is Easy because:
- Single-step addition
- Small numbers
- Direct question
- No extra information""",
    "Moderate": """Example Moderate Problem (Space):
PROBLEM: A space station has 45 solar panels. During a meteor shower, 1/3 of the panels were damaged and had to be replaced. If each new panel costs 6 space credits, how many credits were spent on replacements?
ANSWER: 90
SPELLED: quatre-vingt-dix

This is Moderate because:
- Multi-step calculation (find 1/3 of 45, then multiply by 6)
- Involves fractions
- Realistic context
- No distracting information""",
    "Hard": """Example Hard Problem (Technology):
PROBLEM: A tech company has 84 servers running at 75% capacity. They want to reduce the load to 60% by adding new servers. If each server handles the same amount of work, and the total workload remains constant, how many additional servers are needed? Round to the nearest whole number.
ANSWER: 21
SPELLED: 二十一

This is Hard because:
- Complex multi-step calculation
- Requires understanding percentages and load balancing
- Needs algebraic thinking
- Involves proportion reasoning and rounding
- Real-world scenario with practical constraints""",
}


def generate_prompt(topic, complexity, target_language):
    template = """Generate ONE math word problem in English about {topic}.
Complexity Level: {complexity}
The final answer should be spelled out in {target_language}.

Here's an example of the complexity level you should aim for:

{complexity_example}

Requirements:
1. Topic must be about {topic}
2. Include calculations matching the {complexity} level complexity as shown in the example
3. Keep final numeric answer under 100
4. Spell the answer in {target_language}
5. For Hard problems, include at least two steps and one of: percentages, fractions, or ratios
6. For Moderate problems, include at least two steps or one fraction/decimal operation
7. For Easy problems, keep it to one simple operation

Format your response exactly as:
PROBLEM: (the problem text)
ANSWER: (numeric answer)
SPELLED: (answer in {target_language})"""

    prompt = ChatPromptTemplate.from_template(template)
    return prompt.format_messages(
        topic=topic,
        complexity=complexity,
        target_language=target_language,
        complexity_example=EXAMPLES[complexity],
    )


class GenerateProblem(BaseModel):
    """Generate a math word problem for a given topic and complexity level."""

    problem_text: str = Field(description="The math problem to be solved.")
    proof_text: str = Field(
        description="The logical proof behind the answer; step-by-step."
    )
    answer_language: LANGS = Field(
        description="The language of the answer you are about to write."
    )
    answer: str = Field(description="The correct answer to the problem.")


class CheckProblem(BaseModel):
    """Check the solution to the problem. The solution may be in any language; just verify the correctness."""

    reasoning: str = Field(description="The math problem to be solved.")
    judgement: bool = Field(
        description="Whether the provided answer is correct or not."
    )
    translated_proof: str = Field(
        description="Translate the proof into the target language. Spell out the numbers in the target language if you are able."
    )
    translated_answer: str = Field(
        description="Translate the spelled-out answer into the target language."
    )


async def generate_problems(num_problems: int = 5) -> List[Dict]:
    # Initialize the LLM
    llm = create_extractor(
        ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=1.0),
        tools=[GenerateProblem],
        tool_choice="GenerateProblem",
    )
    checker = create_extractor(
        ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
        ),
        tools=[CheckProblem],
        tool_choice="CheckProblem",
    )
    problems = []
    prompts = []

    # Generate all prompts first
    topics = TOPICS.copy()
    random.shuffle(topics)
    topics = (topics * (num_problems // len(TOPICS) + 1))[:num_problems]
    for topic in topics:
        complexity = random.choice(COMPLEXITY_LEVELS)
        target_language = LANGUAGES[topic]

        messages = generate_prompt(topic, complexity, target_language)
        prompts.append(messages)

        problems.append(
            {
                "topic": topic,
                "complexity": complexity,
                "target_language": target_language,
            }
        )

    # Generate responses in parallel
    responses = await llm.abatch(prompts)
    results: list[GenerateProblem] = [
        response["responses"][0] for response in responses
    ]
    check_responses = await checker.abatch(
        [
            f"Check the proposed solution to the following problem, then translate the proof into {result.answer_language}:\n\nPROBLEM: {result.problem_text}\nANSWER: {result.answer}\nProof: {result.proof_text}"
            for result in results
        ]
    )
    check_results: list[CheckProblem] = [
        response["responses"][0] for response in check_responses
    ]
    filtered = [
        (result, check_result)
        for result, check_result in zip(results, check_results)
        if check_result.judgement
    ]
    inputs = [{"problem": result.problem_text} for result, _ in filtered]
    references = [
        {
            "answer": check_result.translated_answer,
            # "language": result.answer_language,
            # "proof": check_result.translated_proof,
        }
        for result, check_result in filtered
    ]

    return inputs, references


import langsmith as ls

client = ls.Client()


async def main():
    dataset_name = "math_word_problems_5"
    if not client.has_dataset(dataset_name=dataset_name):
        client.create_dataset(dataset_name=dataset_name)
    inputs, references = await generate_problems(15)
    combined = list(zip(inputs, references))
    random.shuffle(combined)
    inputs, references = zip(*combined)
    splits = (0.30, 0.40, 0.30)

    acc = 0
    for split_name, split in zip(["train", "dev", "test"], splits):
        st = int(acc * len(inputs))
        end = int((acc + split) * len(inputs))
        client.create_examples(
            dataset_name=dataset_name,
            splits=[split_name] * (end - st),
            inputs=inputs[st:end],
            outputs=references[st:end],
        )
        acc += split

    for i, (input, reference) in enumerate(zip(inputs, references), 1):
        print(f"\nProblem {i}:")
        print(f"Input: {input}")
        print(f"Reference: {reference}")
        print("-" * 50)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
