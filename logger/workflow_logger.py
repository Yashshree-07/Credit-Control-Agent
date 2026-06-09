import pandas as pd
from datetime import datetime
import os


class WorkflowLogger:

    FILE_PATH = (
        "app/data/workflow_execution_log.xlsx"
    )

    def clear_log(self):

        columns = [

        "run_id",
        "run_date",
        "customer_id",
        "company_name",
        "invoice_id",
        "event_title",
        "event_details",
        "event_type",
        "requires_human"
    ]

        pd.DataFrame(
        columns=columns
        ).to_excel(

        self.FILE_PATH,

        index=False
    )

    def log_event(
        self,
        run_id,
        customer_id,
        company_name,
        invoice_id,
        title,
        details,
        event_type="workflow",
        requires_human=False
    ):

        try:

            if os.path.exists(
                self.FILE_PATH
            ):

                df = pd.read_excel(
                    self.FILE_PATH
                )

            else:

                df = pd.DataFrame()

        except Exception:

            df = pd.DataFrame()

        row = {

            "run_id":
                run_id,

            "run_date":
                str(datetime.now()),

            "customer_id":
                customer_id,

            "company_name":
                company_name,

            "invoice_id":
                invoice_id,

            "event_title":
                title,

            "event_details":
                details,

            "event_type":
                event_type,

            "requires_human":
                requires_human
        }

        df = pd.concat(
            [
                df,
                pd.DataFrame([row])
            ],
            ignore_index=True
        )

        df.to_excel(
            self.FILE_PATH,
            index=False
        )

        