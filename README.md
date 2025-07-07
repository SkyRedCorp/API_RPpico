# API_RPpico
Demonstration: Creating an API Server and Consuming the Service with a Raspberry Pi Pico W

For this project, we created an API server using FastAPI, following guidance from an online tutorial. Once the service was set up, we programmed a Raspberry Pi Pico W (RP2040 or RP2350) using CircuitPython. The microcontroller connects to the API service, reads the internal CPU temperature sensor, determines whether the temperature is considered “hot” or “cold,” and then sends a POST request to register the data in the database.

Below are the tutorial links referenced during the development of this project:

- FastAPI Simple CRUD With MySQL & SQLAlchemy: https://gerrysabar.medium.com/fastapi-simple-crud-with-mysql-sqlalchemy-e60dd04a5c7e
- CircuitPython Temperature register: https://learn.adafruit.com/circuitpython-essentials/circuitpython-cpu-temp
- CircuitPython HTTP/HTTPS Requests: https://learn.adafruit.com/networking-in-circuitpython/making-http-andhttps-requests
- Python return values from Function: https://www.geeksforgeeks.org/python/python-return-statement/#returning-multiple-values
