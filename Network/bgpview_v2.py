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
        url_list = [
                    "https://api.bgpview.io/asn/as_number",
                    "https://api.bgpview.io/asn/as_number/prefixes",
                    "https://api.bgpview.io/asn/as_number/peers",
                    "https://api.bgpview.io/asn/as_number/upstreams",
                    "https://api.bgpview.io/asn/as_number/downstreams",
                    "https://api.bgpview.io/asn/as_number/ixs",
                    "https://api.bgpview.io/prefix/ip_address/cidr",
                    "https://api.bgpview.io/ip/ip_address",
                    "https://api.bgpview.io/ix/ix_id",
                    "https://api.bgpview.io/search?query_term=digitalocean",
                    ]

        for url in url_list:
            if "as_number" in url:
                api_url = self.api_endpoint.replace("as_number", str(asn_ip_var))

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
            try:
                web_request = requests.get(f"{bgpview_url}", verify=False)

                if web_request.status_code == 200:
                    meta = web_request.json()

            except Exception as e:
                traceback.print_exc()
                print(e.message, e.args)
                query_try += 1
                time.sleep(3)


if __name__ == "__main__":
    t1 = RequestBGPendpoint()
    # t1.run_bgpview_api()