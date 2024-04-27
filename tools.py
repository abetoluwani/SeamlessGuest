

import pymysql
from pydantic import BaseModel, Field
from data_sql import db
import os

class PropertyViewSchema(BaseModel):
    view: str = Field(..., title="View", description="Property view required")

class PropertyBedroomSchema(BaseModel):
    bedroom: int = Field(..., title="Bedroom", description="Number of bedrooms required")

class PropertyIndividualSchema(BaseModel):
    individuals: int = Field(..., title="Individuals", description="Number of individuals required")

class PropertyAllSchema(BaseModel):
    additional_parameters: str = Field("", title="Additional Parameters", description="Additional parameters for retrieving all properties")

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
        "name": "retrieve_by_bedroom",
        "description": "Retrieve properties based on the number of bedrooms",
        "parameters": custom_json_schema(PropertyBedroomSchema),
        "runCmd": retrieve_by_bedroom,
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
    }
]







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
