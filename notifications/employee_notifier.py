from datetime import datetime


class EmployeeNotifier:

    def create_notification(

        self,

        company_name,

        invoice_id,

        escalation_reasons,

        customer_email,

        ai_summary
    ):

        return {

            "timestamp":
                datetime.now(),

            "company_name":
                company_name,

            "invoice_id":
                invoice_id,

            "escalation_reason":
                ", ".join(
                    escalation_reasons
                ),

            "customer_email":
                customer_email,

            "ai_summary":
                ai_summary,

            "status":
                "OPEN"
        }