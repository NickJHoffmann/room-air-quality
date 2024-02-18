"""Client script to collect data from the BME68X sensor and post it to the server."""

# The dev image doesn't have the bme68x package installed due to install issues from PyPI
# pylint: disable=import-error

import logging
import time

import bme68xConstants as cnst
import bsecConstants as bsec
import httpx
from bme68x import BME68X

from raq.client.config import ClientSettings

POLLING_INTERVAL = round(1 / bsec.BSEC_SAMPLE_RATE_LP)
TIME_BETWEEN_SERVER_POSTS = 300

bme = BME68X(cnst.BME68X_I2C_ADDR_HIGH, bsec.BSEC_ENABLE)
bme.set_sample_rate(bsec.BSEC_SAMPLE_RATE_LP)


def get_data(sensor):
    """Get data from the sensor."""
    data = {}
    try:
        data = sensor.get_bsec_data()
    except Exception as e:  # pylint: disable=broad-except
        logging.error(e)
        return None

    if not data:
        time.sleep(0.1)
        return None

    time.sleep(POLLING_INTERVAL)
    return data


def post_data(client: httpx.Client, room_id: str, data: dict):
    """Send data to the server."""
    params = {
        "temperature": {
            "value": data["temperature"],
            "unit": "degC"
        },
        "humidity": {
            "value": data["humidity"],
            "unit": "percent"
        },
        "iaq": {
            "value": data["iaq"],
            "unit": "dimensionless"
        },
        "pressure": {
            "value": data["raw_pressure"],
            "unit": "hPa"
        },
    }
    try:
        r = client.post(f"/room_air_quality/{room_id}", json=params)
        if r.status_code == 201:
            logging.info(f"Successfully sent data: {params}")
        else:
            logging.warning(f"Failed to succesfully send data: {r}")
    except Exception as e:  # pylint: disable=broad-except
        logging.error(e)


def main():
    """Run the data collection and posting loop."""
    client = httpx.Client(base_url=ClientSettings().ingress_server_url)
    room_id = ClientSettings().room_id
    last_post = None
    while True:
        data = get_data(bme)
        if not data:
            continue
        now = time.time()
        if last_post is None or ((now - last_post) > TIME_BETWEEN_SERVER_POSTS):
            last_post = now
            post_data(client, room_id, data)


if __name__ == "__main__":
    main()
