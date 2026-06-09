
from pydantic import BaseModel


class CustomerModel(BaseModel):

    customer_id: str

    company_name: str

    email: str

    credit_limit: float