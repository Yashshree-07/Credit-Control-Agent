from fastapi import APIRouter
import pandas as pd
import numpy as np

from app.services.invoice_service import (
    InvoiceService
)

router = APIRouter()

invoice_service = InvoiceService(
    "app/data/invoices.xlsx"
)


# ==========================================
# HELPER FUNCTION
# ==========================================

def clean_dataframe(df):

    df = df.replace(
        [np.inf, -np.inf],
        None
    )

    df = df.fillna("")

    return df


# ==========================================
# GET ALL INVOICES
# ==========================================

@router.get("/invoices")
def get_invoices():

    invoices = (
        invoice_service
        .process_invoices()
    )

    # DEBUG
    print(
        "\n===== NULL COUNTS ====="
    )

    print(
        invoices.isna().sum()
    )

    invoices = clean_dataframe(
        invoices
    )

    return invoices.to_dict(
        orient="records"
    )


# ==========================================
# AGING SUMMARY
# ==========================================

@router.get("/invoices/aging-summary")
def aging_summary():

    df = (
        invoice_service
        .process_invoices()
    )

    df = clean_dataframe(df)

    summary = {

        "0_30_days":
            float(
                pd.to_numeric(
                    df[
                        "amount_left_since_30_days"
                    ],
                    errors="coerce"
                )
                .fillna(0)
                .sum()
            ),

        "31_90_days":
            float(
                pd.to_numeric(
                    df[
                        "amount_left_since_90_days"
                    ],
                    errors="coerce"
                )
                .fillna(0)
                .sum()
            ),

        "91_180_days":
            float(
                pd.to_numeric(
                    df[
                        "amount_left_since_180_days"
                    ],
                    errors="coerce"
                )
                .fillna(0)
                .sum()
            ),

        "total_due":
            float(
                pd.to_numeric(
                    df["amount_left"],
                    errors="coerce"
                )
                .fillna(0)
                .sum()
            )
    }

    return summary


# ==========================================
# OVERDUE INVOICES
# ==========================================

@router.get("/invoices/overdue")
def overdue_invoices():

    df = (
        invoice_service
        .process_invoices()
    )

    overdue_df = df[

        pd.to_numeric(
            df["days_overdue"],
            errors="coerce"
        ).fillna(0)

        > 0
    ]

    overdue_df = clean_dataframe(
        overdue_df
    )

    return overdue_df.to_dict(
        orient="records"
    )