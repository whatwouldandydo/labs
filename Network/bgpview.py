"""
Date: 2021-06-10
Summary: Use BGPView API to perform nslookup for BGP ASN, Prefixes, Peers,
Upstreams, Downstream and IP.
"""

import requests
import json
import time
from pprint import pprint
from urllib3.exceptions import InsecureRequestWarning

""" Disable SSL warning self-sign certificate """
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class BGPView:
    def __init__(self):
        """ Endpoint APIs """
        # Replace as_number with integer.
        self.main_url = "https://api.bgpview.io/"
        self.asn_api = "https://api.bgpview.io/asn/as_number"
        self.asn_prefixes_api = "https://api.bgpview.io/asn/as_number/prefixes"
        self.asn_peers_api = "https://api.bgpview.io/asn/as_number/peers"
        self.asn_upstreams_api = "https://api.bgpview.io/asn/as_number/upstreams"
        self.asn_downstreams_api = "https://api.bgpview.io/asn/as_number/downstreams"
        self.asn_ixs_api = "https://api.bgpview.io/asn/as_number/ixs"

        # Replace ip_address/cidr with network/mask (/24).
        self.prefix_api = "https://api.bgpview.io/prefix/ip_address/cidr"

        # Replace ip_address with individual IP address.
        self.ip_api = "https://api.bgpview.io/ip/ip_address"

        # Replace ix_id with integer.
        self.ix_api = "https://api.bgpview.io/ix/ix_id"

    def get_asn(self, asn_number):
        # Check if asn_number is integer
        try:
            # asn_number = int(asn_number)
            if int(asn_number) == True:
                asn_api = self.asn_api.replace("as_number", asn_number)

        except:
            print("Invalid AS Number")


