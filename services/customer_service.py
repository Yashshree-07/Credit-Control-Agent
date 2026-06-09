import pandas as pd


class CustomerService:

    def __init__(self):

        self.file_path = (
            "app/data/customers.xlsx"
        )

    def get_customers(self):

        return pd.read_excel(
            self.file_path
        )

    def get_customer_by_id(
        self,
        customer_id
    ):

        customers = (
            self.get_customers()
        )

        result = customers[
            customers["customer_id"]
            == customer_id
        ]

        if len(result) > 0:

            return result.iloc[0].to_dict()

        return None