import pymysql
from pydantic import BaseModel, Field
import os
import requests
import json
import logging
from services.properties.properties import PropertyService
from services.paystack.paystack import PaystackService
from services.firebase.firebase import db


class PropertyViewSchema(BaseModel):
    view: str = Field(..., title="View", description="Property view required")

class PropertyBedroomSchema(BaseModel):
    bedroom: int = Field(..., title="Bedroom", description="Number of bedrooms required")

class PropertyAllSchema(BaseModel):
    additional_parameters: str = Field("", title="Additional Parameters", description="Additional parameters for retrieving all properties")

class PaymentSchema(BaseModel):
    room_number: str = Field(..., title="Room Number", description="Room number to pay")
    # payment_amount: float = Field(..., title="Payment Amount", description="Amount to pay, from the Property")
    email: str = Field(..., title="Email", description="Email address for payment, gotten from user input...")

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

def make_payment(room_number: str, email: str):
    try:
        property = PropertyService.get_by_id(room_number)
        response = PaystackService.initialize({
            'email': email,
            'amount': property['price'],
            'callback_url': PaystackService.callback_url,
            'metadata': {
                'email': email,
                'room_number': room_number,
                'amount': property['price'],
            }
        })
        return {
            'paymentLink': response['authorization_url'],
        }

    except Exception as e:
        logging.error(f"Error making payment: {e}")
        return {"message": str(e)}

def get_all():
    properties = PropertyService.get_all()

    # Define the allowed fields
    allowed_fields = [
        'RoomNumber',
        'BuildingName',
        'RoomLatitude',
        'RoomLongitude',
        'RoomSize',
        'Beds',
        'Individuals',
        'ViewDescription',
        'price',
        'available'
    ]

    # Filter and obscure properties
    filtered_properties = []
    for property_data in properties:
        filtered_property = {}
        for field in allowed_fields:
            filtered_property[field] = property_data.get(field, '[Obscured]')
        filtered_properties.append(filtered_property)

    return filtered_properties

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
        "name": "get_all_properties",
        "description": "Get all properties, and list each property information and price",
        "parameters": PropertyAllSchema.schema(),
        "runCmd": get_all,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "make_payment",
        "description": "Make a payment for a room, request for the users email, and attach the room id which they requested!",
        "parameters": custom_json_schema(PaymentSchema),
        "runCmd": make_payment,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },

    # {
    #     "name": "create_paystack_page",
    #     "description": "Create a Paystack page",
    #     "parameters": custom_json_schema(CreatePaystackPageSchema),
    #     "runCmd": create_paystack_page,
    #     "isDangerous": False,
    #     "functionType": "backend",
    #     "isLongRunningTool": False,
    #     "rerun": True,
    #     "rerunWithDifferentParameters": True
    # },
    # {
    #     "name": "initialize_transaction",
    #     "description": "Initialize a Paystack transaction",
    #     "parameters": custom_json_schema(InitializeTransactionSchema),
    #     "runCmd": initialize_transaction,
    #     "isDangerous": False,
    #     "functionType": "backend",
    #     "isLongRunningTool": False,
    #     "rerun": True,
    #     "rerunWithDifferentParameters": True
    # },
    # {
    #     "name": "verify_transaction",
    #     "description": "Verify a Paystack transaction",
    #     "parameters": custom_json_schema(VerifyTransactionSchema),
    #     "runCmd": verify_transaction,
    #     "isDangerous": False,
    #     "functionType": "backend",
    #     "isLongRunningTool": False,
    #     "rerun": True,
    #     "rerunWithDifferentParameters": True
    # },
    # {
    #     "name": "charge_transaction",
    #     "description": "Charge a Paystack transaction",
    #     "parameters": custom_json_schema(ChargeTransactionSchema),
    #     "runCmd": charge_transaction,
    #     "isDangerous": False,
    #     "functionType": "backend",
    #     "isLongRunningTool": False,
    #     "rerun": True,
    #     "rerunWithDifferentParameters": True
    # }
]
