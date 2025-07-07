# SPDX-FileCopyrightText: 2025 Peter Tacon <contacto@petertacon.com>
# SPDX-License-Identifier: MIT

"""Test of Consuming API in RP2040 / RP2350"""


# Importing Required Libraries
import os
import adafruit_connection_manager
import wifi
import adafruit_requests
import microcontroller


# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")


# Set API URL as variables
TEXT_URL = "http://FASTAPI_URL:8000/v1/temptest/5"
JSON_GET_URL = "http://FASTAPI_URL:8000/v1/temptest"
JSON_POST_URL = "http://FASTAPI_URL:8000/v1/temptest"


# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)


# Connecting to WiFi
print(f"\nConnecting to {ssid}...")
try:
    wifi.radio.connect(ssid, password)
except OSError as e:
    print(f"â OSError: {e}")
print("â Wifi!")


# Function to obtain CPU Temperature and calculate the status
def get_cputemp():
    cputemp = microcontroller.cpu.temperature
    if cputemp <= 36.0:
        tempstat = "Cold"
    elif cputemp >= 40.0:
        tempstat = "Hot"
    else:
        tempstat = "Warm"
    return cputemp, tempstat


# GET request for an specific id
print(f" | GET Text Test: {TEXT_URL}")
with requests.get(TEXT_URL) as response:
    print(f" | â GET Response: {response.text}")
print("-" * 80)


# GET request for all registered ID's
print(f" | GET Full Response Test: {JSON_GET_URL}")
with requests.get(JSON_GET_URL) as response:
    print(f" | â Unparsed Full JSON Response: {response.json()}")
print("-" * 80)


# POST request for New CPU Temp registers
cputmp, tmpstat = get_cputemp()
json_data = {"tempreg": str(cputmp), "status": str(tmpstat)}
print(f" | ? JSON 'key':'value' POST Test: {JSON_POST_URL} {json_data}")
with requests.post(JSON_POST_URL, json=json_data) as response:
    json_resp = response.json()
    # Parse out the 'json' key from json_resp dict.
    print(f" | ? JSON 'key':'value' Response: {response.json()}")
print("-" * 80)


print("Finished!")
