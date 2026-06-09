from fastapi import APIRouter

from app.services.invoice_service import (
    InvoiceService
)

router = APIRouter()

invoice_service = InvoiceService(
    "app/data/invoices.xlsx"
)


@router.get("/dashboard")
def dashboard_summary():

    df = invoice_service.process_invoices()

    total_due = df[
        "amount_left"
    ].sum()

    total_overdue = df[
        df["days_overdue"] > 0
    ]["amount_left"].sum()

    total_invoices = len(df)

    critical_cases = len(
        df[df["days_overdue"] > 180]
    )

    return {

        "total_due":
            float(total_due),

        "total_overdue":
            float(total_overdue),

        "total_invoices":
            total_invoices,

        "critical_cases":
            critical_cases
    }