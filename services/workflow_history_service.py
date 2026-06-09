import os
import pandas as pd

from datetime import datetime


class WorkflowHistoryService:

    def __init__(
        self,
        file_path="app/data/workflow_history.xlsx"
    ):

        self.file_path = file_path

        self.columns = [

            "event_id",

            "customer_id",

            "company_name",

            "invoice_id",

            "event_timestamp",

            "event_type",

            "event_details",

            "generated_by",

            "requires_employee_action",

            "workflow_status"
        ]

        self._initialize_file()

    # =====================================
    # INITIALIZE FILE
    # =====================================

    def _initialize_file(self):

        if not os.path.exists(
            self.file_path
        ):

            df = pd.DataFrame(
                columns=self.columns
            )

            df.to_excel(
                self.file_path,
                index=False
            )

    # =====================================
    # LOAD HISTORY
    # =====================================

    def get_history(self):

        return pd.read_excel(
            self.file_path
        )

    def get_all_history(self):

        return self.get_history()

    # =====================================
    # SAVE HISTORY
    # =====================================

    def save_history(
        self,
        df
    ):

        df.to_excel(
            self.file_path,
            index=False
        )

    # =====================================
    # LOG EVENT
    # =====================================

    def log_event(

        self,

        customer_id,

        company_name,

        invoice_id,

        event_type,

        event_details,

        generated_by="AI Agent",

        requires_employee_action=False,

        workflow_status="Active"
    ):

        history = self.get_history()

        event_id = (
            f"EVT{len(history)+1:05d}"
        )

        new_row = {

            "event_id":
                event_id,

            "customer_id":
                customer_id,

            "company_name":
                company_name,

            "invoice_id":
                invoice_id,

            "event_timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "event_type":
                event_type,

            "event_details":
                event_details,

            "generated_by":
                generated_by,

            "requires_employee_action":
                requires_employee_action,

            "workflow_status":
                workflow_status
        }

        history = pd.concat(

            [
                history,
                pd.DataFrame(
                    [new_row]
                )
            ],

            ignore_index=True
        )

        self.save_history(
            history
        )

    # =====================================
    # COMPANY HISTORY
    # =====================================

    def get_company_history(
        self,
        company_name
    ):

        history = self.get_history()

        return history[

            history[
                "company_name"
            ]
            ==
            company_name

        ].sort_values(

            by="event_timestamp",

            ascending=False
        )

    # =====================================
    # CUSTOMER HISTORY
    # =====================================

    def get_customer_history(
        self,
        customer_id
    ):

        history = self.get_history()

        return history[

            history[
                "customer_id"
            ]
            ==
            customer_id

        ].sort_values(

            by="event_timestamp",

            ascending=False
        )

    # =====================================
    # INVOICE HISTORY
    # =====================================

    def get_invoice_history(
        self,
        invoice_id
    ):

        history = self.get_history()

        return history[

            history[
                "invoice_id"
            ]
            ==
            invoice_id

        ].sort_values(

            by="event_timestamp",

            ascending=False
        )

    # =====================================
    # ESCALATIONS
    # =====================================

    def get_escalations(self):

        history = self.get_history()

        return history[

            history[
                "requires_employee_action"
            ]
            ==
            True
        ]

    # =====================================
    # RECENT ACTIVITY
    # =====================================

    def get_recent_activity(
        self,
        limit=50
    ):

        history = self.get_history()

        return history.sort_values(

            by="event_timestamp",

            ascending=False

        ).head(limit)

    # =====================================
    # TODAY ACTIVITY
    # =====================================

    def get_today_activity(self):

        history = self.get_history()

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        return history[

            history[
                "event_timestamp"
            ]
            .astype(str)
            .str.startswith(
                today
            )
        ]

    # =====================================
    # DASHBOARD METRICS
    # =====================================

    def get_dashboard_metrics(self):

        history = self.get_today_activity()

        invoices_processed = len(

            history[

                history[
                    "event_type"
                ]
                ==
                "Invoice Processed"
            ]
        )

        reminders_sent = len(

            history[

                history[
                    "event_type"
                ]
                ==
                "Reminder Sent"
            ]
        )

        replies_processed = len(

            history[

                history[
                    "event_type"
                ]
                ==
                "Customer Reply"
            ]
        )

        escalations = len(

            history[

                history[
                    "requires_employee_action"
                ]
                ==
                True
            ]
        )

        resolved_cases = len(

            history[

                history[
                    "workflow_status"
                ]
                ==
                "Resolved"
            ]
        )

        return {

            "invoices_processed":
                invoices_processed,

            "reminders_sent":
                reminders_sent,

            "replies_processed":
                replies_processed,

            "resolved_cases":
                resolved_cases,

            "escalations":
                escalations
        }