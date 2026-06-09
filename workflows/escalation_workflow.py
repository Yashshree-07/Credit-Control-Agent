from app.agents.payment_monitor_agent import PaymentMonitorAgent
from app.agents.escalation_agent import EscalationAgent


class EscalationWorkflow:

    def __init__(self):

        self.monitor_agent = PaymentMonitorAgent(
            "app/data/invoices.xlsx"
        )

        self.escalation_agent = EscalationAgent()

    def execute(self):

        invoices = self.monitor_agent.process_invoices()

        for _, row in invoices.iterrows():

            escalation = (
                self.escalation_agent
                .check_escalation(
                    row["days_overdue"]
                )
            )

            print(
                row["invoice_id"],
                escalation
            )