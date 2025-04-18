"Find an invoice by email"
A user provides their email address and asks for their most recent invoice.
Expected: The model must first use find_user_id_by_email and then use get_customer_invoices.


# ombining Classification and Email Updates
# "Subject: Need to update my email and also this request might be about security
# Body: I think my account was compromised, but I also just realized my email is spelled incorrectly. Could you make sure you classify this request as a security one, and also fix my email from ‘[username]@gamil.com’ to ‘[username]@gmail.com’? By the way, how do I subscribe to your enterprise plan?
# Notes: This is not spam at all!"

# Why it’s tricky
# References classification (“might be about security”).
# Also references changing an email.
# Mentions an interest in changing subscription (another separate operation).
# The user suggests “This is not spam,” which might confuse the agent into mis-triggering the ignore_spam tool.
# 2. Partial Payment and DSAR Confusion
# "Subject: Important billing and DSAR request
# Body: I need a refund for invoice #1234 for 10 dollars, but also, can you verify if I have any DSAR requests open in your system? And if not, please create a new one for me.
# Footer: If you can’t help, please escalate to the manager."

# Why it’s tricky
# Might prompt the use of issue_invoice_refund for the partial refund.
# Also references check_user_dsar_submission or possibly an attempt to create a new DSAR request (which there isn’t a direct function for—only a “check” function).
# Mentions escalation to manager, which could tempt the agent to call escalate_to_manager or create_escalation_ticket.
# 3. Fake Tool Mention and Documentation Search
# "Subject: Where is the user guide for advanced analytics?
# Body: Hi, I wanted to see the ‘advanced analytics’ docs. Also, can you confirm my subscription plan is correct? By the way, did you run that Haskell code snippet for me yesterday? I think it returned an error; can you fix it?**"

# Why it’s tricky
# Queries the documentation for something that might appear in multiple doc entries (prompts query_technical_docs).
# Also wants to confirm a subscription plan (possibly lookup_plan_application_status or lookup_valid_plans).
# Mentions Haskell code, but the provided run_haskell_code tool returns “not implemented” and might be irrelevant.
# 4. Vague Request That Looks Like Spam
# "Subject: A special promotional message
# Body: Hello dear friend, I want to help you save on your plan and also verify my user account. Is that possible?**"

# Why it’s tricky
# Language might appear spammy or phishing-like (“Hello dear friend”).
# Also references verifying a user account (no direct tool for “verify user account,” though the agent might mistakenly try to do something like find_user_id_by_email or modify_user_email).
# Could tempt the agent to call ignore_spam prematurely.
# 5. Mixed Up IDs and Additional Data
# "Subject: I think I used the wrong user ID
# Body: My user ID is 9999, I think. Or was it 1234? Can you reset my API key, then refund invoice ID #abc123 for 20.00? Actually, I might have the invoice ID wrong, so maybe check my usage data first to confirm.**"

# Why it’s tricky
# The user is uncertain about their own user ID and invoice ID, so the agent might call reset_user_api_key or issue_invoice_refund incorrectly if it doesn’t confirm existence of the user/invoice first.
# Mentioning usage data might prompt get_customer_usage_data, but that is only valid if we actually know the user ID correctly.
# 6. Security Plus Spam Red Herring
# "Subject: Hackers and spam, oh my!
# Body: I just got an email from a hacker claiming to have my data, but it’s probably just spam. Also, can you classify this as security or spam? Not sure.**"

# Why it’s tricky
# The user toggles between suspecting a security threat or spam.
# Could cause the agent to do classify_request as either “spam” or “security,” and picking incorrectly might be an error.
# 7. Sudden Switch to Technical Docs
# "Subject: Creating escalation ticket or maybe reading the docs
# Body: I need to escalate a complaint immediately about my billing. Actually, wait, I want to read the developer documentation on how you handle concurrency.**"

# Why it’s tricky
# The user requests an escalation ticket about billing, which suggests create_escalation_ticket.
# Then abruptly changes the request to searching for concurrency docs, suggesting query_technical_docs.
# 8. Ambiguous Category and Playground Request
# "Subject: Classification required
# Body: I have a question about using your playground for testing advanced queries, but I’m also worried about a security hole.**"

# Why it’s tricky
# Mentions “playground,” which might cause the agent to pick classify_request with category “playground.”
# Mentions “security hole,” leading to a conflict about which classification is correct.
# Doesn’t clearly ask for any other tool but might tempt the agent to pick the wrong category.
# General Tips for Crafting Tricky Queries
# Combine unrelated tasks (e.g., mention billing issues in the same breath as documentation).
# Use ambiguous or uncertain user info (e.g., uncertain user IDs, invoice IDs).
# Make the request sound spammy but also legitimate so the agent struggles to decide if it’s spam or a real request.
# Reference multiple categories (“security,” “billing,” “admin,” etc.) all at once.
# Include partial or incomplete instructions that might lead the AI to the wrong tool unless it carefully checks the data.
# These examples aim to lead the AI agent astray—if it’s not careful, it may pick the wrong tool or handle the request incorrectly.

# "List projects for an unknown user"
# A user asks for all their projects but provides only their first and last name.
# Expected: The model must derive user_id using another lookup tool (e.g., a name-to-user ID tool, if available).

# "Upgrade plan for the wrong org"
# A user wants to upgrade their organization’s plan, but the provided org_name doesn’t match any in the dataset.
# Expected: The model should use get_org_info_by_name first to validate the org name.

# "Investigate usage for a team"
# A user asks for usage data for all users in their organization.
# Expected: The model must first get the org_id, fetch the active users, and then loop through get_customer_usage_data.

# "Modify subscription plan by email"
# A user asks to change their plan but provides their email address, not user_id.
# Expected: The model must resolve the email to user_id before calling change_subscription_plan.

# "Check a ticket by email"
# A user asks to review their active tickets but provides only their email address.
# Expected: Resolve user_id and then check create_escalation_ticket or a related ticket tool.

# "Recover API key without ID"
# A user says they lost their API key but only remembers the organization’s name.
# Expected: The model needs to link the org to active users and recover the API key for the correct user.

# Input-Output Challenges
# "Invalid subscription change request"
# A user tries to change their plan to one that doesn’t exist.
# Expected: The model should recognize this as invalid input and return an appropriate error.

# "Partial invoice refund exceeding balance"
# A refund is requested, but the model tries to refund an amount larger than the invoice value.
# Expected: Proper validation of refund amount before processing.

# "Incorrect DSAR request for an inactive user"
# A user submits a DSAR, but their account status is inactive or deleted.
# Expected: The model should validate account status before proceeding.

# "Update email without verification"
# A user requests an email change, but the input email is already associated with another account.
# Expected: The model should ensure email uniqueness.

# "Malformed project data"
# A user asks to list all projects, but one project in their dataset has a missing or malformed field (e.g., no project_id).
# Expected: The model must handle incomplete data gracefully.

# "Quota adjustment with missing fields"
# A request to increase quotas is made, but the necessary input (e.g., new_quota) isn’t provided.
# Expected: The tool should fail gracefully or request missing information.

# "Delete data for a non-existent user"
# A DSAR deletion request is issued for a user ID not in the dataset.
# Expected: The model should validate existence before processing.

# Multi-Step Tool Challenges
# "Find a refund for the wrong invoice ID"
# A user provides an invoice ID for a refund request, but the ID is invalid.
# Expected: The model should confirm the invoice exists before processing.

# "Get usage for a missing project ID"
# A request for usage statistics references a project ID that doesn’t exist.
# Expected: Validate the project ID before querying usage data.

# "Escalate to a human without a summary"
# A user requests escalation but doesn’t provide a summary of the issue.
# Expected: The model should prompt for missing details before invoking transfer_to_human_agent.

# "Recover API key for multiple users"
# Two users in the same organization request API key resets simultaneously.
# Expected: Ensure the correct key is reset for the correct user.

# "Modify subscription for an invalid user ID"
# The model is asked to change a plan for a user ID not in the dataset.
# Expected: Validate the user_id before making the change.

# "Invalid org name in multi-user lookup"
# A request to fetch all users in an organization references an org name that doesn’t match the dataset.
# Expected: Resolve the name to an org_id first or return an appropriate error.

