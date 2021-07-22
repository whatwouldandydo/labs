"""
Date: 2021-07-21
Summary: Look up phone numbers for their country origin, carrier,
and type (land line, mobile, ect ...)
"""

# Import libaries
import requests
import json
import traceback
import os
from urllib3.exceptions import InsecureRequestWarning
from pprint import pprint

# Disable self-signed certificate warning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

numverify_api_key = os.getenv("NUMVERIFY_API_KEY")
base_url = "http://apilayer.net/api/validate"
phone_number = ""

# print(numverify_api_key)

def phone_number_lookup(number):
    # number = input("Phone Number: ")
    api_url = f"{base_url}?access_key={numverify_api_key}&number={number}"
    print(api_url)

    web_request = requests.get(api_url, verify=False)
    data = web_request.json()
    print(data)


if __name__ == "__main__":
    t1 = phone_number_lookup("12062011501")
    