from trustcall import create_extractor
from langchain.chat_models import init_chat_model
import random
import langsmith as ls

prompt = """STANDARD OPERATING PROCEDURE
Email Triage Classification
Version 1.0

PURPOSE:
To establish consistent guidelines for classifying incoming customer support emails into three categories: ignore, notify, or respond.

SCOPE:
This procedure applies to all incoming customer support emails.

PROCEDURE:

1. IGNORE Classification
   - Obvious spam or automated marketing emails
   - Duplicate emails of already handled issues
   - Test emails or system notifications
   - Emails clearly sent to wrong department/company

2. NOTIFY Classification
   - Feature requests or product suggestions
   - General feedback that requires no immediate action
   - Issues that need internal discussion before responding
   - Non-urgent bugs or system issues
   - Complex questions requiring research or escalation

3. RESPOND Classification
   - Account access or security issues
   - Service outages or critical system failures
   - Billing disputes or payment issues
   - Time-sensitive inquiries
   - Legal or compliance-related matters
   - Clear questions that can be answered immediately

PRIORITY GUIDELINES:
- Always assess urgency first
- Consider potential business impact
- Evaluate if immediate action is required
- Check if the sender is a priority customer

NOTE:
When in doubt about classification, default to NOTIFY to ensure proper visibility to the team."""

email_types = {
    "ignore": [
        "spam",
        "automated marketing",
        "test email",
        "wrong department or company (anyone but langchain; could be microsoft, google, openai, etc.)",
        "internal cc email that's just an fyi",
    ],
    "notify": [
        "feature request",
        "general feedback",
        "issue that requires internal discussion",
        "non-urgent bug or system issue",
        "complex question that requires research or escalation",
    ],
    "respond": [
        "account access or security issue",
        "service outage or critical system failure",
        "billing dispute or payment issue",
        "time-sensitive inquiry",
        "legal or compliance-related matter",
        "clear question that can be answered immediately",
    ],
}

personas = [
    "Someone who only writes in lower-case and with lots of spelling mistakes.",
    "A student from delhi who is earnest but has really poor english grammar.",
    "A busy software engineer who tends to write concise, technical emails with occasional programming jargon",
    "A friendly HR manager who always maintains a warm, professional tone and includes clear action items",
    "A detail-oriented project manager who likes to use bullet points and emphasizes deadlines",
    "A creative marketing director who writes enthusiastic emails with occasional emoji use",
    "A senior executive who writes brief, direct emails often from their mobile device",
    "A 5 year old who stole their parents' phone."
    "A customer support representative who maintains a helpful, patient tone while addressing concerns",
    "A sales representative who writes persuasive emails with a focus on building relationships",
    "A new intern who tends to be extra formal and double-checks everything before sending",
    "A startup founder who writes passionate emails about their vision, sometimes late at night",
    "A university professor who writes structured emails with clear expectations and deadlines",
    "A remote work coordinator who emphasizes clear communication and includes time zones",
    "A product manager who frequently references user feedback and market research",
    "A social media manager who brings a casual, trendy voice to their communications",
    "A technical writer who excels at breaking down complex topics into simple explanations",
]


def write_email_example(subject: str, sender: str, body: str):
    return ""


llm = create_extractor(
    init_chat_model("claude-3-5-sonnet-latest"),
    tools=[write_email_example],
    tool_choice="write_email_example",
)

NAME = "email_cs_simple"
if __name__ == "__main__":
    client = ls.Client()
    if not client.has_dataset(dataset_name=NAME):
        ds = client.create_dataset(dataset_name=NAME)
    else:
        # client.delete_dataset(dataset_name=NAME)
        # ds = client.create_dataset(dataset_name=NAME)
        ds = client.read_dataset(dataset_name=NAME)
    print(ds.url)
    N = 200
    topics = [
        (topic, category)
        for category, topics in email_types.items()
        for topic in topics
    ]
    topics = (topics * (N // len(topics) + 1))[:N]
    random.shuffle(topics)
    personas = personas * (N // len(personas) + 1)
    random.shuffle(personas)
    chain = {
        "messages": lambda x: [
            {
                "role": "system",
                "content": "You are helping LangChain, Inc. test their email triaging system. Role play as the following persona in writing a full-length email for the requested type."
                f"\n\n{x['persona']}",
            },
            {
                "role": "user",
                "content": f"We are testing our email triaging system. Write an email of the following type: {x['topic']}.",
            },
        ],
    } | llm

    data = [
        {"topic": topic, "persona": persona}
        for (topic, _), persona in zip(topics, personas)
    ]

    results = chain.batch(data)
    inputs = [r["responses"][0].model_dump() for r in results]
    outputs = [{"action": category} for _, category in topics]
    splits = (0.30, 0.40, 0.30)

    acc = 0
    for split_name, split in zip(["train", "dev", "test"], splits):
        st = int(acc * len(inputs))
        end = int((acc + split) * len(inputs))
        client.create_examples(
            dataset_name=NAME,
            splits=[split_name] * (end - st),
            inputs=inputs[st:end],
            outputs=outputs[st:end],
        )
        acc += split
