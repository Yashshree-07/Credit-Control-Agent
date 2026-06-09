import pandas as pd


class DashboardMetrics:

    def __init__(self):

        self.invoice_file = (
            "app/data/invoices.xlsx"
        )

        self.reply_file = (
            "app/data/customer_replies.xlsx"
        )

        self.reminder_file = (
            "app/data/reminder_logs.xlsx"
        )

    # =======================================
    # INVOICES PROCESSED
    # =======================================

    def invoices_processed(self):

        try:

            df = pd.read_excel(
                self.invoice_file
            )

            return len(df)

        except:

            return 0

    # =======================================
    # REMINDERS SENT
    # =======================================

    def reminders_sent(self):

        try:

            df = pd.read_excel(
                self.reminder_file
            )

            return len(df)

        except:

            return 0

    # =======================================
    # REPLIES ANALYZED
    # =======================================

    def replies_analyzed(self):

        try:

            df = pd.read_excel(
                self.reply_file
            )

            return len(df)

        except:

            return 0

    # =======================================
    # AUTO RESOLVED
    # =======================================

    def auto_resolved(self):

        try:

            df = pd.read_excel(
                self.reply_file
            )

            resolved = df[

                df[
                    "workflow_resolution_status"
                ]
                ==
                "resolved"
            ]

            return len(
                resolved
            )

        except:

            return 0

    # =======================================
    # ESCALATIONS
    # =======================================

    def escalations(self):

        try:

            invoices = pd.read_excel(
                self.invoice_file
            )

            escalated = invoices[

                invoices[
                    "human_intervention_required"
                ]
                ==
                True
            ]

            return len(
                escalated
            )

        except:

            return 0

    # =======================================
    # DASHBOARD SUMMARY
    # =======================================

    def get_summary(self):

        return {

            "Invoices Processed":
                self.invoices_processed(),

            "Reminders Generated":
                self.reminders_sent(),

            "Replies Analyzed":
                self.replies_analyzed(),

            "Auto Resolved":
                self.auto_resolved(),

            "Escalated Cases":
                self.escalations()
        }