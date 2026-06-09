import pandas as pd


class WorkflowLogService:

    FILE_PATH = (
        "app/data/workflow_execution_log.xlsx"
    )

    def get_logs(self):

        try:

            return pd.read_excel(
                self.FILE_PATH
            )

        except Exception:

            return pd.DataFrame()

    def get_companies(self):

        df = self.get_logs()

        if len(df) == 0:

            return []

        return sorted(

            df["company_name"]
            .dropna()
            .unique()
        )

    def get_company_logs(
        self,
        company_name
    ):

        df = self.get_logs()

        return df[

            df["company_name"]
            ==
            company_name
        ]