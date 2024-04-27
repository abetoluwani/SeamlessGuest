import pymysql
from pydantic import BaseModel, Field
import os
import requests
import json
import logging


class PropertyViewSchema(BaseModel):
    view: str = Field(..., title="View", description="Property view required")

class PropertyBedroomSchema(BaseModel):
    bedroom: int = Field(..., title="Bedroom", description="Number of bedrooms required")

class PropertyAllSchema(BaseModel):
    additional_parameters: str = Field(..., title="Additional Parameters", description="Additional parameters for retrieving all properties")

class PaymentSchema(BaseModel):
    room_number: int = Field(..., title="Room Number", description="Room number to pay for")
    payment_amount: float = Field(..., title="Payment Amount", description="Amount to pay")
    email: str = Field(..., title="Email", description="Email address for payment")

class CreatePaystackPageSchema(BaseModel):
    name: str = Field(..., title="Page Name", description="Name of the page")
    amount: int = Field(..., title="Amount", description="Amount of the page")
    description: str = Field(..., title="Description", description="Description of the page")

class InitializeTransactionSchema(BaseModel):
    amount: int = Field(..., title="Amount", description="Amount of the transaction")
    email: str = Field(..., title="Email", description="Email address for the transaction")
    reference: str = Field("", title="Reference", description="Reference for the transaction")

class VerifyTransactionSchema(BaseModel):
    reference: str = Field(..., title="Reference", description="Reference for the transaction")

class ChargeTransactionSchema(BaseModel):
    authorization_code: str = Field(..., title="Authorization Code", description="Authorization code for the transaction")
    amount: int = Field(..., title="Amount", description="Amount of the transaction")
    email: str = Field(..., title="Email", description="Email address for the transaction")
    reference: str = Field(..., title="Reference", description="Reference for the transaction")   
     
def custom_json_schema(model):
    schema = model.schema()
    properties_formatted = {
        k: {
            "title": v.get("title"),
            "type": v.get("type")
        } for k, v in schema["properties"].items()
    }

    return {
        "type": "object",
        "default": {},
        "properties": properties_formatted,
        "required": schema.get("required", [])
    }

def retrieve_by_view(view: str):
    cursor = db.cursor()
    sql = "SELECT * FROM Rooms WHERE ViewDescription = %s"
    cursor.execute(sql, (view,))
    return cursor.fetchall()

def retrieve_by_bedroom(bedroom: int):
    cursor = db.cursor()
    sql = "SELECT * FROM Rooms WHERE Beds = %s"
    cursor.execute(sql, (bedroom,))
    return cursor.fetchall()

def retrieve_by_individual(individuals: int):
    cursor = db.cursor()
    sql = "SELECT * FROM Rooms WHERE Individuals = %s"
    cursor.execute(sql, (individuals,))
    return cursor.fetchall()

def retrieve_all():
    cursor = db.cursor()
    sql = "SELECT * FROM Rooms"
    cursor.execute(sql)
    return cursor.fetchall()

def create_paystack_page():
    url = "https://api.paystack.co/page"
    headers = {
        "Authorization": f"Bearer {os.getenv('PAYSTACK_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "name": "Buttercup Brunch",
        "amount": 500000,
        "description": "Gather your friends for the ritual that is brunch"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info("Paystack page created successfully")
        return response.json()
    else:
        error_msg = f"Failed to create Paystack page. Status code: {response.status_code}"
        logging.error(error_msg)
        raise Exception(error_msg)

def initialize_transaction(amount, email, ref=None):
    api_secret = os.getenv('PAYSTACK_KEY')
    data = {'amount': amount, 'email': email, 'reference': ref}
    headers = {'Authorization': f'Bearer {api_secret}'}
    url = 'https://api.paystack.co/transaction/initialize'
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info("Transaction initialized successfully")
        return response.json()
    else:
        error_msg = f"Failed to initialize transaction. Status code: {response.status_code}"
        logging.error(error_msg)
        raise Exception(error_msg)

def verify_transaction(ref):
    api_secret = os.getenv('PAYSTACK_KEY')
    headers = {'Authorization': f'Bearer {api_secret}'}
    url = f'https://api.paystack.co/transaction/verify/{ref}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logging.info("Transaction verified successfully")
        return response.json()
    else:
        error_msg = f"Failed to verify transaction. Status code: {response.status_code}"
        logging.error(error_msg)
        raise Exception(error_msg)

def charge_transaction(auth_code=None, amount=None, email=None, reference=None):
    api_secret = os.getenv('PAYSTACK_KEY')
    data = {'authorization_code': auth_code, 'amount': amount, 'email': email, 'reference': reference}
    headers = {'Authorization': f'Bearer {api_secret}'}
    url = 'https://api.paystack.co/transaction/charge'
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info("Transaction charged successfully")
        return response.json()
    else:
        error_msg = f"Failed to charge transaction. Status code: {response.status_code}"
        logging.error(error_msg)
        raise Exception(error_msg)

def make_payment(room_number: int, payment_amount: float, email: str):
    try:
        ref = f"room-{room_number}-payment"
        initialize_transaction
        response = initialize_transaction(int(payment_amount * 100), email, ref)

        if response.get("status") == True:
            auth_code = response.get("data").get("authorization_code")
            response = charge_transaction(auth_code, int(payment_amount * 100), email, ref)
            if response.get("status") == True:
                logging.info("Payment successful")
                return {"message": "Payment successful"}
            else:
                logging.error("Payment failed during charge")
                return {"message": "Payment failed"}
        else:
            logging.error("Failed to initialize transaction")
            return {"message": "Failed to initialize transaction"}
    except Exception as e:
        logging.error(f"Error making payment: {e}")
        return {"message": str(e)}

# Define tool configurations here

tools = [
    # { // 5 bedrooms
    #     "name": "retrieve_by_bedroom",
    #     "description": "Retrieve properties based on the number of bedrooms",
    #     "parameters": custom_json_schema(PropertyBedroomSchema),
    #     "runCmd": retrieve_by_bedroom,
    #     "isDangerous": False,
    #     "functionType": "backend",
    #     "isLongRunningTool": False,
    #     "rerun": True,
    #     "rerunWithDifferentParameters": True
    # },
    {
        "name": "retrieve_all",
        "description": "Retrieve all properties, and list each property information and price",
        "parameters": custom_json_schema(PropertyAllSchema),
        "runCmd": retrieve_all,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "make_payment",
        "description": "Make a payment for a room",
        "parameters": custom_json_schema(PaymentSchema),
        "runCmd": make_payment,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },

    {
        "name": "create_paystack_page",
        "description": "Create a Paystack page",
        "parameters": custom_json_schema(CreatePaystackPageSchema),
        "runCmd": create_paystack_page,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "initialize_transaction",
        "description": "Initialize a Paystack transaction",
        "parameters": custom_json_schema(InitializeTransactionSchema),
        "runCmd": initialize_transaction,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "verify_transaction",
        "description": "Verify a Paystack transaction",
        "parameters": custom_json_schema(VerifyTransactionSchema),
        "runCmd": verify_transaction,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "charge_transaction",
        "description": "Charge a Paystack transaction",
        "parameters": custom_json_schema(ChargeTransactionSchema),
        "runCmd": charge_transaction,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
