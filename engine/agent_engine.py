import time
import pandas as pd

from datetime import datetime

from app.services.invoice_service import (
    InvoiceService
)

from app.services.customer_service import (
    CustomerService
)

from app.services.reminder_service import (
    ReminderService
)

from app.services.sentiment_service import (
    SentimentService
)

from app.ai.intent_classifier import (
    IntentClassifier
)

from app.ai.response_generator import (
    ResponseGenerator
)

from app.memory.workflow_memory import (
    WorkflowMemory
)

from app.orchestration.escalation_manager import (
    EscalationManager
)

from app.orchestration.notification_manager import (
    NotificationManager
)

from app.state.workflow_state import (
    workflow_state
)

from app.services.workflow_logger import (
    WorkflowLogger
)


class AgentEngine:

    def __init__(self):

        self.invoice_service = (
            InvoiceService(
                "app/data/invoices.xlsx"
            )
        )

        self.customer_service = (
            CustomerService()
        )

        self.reminder_service = (
            ReminderService()
        )

        self.sentiment_service = (
            SentimentService()
        )

        self.intent_classifier = (
            IntentClassifier()
        )

        self.response_generator = (
            ResponseGenerator()
        )

        self.workflow_memory = (
            WorkflowMemory()
        )

        self.escalation_manager = (
            EscalationManager()
        )

        self.notification_manager = (
            NotificationManager()
        )

        self.workflow_logger = (
            WorkflowLogger()
        )

        self.current_run_id = (
            datetime.now().strftime(
            "RUN_%Y%m%d_%H%M%S"
            )
        )

    # =====================================
    # ADD EVENT
    # =====================================

    def add_event(
    self,
    title,
    details,
    customer_id="",
    company_name="",
    invoice_id="",
    requires_human=False
):

        workflow_state.add_event({

        "title": title,

        "details": details
    })

        self.workflow_logger.log_event(

        run_id=
            self.current_run_id,

        customer_id=
            customer_id,

        company_name=
            company_name,

        invoice_id=
            invoice_id,

        title=
            title,

        details=
            details,

        requires_human=
            requires_human
    )

    # =====================================
    # MAIN WORKFLOW
    # =====================================

    def run_company_workflow(
        self,
        customer_id
    ):

        workflow_state.clear()

        customer = (
            self.customer_service
            .get_customer_by_id(
                customer_id
            )
        )

        if not customer:

            self.add_event(

                "Customer Error",

                "Customer not found"
            )

            return

        workflow_state.set_current_case({

            "customer": customer
        })

        company_name = (
            customer["company_name"]
        )

        invoices = (
            self.invoice_service
            .process_invoices()
        )

        customer_invoices = invoices[

            invoices["customer_id"]
            ==
            customer_id
        ]

        if len(customer_invoices) == 0:

            self.add_event(

                "No Invoices",

                "No invoices found."
            )

            return

        # =====================================
        # PROCESS ALL INVOICES
        # =====================================

        for _, invoice in (
            customer_invoices.iterrows()
        ):

            invoice_id = (
                invoice["invoice_id"]
            )

            overdue_days = int(
                invoice["days_overdue"]
            )

            amount_left = (
                invoice["amount_left"]
            )

            reminder_count = int(
                invoice.get(
                    "reminder_count",
                    0
                )
            )

            self.add_event(

            "Invoice Detected",

            f"""
            Invoice ID:
            {invoice_id}
            """,

            customer_id=
                customer_id,

            company_name=
                company_name,

            invoice_id=
                invoice_id
            )

            time.sleep(1)

            # =====================================
            # DETERMINE REMINDER TYPE
            # =====================================

            reminder_type = (

                self.reminder_service
                .determine_reminder_type(
                    overdue_days
                )
            )

            # =====================================
            # GENERATE REMINDER
            # =====================================

            reminder_message = (

                self.reminder_service
                .create_reminder_message(

                    company_name=
                        company_name,

                    invoice_id=
                        invoice_id,

                    amount=
                        amount_left,

                    days_overdue=
                        overdue_days
                )
            )

            self.add_event(

    "AI Reminder Generated",

    reminder_message,

    customer_id=customer_id,

    company_name=company_name,

    invoice_id=invoice_id
)

            workflow_state.add_email_thread({

                "type":
                    "agent_email",

                "title":
                    "Payment Reminder",

                "message":
                    reminder_message
            })

            # =====================================
            # STORE REMINDER LOG
            # =====================================

            reminder_data = {

                "reminder_id":
                    f"REM-{datetime.now().timestamp()}",

                "invoice_id":
                    invoice_id,

                "customer_id":
                    customer_id,

                "company_name":
                    company_name,

                "reminder_type":
                    reminder_type,

                "reminder_channel":
                    "email",

                "sent_date":
                    str(datetime.now()),

                "email_subject":
                    f"Payment Reminder - {invoice_id}",

                "email_body":
                    reminder_message,

                "ai_generated":
                    True,

                "customer_replied":
                    False,

                "reply_received_date":
                    "",

                "reply_sentiment":
                    "",

                "reply_intent":
                    "",

                "agent_action_taken":
                    "Reminder Sent",

                "escalated_to_employee":
                    False,

                "employee_intervention_required":
                    False,

                "workflow_status":
                    "active",

                "delivery_status":
                    "delivered",

                "followup_sequence":
                    reminder_count + 1
            }

            self.workflow_memory.add_reminder_log(
                reminder_data
            )

            # =====================================
            # UPDATE INVOICE EXCEL
            # =====================================

            self.workflow_memory.update_invoice(

                invoice_id,

                {

                    "last_reminder_sent":
                        str(datetime.now()),

                    "reminder_count":
                        reminder_count + 1,

                    "workflow_stage":
                        reminder_type,

                    "last_ai_action":
                        "Reminder Sent",

                    "workflow_last_updated":
                        str(datetime.now()),

                    "assigned_agent_status":
                        "active"
                }
            )

            time.sleep(1)

            # =====================================
            # HIGH RISK ESCALATION
            # =====================================

            if overdue_days >= 90:

                self.add_event(

                    "High Risk Invoice",

                    """
                    Invoice crossed
                    90 overdue days.
                    Escalation initiated.
                    """
                )

                self.workflow_memory.update_invoice(

                    invoice_id,

                    {

                        "escalation_required":
                            True,

                        "human_intervention_required":
                            True,

                        "workflow_stage":
                            "Escalated"
                    }
                )

        # =====================================
        # PROCESS CUSTOMER EMAILS
        # =====================================

        replies = pd.read_excel(
            "app/data/customer_replies.xlsx"
        )

        customer_replies = replies[

            replies["customer_id"]
            ==
            customer_id
        ]

        if len(customer_replies) > 0:

            for _, reply in (
                customer_replies.iterrows()
            ):

                invoice_id = (
                    reply["invoice_id"]
                )

                email_text = (
                    reply["email_text"]
                )

                self.add_event(

    "Customer Email Received",

    email_text,

    customer_id=customer_id,

    company_name=company_name,

    invoice_id=invoice_id
)

                workflow_state.add_email_thread({

                    "type":
                        "customer_email",

                    "title":
                        "Customer Reply",

                    "message":
                        email_text
                })

                time.sleep(1)

                # =====================================
                # SENTIMENT ANALYSIS
                # =====================================

                sentiment = (

                    self.sentiment_service
                    .analyze(
                        email_text
                    )
                )

                self.add_event(

    "Sentiment Analysis",

    f"""
    Label:
    {sentiment['label']}

    Score:
    {sentiment['score']}
    """,

    customer_id=customer_id,

    company_name=company_name,

    invoice_id=invoice_id
)

                # =====================================
                # INTENT CLASSIFICATION
                # =====================================

                detected_intent = (

                    self.intent_classifier
                    .classify(
                        email_text
                    )
                )

                self.add_event(

    "Intent Detected",

    detected_intent,

    customer_id=customer_id,

    company_name=company_name,

    invoice_id=invoice_id
)

                time.sleep(1)

                # =====================================
                # GENERATE AI RESPONSE
                # =====================================

                ai_response = (

                    self.response_generator
                    .generate_response(

                        email_text,

                        detected_intent
                    )
                )

                self.add_event(

    "AI Response Generated",

    ai_response,

    customer_id=customer_id,

    company_name=company_name,

    invoice_id=invoice_id
)

                workflow_state.add_email_thread({

                    "type":
                        "ai_response",

                    "title":
                        "AI Generated Reply",

                    "message":
                        ai_response
                })

                time.sleep(1)

                # =====================================
                # DETERMINE ACTION
                # =====================================

                action_taken = ""

                requires_human = False

                if (
                    detected_intent
                    ==
                    "invoice_missing"
                ):

                    action_taken = (
                        "Invoice Resent"
                    )

                elif (
                    detected_intent
                    ==
                    "payment_claim"
                ):

                    action_taken = (
                        "Requested Payment Proof"
                    )

                elif (
                    detected_intent
                    ==
                    "extension_request"
                ):

                    action_taken = (
                        "Extension Requested"
                    )

                elif (
                    detected_intent
                    ==
                    "invoice_dispute"
                ):

                    action_taken = (
                        "Dispute Raised"
                    )

                    requires_human = True

                else:

                    action_taken = (
                        "General Follow-up"
                    )

                self.add_event(

    "Action Taken",

    action_taken,

    customer_id=customer_id,

    company_name=company_name,

    invoice_id=invoice_id
)

                # =====================================
                # ESCALATION CHECK
                # =====================================

                confidence_score = 0.72

                invoice_data = customer_invoices[

                    customer_invoices[
                        "invoice_id"
                    ]
                    ==
                    invoice_id
                ]

                if len(invoice_data) > 0:

                    invoice_data = (
                        invoice_data.iloc[0]
                    )

                    overdue_days = int(
                        invoice_data[
                            "days_overdue"
                        ]
                    )

                    amount = (
                        invoice_data[
                            "amount_left"
                        ]
                    )

                    reminder_count = int(

                invoice_data.get(
                "reminder_count",
                    0
                    )
                    )

                    
                    

                    should_escalate = (

                        self.escalation_manager
                        .should_escalate(

                            overdue_days=
                                overdue_days,

                            sentiment=
                                sentiment[
                                    "label"
                                ],

                            confidence_score=
                                confidence_score,

                            amount=
                                amount,

                            reminder_count=
                                reminder_count
                        )
                    )

                    if should_escalate:

                        requires_human = True

                        escalation_reasons = (

                            self.escalation_manager
                            .get_escalation_reason(

                                overdue_days=
                                    overdue_days,

                                sentiment=
                                    sentiment[
                                        "label"
                                    ],

                                confidence_score=
                                    confidence_score,

                                amount=
                                    amount,

                                reminder_count=
                                    reminder_count
                            )
                        )

                        notification = (

                            self.notification_manager
                            .notify_credit_controller(

                                company_name=
                                    company_name,

                                invoice_id=
                                    invoice_id,

                                escalation_reasons=
                                    escalation_reasons,

                                customer_email=
                                    email_text,

                                ai_summary=
                                    ai_response
                            )
                        )

                        self.add_event(

    "Employee Escalation",

    notification,

    customer_id=customer_id,

    company_name=company_name,

    invoice_id=invoice_id,

    requires_human=True
)

                # =====================================
                # UPDATE CUSTOMER REPLY EXCEL
                # =====================================

                replies.loc[
                    replies["reply_id"]
                    ==
                    reply["reply_id"],

                    "detected_intent"

                ] = detected_intent

                replies.loc[
                    replies["reply_id"]
                    ==
                    reply["reply_id"],

                    "sentiment"

                ] = sentiment["label"]

                replies.loc[
                    replies["reply_id"]
                    ==
                    reply["reply_id"],

                    "confidence_score"

                ] = confidence_score

                replies.loc[
                    replies["reply_id"]
                    ==
                    reply["reply_id"],

                    "ai_response_generated"

                ] = ai_response

                replies.loc[
                    replies["reply_id"]
                    ==
                    reply["reply_id"],

                    "action_taken"

                ] = action_taken

                replies.loc[
                    replies["reply_id"]
                    ==
                    reply["reply_id"],

                    "requires_human_intervention"

                ] = requires_human

                replies.loc[
                    replies["reply_id"]
                    ==
                    reply["reply_id"],

                    "workflow_resolution_status"

                ] = (
                    "Escalated"
                    if requires_human
                    else "Resolved by AI"
                )

                # =====================================
                # UPDATE INVOICE STATUS
                # =====================================

                self.workflow_memory.update_invoice(

                    invoice_id,

                    {

                        "last_customer_response":
                            email_text,

                        "last_customer_sentiment":
                            sentiment["label"],

                        "workflow_stage":
                            (
                                "Escalated"
                                if requires_human
                                else "AI Handling"
                            ),

                        "human_intervention_required":
                            requires_human,

                        "workflow_last_updated":
                            str(datetime.now()),

                        "last_ai_action":
                            action_taken
                    }
                )

        # =====================================
        # SAVE CUSTOMER REPLIES
        # =====================================

        replies.to_excel(
            "app/data/customer_replies.xlsx",
            index=False
        )

        self.add_event(

    "Workflow Completed",

    f"""
    AI workflow completed
    for {company_name}
    """,

    customer_id=customer_id,

    company_name=company_name
)