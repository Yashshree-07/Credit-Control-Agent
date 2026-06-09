import pandas as pd


class WorkflowEventService:

    def __init__(self):

        self.file_path = (
            "app/data/workflow_events.xlsx"
        )

    def get_events(self):

        return pd.read_excel(
            self.file_path
        )

    def get_company_events(
        self,
        company_name
    ):

        events = self.get_events()

        return events[

            events["company_name"]
            ==
            company_name
        ]