from typing import TypedDict

from langgraph.graph import StateGraph


class CreditState(TypedDict):
    invoice_id: str
    overdue_days: int
    action: str


def check_invoice(state):

    overdue_days = state["overdue_days"]

    if overdue_days <= 0:
        state["action"] = "close"

    elif overdue_days <= 30:
        state["action"] = "send_reminder"

    elif overdue_days <= 90:
        state["action"] = "escalate"

    else:
        state["action"] = "legal"

    return state


workflow = StateGraph(CreditState)

workflow.add_node(
    "invoice_check",
    check_invoice
)

workflow.set_entry_point(
    "invoice_check"
)

workflow.set_finish_point(
    "invoice_check"
)

app = workflow.compile()