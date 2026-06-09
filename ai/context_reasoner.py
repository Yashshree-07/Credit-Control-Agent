from datetime import datetime, timedelta
import re


class ContextReasoner:

    def analyze_customer_context(

        self,

        email_text,

        detected_intent,

        sentiment
    ):

        text = email_text.lower()

        result = {

            "customer_cooperative": False,

            "payment_commitment": False,

            "requested_extension": False,

            "dispute_detected": False,

            "likely_payment_date": None,

            "recommended_action": None
        }

        # =====================================
        # PAYMENT PROMISE
        # =====================================

        if any(

            keyword in text

            for keyword in [

                "clear dues",

                "pay next",

                "payment by",

                "will pay",

                "release payment",

                "process payment"
            ]
        ):

            result[
                "payment_commitment"
            ] = True

            result[
                "customer_cooperative"
            ] = True

            result[
                "recommended_action"
            ] = "wait_for_payment"

        # =====================================
        # EXTENSION REQUEST
        # =====================================

        if any(

            keyword in text

            for keyword in [

                "need more time",

                "extension",

                "few more days"
            ]
        ):

            result[
                "requested_extension"
            ] = True

            result[
                "recommended_action"
            ] = "schedule_followup"

        # =====================================
        # DISPUTE
        # =====================================

        if any(

            keyword in text

            for keyword in [

                "incorrect invoice",

                "wrong amount",

                "dispute",

                "issue in invoice"
            ]
        ):

            result[
                "dispute_detected"
            ] = True

            result[
                "recommended_action"
            ] = "human_review"

        return result