class EmailUnderstandingAgent:

    def classify_intent(self, email_text):

        email = email_text.lower()

        if "already paid" in email:

            return "payment_claim"

        elif "didn't receive" in email:

            return "invoice_missing"

        elif "need more time" in email:

            return "extension_request"

        elif "incorrect" in email:

            return "invoice_dispute"

        elif "pay next week" in email:

            return "payment_commitment"

        return "general_query"

    def analyze_sentiment(self, email_text):

        email = email_text.lower()

        if (
            "angry" in email
            or "issue" in email
            or "incorrect" in email
        ):

            return {
                "label": "NEGATIVE",
                "score": 0.85
            }

        elif (
            "paid" in email
            or "thanks" in email
        ):

            return {
                "label": "POSITIVE",
                "score": 0.90
            }

        return {
            "label": "NEUTRAL",
            "score": 0.70
        }

    def process_email(self, email_text):

        intent = self.classify_intent(
            email_text
        )

        sentiment = self.analyze_sentiment(
            email_text
        )

        return {

            "intent": intent,

            "sentiment": sentiment
        }