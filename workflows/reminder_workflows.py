from app.agents.payment_monitor_agent import PaymentMonitorAgent
from app.agents.reminder_agent import ReminderAgent


class ReminderWorkflow:

    def __init__(self):

        self.monitor_agent = PaymentMonitorAgent(
            "app/data/invoices.xlsx"
        )

        self.reminder_agent = ReminderAgent()

    def execute(self):

        invoices = self.monitor_agent.process_invoices()

        for _, row in invoices.iterrows():

            reminder_type = (
                self.reminder_agent
                .determine_reminder_type(
                    row["days_overdue"]
                )
            )

            message = (
                self.reminder_agent
                .generate_message(
                    customer_name=row["customer_id"],
                    invoice_id=row["invoice_id"],
                    amount=row["amount_left"],
                    reminder_type=reminder_type
                )
            )

            print(message)