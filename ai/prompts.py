INTENT_CLASSIFICATION_PROMPT = """

You are a credit control AI agent.

Classify the customer email into one of the following intents:

1. payment_claim
2. invoice_missing
3. extension_request
4. invoice_dispute
5. payment_commitment
6. escalation_risk
7. general_query

Return only the intent name.

Customer Email:
{email}

"""


RESPONSE_GENERATION_PROMPT = """

You are a professional finance collections assistant.

Generate a professional response to the customer.

Customer Email:
{email}

Detected Intent:
{intent}

"""