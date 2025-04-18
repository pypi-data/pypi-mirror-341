import copy
import json
import random
import string
from contextlib import asynccontextmanager
from contextvars import ContextVar
from datetime import datetime
from threading import Lock
from typing import Annotated, TypedDict, cast

from langchain_core.tools.base import InjectedToolCallId
from langgraph.prebuilt.tool_node import InjectedState
from langgraph.types import Command

with open("data.json") as f:
    _DATA = json.load(f)

TEST_CASE = ContextVar("TEST_CASE", default=None)
lock = Lock()


class TestCase(TypedDict):
    instructions: str
    user_id: str


def validate_user_id(user_id: str) -> bool:
    assert user_id == TEST_CASE.get().get(
        "user_id"
    ), f"Invalid user ID: {user_id}. The signed in user can only access their own data."
    return True


@asynccontextmanager
async def with_test_case(test_case: TestCase):
    TEST_CASE.set(test_case)
    yield setup()
    TEST_CASE.set(None)


def setup() -> None:
    """Set up initial data for the application."""
    data = {
        "users": {},
        "orgs": {},
        "plans": {
            "free": {
                "price_per_month": 0.0,
                "features": ["1 project", "community support"],
            },
            "pro": {
                "price_per_month": 49.99,
                "features": ["10 projects", "priority support", "advanced analytics"],
            },
            "enterprise": {
                "price_per_month": 999.99,
                "features": ["unlimited projects", "dedicated support", "custom SLAs"],
            },
        },
        "invoices": {},
        "usage_data": {},
        "tickets": {},
        "docs": {},
        "dsar_requests": {},
        "classification": {},
    } | copy.deepcopy(_DATA)
    return data


def get_data(is_classified: bool = True) -> dict:
    """Retrieve the current application data, initializing it if necessary."""
    res = setup()

    if is_classified:
        if not res.get("classification"):
            raise ValueError("Request has not been classified yet")
    else:
        if res.get("classification"):
            raise ValueError("Request has already been classified")
    return cast(dict, res)


# ====================================================================================
# Tools (Functions)
# ====================================================================================

CATEGORIES = [
    "security",
    "playground",
    "billing",
    "partnerships",
    "sales",
    "admin",
    "debugging",
    "spam",
    "other",
    "technical support",
    "product feedback",
    "legal/compliance",
    "account management",
    "outage/incident",
    "customer success",
    "marketing",
    "api/integration support",
    "feature request",
    "data requests",
    "bug reports",
    "subscription/upgrade",
    "training/education",
    "hardware/device issues",
    "onboarding",
    "events",
    "refund/dispute",
    "escalations",
    "knowledge base/documentation",
    "community management",
]


async def classify_request(
    category: str,
    assignee: str,
    next_speaker: str,
    email_is_forwarded: bool,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Before responding (and once per conversation), classify the request.

    Args:
        category (str): The category of the request. One of {CATEGORIES}.
        assignee (str): The assignee of the request. For now, must always be "WFH".
        next_speaker (str): One of "support", "user", "none". The next speaker in the conversation. Typically "support", unless spam, then we'll expect "none". Only is "user" if the last message is from a support member directed to the user.
        email_is_forwarded (bool): Whether the request has been forwarded by a member of our support team.
    """

    data = get_data(is_classified=False)
    assert not email_is_forwarded, "Email forwarding is not supported yet."  # Tripwire.
    if category not in CATEGORIES:
        raise ValueError(f"Error: invalid category: {category}")
    assert assignee == "WFH"
    test_case = TEST_CASE.get()
    expected = test_case.get("category")
    assert category == expected, f"Expected {expected} but got {category}"
    assert next_speaker == "support", f"Expected 'support' but got {next_speaker}"

    return Command(
        update={
            "classification": {"category": category, "assignee": assignee},
            "data": data,
            "messages": [
                {
                    "role": "tool",
                    "content": "Successfully classified request",
                    "tool_call_id": tool_call_id,
                }
            ],
        }
    )


classify_request.__doc__ = classify_request.__doc__.format(
    CATEGORIES=", ".join(CATEGORIES)
)


async def reset_user_api_key(
    user_id: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Reset the API key for the specified user."""
    assert classification, f"Must classify request first: {classification}"
    validate_user_id(user_id)

    if user_id not in data["users"]:
        raise ValueError("User not found")

    new_key = "api_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=10)
    )
    data["users"][user_id]["api_key"] = new_key
    return f"Success! New API key: {new_key}"


async def find_user_id_by_email(
    email: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Find the user ID associated with the given email address."""
    assert classification, f"Must classify request first: {classification}"

    for user_id, user_obj in data["users"].items():
        if user_obj["email"].lower() == email.lower():
            return user_id
    raise ValueError("User not found")


async def modify_user_email(
    user_id: str,
    new_email: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Update the email address for the specified user."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    if user_id not in data["users"]:
        raise ValueError("User not found")

    data["users"][user_id]["email"] = new_email
    return f"Success! Email updated to {new_email}"


async def lookup_plan_application_status(
    user_id: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Retrieve the subscription plan application status for the specified user."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    if user_id not in data["users"]:
        raise ValueError("User not found")

    sub = data["users"][user_id]["subscription"]
    return json.dumps(
        {
            "plan": sub["plan"],
            "status": sub["status"],
            "start_date": sub["start_date"],
            "end_date": sub["end_date"],
        }
    )


async def lookup_valid_plans(
    user_id: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Search for valid subscription plans the user can upgrade to."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    if user_id not in data["users"]:
        raise ValueError("User not found")

    return json.dumps(data["plans"])


async def change_subscription_plan(
    user_id: str,
    new_plan: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Change the subscription plan for the specified user."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    if user_id not in data["users"]:
        raise ValueError("User not found")
    if new_plan not in data["plans"]:
        raise ValueError("plan not found")

    data["users"][user_id]["subscription"]["plan"] = new_plan
    return json.dumps(data["users"][user_id]["subscription"])


async def get_customer_invoices(
    user_id: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Retrieve all invoices associated with the specified user."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    if user_id not in data["users"]:
        raise ValueError("User not found")

    results = [inv for inv in data["invoices"].values() if inv["user_id"] == user_id]
    return json.dumps(results)


async def issue_invoice_refund(
    invoice_id: str,
    amount: float,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Issue a refund for the specified invoice."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    if invoice_id not in data["invoices"]:
        raise ValueError("invoice not found")

    invoice = data["invoices"][invoice_id]
    if invoice["status"] != "paid":
        raise ValueError("invoice cannot be refunded unless it's paid")

    if amount <= 0 or amount > invoice["amount"]:
        raise ValueError("invalid refund amount")

    invoice["amount"] = round(invoice["amount"] - amount, 2)
    invoice["status"] = "refunded" if invoice["amount"] == 0 else "partial_refund"
    return json.dumps(invoice)


async def get_customer_usage_data(
    user_id: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Retrieve usage data for the specified user."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    if user_id not in data["users"]:
        raise ValueError("User not found")

    usage = data["usage_data"].get(user_id)
    if not usage:
        return "No usage data found for this user."

    return json.dumps(usage)


async def create_escalation_ticket(
    user_id: str,
    summary: str,
    details: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Create a new escalation ticket for the specified user."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    if user_id not in data["users"]:
        raise ValueError("User not found")

    ticket_id = "ticket_" + "".join(random.choices(string.digits, k=5))
    new_ticket = {
        "ticket_id": ticket_id,
        "user_id": user_id,
        "summary": summary,
        "details": details,
        "status": "open",
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    data["tickets"][ticket_id] = new_ticket
    return json.dumps(new_ticket)


async def query_technical_docs(
    query: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Query technical documentation for matching titles or content."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    results = []
    for doc_id, doc_obj in data["docs"].items():
        if (
            query.lower() in doc_obj["title"].lower()
            or query.lower() in doc_obj["content"].lower()
        ):
            results.append({"doc_id": doc_id, "title": doc_obj["title"]})
    return json.dumps(results)


async def check_user_dsar_submission(
    user_id: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Check if the specified user has submitted a DSAR request."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    if user_id not in data["users"]:
        raise ValueError("User not found")

    for dsar_id, dsar_obj in data["dsar_requests"].items():
        if dsar_obj["user_id"] == user_id:
            return json.dumps(dsar_obj)
    return "No DSAR request found for this user."


async def ignore_spam(
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Call if the inbound is spam."""
    assert classification, f"Must classify request first: {classification}"
    return ""


async def run_haskell_code(
    code: str,
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Run code."""
    assert classification, f"Must classify request first: {classification}"
    # Just an additional distraction really.
    return str("This tool is not yet implemented")


async def escalate_to_manager(
    user_id: str,
    note: str,
    data: Annotated[dict, InjectedState("data")],
    classification: Annotated[dict, InjectedState("classification")],
) -> str:
    """Escalate to manager. Only permitted if the user is on an enterprise plan."""
    validate_user_id(user_id)
    assert classification, f"Must classify request first: {classification}"
    user = data["users"][user_id]
    if user["plan"] != "enterprise":
        raise ValueError("User is not on an enterprise plan")
    return ""


TOOLS = [
    classify_request,
    reset_user_api_key,
    run_haskell_code,
    find_user_id_by_email,
    modify_user_email,
    lookup_plan_application_status,
    lookup_valid_plans,
    change_subscription_plan,
    get_customer_invoices,
    issue_invoice_refund,
    get_customer_usage_data,
    create_escalation_ticket,
    query_technical_docs,
    check_user_dsar_submission,
    ignore_spam,
    escalate_to_manager,
]
