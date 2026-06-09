from datetime import datetime


class ReminderService:

    def determine_reminder_type(
        self,
        days_overdue
    ):

        if days_overdue <= 0:
            return "No Reminder"

        elif days_overdue <= 7:
            return "Friendly Reminder"

        elif days_overdue <= 15:
            return "Follow-up Reminder"

        elif days_overdue <= 30:
            return "Firm Reminder"

        elif days_overdue <= 90:
            return "Escalation Reminder"

        return "Critical Reminder"

    def create_reminder_message(
        self,
        company_name,
        invoice_id,
        amount,
        days_overdue
    ):

        reminder_type = (
            self.determine_reminder_type(
                days_overdue
            )
        )

        message = f"""
Dear {company_name},

This is a {reminder_type}
regarding Invoice {invoice_id}.

Outstanding Amount: ₹{amount}

Days Overdue: {days_overdue}

Please process payment at the earliest.

Regards,
Finance Team
"""

        return message