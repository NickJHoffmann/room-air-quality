"""Data models for the server."""

from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    """Location of a room."""
    name: str
    display_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FloatValue(BaseModel):
    """Float value with a unit."""
    value: float
    unit: str


class RoomAirQuality(BaseModel):
    """API Post Request Body"""
    temperature: Optional[FloatValue] = None
    humidity: Optional[FloatValue] = None
    iaq: Optional[FloatValue] = None
    pressure: Optional[FloatValue] = None
