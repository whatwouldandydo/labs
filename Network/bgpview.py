"""
Author: www.linkedin.com/in/whatwouldandydo
Date: 2021-06-10
Summary: Use BGPView API to perform nslookup for BGP ASN, Prefixes, Peers,
Upstreams, Downstream and IP.
"""

import requests
import json
import time
import traceback
from pprint import pprint
from urllib3.exceptions import InsecureRequestWarning

""" Disable SSL warning self-sign certificate """
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class BGPView:
    """ Endpoint APIs """
    # Replace as_number with integer.
    main_url = "https://api.bgpview.io/"
    asn_api = "https://api.bgpview.io/asn/as_number"
    asn_prefixes_api = "https://api.bgpview.io/asn/as_number/prefixes"
    asn_peers_api = "https://api.bgpview.io/asn/as_number/peers"
    asn_upstreams_api = "https://api.bgpview.io/asn/as_number/upstreams"
    asn_downstreams_api = "https://api.bgpview.io/asn/as_number/downstreams"
    asn_ixs_api = "https://api.bgpview.io/asn/as_number/ixs"

    # Replace ip_address/cidr with network/mask (/24).
    prefix_api = "https://api.bgpview.io/prefix/ip_address/cidr"

    # Replace ip_address with individual IP address.
    ip_api = "https://api.bgpview.io/ip/ip_address"

    # Replace ix_id with integer.
    ix_api = "https://api.bgpview.io/ix/ix_id"

    def __init__(self):
        # ASN health status
        self.status = None
        # ASN number
        self.asn = None
        # ASN origin country code
        self.country_code = None
        # ASN name
        self.description_short = None
        # ASN looking glass website 
        self.looking_glass = None
        # ASN RIR name
        self.rir_name = None
        # ASN regional (IRIN) allocation status (assigned, unassigned)
        self.allocation_status = None
        # ASN creation date
        self.date_allocated = None
        # ASN traffic direction
        self.traffic_estimation = None
        # ASN traffic ratio
        self.traffic_ratio = None
        # ASN company website
        self.website = None
        # ASN IANA allocation status (assigned, unassigned)
        self.assignment_status = None
        # ASN last updated date
        self.date_updated = None

    def get_asn(self, *as_number):
        """
        Allow as many AS number as input and find ASN
        information such as, name, country, looking glass,
        bandwidth, allocation status, and more.
        """
        for number in as_number:
            try:
                asn_api = self.asn_api.replace("as_number", str(number))
                print(asn_api)
                web_request = requests.get(f"{asn_api}", verify=False)
                # print(web_request) # <Response [200]>

                # When API request fails, retry it 3 times with 3 seconds wait
                query_count = 0
                while query_count != 3:
                    query_count += 1
                    time.sleep(3)

                    if web_request.status_code == 200:
                        meta = web_request.json()
                        data = meta["data"]
                        self.status = meta["status"]
                        self.asn = data["asn"]
                        self.country_code = data["country_code"]
                        self.description_short = data["description_short"]
                        self.looking_glass = data["looking_glass"]
                        self.rir_name = data["rir_allocation"]["rir_name"]
                        self.allocation_status = data["rir_allocation"]["allocation_status"]
                        self.date_allocated = data["rir_allocation"]["date_allocated"]
                        self.traffic_estimation = data["traffic_estimation"]
                        self.traffic_ratio = data["traffic_ratio"]
                        self.website = data["website"]
                        self.assignment_status = data["iana_assignment"]["assignment_status"]
                        self.date_updated = data["date_updated"]
                        break

                else:
                    print(f"ERROR {web_request}: Try to access {asn_api} three times but fail.\n")

            except KeyError:
                print(f"ERROR: {number} is NOT a valid AS number.\n")

            except:
                print(f"UNKNOWN ERROR: See debug output below...")
                traceback.print_exc()
                print()


"""
3. Can not get all the  instances from get_asn(1000,2000,3000,4000).
Only retreive instances from the last 4000

https://api.bgpview.io/asn/1000
https://api.bgpview.io/asn/2000
https://api.bgpview.io/asn/3000
https://api.bgpview.io/asn/4000
4000 Sprint International ok
"""

print()
t1 = BGPView()
# t1.get_asn(1,100,"dfsd",555.55,"666.abc","xyz.987")
t1.get_asn(1000,2000,3000,4000)
print(t1.asn, t1.description_short, t1.country_code)

print()
t2 = BGPView()
t2.get_asn(111)
print(t2.asn, t2.description_short, t2.country_code)
t2.get_asn(222)
print(t2.asn, t2.description_short, t2.country_code)

print()
# t3 = BGPView()
# print(t3.asn)
# print(t3.status)

print()
import datetime
d1 = datetime.datetime.now()
t4 = BGPView()
for i in range(5):
    d2 = datetime.datetime.now()
    t4.get_asn(i)
    print(t4.asn,t4.description_short,t4.country_code)
    d3 = datetime.datetime.now()
    print(d2 - d1)
    print(d3 - d2)
    print()
