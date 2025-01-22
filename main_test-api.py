# This is a sample Python script.

import requests
import os
from dotenv import load_dotenv

load_dotenv()

HOME_ASSISTANT_URL = os.getenv('HOME_ASSISTANT_URL')
API_TOKEN = os.getenv('API_TOKEN')

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

URL_STATES_LED_EG = f"{HOME_ASSISTANT_URL}/api/states/light.wled_eg"
URL_ACTIVATE_LED_EG = f"{HOME_ASSISTANT_URL}/api/events/api_call_eg_light_on"
URL_DEACTIVATE_LED_EG = f"{HOME_ASSISTANT_URL}/api/events/api_call_eg_light_off"

def testAPI():
    response = requests.get(URL_STATES_LED_EG, headers=HEADERS)
    print(response)
    print(response.status_code)
    print(response.text)

def activateLED():
    response = requests.post(URL_ACTIVATE_LED_EG, headers=HEADERS)
    print(response)
    print(response.status_code)
    print(response.text)

def deactivateLED():
    response = requests.post(URL_DEACTIVATE_LED_EG, headers=HEADERS)
    print(response)
    print(response.status_code)
    print(response.text)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    testAPI()
    activateLED()
    # deactivateLED()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
