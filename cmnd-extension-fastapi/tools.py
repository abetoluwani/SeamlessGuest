import os
from pydantic import BaseModel, Field
import httpx

class ProductFinderSchema(BaseModel):
    product: str = Field(..., title="Product", description="Product name required")

class WeatherCitySchema(BaseModel):
    city: str = Field(..., title="City", description="City name required")

class FilePathSchema(BaseModel):
    filePath: str = Field(..., title="Filepath", description="File path required")

async def product_finder(product: str):
    url = f"https://dummyjson.com/products/search?q={product}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def weather_from_location(city: str):
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        raise ValueError("API key for weather data is not set in environment variables.")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


async def file_reader(filePath: str):
    try:
        with open(filePath, 'r') as file:
            return file.read()
    except Exception as e:
        return str(e)

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

tools = [
    {
        "name": "product_finder",
        "description": "Finds and returns dummy products details based on the product name passed to it",
        "parameters": custom_json_schema(ProductFinderSchema),
        "runCmd": product_finder,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "weather_from_location",
        "description": "Gets the weather details from a given city name",
        "parameters": custom_json_schema(WeatherCitySchema),
        "runCmd": weather_from_location,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "file_reader",
        "description": "Returns the contents of a file given its filepath",
        "parameters": custom_json_schema(FilePathSchema),
        "runCmd": file_reader,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
