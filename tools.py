import pymysql
from pydantic import BaseModel, Field
from data_sql import db
import os
import requests
import json
import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PropertyViewSchema(BaseModel):
    view: str = Field(..., title="View", description="Property view required")

class PropertyBedroomSchema(BaseModel):
    bedroom: int = Field(..., title="Bedroom", description="Number of bedrooms required")

class PropertyIndividualSchema(BaseModel):
    individuals: int = Field(..., title="Individuals", description="Number of individuals required")

class PropertyAllSchema(BaseModel):
    additional_parameters: str = Field("", title="Additional Parameters", description="Additional parameters for retrieving all properties")

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
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM Rooms WHERE ViewDescription = %s"
        cursor.execute(sql, (view,))
        result = cursor.fetchall()
        logging.info(f"Retrieved {len(result)} records for view: {view}")
        return result
    except pymysql.Error as e:
        logging.error(f"Database error occurred: {e}")
        raise Exception(f"Failed to retrieve records: {e}")

def retrieve_by_bedroom(bedroom: int):
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM Rooms WHERE Beds = %s"
        cursor.execute(sql, (bedroom,))
        result = cursor.fetchall()
        logging.info(f"Retrieved {len(result)} records for bedroom count: {bedroom}")
        return result
    except pymysql.Error as e:
        logging.error(f"Database error occurred: {e}")
        raise Exception(f"Failed to retrieve records: {e}")

def retrieve_by_individual(individuals: int):
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM Rooms WHERE Individuals = %s"
        cursor.execute(sql, (individuals,))
        result = cursor.fetchall()
        logging.info(f"Retrieved {len(result)} records for individual count: {individuals}")
        return result
    except pymysql.Error as e:
        logging.error(f"Database error occurred: {e}")
        raise Exception(f"Failed to retrieve records: {e}")

def retrieve_all():
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM Rooms"
        cursor.execute(sql)
        result = cursor.fetchall()
        logging.info(f"Retrieved all rooms, count: {len(result)}")
        return result
    except pymysql.Error as e:
        logging.error(f"Database error occurred: {e}")
        raise Exception(f"Failed to retrieve records: {e}")

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
    {
        "name": "retrieve_by_view",
        "description": "Retrieve properties based on the view",
        "parameters": custom_json_schema(PropertyViewSchema),
        "runCmd": retrieve_by_view,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "retrieve_by_individual",
        "description": "Retrieve properties based on the number of individuals",
        "parameters": custom_json_schema(PropertyIndividualSchema),
        "runCmd": retrieve_by_individual,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "retrieve_all",
        "description": "Retrieve all properties",
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













# import pymysql
# from pydantic import BaseModel, Field
# from data_sql import db
# import os
# import requests

# class PropertyViewSchema(BaseModel):
#     view: str = Field(..., title="View", description="Property view required")

# class PropertyBedroomSchema(BaseModel):
#     bedroom: int = Field(..., title="Bedroom", description="Number of bedrooms required")

# class PropertyIndividualSchema(BaseModel):
#     individuals: int = Field(..., title="Individuals", description="Number of individuals required")

# class PropertyAllSchema(BaseModel):
#     additional_parameters: str = Field("", title="Additional Parameters", description="Additional parameters for retrieving all properties")

# class PaymentSchema(BaseModel):
#     room_number: int = Field(..., title="Room Number", description="Room number to pay for")
#     payment_amount: float = Field(..., title="Payment Amount", description="Amount to pay")

# def custom_json_schema(model):
#     schema = model.schema()
#     properties_formatted = {
#         k: {
#             "title": v.get("title"),
#             "type": v.get("type")
#         } for k, v in schema["properties"].items()
#     }

#     return {
#         "type": "object",
#         "default": {},
#         "properties": properties_formatted,
#         "required": schema.get("required", [])
#     }

# def retrieve_by_view(view: str):
#     cursor = db.cursor()
#     sql = "SELECT * FROM Rooms WHERE ViewDescription = %s"
#     cursor.execute(sql, (view,))
#     return cursor.fetchall()

# def retrieve_by_bedroom(bedroom: int):
#     cursor = db.cursor()
#     sql = "SELECT * FROM Rooms WHERE Beds = %s"
#     cursor.execute(sql, (bedroom,))
#     return cursor.fetchall()

# def retrieve_by_individual(individuals: int):
#     cursor = db.cursor()
#     sql = "SELECT * FROM Rooms WHERE Individuals = %s"
#     cursor.execute(sql, (individuals,))
#     return cursor.fetchall()

# def retrieve_all():
#     cursor = db.cursor()
#     sql = "SELECT * FROM Rooms"
#     cursor.execute(sql)
#     return cursor.fetchall()

# def make_payment(room_number: int, payment_amount: float):
#     url = "https://api.paystack.co/page"
#     authorization = "Authorization: Bearer sk_test_1234567890abcdef"
#     content_type = "Content-Type: application/json"
#     data = {
#         "name": "Room Payment",
#         "amount": int(payment_amount * 100),  # Convert to kobo
#         "description": "Payment for room {}".format(room_number)
#     }
#     response = requests.post(url, headers={"Authorization": authorization, "Content-Type": "application/json"}, json=data)
#     if response.status_code == 200:
#         return {"message": "Payment successful"}
#     else:
#         return {"message": "Payment failed"}

# tools = [
#     {
#         "name": "retrieve_by_view",
#         "description": "Retrieve properties based on the view",
#         "parameters": custom_json_schema(PropertyViewSchema),
#         "runCmd": retrieve_by_view,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     },
#     {
#         "name": "retrieve_by_bedroom",
#         "description": "Retrieve properties based on the number of bedrooms",
#         "parameters": custom_json_schema(PropertyBedroomSchema),
#         "runCmd": retrieve_by_bedroom,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     },
#    {
#         "name": "retrieve_by_individual",
#         "description": "Retrieve properties based on the number of individuals",
#         "parameters": custom_json_schema(PropertyIndividualSchema),
#         "runCmd": retrieve_by_individual,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     },
#     {
#         "name": "retrieve_all",
#         "description": "Retrieve all properties",
#         "parameters": custom_json_schema(PropertyAllSchema),
#         "runCmd": retrieve_all,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     },
#     {
#         "name": "make_payment",
#         "description": "Make a payment for a room",
#         "parameters": custom_json_schema(PaymentSchema),
#         "runCmd": make_payment,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     }
# ]







# import os
# from pydantic import BaseModel, Field
# import requests

# class PropertyViewSchema(BaseModel):
#     view: str = Field(..., title="View", description="Property view required")

# class PropertyBedroomSchema(BaseModel):
#     bedroom: int = Field(..., title="Bedroom", description="Number of bedrooms required")

# class PropertyIndividualSchema(BaseModel):
#     id: int = Field(..., title="ID", description="Property ID required")

# class PropertyAllSchema(BaseModel):
#     additional_parameters: str = Field("", title="Additional Parameters", description="Additional parameters for retrieving all properties")


# def retrieve_by_view(view: str):
#     url = f"https://dummyjson.com/products/search?q={view}"
#     response = requests.get(url)
#     return response.json()

# def retrieve_by_bedroom(bedroom: int):
#     url = f"https://dummyjson.com/products/search?q={bedroom}"
#     response = requests.get(url)
#     return response.json()

# def retrieve_by_individual(id: int):
#     url = f"https://dummyjson.com/products/search?q={id}"
#     response = requests.get(url)
#     return response.json()

# def retrieve_all():
#     url = "https://dummyjson.com/products"
#     response = requests.get(url)
#     return response.json()


# def custom_json_schema(model):
#     schema = model.schema()
#     properties_formatted = {
#         k: {
#             "title": v.get("title"),
#             "type": v.get("type")
#         } for k, v in schema["properties"].items()
#     }

#     return {
#         "type": "object",
#         "default": {},
#         "properties": properties_formatted,
#         "required": schema.get("required", [])
#     }

# tools = [
#     {
#         "name": "retrieve_by_view",
#         "description": "Retrieve properties based on the view",
#         "parameters": custom_json_schema(PropertyViewSchema),
#         "runCmd": retrieve_by_view,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     },
#     {
#         "name": "retrieve_by_bedroom",
#         "description": "Retrieve properties based on the number of bedrooms",
#         "parameters": custom_json_schema(PropertyBedroomSchema),
#         "runCmd": retrieve_by_bedroom,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     },
#     {
#         "name": "retrieve_by_individual",
#         "description": "Retrieve a property based on its ID",
#         "parameters": custom_json_schema(PropertyIndividualSchema),
#         "runCmd": retrieve_by_individual,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     },
#     {
#         "name": "retrieve_all",
#         "description": "Retrieve all properties",
#         "parameters": custom_json_schema(PropertyAllSchema),
#         "runCmd": retrieve_all,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     }
# ]

















# import os
# from pydantic import BaseModel, Field
# import requests


# class ProductFinderSchema(BaseModel):
#     product: str = Field(..., title="Product", description="Product name required")

# class WeatherCitySchema(BaseModel):
#     city: str = Field(..., title="City", description="City name required")

# class FilePathSchema(BaseModel):
#     filePath: str = Field(..., title="Filepath", description="File path required")

# def product_finder(product: str):
#     url = f"https://dummyjson.com/products/search?q={product}"
#     response = requests.get(url)
#     return response.json()

# def weather_from_location(city: str):
#     api_key = os.getenv('WEATHER_API_KEY')
#     if not api_key:
#         raise ValueError("API key for weather data is not set in environment variables.")
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
#     response = requests.get(url)
#     return response.json()

# def file_reader(filePath: str):
#     try:
#         with open(filePath, 'r') as file:
#             return file.read()
#     except Exception as e:
#         return str(e)

# def custom_json_schema(model):
#     schema = model.schema()
#     properties_formatted = {
#         k: {
#             "title": v.get("title"),
#             "type": v.get("type")
#         } for k, v in schema["properties"].items()
#     }

#     return {
#         "type": "object",
#         "default": {},
#         "properties": properties_formatted,
#         "required": schema.get("required", [])
#     }

# tools = [
#     {
#         "name": "product_finder",
#         "description": "Finds and returns dummy products details based on the product name passed to it",
#         "parameters": custom_json_schema(ProductFinderSchema),
#         "runCmd": product_finder,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     },
#     {
#         "name": "weather_from_location",
#         "description": "Gets the weather details from a given city name",
#         "parameters": custom_json_schema(WeatherCitySchema),
#         "runCmd": weather_from_location,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     },
#     {
#         "name": "file_reader",
#         "description": "Returns the contents of a file given its filepath",
#         "parameters": custom_json_schema(FilePathSchema),
#         "runCmd": file_reader,
#         "isDangerous": False,
#         "functionType": "backend",
#         "isLongRunningTool": False,
#         "rerun": True,
#         "rerunWithDifferentParameters": True
#     }
# ]
# # retrieve by view 
# # retieve by bedroom  
# # retrive by individual 
# # retrive by All
