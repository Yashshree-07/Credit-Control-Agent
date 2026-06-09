import pandas as pd
from datetime import datetime


class PaymentMonitorAgent:

    def __init__(self, invoice_path):
        self.invoice_path = invoice_path

    def load_invoices(self):
        return pd.read_excel(self.invoice_path)

    def calculate_overdue_days(self, df):
        today = datetime.today()

        df["due_date"] = pd.to_datetime(df["due_date"])

        df["days_overdue"] = (
            today - df["due_date"]
        ).dt.days

        df["days_overdue"] = df["days_overdue"].apply(
            lambda x: max(x, 0)
        )

        return df

    def assign_aging_bucket(self, days):

        if days <= 30:
            return "0-30 Days"

        elif days <= 90:
            return "31-90 Days"

        elif days <= 180:
            return "91-180 Days"

        return "180+ Days"

    def process_invoices(self):

        df = self.load_invoices()

        df = self.calculate_overdue_days(df)

        df["aging_bucket"] = df[
            "days_overdue"
        ].apply(self.assign_aging_bucket)

        return df