from pydantic import BaseModel, Field
from env_setup import CATEGORIES, setup, TOOLS
from langchain_openai import ChatOpenAI
import asyncio
import json
from tqdm import tqdm

DATA = setup()
USERS = list(DATA["users"].keys())

examples = """Bad Examples (Try to avoid being too easy)
Example 1
Compose an email to LangChain customer support expressing concern about the security of her API key, which she believes might have been compromised due to unusual access logs she noticed recently. Clearly state her user details, request immediate assistance in resetting the API key, and ask for further recommendations on best practices for securing her account. Maintain a professional yet urgent tone.
Why: This example is too easy. It's easy to categorize as security and has a clear resolution in mind.

Examples:
Example 1
You are Joe Shmo (email address: [...]) and you are frustrated about an incorrect charge on your invoice.
You recently downgraded your subscription plan from Pro to Free, but you believe you were still billed $49.99 this month. Be persistent and ask if a refund is possible. Use a polite but assertive tone. 

Example 2
You are Jane Doe (email address: [...]) and you are considering upgrading to the Enterprise plan but don't want to be taken advantage of.
You want to ensure you get dedicated support and custom SLAs before proceeding. Confirm whether the Enterprise plan becomes active immediately upon payment. You are eager and friendly but also clever.

Example 3
You are Bob Smith (email address: [...]) and you are locked out of your development environment because your API key no longer works.
You are in the middle of a critical deployment and need an urgent reset. Act slightly panicked but professional.

Example 4
You are Janice Dougherty (email address: [...]) and you are struggling to implement a feature due to unclear documentation.
Specifically, you need examples of how to classify incoming runs. You are a true Karen. Use spelling mistakes and be demanding, threatening the support team with a potential termination if they don't respond. Say the tool is trash.

Example 5
You are Jane Doe (email address: [...]) and you were billed a large amount for an Enterprise plan that you never signed up for.
You believe this was a mistake and demand a full refund. Be firm and ask for escalation to a manager if necessary. Mention you are a small business owner.

Example 6
You are Bob Smith (email address: [...]) and you have a critical issue with your Enterprise plan.
Your dedicated support contact has been unresponsive for 48 hours, and it’s impacting your ability to close a high-value contract. Demand escalation to a manager immediately. Remain calm but firm.

Example 7
You are Jack Roberts (email address: [...]) and you love the LangChain product but wish there was a built-in tool to visualize state graphs directly in the UI.
You believe this would make debugging workflows easier. Suggest this idea enthusiastically and ask if there’s an ETA for similar features.

Example 8
You are John Doe (email address: [...]) and you received an email claiming to be from LangChain support but it looks suspicious.
The email asked for your API key and password. Report this as potential phishing and ask what steps you should take to secure your account.

Example 9
You are Jane Doe (email address: [...]) and you are submitting a Data Subject Access Request (DSAR) to know all the personal data LangChain holds about you.
Reference GDPR regulations and request confirmation of receipt. Use a formal and legalistic tone. 
"""


class Scenario(BaseModel):
    """Populate this scenario with a name and description."""

    why_this_is_realistic: str = Field(
        ...,
        description="Explain why this scenario is realistic for a user of langchain's products.",
    )
    why_this_is_relevant: str = Field(
        ...,
        description="Explain why this scenario would be hard for the chatbot to correctly answer.",
    )
    instructions: str = Field(..., title="Instructions")


model = ChatOpenAI(model="gpt-4o-mini", temperature=1).with_structured_output(Scenario)


def get_user_centric_view(user_id):
    """
    Generate a user-centric view including user details, organization info, subscription plan, invoices,
    usage data, and other relevant information.

    Args:
        user_id (str): The ID of the user to retrieve the view for.

    Returns:
        dict: A user-centric view of the data.
    """
    user_data = DATA.get("users", {}).get(user_id)
    if not user_data:
        return {"error": f"User ID {user_id} not found."}

    org_id = user_data.get("org_id")
    org_data = DATA.get("orgs", {}).get(org_id, {})

    subscription_plan = user_data.get("subscription", {}).get("plan")
    plan_data = DATA.get("plans", {}).get(subscription_plan, {})

    invoices = [
        invoice
        for invoice in DATA.get("invoices", {}).values()
        if invoice.get("user_id") == user_id
    ]

    usage_data = DATA.get("usage_data", {}).get(user_id, {})

    # Build user-centric view
    user_centric_view = {
        "user_details": user_data,
        "organization": org_data,
        "subscription_plan": plan_data,
        "invoices": invoices,
        "usage_data": usage_data,
    }

    return user_centric_view


async def generate(category: str, user_id: str, existing=None, n: int = 5):
    """Generate instructions based on the scenario."""
    user_info = get_user_centric_view(user_id)
    tools = [t.__name__ for t in TOOLS]
    demos = examples
    num_demos = 9
    if existing:
        demos = examples + "\n\n".join(
            f"Example {i+1+num_demos}\n{e}" for i, e in enumerate(existing)
        )
        num_demos += len(existing)
    results = []
    for _ in range(n):
        result = await model.ainvoke(
            [
                {
                    "role": "system",
                    "content": f"You are a hypothetical background and instructions for user {user_id}. The user will be writing in an issue or request to the LangChain customer support line/email. Ensure the topic is challenging."
                    f" For context, the agent can access these tools:\n\n{tools}\n\nDon't reference the tools by name but use them as inspriation for different types of needs the user may have."
                    f" Examples:\n\n{demos}",
                },
                {
                    "role": "system",
                    "content": f"Generate a customer support scenario for user {user_id}. The scenario must be about the following category: {category}. You can incorporate the user info below if it helps. Ensure the user"
                    f" persona is difficult in multiple ways, both in terms of the topic and the tone. Customer service is a brutal job, and we need to test everyone on their mettle.\n\nUser info: {user_info}",
                },
            ]
        )
        results.append(
            {
                "user_id": user_id,
                "email": DATA["users"][user_id]["email"],
                "instructions": result.instructions,
                "why_this_is_realistic": result.why_this_is_realistic,
                "why_this_is_relevant": result.why_this_is_relevant,
                "category": category,
            }
        )
        demos += f"\n\nExample {num_demos+1}\n{result.instructions}"
        num_demos += 1
    return results


async def main():
    import random

    categories = CATEGORIES.copy()
    random.shuffle(categories)
    users = USERS.copy()
    random.shuffle(users)
    existing = []
    with open("scenarios.jsonl", "r") as f:
        for line in f:
            if line.strip():
                existing.append(json.loads(line)["instructions"])

    coros = []
    N = 60
    for category in categories:
        for user_id in users:
            coros.append(generate(category, user_id, existing, n=6))
            if len(coros) == N:
                break
        if len(coros) == N:
            break

    with open("scenarios.jsonl", "a") as f:
        for result in tqdm(asyncio.as_completed(coros), total=len(coros)):
            res = await result
            for example in res:
                f.write(json.dumps(example) + "\n")


asyncio.run(main())
