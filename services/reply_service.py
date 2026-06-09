import pandas as pd


class ReplyService:

    def __init__(

        self,

        file_path="app/data/customer_replies.xlsx"
    ):

        self.file_path = file_path

    # =================================================
    # LOAD REPLIES
    # =================================================

    def get_replies(self):

        try:

            df = pd.read_excel(
                self.file_path
            )

            # =========================================
            # SAFE DATE PARSING
            # =========================================

            if "reply_date" in df.columns:

                df["reply_date"] = pd.to_datetime(

                    df["reply_date"],

                    errors="coerce"
                )

            return df

        except Exception as e:

            print(
                f"Reply Load Error: {str(e)}"
            )

            return pd.DataFrame()