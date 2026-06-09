import pandas as pd


class WorkflowState:

    def __init__(self):

        # =====================================
        # WORKFLOW TIMELINE
        # =====================================
        self.timeline = []

        # =====================================
        # EMAIL COMMUNICATIONS
        # =====================================
        self.email_threads = []

        # =====================================
        # ESCALATIONS
        # =====================================
        self.escalations = []

        # =====================================
        # SCHEDULER SUMMARY
        # =====================================
        self.scheduler_summary = {}

        # =====================================
        # COMPANY WORKFLOWS
        # =====================================
        self.company_workflows = {}

        # =====================================
        # FILE PATHS (FIXED MISSING ATTRIBUTES)
        # =====================================
        self.invoice_file = "app/data/invoices.xlsx"
        self.reply_file = "app/data/customer_replies.xlsx"

    # =================================================
    # SCHEDULER SUMMARY
    # =================================================
    def set_scheduler_summary(self, summary):
        self.scheduler_summary = summary

    # =================================================
    # ADD TIMELINE EVENT
    # =================================================
    def add_event(self, event_type=None, title=None, details=None, event=None):

        if event is not None:
            self.timeline.append(event)
            return

        event_data = {
            "event_type": event_type if event_type else "INFO",
            "title": title if title else "Workflow Event",
            "details": details if details else ""
        }

        self.timeline.append(event_data)

    # =================================================
    # COMPANY WORKFLOW
    # =================================================
    def store_company_workflow(self, company_name, event):

        if company_name not in self.company_workflows:
            self.company_workflows[company_name] = []

        self.company_workflows[company_name].append(event)

    def get_company_workflow(self, company_name):
        return self.company_workflows.get(company_name, [])

    # =================================================
    # GET ALL INVOICES
    # =================================================
    def get_all_invoices(self):
        try:
            return pd.read_excel(self.invoice_file)
        except Exception:
            return pd.DataFrame()

    # =================================================
    # GET ALL REPLIES
    # =================================================
    def get_all_replies(self):
        try:
            return pd.read_excel(self.reply_file)
        except Exception:
            return pd.DataFrame()

    # =================================================
    # SAVE WORKFLOW EXECUTION
    # =================================================
    def save_workflow_execution(self, execution_data):

        execution_file = "app/data/workflow_execution_logs.xlsx"

        try:
            df = pd.read_excel(execution_file)
        except Exception:
            df = pd.DataFrame()

        new_row = pd.DataFrame([execution_data])

        df = pd.concat([df, new_row], ignore_index=True)

        df.to_excel(execution_file, index=False)

    # =================================================
    # ADD EMAIL THREAD
    # =================================================
    def add_email_thread(self, thread_type=None, title=None, message=None, thread=None):

        if thread is not None:
            self.email_threads.append(thread)
            return

        thread_data = {
            "type": thread_type if thread_type else "Communication",
            "title": title if title else "Email Thread",
            "message": message if message else ""
        }

        self.email_threads.append(thread_data)

    # =================================================
    # ADD ESCALATION
    # =================================================
    def add_escalation(self, title=None, details=None, escalation=None):

        if escalation is not None:
            self.escalations.append(escalation)
            return

        escalation_data = {
            "title": title if title else "Escalation",
            "details": details if details else ""
        }

        self.escalations.append(escalation_data)

    # =================================================
    # CLEAR STATE
    # =================================================
    def clear(self):
        self.timeline.clear()
        self.email_threads.clear()
        self.escalations.clear()
        self.scheduler_summary = {}


# =====================================================
# GLOBAL STATE
# =====================================================
workflow_state = WorkflowState()