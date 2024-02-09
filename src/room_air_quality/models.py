from pydantic import BaseModel
from typing import Optional

class Location(BaseModel):
    name: str
    display_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FloatValue(BaseModel):
    value: float
    unit: str


class RoomAirQuality(BaseModel):
    temperature: Optional[FloatValue] = None
    humidity: Optional[FloatValue] = None
    iaq: Optional[FloatValue] = None
    pressure: Optional[FloatValue] = None
