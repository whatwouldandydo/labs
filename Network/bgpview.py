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
        self.asn_status = None
        # ASN number
        self.asn_number = None
        # ASN origin country code
        self.asn_country_code = None
        # ASN name
        self.asn_name = None
        # ASN looking glass website 
        self.asn_looking_glass_website = None
        # ASN RIR name
        self.asn_rir_name = None
        # ASN regional (IRIN) allocation status (assigned, unassigned)
        self.asn_allocation_status = None
        # ASN creation date
        self.asn_date_allocated = None
        # ASN traffic direction
        self.asn_traffic_estimation = None
        # ASN traffic ratio
        self.asn_traffic_ratio = None
        # ASN company website
        self.asn_company_website = None
        # ASN IANA allocation status (assigned, unassigned)
        self.asn_assignment_status = None
        # ASN last updated date
        self.asn_date_updated = None

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
                        self.asn_status = meta["status"]
                        self.asn_number = data["asn"]
                        self.asn_country_code = data["country_code"]
                        self.asn_name = data["description_short"]
                        self.asn_looking_glass_website = data["looking_glass"]
                        self.asn_rir_name = data["rir_allocation"]["rir_name"]
                        self.asn_allocation_status = data["rir_allocation"]["allocation_status"]
                        self.asn_date_allocated = data["rir_allocation"]["date_allocated"]
                        self.asn_traffic_estimation = data["traffic_estimation"]
                        self.asn_traffic_ratio = data["traffic_ratio"]
                        self.asn_company_website = data["website"]
                        self.asn_assignment_status = data["iana_assignment"]["assignment_status"]
                        self.asn_date_updated = data["date_updated"]
                        break

                else:
                    print(f"ERROR {web_request}: Try to access {asn_api} three times but fail.\n")

            except KeyError:
                print(f"ERROR: {number} is NOT a valid AS number.\n")

            except:
                print(f"UNKNOWN ERROR: See debug output below...")
                traceback.print_exc()
                print()

    def get_asn_prefixes(self, as_number):
        """ Get prefixes IPv4 and IPv6 from the AS number """
        # try:
        asn_prefixes_api = self.asn_prefixes_api.replace("as_number", str(as_number))
        print(asn_prefixes_api)
        web_request = requests.get(f"{asn_prefixes_api}", verify=False)
        print(web_request)

        query_count = 0
        while query_count != 3:
            query_count += 1
            time.sleep(3)

            if web_request.status_code == 200:
                meta = web_request.json()
                # pprint(meta)
                status_code = meta["status"]

                if status_code == "error":
                    print(f"ERORR: {as_number} is not a valid.")
                    break
                elif status_code == "ok":
                    data = meta["data"]
                    ipv4_prefixes = data["ipv4_prefixes"]
                    ipv6_prefixes = data["ipv6_prefixes"]
                    
                    ipv4_parent_prefixes = []

                    for _ in ipv4_prefixes:
                        # print(type(prefix)) # dict
                        # print(prefix)
                        for k, v in _.items():
                            if type(v) == dict:
                                if v["prefix"] != None:

                                # parent = v["prefix"]
                                    parent = v["prefix"]
                                    print(type(parent))
                                    # print(parent)
                                    ipv4_parent_prefixes.append(parent)
                                    # input()

                                
                                # for k2, v2 in parent.items():
                                #     # print(v2)
                                #     ipv4_parent_prefixes = []
                                #     if k2 == "prefix" and v2 != None:
                                #         super_net = list(v2)
                                #         ipv4_parent_prefixes.append(super_net)
                                #         # print(type(super_net), super_net)
                                #         # print()
                                #         # input()
                                # # super_net.append(self.ipv4_parent_prefixes)
                                # # print(super_net)
                                #         # ipv4_parent_prefixes.append(super_net)
                                #     # print(ipv4_parent_prefixes)
                            elif k == "prefix":
                                ipv4_subnet = v
                                # print(ipv4_subnet)
                            elif k == "name":
                                ipv4_subnet_name = v
                                # print(ipv4_subnet_name)
                            elif k == "description":
                                ipv4_subet_description = v
                                # print(ipv4_subet_description)
                            elif k == "country_code":
                                ipv4_subnet_country = v
                                # print(ipv4_subnet_country)

                    print(ipv4_parent_prefixes)

                    # Remove parent prefixes from list
                    self.ipv4_parent_prefixes = list(dict.fromkeys(ipv4_parent_prefixes))
                    print(self.ipv4_parent_prefixes)



                    break

        # except KeyError:
            # print(f"ERROR {web_request}: Try to access {asn_api} three times but fail.\n"
            


"""
3. Can not get all the  instances from get_asn(3000,4000).
Only retreive instances from the last 4000

https://api.bgpview.io/asn/3000
https://api.bgpview.io/asn/4000
4000 Sprint International ok
"""


if __name__ == "__main__":
    print()
    t1 = BGPView()
    # t1.get_asn(1,100,"dfsd",555.55,"666.abc","xyz.987")
    # t1.get_asn(3000, 4000)
    # print(t1.asn_number, t1.asn_name, t1.asn_country_code)
    t1.get_asn_prefixes("andy")
    t1.get_asn_prefixes(1)
    # t1.get_asn_prefixes("11")
    # t1.get_asn_prefixes("a")

    # print()
    # t2 = BGPView()
    # t2.get_asn("ad")
    # print(t2.asn_number, t2.asn_name, t2.asn_country_code)
    # t2.get_asn(222)
    # print(t2.asn_number, t2.asn_name, t2.asn_country_code)

    # print()
    # t3 = BGPView()
    # print(t3.asn)
    # print(t3.status)

    # print()
    # import datetime
    # d1 = datetime.datetime.now()
    # t4 = BGPView()
    # for i in range(5):
    #     d2 = datetime.datetime.now()
    #     t4.get_asn(i)
    #     print(t4.asn_number,t4.asn_name,t4.asn_country_code)
    #     d3 = datetime.datetime.now()
    #     print(d2 - d1)
    #     print(d3 - d2)
    #     print()
