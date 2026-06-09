from rapidfuzz import fuzz


class IntentClassifier:

    def __init__(self):

        self.intent_patterns = {

            "payment_commitment": [

                "will pay",
                "payment initiated",
                "clear dues",
                "release payment",
                "payment by friday",
                "payment in process"
            ],

            "invoice_missing": [

                "did not receive invoice",
                "invoice missing",
                "resend invoice",
                "unable to find invoice"
            ],

            "extension_request": [

                "need more time",
                "extension",
                "few more days",
                "delay payment"
            ],

            "invoice_dispute": [

                "incorrect invoice",
                "wrong amount",
                "invoice issue",
                "pricing mismatch",
                "dispute"
            ],

            "already_paid": [

                "already paid",
                "payment completed",
                "paid yesterday",
                "payment done"
            ]
        }

    def classify(

        self,

        email_text
    ):

        # ==========================
        # HANDLE EMPTY VALUES
        # ==========================

        if email_text is None:

            return {

                "intent": "no_response",

                "confidence": 0
            }

        if str(email_text).strip() == "":

            return {

                "intent": "no_response",

                "confidence": 0
            }

        text = str(email_text).lower()

        best_intent = "general_query"

        highest_score = 0

        for intent, phrases in (

            self.intent_patterns.items()

        ):

            for phrase in phrases:

                score = fuzz.partial_ratio(

                    text,

                    phrase
                )

                if score > highest_score:

                    highest_score = score

                    best_intent = intent

        confidence = round(

            highest_score / 100,

            2
        )

        return {

            "intent": best_intent,

            "confidence": confidence
        }