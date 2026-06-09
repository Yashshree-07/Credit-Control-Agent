import pandas as pd

from app.services.invoice_service import (
    InvoiceService
)

from app.services.reminder_service import (
    ReminderService
)

from app.agents.escalation_agent import (
    EscalationAgent
)

from app.ai.intent_classifier import (
    IntentClassifier
)

from app.ai.response_generator import (
    ResponseGenerator
)

from app.services.sentiment_service import (
    SentimentService
)

from app.utils.logger import (
    log_event
)


class MasterWorkflow:

    def __init__(self):

        self.invoice_service = (
            InvoiceService(
                "app/data/invoices.xlsx"
            )
        )

        self.reminder_service = (
            ReminderService()
        )

        self.escalation_agent = (
            EscalationAgent()
        )

        self.intent_classifier = (
            IntentClassifier()
        )

        self.response_generator = (
            ResponseGenerator()
        )

        self.sentiment_service = (
            SentimentService()
        )

    def process_invoices(self):

        log_event(
            "Checking overdue invoices..."
        )

        invoices = (
            self.invoice_service
            .process_invoices()
        )

        for _, row in invoices.iterrows():

            invoice_id = row["invoice_id"]

            customer_id = row["customer_id"]

            overdue_days = row[
                "days_overdue"
            ]

            amount = row["amount_left"]

            if overdue_days > 0:

                reminder_type = (
                    self.reminder_service
                    .determine_reminder_type(
                        overdue_days
                    )
                )

                log_event(
                    f"{invoice_id} overdue "
                    f"by {overdue_days} days"
                )

                log_event(
                    f"Sending "
                    f"{reminder_type} "
                    f"to {customer_id}"
                )

                message = (
                    self.reminder_service
                    .create_reminder_message(
                        company_name=customer_id,
                        invoice_id=invoice_id,
                        amount=amount,
                        days_overdue=overdue_days
                    )
                )

                print(message)

                escalation = (
                    self.escalation_agent
                    .check_escalation(
                        overdue_days
                    )
                )

                if escalation != (
                    "No Escalation"
                ):

                    log_event(
                        f"{invoice_id} "
                        f"Escalated: "
                        f"{escalation}"
                    )

    def process_customer_replies(self):

        log_event(
            "Processing customer replies..."
        )

        replies = pd.read_excel(
            "app/data/customer_replies.xlsx"
        )

        for _, row in replies.iterrows():

            company_name = row[
                "company_name"
            ]

            email_text = row[
                "email_text"
            ]

            log_event(
                f"Customer Reply "
                f"from {company_name}"
            )

            print(
                f"\nEMAIL:\n{email_text}\n"
            )

            detected_intent = (
                self.intent_classifier
                .classify(email_text)
            )

            sentiment = (
                self.sentiment_service
                .analyze(email_text)
            )

            log_event(
                f"Intent Detected: "
                f"{detected_intent}"
            )

            log_event(
                f"Sentiment: "
                f"{sentiment['label']}"
            )

            ai_response = (
                self.response_generator
                .generate_response(
                    email_text,
                    detected_intent
                )
            )

            print(
                "\nAI RESPONSE:\n"
            )

            print(ai_response)

            if (
                detected_intent
                == "invoice_missing"
            ):

                log_event(
                    "Action Taken: "
                    "Invoice Resent"
                )

            elif (
                detected_intent
                == "payment_claim"
            ):

                log_event(
                    "Action Taken: "
                    "Payment Verification Requested"
                )

            elif (
                detected_intent
                == "extension_request"
            ):

                log_event(
                    "Action Taken: "
                    "Credit Controller Notified"
                )

            elif (
                detected_intent
                == "invoice_dispute"
            ):

                log_event(
                    "Action Taken: "
                    "Dispute Ticket Raised"
                )

    def run(self):

        log_event(
            "MASTER WORKFLOW STARTED"
        )

        self.process_invoices()

        self.process_customer_replies()

        log_event(
            "MASTER WORKFLOW COMPLETED"
        )