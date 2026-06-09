import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
import pandas as pd

from app.services.invoice_service import InvoiceService
from app.services.customer_service import CustomerService

from app.orchestration.workflow_manager import WorkflowManager

from app.state.workflow_state import workflow_state

from app.scheduler.scheduler_service import (
    SchedulerService
)

from app.analytics.dashboard_metrics import (
    DashboardMetrics
)
from app.state.scheduler_state import (
    scheduler_state
)

from app.services.workflow_log_service import (
    WorkflowLogService
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="AI Credit Control Agent",

    layout="wide"
)


# =====================================================
# SESSION STATE
# =====================================================

if "selected_invoice_id" not in st.session_state:

    st.session_state.selected_invoice_id = None

if "workflow_loaded" not in st.session_state:

    st.session_state.workflow_loaded = False


# =====================================================
# HEADER
# =====================================================

st.title(
    "AI Credit Control Agent"
)

st.caption(
    "Autonomous Collections • Email Intelligence • Workflow Orchestration"
)

st.divider()

st.subheader(
    "Autonomous AI Operations"
)

metrics = DashboardMetrics()

summary = metrics.get_summary()

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric(
    "Invoices",
    summary["Invoices Processed"]
)

m2.metric(
    "Reminders",
    summary["Reminders Generated"]
)

m3.metric(
    "Replies",
    summary["Replies Analyzed"]
)

m4.metric(
    "Resolved",
    summary["Auto Resolved"]
)

m5.metric(
    "Escalations",
    summary["Escalated Cases"]
)

scheduler_col1, scheduler_col2 = st.columns(
    [4, 1]
)

with scheduler_col2:

    if st.button(
        "Run Scheduler",
        use_container_width=True
    ):

        scheduler = SchedulerService()

        result = (
            scheduler.run_scheduler()
        )

        workflow_state.set_scheduler_summary(
            result
        )

        st.success(
            "Scheduler Completed"
        )

with scheduler_col1:

    if workflow_state.scheduler_summary:

        scheduler_data = (
            workflow_state.scheduler_summary
        )

        st.info(
            f"""
Invoices Processed:
{scheduler_data['processed']}

Reminders Generated:
{scheduler_data['reminders']}

Replies Analyzed:
{scheduler_data['replies']}

Auto Resolved:
{scheduler_data['auto_resolved']}

Escalations:
{scheduler_data['escalations']}
"""
        )

st.divider()


# =====================================================
# LOAD SERVICES
# =====================================================

invoice_service = InvoiceService(
    "app/data/invoices.xlsx"
)

customer_service = CustomerService()

workflow_manager = WorkflowManager()

workflow_log_service = (
    WorkflowLogService()
)


# =====================================================
# LOAD DATA
# =====================================================

invoice_df = invoice_service.process_invoices()

customer_df = customer_service.get_customers()


# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header(
    "Workflow Filters"
)

amount_filter = st.sidebar.selectbox(

    "Outstanding Amount",

    [
        "All",
        "< 100000",
        "100000 - 500000",
        "> 500000"
    ]
)

overdue_filter = st.sidebar.selectbox(

    "Overdue Days",

    [
        "All",
        "0-30",
        "31-90",
        "91-180",
        "180+"
    ]
)


# =====================================================
# APPLY FILTERS
# =====================================================

filtered_df = invoice_df.copy()

# ---------------------------------
# Amount Filter
# ---------------------------------

if amount_filter == "< 100000":

    filtered_df = filtered_df[
        filtered_df["amount_left"] < 100000
    ]

elif amount_filter == "100000 - 500000":

    filtered_df = filtered_df[

        (
            filtered_df["amount_left"] >= 100000
        )

        &

        (
            filtered_df["amount_left"] <= 500000
        )
    ]

elif amount_filter == "> 500000":

    filtered_df = filtered_df[
        filtered_df["amount_left"] > 500000
    ]

# ---------------------------------
# Overdue Filter
# ---------------------------------

if overdue_filter == "0-30":

    filtered_df = filtered_df[

        (
            filtered_df["days_overdue"] >= 0
        )

        &

        (
            filtered_df["days_overdue"] <= 30
        )
    ]

elif overdue_filter == "31-90":

    filtered_df = filtered_df[

        (
            filtered_df["days_overdue"] >= 31
        )

        &

        (
            filtered_df["days_overdue"] <= 90
        )
    ]

elif overdue_filter == "91-180":

    filtered_df = filtered_df[

        (
            filtered_df["days_overdue"] >= 91
        )

        &

        (
            filtered_df["days_overdue"] <= 180
        )
    ]

elif overdue_filter == "180+":

    filtered_df = filtered_df[
        filtered_df["days_overdue"] > 180
    ]


# =====================================================
# CUSTOMER QUEUE
# =====================================================

st.sidebar.divider()

st.sidebar.subheader(
    "Collections Queue"
)

customer_cards = []

customer_ids = filtered_df[
    "customer_id"
].unique()

for customer_id in customer_ids:

    customer_match = customer_df[

        customer_df["customer_id"]
        ==
        customer_id
    ]

    if customer_match.empty:

        continue

    customer_info = customer_match.iloc[0]

    company_name = customer_info[
        "company_name"
    ]

    customer_invoices = filtered_df[

        filtered_df["customer_id"]
        ==
        customer_id
    ]

    total_due = customer_invoices[
        "amount_left"
    ].sum()

    max_overdue = customer_invoices[
        "days_overdue"
    ].max()

    label = (
        f"{company_name} | "
        f"₹{total_due:,.0f} | "
        f"{max_overdue} days"
    )

    customer_cards.append({

        "label": label,

        "customer_id": customer_id,

        "company_name": company_name
    })


# =====================================================
# NO RESULTS
# =====================================================

if len(customer_cards) == 0:

    st.warning(
        "No companies found."
    )

    st.stop()


# =====================================================
# SELECT CUSTOMER
# =====================================================

selected_label = st.sidebar.selectbox(

    "Accounts",

    options=[

        c["label"]

        for c in customer_cards
    ]
)

selected_customer = next(

    (
        c

        for c in customer_cards

        if c["label"]
        ==
        selected_label
    ),

    None
)

if selected_customer is None:

    st.warning(
        "No customer selected."
    )

    st.stop()

selected_customer_id = (
    selected_customer["customer_id"]
)

selected_company = (
    selected_customer["company_name"]
)


# =====================================================
# CUSTOMER DATA
# =====================================================

customer_invoice_data = filtered_df[

    filtered_df["customer_id"]
    ==
    selected_customer_id
]

if customer_invoice_data.empty:

    st.warning(
        "No invoices found."
    )

    st.stop()


# =====================================================
# MAIN LAYOUT
# =====================================================

left_col, center_col, right_col = st.columns(
    [1.2, 1.2, 1.8]
)


# =====================================================
# LEFT PANEL
# =====================================================

with left_col:

    st.subheader(selected_company)

    total_due = customer_invoice_data[
        "amount_left"
    ].sum()

    total_invoices = len(
        customer_invoice_data
    )

    max_overdue = customer_invoice_data[
        "days_overdue"
    ].max()

    with st.container(border=True):

        st.markdown(
        "### Customer Portfolio"
    )

    st.metric(
        "Outstanding",
        f"₹{total_due:,.0f}"
    )

    st.metric(
        "Invoices",
        total_invoices
    )

    st.metric(
        "Max Overdue",
        f"{max_overdue} days"
    )

    st.write(
        f"Customer ID: {selected_customer_id}"
    )

    st.divider()

    st.subheader("Invoices")

    for _, invoice in customer_invoice_data.iterrows():

        invoice_id = invoice["invoice_id"]

        workflow_stage = invoice.get(
            "workflow_stage",
            "Pending"
        )

        with st.container(border=True):

            st.markdown(
                f"### {invoice_id}"
            )

            st.write(
                f"Outstanding: ₹{invoice['amount_left']:,.0f}"
            )

            st.write(
                f"Overdue: {invoice['days_overdue']} days"
            )

            st.write(
                f"Workflow: {workflow_stage}"
            )

            st.write(
                f"Status: {invoice['status']}"
            )

            if st.button(

                f"Select {invoice_id}",

                key=f"select_{invoice_id}",

                use_container_width=True
            ):

                st.session_state.selected_invoice_id = (
                    invoice_id
                )

                st.rerun()


# =====================================================
# CENTER PANEL
# =====================================================

with center_col:

    st.subheader(
        "Invoice Intelligence"
    )

    selected_invoice_id = (
        st.session_state.selected_invoice_id
    )

    if selected_invoice_id:

        selected_invoice_df = customer_invoice_data[

            customer_invoice_data["invoice_id"]
            ==
            selected_invoice_id
        ]

        if not selected_invoice_df.empty:

            selected_invoice = (
                selected_invoice_df.iloc[0]
            )

            with st.container(border=True):

                st.markdown(
                    f"### {selected_invoice_id}"
                )

                st.write(
                    f"Outstanding Amount: ₹{selected_invoice['amount_left']:,.0f}"
                )

                st.write(
                    f"Invoice Amount: ₹{selected_invoice['invoice_amount']:,.0f}"
                )

                st.write(
                    f"Days Overdue: {selected_invoice['days_overdue']}"
                )

                st.write(
                    f"Workflow Stage: {selected_invoice.get('workflow_stage', 'Pending')}"
                )

                st.write(
                    f"Reminder Count: {selected_invoice.get('reminder_count', 0)}"
                )

                st.write(
                    f"Last Sentiment: {selected_invoice.get('last_customer_sentiment', 'Unknown')}"
                )

                st.write(
                    f"Next Followup: {selected_invoice.get('next_followup_date', '-')}"
                )

            st.divider()

            # =========================================
            # RUN WORKFLOW BUTTON
            # =========================================

            if st.button(

                "Run Autonomous Email Workflow",

                use_container_width=True
            ):

                try:

                    workflow_state.clear()

                    manager = WorkflowManager()

                    manager.run_invoice_workflow(

                        customer_id=selected_customer_id,

                        invoice_id=selected_invoice_id
                    )

                    st.session_state.workflow_loaded = True

                    st.success(
                        f"Workflow executed for {selected_invoice_id}"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Workflow Error: {str(e)}"
                    )

    else:

        st.info(
            "Select an invoice to begin workflow."
        )


# =====================================================
# RIGHT PANEL
# =====================================================

with right_col:

    tab1, tab2, tab3,tab4 = st.tabs([

        "Workflow Timeline",

        "Email Intelligence",

        "Escalation Center",

        "Autonomous AI"

    ])

    # =================================================
    # TIMELINE
    # =================================================

    with tab1:

        if len(workflow_state.timeline) > 0:

            for idx, event in enumerate(
    workflow_state.timeline,
    start=1
):

                with st.container(border=True):

                    st.markdown(
                         f"### {idx}. {event['title']}"
                    )

                    st.write(
                        event["details"]
                    )

        else:

            st.info(
                "No workflow activity."
            )

    # =================================================
    # EMAILS
    # =================================================

    with tab2:

        if len(workflow_state.email_threads) > 0:

            for thread in workflow_state.email_threads:

                with st.container(border=True):

                    st.caption(
    thread["type"].upper()
)

                    st.markdown(
                        f"#### {thread['title']}"
                    )

                    st.write(
                        thread["message"]
                    )

        else:

            st.info(
                "No communication activity."
            )

    # =================================================
    # ESCALATIONS
    # =================================================

    with tab3:

        if len(workflow_state.escalations) > 0:

            for escalation in workflow_state.escalations:

                with st.container(border=True):

                    st.markdown(
                        f"#### {escalation['title']}"
                    )

                    st.write(
                        escalation["details"]
                    )

                    st.warning(
                        "Credit Controller Action Required"
                        )

        else:

            st.info(
                "No escalations."
            )
    with tab4:

            st.subheader(
            "Autonomous Scheduler Activity"
    )

    try:

        history_df = (
            workflow_log_service
            .get_logs()
        )

    except Exception:

        st.info(
            "No scheduler activity available."
        )

        history_df = pd.DataFrame()

    if history_df.empty:

        st.info(
            "Run the Scheduler to generate AI activity."
        )

    else:

        # =====================================
        # COMPANY SELECTOR
        # =====================================

        companies = sorted(

            history_df[
                "company_name"
            ]
            .dropna()
            .unique()
        )

        col1, col2 = st.columns(
            [2, 1]
        )

        with col1:

            selected_scheduler_company = (

                st.radio(

                    "Select Company",

                    companies,

                    key="scheduler_company"
                )
            )

        with col2:

            event_filter = st.selectbox(

                "Event Type",

                [

                    "All",

                    "invoice",

                    "reminder",

                    "reply",

                    "analysis",

                    "response",

                    "resolution",

                    "escalation"
                ],

                key="event_filter"
            )

        # =====================================
        # FILTER COMPANY EVENTS
        # =====================================

        company_history = history_df[

            history_df[
                "company_name"
            ]
            ==
            selected_scheduler_company
        ]

        if event_filter != "All":

            company_history = (

                company_history[

                    company_history[
                        "event_type"
                    ]
                    ==
                    event_filter
                ]
            )

        # =====================================
        # METRICS
        # =====================================

        st.metric(

            "Events Processed",

            len(company_history)
        )

        st.divider()

        # =====================================
        # TIMELINE
        # =====================================

        company_history = (

            company_history
            .sort_values(
                "run_date"
            )
        )

        for _, row in (
            company_history.iterrows()
        ):

            with st.container(
                border=True
            ):

                col_a, col_b = st.columns(
                    [4, 1]
                )

                with col_a:

                    st.markdown(

                        f"""
### {row['event_title']}
"""
                    )

                with col_b:

                    if row[
                        "requires_human"
                    ]:

                        st.warning(
                            "Human"
                        )

                st.caption(

                    f"""
Invoice:
{row['invoice_id']}
"""
                )

                st.write(
                    row[
                        "event_details"
                    ]
                )

                st.caption(

                    f"""
Run:
{row['run_id']}

{row['run_date']}
"""
                )

    

    


# =====================================================
# DEBUG
# =====================================================

with st.expander(
    "System Diagnostics"
):
    st.write(
        "Selected Customer:",
        selected_customer_id
    )

    st.write(
        "Selected Invoice:",
        st.session_state.selected_invoice_id
    )

    st.write(
        "Workflow Events:",
        len(workflow_state.timeline)
    )

    st.write(
        "Email Threads:",
        len(workflow_state.email_threads)
    )

    if hasattr(
    workflow_state,
    "scheduler_summary"
):

        st.write(
        "Scheduler Summary:",
        workflow_state.scheduler_summary
    )