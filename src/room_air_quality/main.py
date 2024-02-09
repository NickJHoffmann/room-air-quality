from fastapi import FastAPI, Depends, Response
from pint import UnitRegistry
from room_air_quality.models import RoomAirQuality, FloatValue
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from room_air_quality.config import ServerSettings
from typing import Annotated
from http import HTTPStatus

async def db_client():
    s = ServerSettings()
    return InfluxDBClient(url=s.influxdb_url, token=s.influxdb_token.get_secret_value(), org=s.influxdb_org)

DBClient = Annotated[InfluxDBClient, Depends(db_client)]

app = FastAPI()
ureg = UnitRegistry()

@app.get("/")
async def root():
    return {"message": "Hello World"}


DESIRED_UNITS = {
    "temperature": "degF",
    "humidity": "percent",
    "iaq": "ppm",
    "pressure": "hPa",
}

def convert_to_desired_units(point: Point, raw_measurement: FloatValue, type: str) -> Point:
    meas = ureg.Quantity(raw_measurement, raw_measurement.unit)
    desired_unit = DESIRED_UNITS[type]
    converted_magnitude = meas.to(desired_unit).magnitude
    return point.field(type, converted_magnitude)


@app.post("/room_air_quality/{room_id}")
async def room_air_quality(room_id: str, room_air_quality: RoomAirQuality, db_client: DBClient):
    s = ServerSettings()
    point = Point(s.influxdb_measurement).tag("room", room_id)

    if room_air_quality.temperature:
        point = convert_to_desired_units(point, room_air_quality.temperature, "temperature")

    if room_air_quality.humidity:
        point = convert_to_desired_units(point, room_air_quality.humidity, "humidity")

    if room_air_quality.iaq:
        point = convert_to_desired_units(point, room_air_quality.iaq, "iaq")

    if room_air_quality.pressure:
        point = convert_to_desired_units(point, room_air_quality.pressure, "pressure")

    write_api = db_client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=s.influxdb_bucket, org=s.influxdb_org, record=point)

    return Response(status_code=HTTPStatus.CREATED)
