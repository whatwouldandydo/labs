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

    def get_asn(self, as_number):
        """
        Get AS information such as country, name, looking glass,
        bandwidth, allocation status.
        """
        try:
            # Check if as_number is integer
            # as_number = int(input("AS Number: "))
            as_number = 59687
            asn_api = self.asn_api.replace("as_number", str(as_number))
            # print(asn_api)
            # return asn_api
            web_request = requests.get(f"{asn_api}", verify=False)
            print(web_request) # <Response [200]>
            meta = web_request.json()
            # pprint(meta)
            data = meta["data"]
            """
            data dict_keys(['asn', 'name', 'description_short', 'description_full',
            'country_code', 'website', 'email_contacts', 'abuse_contacts',
            'looking_glass', 'traffic_estimation', 'traffic_ratio',
            'owner_address', 'rir_allocation', 'iana_assignment', 'date_updated'])
            """
            # pprint(data)
            status = meta["status"]
            print(status)
            asn = data["asn"]
            print(asn)
            country_code = data["country_code"]
            # country = data["owner_address"]
            print(country_code)
            # print(country)
            description_short = data["description_short"]
            print(description_short)
            looking_glass = data["looking_glass"]
            print(looking_glass)
            rir_name = data["rir_allocation"]["rir_name"]
            print(rir_name)
            allocation_status = data["rir_allocation"]["allocation_status"]
            print(allocation_status)
            date_allocated = data["rir_allocation"]["date_allocated"]
            print(date_allocated)
            traffic_estimation = data["traffic_estimation"]
            print(traffic_estimation)
            traffic_ratio = data["traffic_ratio"]
            print(traffic_ratio)
            website = data["website"]
            print(website)
            assignment_status = data["iana_assignment"]["assignment_status"]
            print(assignment_status)
            date_updated = data["date_updated"]
            print(date_updated)


        except:
            print("Invalid AS Number")



t1 = BGPView()
t1.get_asn(1234)

t2 = BGPView()
# t2.get_asn("dsd")