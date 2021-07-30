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

# API token stored in secret environment
numverify_api_key = os.getenv("NUMVERIFY_API_KEY")
base_url = "http://apilayer.net/api/validate"


def phone_number_lookup():
    # Run a GET request to API endpoint with token and phone number.
    print("#" * 80)
    number = input("Phone Number (Example 14158586273): ")
    api_url = f"{base_url}?access_key={numverify_api_key}&number={number}"
    web_request = requests.get(api_url, verify=False)
    data = web_request.json()

    try:
        # Print information of a valid phone number.
        if data["valid"] is True:
            international_code = data["country_prefix"]
            local_format = data["local_format"]
            country_code = data["country_name"]
            location = data["location"]
            carrier = data["carrier"]
            line_type = data["line_type"]

            print()
            print(f"Internation Code: {international_code}")
            print(f"Local Format: {local_format}")
            print(f"Country: {country_code}")
            print(f"Location: {location}")
            print(f"Carrier Name: {carrier}")
            print(f"Line Type: {line_type}")
            print("#" * 80)
            print()

        # Capture phone number with missing country_prefix
        elif data["valid"] is False:
            print(f"HINT: The {number} is missing an Internation Code.")

    except KeyError:
        # Capture error of a wrong number or non-integer value.
        if data["success"] is False:
            print(f"ERROR: {number} is not a valid number.")

    except Exception as e:
        # Capture other errors and print out traceback code.
        print(f"ERROR: {e.args}")
        traceback.print_exc()


if __name__ == "__main__":
    t1 = phone_number_lookup()
