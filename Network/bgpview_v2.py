"""
Author: www.linkedin.com/in/whatwouldandydo
Date: 2021-06-17
Summary: Edit codes from bgpview.py to make it shorter, don't repeat same code.
Use BGPView API to perform nslookup for BGP ASN, Prefixes, Peers,
Upstreams, Downstream and IP.
"""

import requests
import json
import time
import traceback
from pprint import pprint
from urllib3.exceptions import InsecureRequestWarning

""" Disable SSL self-sign certificate warning """
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class RequestBGPendpoint:
    """ Replace as_number with variable.
    Main URL = "https://api.bgpview.io/"
    ASN = "https://api.bgpview.io/asn/as_number"
    ASN Prefixes = "https://api.bgpview.io/asn/as_number/prefixes"
    ASN Peers = "https://api.bgpview.io/asn/as_number/peers"
    ASN Upstreams = "https://api.bgpview.io/asn/as_number/upstreams"
    ASN Downstreams = "https://api.bgpview.io/asn/as_number/downstreams"
    ASN IXs = "https://api.bgpview.io/asn/as_number/ixs"

    # Replace ip_address/cidr with network/mask (/24).
    Prefix = "https://api.bgpview.io/prefix/ip_address/cidr"

    # Replace ip_address with individual IP address.
    IP = "https://api.bgpview.io/ip/ip_address"

    # Replace ix_id with integer.
    IX = "https://api.bgpview.io/ix/ix_id"

    # Replace digitalocean with words
    Search = https://api.bgpview.io/search?query_term=digitalocean
    """

    def __init__(self, api_endpoint, asn_ip_var):
        """ Get variables for API endpoint and ASN/IP/IX/Prefix """
        self.api_endpoint = api_endpoint
        self.asn_ip_var = asn_ip_var

    def run_bgpview_api(self):
        """ A Global method to run API request
        Replace as_number, ip_address/cidr, ip_address, ix_id,
        and digitalocean with valid user entered variable
        """
        # asn_url = "https://api.bgpview.io/asn/as_number",
        # asn_prefixes_url = "https://api.bgpview.io/asn/as_number/prefixes",
        # asn_peers_url = "https://api.bgpview.io/asn/as_number/peers",
        # asn_upstreams_url = "https://api.bgpview.io/asn/as_number/upstreams",
        # asn_downstreams_url = "https://api.bgpview.io/asn/as_number/downstreams",
        # asn_ixs_url = "https://api.bgpview.io/asn/as_number/ixs",
        # prefix_url = "https://api.bgpview.io/prefix/ip_address/cidr",
        # ip_address_url = "https://api.bgpview.io/ip/ip_address",
        # internet_exchanges_url = "https://api.bgpview.io/ix/ix_id",
        # search_url = "https://api.bgpview.io/search?query_term=digitalocean",

        self.meta_data = None

        if "as_number" in self.api_endpoint:
            bgpview_url = self.api_endpoint.replace("as_number", str(self.asn_ip_var))
        elif "ip_address/cidr" in self.api_endpoint:
            bgpview_url = self.api_endpoint.replace("ip_address/cidr", str(self.asn_ip_var))
        elif "ip_address" in self.api_endpoint:
            bgpview_url = self.api_endpoint.replace("ip_address", str(self.asn_ip_var))
        elif "ix_id" in self.api_endpoint:
            bgpview_url = self.api_endpoint.replace("ix_id", str(self.asn_ip_var))
        elif "digitalocean" in self.api_endpoint:
            bgpview_url = self.api_endpoint.replace("digitalocean", str(self.asn_ip_var))

        """ When API request fails, retry it 3 times with 3 seconds wait """
        query_try = 0
        while query_try != 3:
            print(query_try)
            try:
                web_request = requests.get(f"{bgpview_url}", verify=False)
                print(bgpview_url)
                print(web_request)

                if web_request.status_code == 500:
                    meta_data = web_request.json()
                    self.meta_data = meta_data
                    break

            except Exception as e:
                print(f"===> ERROR: {e.args}\n")
                # print(e.message)
                traceback.print_exc()

            query_try += 1
            print("Sleep 3 seconds")
            time.sleep(3)
        else:
            print(f"===> ERROR: Try to query {bgpview_url} 3 times but failed.\n")

        return self.meta_data



if __name__ == "__main__":
    a = "https://api.bgpview.io/asn/as_number"
    b = 126
    t1 = RequestBGPendpoint(a, b)
    # t1.run_bgpview_api()
    print(t1.run_bgpview_api())
