from fastapi import FastAPI

from app.api.invoices import router as invoice_router
from app.api.reminders import router as reminder_router
from app.api.emails import router as email_router
from app.api.dashboard import router as dashboard_router

app = FastAPI(debug=True)

app.include_router(invoice_router)
app.include_router(reminder_router)
app.include_router(email_router)
app.include_router(dashboard_router)


@app.get("/")
def home():

    return {
        "message": "Credit Control Agent Running"
    }

