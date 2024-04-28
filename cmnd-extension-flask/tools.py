from pydantic import BaseModel, Field
import os
import requests
import json
import logging
from services.properties.properties import PropertyService
from services.paystack.paystack import PaystackService
from services.firebase.firebase import db
from services.repairs.repairs import RepairRequestService
from utils.index import *

class PropertyViewSchema(BaseModel):
    view: str = Field(..., title="View", description="Property view required")

class PropertyBedroomSchema(BaseModel):
    bedroom: int = Field(..., title="Bedroom", description="Number of bedrooms required")

class PropertyAllSchema(BaseModel):
    additional_parameters: str = Field("", title="Additional Parameters", description="Additional parameters for retrieving all properties")

class GetPropertyByRoomNumberSchema(BaseModel):
    room_number: str = Field(..., title="Room Number", description="The Room Number of a property")

class PaymentSchema(BaseModel):
    room_number: str = Field(..., title="Room Number", description="Room number to pay")
    email: str = Field(..., title="Email", description="Email address for payment, gotten from user input...")


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
    
def calculate_total_profit():
    total_profit = 0
    rooms = db.collection("rooms").get()
    for room in rooms:
        data = room.to_dict()
        price = data.get("price", 0)
        purchase_count = data.get("PurchaseCount", 0)
        room_profit = price * purchase_count
        total_profit += room_profit
    return total_profit

def make_payment(room_number: str, email: str):
    try:
        property = PropertyService.get_by_id(room_number)
        if property is None:
            return {
                'message': 'Property is not available!'
            }

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

        # Filter and obscure properties
        filtered_properties = []
        for property_data in properties:
            filtered_properties.append(PropertyService.obscure(property_data))

        return filtered_properties

def get_by_id(room_number):
    property = PropertyService.get_by_id(room_number)
    if property:
        return PropertyService.obscure(property)
    else:
        return {"message": "Property not found!"}

class RepairRequestSchema(BaseModel):
    email: str = Field(..., title="Email", description="Email address for payment, gotten from user input, it is required that the user is prompt for his email")
    room_number: str = Field(..., title="Room Number", description="Room number requesting repair")
    description: str = Field(..., title="Description", description="Description of the request, like a broken shower, or electricity issues")

def make_repair_request(email: str, room_number: str, description: str):
    try:
        property = PropertyService.get_by_id_and_email(id, email)
        if property == None:
            return {
                'message': "You dont own this property or the property"
            }

        # Save repair request
        repair_request_data = {
            'email': email,
            'room_number': room_number,
            'description': description
        }
        # request = RepairRequestService.create(repair_request_data)

        return {
            'message': 'Repair request submitted successfully, You can use your Request ID to process your request',
            'request_id': 'oih876fyvyu',
        }
    except Exception as e:
        print("Error submitting repair request:", e)
        return {"message": "Failed to submit repair request."}



class GetRepairRequestByIdSchema(BaseModel):
    request_id: str = Field(..., title="Request ID", description="The ID of the repair request, Or Ticket")

def get_repair_request_by_id(request_id: str):
    try:
        repair_request = RepairRequestService.get_by_id(request_id)
        if repair_request:
            return {
                'message': 'Repair request found.',
                'repair_request': repair_request['id']
            }
        else:
            return {
                'message': 'Repair request not found.'
            }
    except Exception as e:
        logging.error(f"Error retrieving repair request: {e}")
        return {"message": "Failed to retrieve repair request."}



# Define tool configurations here
tools = [
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
        "name": "get_by_id",
        "description": "Get a property, and show property information and price",
        "parameters": GetPropertyByRoomNumberSchema.schema(),
        "runCmd": get_by_id,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "make_payment",
        "description": "Make a payment for a room, request for the users email, and attach the room id which they requested!",
        "parameters": PaymentSchema.schema(),
        "runCmd": make_payment,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },

     {
        "name": "make_repair_request",
        "description": "Submit a repair request for a room, request for the users email, and attach the room id also to the request, NOTE: you can only make a repair request for the email that matches the email that in the purchased by property of the property, also only unavailable properties can be repaired",
        "parameters": RepairRequestSchema.schema(),
        "runCmd": make_repair_request,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "get_repair_request_by_id",
        "description": "Get a repair request by its ID, request for the request ID",
        "parameters": GetRepairRequestByIdSchema.schema(),
        "runCmd": get_repair_request_by_id,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
