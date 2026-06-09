class SchedulerState:

    def __init__(self):

        self.events = []

    def add_event(

        self,

        company,

        invoice,

        step,

        details
    ):

        self.events.append({

            "company": company,

            "invoice": invoice,

            "step": step,

            "details": details
        })

    def clear(self):

        self.events.clear()


scheduler_state = SchedulerState()