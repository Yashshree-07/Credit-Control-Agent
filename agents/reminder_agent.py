from datetime import datetime


class ReminderAgent:

    def determine_reminder_type(self, days_overdue):

        if days_overdue == 0:
            return "No Reminder"

        elif days_overdue <= 7:
            return "Friendly Reminder"

        elif days_overdue <= 15:
            return "Follow-up Reminder"

        elif days_overdue <= 30:
            return "Firm Reminder"

        elif days_overdue <= 90:
            return "Escalation Reminder"

        return "Critical Collection Reminder"

    def generate_message(
        self,
        customer_name,
        invoice_id,
        amount,
        reminder_type
    ):

        return f"""
Dear {customer_name},

This is regarding Invoice {invoice_id}.

Outstanding Amount: ₹{amount}
Reminder Type: {reminder_type}

Please process payment at the earliest.

Regards,
Finance Team
"""