import uuid

from datetime import datetime

import pandas as pd

from app.memory.workflow_memory import (
    WorkflowMemory
)

from app.services.invoice_service import (
    InvoiceService
)

from app.state.scheduler_state import (
    scheduler_state
)
from app.logger.workflow_logger import (
    WorkflowLogger
)


class SchedulerService:

    def __init__(self):

        self.memory = WorkflowMemory()

        self.invoice_service = InvoiceService(
            "app/data/invoices.xlsx"
        )

        self.workflow_logger = (
        WorkflowLogger()
    )


    # =====================================
    # RUN AUTONOMOUS SCHEDULER
    # =====================================

    def run_scheduler(self):

        scheduler_state.clear()
        
        self.workflow_logger.clear_log()

        run_id = str(
            uuid.uuid4()
        )

        invoices = (
            self.invoice_service.process_invoices()
        )

        replies = (
            self.memory.get_all_replies()
        )

        customers = pd.read_excel(
            "app/data/customers.xlsx"
        )

        processed_count = 0
        reminder_count = 0
        escalation_count = 0
        auto_resolved_count = 0

        reply_count = len(replies)

        # =================================
        # PROCESS ALL INVOICES
        # =================================

        for _, invoice in invoices.iterrows():

            processed_count += 1

            invoice_id = str(
                invoice["invoice_id"]
            )

            customer_id = str(
                invoice["customer_id"]
            )

            amount = float(
                invoice.get(
                    "amount_left",
                    0
                )
            )

            overdue = int(
                invoice.get(
                    "days_overdue",
                    0
                )
            )

            # =========================
            # CUSTOMER LOOKUP
            # =========================

            customer_match = customers[

                customers["customer_id"]
                .astype(str)
                ==
                customer_id
            ]

            if len(customer_match) > 0:

                company_name = (
                    customer_match.iloc[0][
                        "company_name"
                    ]
                )

            else:

                company_name = (
                    "Unknown Company"
                )

            # =========================
            # INVOICE DETECTED
            # =========================

            scheduler_state.add_event(

                company=company_name,

                invoice=invoice_id,

                step="Invoice Detected",

                details=f"""
Outstanding:
₹{amount:,.0f}

Overdue:
{overdue} days
"""
            )

            self.workflow_logger.log_event(

    run_id=run_id,

    customer_id=customer_id,

    company_name=company_name,

    invoice_id=invoice_id,

    title="Invoice Detected",

    details=f"""
Outstanding:
₹{amount:,.0f}

Overdue:
{overdue} days
""",

    event_type="invoice"
)

            # =========================
            # REMINDER LOGIC
            # =========================

            if overdue > 0:

                reminder_count += 1

                scheduler_state.add_event(

                    company=company_name,

                    invoice=invoice_id,

                    step="Reminder Generated",

                    details=f"""
Reminder sent automatically.

Outstanding:
₹{amount:,.0f}

Overdue:
{overdue} days
"""
                )

                self.workflow_logger.log_event(
    run_id=run_id,
    customer_id=customer_id,
    company_name=company_name,
    invoice_id=invoice_id,
    title="Reminder Generated",
    details=f"""
Reminder sent automatically.

Outstanding:
₹{amount:,.0f}

Overdue:
{overdue} days
""",
    event_type="reminder"
)

            # =========================
            # CUSTOMER REPLY CHECK
            # =========================

            invoice_replies = replies[

                replies["invoice_id"]
                .astype(str)
                ==
                invoice_id
            ]

            if len(invoice_replies) > 0:

                latest_reply = (
                    invoice_replies
                    .iloc[-1]
                )

                email_text = str(

                    latest_reply.get(
                        "email_text",
                        ""
                    )
                )

                intent = str(

                    latest_reply.get(
                        "detected_intent",
                        "Unknown"
                    )
                )

                sentiment = str(

                    latest_reply.get(
                        "sentiment",
                        "Neutral"
                    )
                )

                ai_response = str(

                    latest_reply.get(
                        "ai_response_generated",
                        "Response Generated"
                    )
                )

                scheduler_state.add_event(

                    company=company_name,

                    invoice=invoice_id,

                    step="Customer Reply",

                    details=email_text
                )

                self.workflow_logger.log_event(
    run_id=run_id,
    customer_id=customer_id,
    company_name=company_name,
    invoice_id=invoice_id,
    title="Customer Reply",
    details=email_text,
    event_type="reply"
)

                scheduler_state.add_event(

                    company=company_name,

                    invoice=invoice_id,

                    step="AI Analysis",

                    details=f"""
Intent:
{intent}

Sentiment:
{sentiment}
"""
                )


                self.workflow_logger.log_event(
    run_id=run_id,
    customer_id=customer_id,
    company_name=company_name,
    invoice_id=invoice_id,
    title="AI Analysis",
    details=f"""
Intent:
{intent}

Sentiment:
{sentiment}
""",
    event_type="analysis"
)

                
    



                scheduler_state.add_event(

                    company=company_name,

                    invoice=invoice_id,

                    step="AI Response",

                    details=ai_response
                )

                self.workflow_logger.log_event(
    run_id=run_id,
    customer_id=customer_id,
    company_name=company_name,
    invoice_id=invoice_id,
    title="AI Response",
    details=ai_response,
    event_type="response"
)

                

                if intent in [

                    "invoice_not_received",

                    "payment_promise",

                    "already_paid"
                ]:

                    auto_resolved_count += 1

                    scheduler_state.add_event(

                        company=company_name,

                        invoice=invoice_id,

                        step="Auto Resolved",

                        details="""
AI handled
customer interaction
without employee involvement.
"""
                    )

                    self.workflow_logger.log_event(
    run_id=run_id,
    customer_id=customer_id,
    company_name=company_name,
    invoice_id=invoice_id,
    title="Auto Resolved",
    details="AI handled customer interaction automatically.",
    event_type="resolution"
)
              


            # =========================
            # ESCALATION LOGIC
            # =========================

            if overdue > 90:

                escalation_count += 1

                self.memory.update_invoice(

                    invoice_id,

                    {

                        "human_intervention_required":
                            True,

                        "workflow_stage":
                            "Escalated"
                    }
                )

                scheduler_state.add_event(

                    company=company_name,

                    invoice=invoice_id,

                    step="Escalated",

                    details="""
90+ day overdue.

Credit Controller
notification generated.
"""
                )

                self.workflow_logger.log_event(
    run_id=run_id,
    customer_id=customer_id,
    company_name=company_name,
    invoice_id=invoice_id,
    title="Escalated",
    details="""
90+ day overdue.

Credit Controller notification generated.
""",
    event_type="escalation",
    requires_human=True
)

        # =================================
        # SAVE EXECUTION LOG
        # =================================

        execution_id = str(
            uuid.uuid4()
        )

        self.memory.save_workflow_execution(

            {

                "run_id":
                    execution_id,

                "run_date":
                    datetime.now(),

                "step_name":
                    "Scheduler Run",

                "status":
                    "Completed",

                "records_processed":
                    processed_count,

                "execution_time":
                    datetime.now()
            }

            
        )
        # =================================
        # DASHBOARD SUMMARY
        # =================================

        summary = {

            "processed":
                processed_count,

            "reminders":
                reminder_count,

            "replies":
                reply_count,

            "auto_resolved":
                auto_resolved_count,

            "escalations":
                escalation_count
        }

        return summary
    
    