from datetime import datetime, timedelta


class FollowupScheduler:

    def calculate_next_followup(

        self,

        decision
    ):

        today = datetime.now()

        action = decision["action"]

        if action == "pause_reminders":

            return (
                today + timedelta(days=7)
            )

        if action == "schedule_followup":

            return (
                today + timedelta(days=5)
            )

        if action == "continue_followup":

            return (
                today + timedelta(days=3)
            )

        if action == "high_risk_escalation":

            return (
                today + timedelta(days=1)
            )

        return (
            today + timedelta(days=7)
        )