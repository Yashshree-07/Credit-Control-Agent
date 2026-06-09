import pandas as pd

from datetime import datetime


class InvoiceService:

    def __init__(self, invoice_path):

        self.invoice_path = invoice_path

    def load_invoices(self):

        df = pd.read_excel(
            self.invoice_path
        )

        return df

    def calculate_days_overdue(
        self,
        df
    ):

        today = datetime.today()

        df["due_date"] = pd.to_datetime(
            df["due_date"],
            errors="coerce"
        )

        df["days_overdue"] = (
            today - df["due_date"]
        ).dt.days

        df["days_overdue"] = df[
            "days_overdue"
        ].fillna(0)

        df["days_overdue"] = df[
            "days_overdue"
        ].apply(
            lambda x: max(x, 0)
        )

        return df

    def calculate_aging_amounts(
        self,
        df
    ):

        numeric_columns = [

            "amount_left",

            "amount_left_since_30_days",

            "amount_left_since_90_days",

            "amount_left_since_180_days"
        ]

        for col in numeric_columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

        df[
            "amount_left_since_30_days"
        ] = df.apply(

            lambda row:
            row["amount_left"]

            if row["days_overdue"] <= 30

            else 0,

            axis=1
        )

        df[
            "amount_left_since_90_days"
        ] = df.apply(

            lambda row:
            row["amount_left"]

            if 30 < row["days_overdue"] <= 90

            else 0,

            axis=1
        )

        df[
            "amount_left_since_180_days"
        ] = df.apply(

            lambda row:
            row["amount_left"]

            if 90 < row["days_overdue"] <= 180

            else 0,

            axis=1
        )

        return df

    def assign_aging_bucket(
        self,
        days
    ):

        if days <= 30:

            return "0-30 Days"

        elif days <= 90:

            return "31-90 Days"

        elif days <= 180:

            return "91-180 Days"

        return "180+ Days"

    def process_invoices(self):

        df = self.load_invoices()

        df = self.calculate_days_overdue(
            df
        )

        df = self.calculate_aging_amounts(
            df
        )

        df["aging_bucket"] = df[
    "days_overdue"
        ].apply(
        self.assign_aging_bucket
    )

        df = df.replace(
        [float("inf"), float("-inf")],
        None
        )

        df = df.fillna("")

        return df

        