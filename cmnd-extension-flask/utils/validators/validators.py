from pydantic import BaseModel, Field, validator

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
        if int(v) <= 0:
            raise ValueError("RoomNumber must be a positive integer")
        return v

    # Add more validators for other fields as needed...
