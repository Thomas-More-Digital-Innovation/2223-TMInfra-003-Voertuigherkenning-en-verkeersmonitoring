import network
import socket
import time
import re

from machine import Pin

import secrets

PULSE_OUTPUT_PIN = "LED"
PULSE_TIME = 1 # seconds

pulse_output = Pin(PULSE_OUTPUT_PIN, Pin.OUT)

if not (secrets.SSID and secrets.PASSWORD and secrets.API_KEY):
    raise ValueError("Secrets not set! Create a file called secrets.py with SSID, PASSWORD, and API_KEY variables.")



ssid = secrets.SSID

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)

print("Connecting to %s" % secrets.SSID)
connect_timeout = 60
while connect_timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    connect_timeout -= 1
    print('.', end='')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)

        request = str(request)
        route_pulse = request.find('/pulse') is not -1


        # This is not optimal AT ALL
        # Regex should work (?<=x-api-key: )[0-9a-zA-Z-]*
        api_key = request[request.find("x-api-key: ")+len("x-api-key: "):request.find("\\r",request.find("x-api-key: "))]

        response = "OK"

        authorized = (api_key == secrets.API_KEY)

        if not authorized:
          print("Unauthorized")
          response = "Unauthorized"
          cl.send('HTTP/1.0 401 Unauthorized\r\nContent-type: text/html\r\n\r\n')
          cl.close()
          continue

        if route_pulse and authorized:
            print("PULSE SENT")
            pulse_output.value(True)
            time.sleep(PULSE_TIME)
            pulse_output.value(False)
            response = "PULSE SENT"

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')