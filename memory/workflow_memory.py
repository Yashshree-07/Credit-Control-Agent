import pandas as pd


class WorkflowMemory:

    def __init__(self):

        self.invoice_file = (
            "app/data/invoices.xlsx"
        )

        self.reminder_file = (
            "app/data/reminder_logs.xlsx"
        )

        self.reply_file = (
            "app/data/customer_replies.xlsx"
        )

    # =========================================
    # SAFE COLUMN CONVERSION
    # =========================================

    def _convert_column_to_object(

        self,

        df,

        column
    ):

        if column in df.columns:

            df[column] = (
                df[column]
                .astype(object)
            )

        return df

    # =========================================
    # UPDATE INVOICE
    # =========================================

    def update_invoice(

        self,

        invoice_id,

        updates
    ):

        df = pd.read_excel(
            self.invoice_file
        )

        for column in updates.keys():

            df = self._convert_column_to_object(

                df,

                column
            )

        for column, value in updates.items():

            df.loc[

                df["invoice_id"]
                ==
                invoice_id,

                column

            ] = value

        df.to_excel(

            self.invoice_file,

            index=False
        )

    # =========================================
    # ADD REMINDER LOG
    # =========================================

    def add_reminder_log(

        self,

        reminder_data
    ):

        try:

            df = pd.read_excel(
                self.reminder_file
            )

        except:

            df = pd.DataFrame()

        new_row = pd.DataFrame([
            reminder_data
        ])

        df = pd.concat(

            [df, new_row],

            ignore_index=True
        )

        df.to_excel(

            self.reminder_file,

            index=False
        )

    # =========================================
    # ADD CUSTOMER REPLY
    # =========================================

    def add_customer_reply(

        self,

        reply_data
    ):

        try:

            df = pd.read_excel(
                self.reply_file
            )

        except:

            df = pd.DataFrame()

        # -------------------------------------
        # PREVENT DUPLICATE STORAGE
        # -------------------------------------

        if not df.empty:

            duplicate = df[

                (
                    df["invoice_id"]
                    ==
                    reply_data["invoice_id"]
                )

                &

                (
                    df["email_text"]
                    ==
                    reply_data["email_text"]
                )
            ]

            if len(duplicate) > 0:
                return

        new_row = pd.DataFrame([
            reply_data
        ])

        df = pd.concat(

            [df, new_row],

            ignore_index=True
        )

        df.to_excel(

            self.reply_file,

            index=False
        )

    # =========================================
    # GET REMINDER COUNT
    # =========================================

    def get_reminder_count(

        self,

        invoice_id
    ):

        try:

            df = pd.read_excel(
                self.reminder_file
            )

        except:

            return 0

        filtered = df[

            df["invoice_id"]
            ==
            invoice_id
        ]

        return len(filtered)
       # =========================================
    # GET ALL INVOICES
    # =========================================

    def get_all_invoices(self):

        try:

            return pd.read_excel(
                self.invoice_file
            )

        except Exception as e:

            print(
                "Invoice Load Error:",
                e
            )

            return pd.DataFrame()

    # =========================================
    # GET ALL REPLIES
    # =========================================

    def get_all_replies(self):

        try:

            return pd.read_excel(
                self.reply_file
            )

        except Exception as e:

            print(
                "Reply Load Error:",
                e
            )

            return pd.DataFrame()

    # =========================================
    # GET ALL REMINDERS
    # =========================================

    def get_all_reminders(self):

        try:

            return pd.read_excel(
                self.reminder_file
            )

        except Exception:

            return pd.DataFrame()

    # =========================================
    # SAVE WORKFLOW EXECUTION
    # =========================================

    def save_workflow_execution(

        self,

        execution_data
    ):

        file_path = (
            "app/data/workflow_execution_log.xlsx"
        )

        try:

            df = pd.read_excel(
                file_path
            )

        except:

            df = pd.DataFrame()

        new_row = pd.DataFrame([
            execution_data
        ])

        df = pd.concat(

            [df, new_row],

            ignore_index=True
        )

        df.to_excel(

            file_path,

            index=False
        )