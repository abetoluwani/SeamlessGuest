from pydantic import BaseModel, Field, validator
from services.properties.properties import PropertyService

class PropertyCreateRequest(BaseModel):
    RoomNumber: str
    BuildingName: str
    RoomLatitude: float
    RoomLongitude: float
    RoomSize: int
    Beds: int
    Individuals: int
    ViewDescription: str
    price: float

    @validator("RoomNumber")
    def room_number_must_be_positive(cls, v):
        """
        The room number must be a positive integer.
        """
        if int(v) <= 0:
            raise ValueError("RoomNumber must be a positive integer")
    
        duplicate = PropertyService.get_by_id(v)
        if duplicate:
            raise ValueError("RoomNumber must be unique!")

        return v

    # Add more validators for other fields as needed...

