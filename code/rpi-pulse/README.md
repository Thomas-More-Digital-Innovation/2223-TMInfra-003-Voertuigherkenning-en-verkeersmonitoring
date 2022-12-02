
# Pulse signal Pi

## General information

### Variables

Create a file called `secrets.py` and populate it with the content below. Change the variables where needed. \
The api key is variable. This will need to be passed along as a header (`x-api-key`) to authorize requests.

  ```py
    SSID = 'SSID'
    PASSWORD = 'PASS'
    API_KEY = "CHOOSEN_API_KEY" # only alphabetical, numerical and "-" symbol supported
  ```

### Paths

| path  | action |
| ----- | ------ |
| /     | Returns "OK" if authorized
| /pulse | Returns "PULSE SENT" if authorized and sends a signal through a given `PULSE_OUTPUT_PIN` for a given `PULSE_TIME`

# Instructions

1. Install [MicroPython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) on the Raspberri Pi Pico W
2. Using Visual Studio Code, install the [Pico-W-Go](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) extension
3. Make sure the `Pico-W-Go` extension is enabled, and navigate to the `/code/rpi-pulse` directory.
4. To get started, execute the **Pico-W-Go > Upload project** command, and read the serial port connection to get the IP address

## Notes

Please note that this program will send a pulse of **3.3V**. To generate **5V**, a transistor will need to be paired up with the 5V output of the  Raspberri Pi Pico.
