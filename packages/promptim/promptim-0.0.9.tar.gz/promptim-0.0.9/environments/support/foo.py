import random
import string
from datetime import datetime, timedelta


# Helper functions to generate random data
def random_string(length=8):
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email():
    return f"{random_string()}@example.com"


def random_name():
    first_names = [
        "Alice",
        "Bob",
        "Charlie",
        "Diana",
        "Eve",
        "Frank",
        "Grace",
        "Hank",
        "Ivy",
        "Jack",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Brown",
        "Williams",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Martinez",
        "Lopez",
    ]
    return random.choice(first_names), random.choice(last_names)


def random_date(start_year=2020, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 1, 1)
    return start + timedelta(days=random.randint(0, (end - start).days))


# Initialize synthetic data
DATA = {
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
        "starter": {
            "price_per_month": 19.99,
            "features": ["3 projects", "email support"],
        },
        "premium": {
            "price_per_month": 299.99,
            "features": ["50 projects", "priority support", "custom analytics"],
        },
    },
    "invoices": {},
    "usage_data": {},
    "tickets": {},
    "docs": {},
    "dsar_requests": {},
}

# Generate organizations
for i in range(10):
    org_id = f"org_{i+1:03}"
    DATA["orgs"][org_id] = {
        "org_id": org_id,
        "org_name": f"Organization_{i+1}",
        "active_users": [],
    }

# Generate users and associate them with orgs
for i in range(20):
    user_id = f"user_{i+1:03}"
    first_name, last_name = random_name()
    email = random_email()
    org_id = random.choice(list(DATA["orgs"].keys()))
    plan = random.choice(list(DATA["plans"].keys()))
    subscription_start = random_date()
    subscription_end = (
        None if plan != "free" else subscription_start + timedelta(days=30)
    )
    api_key = f"api_{random_string(16)}"

    DATA["users"][user_id] = {
        "user_id": user_id,
        "email": email,
        "name": {"first_name": first_name, "last_name": last_name},
        "org_id": org_id,
        "api_key": api_key,
        "subscription": {
            "plan": plan,
            "status": "active",
            "start_date": subscription_start.isoformat(),
            "end_date": subscription_end.isoformat() if subscription_end else None,
        },
        "payment_methods": {
            "cc_ending_1234": {
                "source": "credit_card",
                "card_number_last4": "1234",
                "expiration": "01/30",
            },
            "credits_123": {
                "source": "credit_balance",
                "balance": round(random.uniform(0, 100), 2),
            },
        },
        "projects": {
            f"proj_{j+1:03}": {
                "project_id": f"proj_{j+1:03}",
                "name": f"Project_{j+1}",
                "status": "running",
                "last_deploy_time": random_date().isoformat(),
            }
            for j in range(random.randint(1, 5))
        },
    }
    DATA["orgs"][org_id]["active_users"].append(user_id)

# Generate invoices for users
for user_id in DATA["users"].keys():
    for i in range(random.randint(1, 3)):
        invoice_id = f"inv_{user_id}_{i+1:02}"
        amount = round(random.uniform(10, 1000), 2)
        status = random.choice(["paid", "unpaid", "refunded"])
        date_issued = random_date().isoformat()

        DATA["invoices"][invoice_id] = {
            "invoice_id": invoice_id,
            "user_id": user_id,
            "amount": amount,
            "status": status,
            "date_issued": date_issued,
        }

# Generate usage data for users
for user_id in DATA["users"].keys():
    DATA["usage_data"][user_id] = {
        "monthly_calls": random.randint(100, 50000),
        "current_month": "2025-01",
        "bandwidth_gb": round(random.uniform(0.1, 100.0), 2),
    }
import json

with open("data.json", "w") as f:
    json.dump(DATA, f, indent=2)
