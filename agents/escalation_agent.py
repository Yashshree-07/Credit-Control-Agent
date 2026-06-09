class EscalationAgent:

    def check_escalation(self, days_overdue):

        if days_overdue >= 180:
            return "Legal Escalation"

        elif days_overdue >= 90:
            return "Management Escalation"

        elif days_overdue >= 30:
            return "Internal Finance Escalation"

        return "No Escalation"