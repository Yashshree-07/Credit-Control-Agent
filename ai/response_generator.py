class ResponseGenerator:

    def generate_response(

        self,

        customer_name,

        invoice_id,

        intent,

        sentiment,

        overdue_days
    ):

        # =====================================
        # PAYMENT COMMITMENT
        # =====================================

        if intent == "payment_commitment":

            return f"""

Dear {customer_name},

Thank you for confirming the payment update for invoice {invoice_id}.

We appreciate your response and have temporarily paused further reminders.

Our system will follow up again after the committed payment timeline.

Regards,
AI Credit Control Agent
"""

        # =====================================
        # INVOICE MISSING
        # =====================================

        elif intent == "invoice_missing":

            return f"""

Dear {customer_name},

Thank you for informing us.

We have re-shared invoice {invoice_id} with this email.

Please review the invoice and let us know if any clarification is required.

Regards,
AI Credit Control Agent
"""

        # =====================================
        # EXTENSION REQUEST
        # =====================================

        elif intent == "extension_request":

            return f"""

Dear {customer_name},

We acknowledge your request for additional time regarding invoice {invoice_id}.

Your request has been noted and a revised follow-up schedule has been created.

Please ensure payment is processed within the discussed timeline.

Regards,
AI Credit Control Agent
"""

        # =====================================
        # DISPUTE
        # =====================================

        elif intent == "invoice_dispute":

            return f"""

Dear {customer_name},

We understand there may be an issue regarding invoice {invoice_id}.

The case has been forwarded to the credit control team for detailed review.

Our team will contact you shortly.

Regards,
AI Credit Control Agent
"""

        # =====================================
        # ALREADY PAID
        # =====================================

        elif intent == "already_paid":

            return f"""

Dear {customer_name},

Thank you for the payment confirmation.

We request you to kindly share remittance details or payment proof for reconciliation.

Once verified, the invoice status will be updated.

Regards,
AI Credit Control Agent
"""

        # =====================================
        # DEFAULT
        # =====================================

        else:

            if overdue_days > 90:

                tone = (
                    "urgent"
                )

            else:

                tone = (
                    "professional"
                )

            return f"""

Dear {customer_name},

Thank you for your response regarding invoice {invoice_id}.

Our system has recorded your communication and the collections workflow is currently active.

Please contact the credit control team if further clarification is required.

Regards,
AI Credit Control Agent
"""