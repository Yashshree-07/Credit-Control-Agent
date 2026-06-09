import pandas as pd

from fastapi import APIRouter

from app.ai.intent_classifier import (
    IntentClassifier
)

from app.ai.response_generator import (
    ResponseGenerator
)

from app.services.sentiment_service import (
    SentimentService
)

router = APIRouter()

intent_classifier = IntentClassifier()

response_generator = ResponseGenerator()

sentiment_service = SentimentService()


@router.get("/emails/process")
def process_customer_emails():

    df = pd.read_excel(
        "app/data/customer_replies.xlsx"
    )

    results = []

    for _, row in df.iterrows():

        # ==========================
        # SAFE EMAIL TEXT
        # ==========================

        email_text = row.get(
            "email_text",
            ""
        )

        if pd.isna(email_text):

            email_text = ""

        email_text = str(
            email_text
        ).strip()

        # ==========================
        # SKIP EMPTY ROWS
        # ==========================

        if email_text == "":

            continue

        # ==========================
        # INTENT
        # ==========================

        intent_result = (
            intent_classifier.classify(
                email_text
            )
        )

        intent = intent_result[
            "intent"
        ]

        confidence = intent_result[
            "confidence"
        ]

        # ==========================
        # SENTIMENT
        # ==========================

        sentiment_result = (
            sentiment_service.analyze(
                email_text
            )
        )

        sentiment = (
            sentiment_result.get(
                "label",
                "Neutral"
            )
        )

        # ==========================
        # CUSTOMER INFO
        # ==========================

        company_name = str(
            row.get(
                "company_name",
                "Customer"
            )
        )

        invoice_id = str(
            row.get(
                "invoice_id",
                "Unknown"
            )
        )

        overdue_days = int(
            row.get(
                "days_overdue",
                0
            )
            if pd.notna(
                row.get(
                    "days_overdue",
                    0
                )
            )
            else 0
        )

        # ==========================
        # GENERATE RESPONSE
        # ==========================

        generated_response = (

            response_generator
            .generate_response(

                customer_name=company_name,

                invoice_id=invoice_id,

                intent=intent,

                sentiment=sentiment,

                overdue_days=overdue_days
            )
        )

        results.append({

            "company_name":
                company_name,

            "invoice_id":
                invoice_id,

            "customer_email":
                email_text,

            "intent":
                intent,

            "confidence":
                confidence,

            "sentiment":
                sentiment,

            "generated_response":
                generated_response
        })

    return results