"""Ingress server for air quality data.
Serves to convert units and store data in InfluxDB.
"""

import logging
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, Response
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from pint import UnitRegistry

from raq.server.config import ServerSettings
from raq.server.models import FloatValue, RoomAirQuality


async def db_client_dependency():
    """"Database client dependency."""
    s = ServerSettings()
    return InfluxDBClient(url=s.influxdb_url,
                          token=s.influxdb_token.get_secret_value(),
                          org=s.influxdb_org)


DBClient = Annotated[InfluxDBClient, Depends(db_client_dependency)]

app = FastAPI()
ureg = UnitRegistry()


@app.get("/")
async def root():
    """Liveliness check."""
    return {"message": "Hello World"}


DESIRED_UNITS = {
    "temperature": "degF",
    "humidity": "percent",
    "iaq": "dimensionless",
    "pressure": "hPa",
}


def convert_to_desired_units(point: Point, raw_measurement: FloatValue,
                             data_type: str) -> Point:
    """"Add a field to a point with a converted value."""
    meas = ureg.Quantity(raw_measurement.value, raw_measurement.unit)
    desired_unit = DESIRED_UNITS[data_type]
    converted_magnitude = meas.to(desired_unit).magnitude
    return point.field(data_type, converted_magnitude)


@app.post("/room_air_quality/{room_id}")
async def post_room_air_quality(room_id: str, room_air_quality: RoomAirQuality,
                                db_client: DBClient):
    """Receive room air quality data."""
    s = ServerSettings()
    point = Point(s.influxdb_measurement).tag("room", room_id)

    if room_air_quality.temperature:
        point = convert_to_desired_units(point, room_air_quality.temperature,
                                         "temperature")

    if room_air_quality.humidity:
        point = convert_to_desired_units(point, room_air_quality.humidity, "humidity")

    if room_air_quality.iaq:
        point = convert_to_desired_units(point, room_air_quality.iaq, "iaq")

    if room_air_quality.pressure:
        point = convert_to_desired_units(point, room_air_quality.pressure, "pressure")

    write_api = db_client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=s.influxdb_bucket, org=s.influxdb_org, record=point)

    logging.info(f"Received room air quality data for room {room_id}: {room_air_quality}")

    return Response(status_code=HTTPStatus.CREATED)
