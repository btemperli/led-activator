# Python Script to activate a LED-Light based on two different motion sensors.

import requests
import threading
import time
import os

from datetime import datetime
from gpiozero import MotionSensor
from dotenv import load_dotenv

load_dotenv()

HOME_ASSISTANT_URL = os.getenv('HOME_ASSISTANT_URL')
API_TOKEN = os.getenv('API_TOKEN')
LED_POSITION = os.getenv('LED_POSITION')
PIR_LEFT_PIN = os.getenv('PIR_LEFT_PIN')
PIR_RIGHT_PIN = os.getenv('PIR_RIGHT_PIN')


HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

URL_STATES_LED = f"{HOME_ASSISTANT_URL}/api/states/light.wled_{LED_POSITION}"
URL_ACTIVATE_LED = f"{HOME_ASSISTANT_URL}/api/events/api_call_{LED_POSITION}_light_on"
URL_DEACTIVATE_LED = f"{HOME_ASSISTANT_URL}/api/events/api_call_{LED_POSITION}_light_off"

# variables
led_is_active = False
movement_timer = None

# activate Sensor
pir_left = MotionSensor(PIR_LEFT_PIN)
pir_right = MotionSensor(PIR_RIGHT_PIN)


def prnt(nachricht, log_to_file=False):
    print(nachricht)
    if log_to_file:
        log_datei = "log.txt"
        zeitstempel = datetime.now().strftime("%Y-%m-%d %H:%M")
        neue_zeile = f"{zeitstempel} | {nachricht}\n"

        if os.path.exists(log_datei):
            with open(log_datei, "r", encoding="utf-8") as f:
                zeilen = f.readlines()
        else:
            zeilen = []

        zeilen.insert(0, neue_zeile)

        if len(zeilen) > 200:
            zeilen.pop()

        with open(log_datei, "w", encoding="utf-8") as f:
            f.writelines(zeilen)


def reset_timer():
    global movement_timer
    if movement_timer is not None:
        movement_timer.cancel()  # Den vorherigen Timer abbrechen

    # Einen neuen Timer starten, der nach 3 Minuten deactivateLED aufruft
    movement_timer = threading.Timer(60, stop_movement)
    movement_timer.start()


def movement_left():
    movement_callback("left")


def movement_right():
    movement_callback("right")


def movement_callback(name):
    global led_is_active
    prnt(f"movement on {name}")

    if not led_is_active:
        led_is_active = True
        prnt(f"movement on {name}. activate LED.", True)
        activate_led()
        reset_timer()


def stop_movement():
    global led_is_active
    global movement_timer
    movement_timer = None
    led_is_active = False
    deactivate_led()


def api_call_get(url):
    prnt(f"Calling {url} with GET")
    response = requests.get(url, headers=HEADERS)
    prnt(response.status_code)

    if response.status_code != 200:
        prnt('-------------------')
        prnt('Error GET Response:', True)
        prnt(response.text, True)
        prnt(response)

    return response


def api_call_post(url):
    prnt(f"Calling {url} with POST")
    response = requests.post(url, headers=HEADERS)
    prnt(response.status_code)
    if response.status_code != 200:
        prnt('-------------------')
        prnt('Error POST Response:', True)
        prnt(response.text, True)
        prnt(response)
    return response


def test_api():
    response = api_call_get(URL_STATES_LED)
    prnt(response.text)


def activate_led():
    # prnt("ACTIVATING LED")
    api_call_post(URL_ACTIVATE_LED)


def deactivate_led():
    prnt(f"no movement. deactivate LED.", True)

    api_call_post(URL_DEACTIVATE_LED)


if __name__ == '__main__':
    prnt("start program.", True)
    test_api()

    try:
        pir_left.when_motion = movement_left
        pir_right.when_motion = movement_right

        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        prnt("quit program: KeyboardInterrupt", True)
