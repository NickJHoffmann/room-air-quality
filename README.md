# Room Air Quality Logger

## Overview
This is a small project meant to collect IAQ data because I get sick pretty regularly and I'm convinced it's because there's lingering mold and mildew from when this place flooded before I moved in.
This is meant to use a BME68x sensor on a network-enabled Raspberry Pi to collect data and send it through an ingress server to store in an InfluxDB database, all hosted on an on-prem server.
Because I built this to host myself on-prem, and it's a just a toy project, I didn't bother doing any sort of authentication or authorization. If you get access to my network to mess around with
my air quality database, I have much bigger things to worry about.

## Getting Started
For the server:
- Run `make build-server`
- Run `make start-prod`
- Login to the InfluxDB server and generate a token to use for the ingress server
- Rename `server.env.example` to `server.env` and update the config inside it with your InfluxDB token and URL

For the client:
- Clone this repo to a Raspberry Pi with the BME680 sensor connected to it
- Run `poetry env use python3` and `poetry shell`
- Run `poetry install --with client`
- This depends on https://github.com/pi3g/bme68x-python-library, but building it from PyPI fails for me and I want to enable BSEC anyway, so use the manual installation
  - Clone that repo to a subdirectory of this repo and `cd` into it
  - With the poetry shell active, run the manual installation steps. Ensure that you are using BSEC
  - `cd` back to the top level of this repo
- Rename `client.env.example` to `client.env` and update the config inside it according to your setup
- Run `python3 src/raq/client/main.py`
