class ActionDecisionEngine:

    def decide_next_action(

        self,

        context_result,

        overdue_days,

        amount
    ):

        if (
            context_result[
                "payment_commitment"
            ]
        ):

            return {

                "action":
                    "pause_reminders",

                "human_intervention":
                    False,

                "workflow_stage":
                    "Waiting For Payment"
            }

        if (
            context_result[
                "requested_extension"
            ]
        ):

            return {

                "action":
                    "schedule_followup",

                "human_intervention":
                    False,

                "workflow_stage":
                    "Extension Requested"
            }

        if (
            context_result[
                "dispute_detected"
            ]
        ):

            return {

                "action":
                    "escalate_dispute",

                "human_intervention":
                    True,

                "workflow_stage":
                    "Dispute Escalated"
            }

        if overdue_days > 90:

            return {

                "action":
                    "high_risk_escalation",

                "human_intervention":
                    True,

                "workflow_stage":
                    "Critical Overdue"
            }

        return {

            "action":
                "continue_followup",

            "human_intervention":
                False,

            "workflow_stage":
                "Automated Followup"
        }