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
                web_request = requests.get(f"{asn_api}", verify=False)
                
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
        asn_prefixes_api = self.asn_prefixes_api.replace("as_number", str(as_number))
        web_request = requests.get(f"{asn_prefixes_api}", verify=False)

        # Get IPv4 data from ipv4_prefixes array
        ipv4_parent_prefixes = []
        ipv4_subnets = []
        ipv4_subnet_names = []
        ipv4_subnet_descriptions = []
        ipv4_subnet_countries = []

        # Get IPv6 data from ipv6_prefixes array
        ipv6_parent_prefixes = []
        ipv6_subnets = []
        ipv6_subnet_names = []
        ipv6_subnet_descriptions = []
        ipv6_subnet_countries = []

        # When API request fails, retry it 3 times with 3 seconds wait
        query_count = 0
        while query_count != 3:
            query_count += 1
            time.sleep(3)

            if web_request.status_code == 200:
                meta = web_request.json()
                status_code = meta["status"]

                if status_code == "error":
                    print(f"ERORR: {as_number} is not a valid number.")
                    break
                elif status_code == "ok":
                    data = meta["data"]
                    ipv4_prefixes = data["ipv4_prefixes"]
                    ipv6_prefixes = data["ipv6_prefixes"]

                    # Loop through IPv4 array
                    for _ in ipv4_prefixes:
                        for k, v in _.items():
                            if type(v) == dict:
                                if v["prefix"] != None:
                                    parent = v["prefix"]
                                    ipv4_parent_prefixes.append(parent)
                            elif k == "prefix":
                                ipv4_subnets.append(v)
                            elif k == "name":
                                ipv4_subnet_names.append(v)
                            elif k == "description":
                                ipv4_subnet_descriptions.append(v)
                            elif k == "country_code":
                                ipv4_subnet_countries.append(v)

                    # Loop through IPv6 array
                    for _ in ipv6_prefixes:
                        for k, v in _.items():
                            if type(v) == dict:
                                if v["prefix"] != None:
                                    parent = v["prefix"]
                                    ipv6_parent_prefixes.append(parent)
                            elif k == "prefix":
                                ipv6_subnets.append(v)
                            elif k == "name":
                                ipv6_subnet_names.append(v)
                            elif k == "description":
                                ipv6_subnet_descriptions.append(v)
                            elif k == "country_code":
                                ipv6_subnet_countries.append(v)
                break

        else:
            print(f"ERROR {web_request}: Try to access {asn_prefixes_api} three times but fail.\n")

        # Combining IPv4 prefix, description, and country in 1 line
        ipv4_prefixes_info = []
        for i in range(len(ipv4_subnets)):
            ip = str(ipv4_subnets[i])
            name = str(ipv4_subnet_descriptions[i])
            country = str(ipv4_subnet_countries[i])
            ip_data = f"{ip} = {name} ({country})"
            ipv4_prefixes_info.append(ip_data)

        # Combining IPv6 prefix, description, and country in 1 line
        ipv6_prefixes_info = []
        for i in range(len(ipv6_subnets)):
            ip = str(ipv6_subnets[i])
            name = str(ipv6_subnet_descriptions[i])
            country = str(ipv6_subnet_countries[i])
            ip_data = f"{ip} = {name} ({country})"
            ipv6_prefixes_info.append(ip_data)

        # Remove duplicate IPv4 parent prefixes or supernet from list
        self.ipv4_parent_prefixes = list(dict.fromkeys(ipv4_parent_prefixes))

        # IPv4 Prefixes instance info such as owner and country
        self.ipv4_prefixes_info = ipv4_prefixes_info

        # Remove duplicate IPv6 parent prefixes or supernet from list
        self.ipv6_parent_prefixes = list(dict.fromkeys(ipv6_parent_prefixes))

        # IPv6 Prefixes instance info such as owner and country
        self.ipv6_prefixes_info = ipv6_prefixes_info

    def get_asn_peers(self, as_number):
        """ Get ASN IPv4 and IPv6 peering partners"""
        asn_peers_api = self.asn_peers_api.replace("as_number", str(as_number))
        web_request = requests.get(f"{asn_peers_api}", verify=False)

        ipv4_remote_asn_numbers = []
        ipv4_remote_asn_names = []
        ipv4_remote_asn_descriptions = []
        ipv4_remote_asn_countries = []

        ipv6_remote_asn_numbers = []
        ipv6_remote_asn_names = []
        ipv6_remote_asn_descriptions = []
        ipv6_remote_asn_countries = []

        # When API request fails, retry it 3 times with 3 seconds wait
        query_try = 0
        while query_try != 3:
            query_try += 1
            time.sleep(3)

            if web_request.status_code == 200:
                meta = web_request.json()
                status_code = meta["status"]
                print(status_code)

                if status_code == "error":
                    print(f"ERROR: {as_number} is not a valid number.")
                elif status_code == "ok":
                    data = meta["data"]
                    ipv4_peers = data["ipv4_peers"]
                    ipv6_peers = data["ipv6_peers"]

                    # Loop through IPv4 peers array
                    for _ in ipv4_peers:
                        for k, v in _.items():
                            if k == "asn":
                                ipv4_remote_asn_numbers.append(v)
                            elif k == "name":
                                ipv4_remote_asn_names.append(v)
                            elif k == "description":
                                ipv4_remote_asn_descriptions.append(v)
                            elif k == "country_code":
                                ipv4_remote_asn_countries.append(v)

                    # Loop through IPv6 peers array
                    for _ in ipv6_peers:
                        for k, v in _.items():
                            if k == "asn":
                                ipv6_remote_asn_numbers.append(v)
                            elif k == "name":
                                ipv6_remote_asn_names.append(v)
                            elif k == "description":
                                ipv6_remote_asn_descriptions.append(v)
                            elif k == "country_code":
                                ipv6_remote_asn_countries.append(v)
                break
        else:
            print(f"ERROR {web_request}: Try to access {asn_peers_api} three times but fail.\n")

        # Combing IPv4 peer ASN, description, and country
        ipv4_remote_peers_info = []
        for i in range(len(ipv4_remote_asn_numbers)):
            asn = str(ipv4_remote_asn_numbers[i])
            description = str(ipv4_remote_asn_descriptions[i])
            country = str(ipv4_remote_asn_countries[i])
            asn_data = f"{asn} ==> {description} ({country})"
            ipv4_remote_peers_info.append(asn_data)

        # Combing IPv6 peer ASN, description, and country
        ipv6_remote_peers_info = []
        for i in range(len(ipv6_remote_asn_numbers)):
            asn = str(ipv6_remote_asn_numbers[i])
            description = str(ipv6_remote_asn_descriptions[i])
            country = str(ipv6_remote_asn_countries[i])
            asn_data = f"{asn} ==> {description} ({country})"
            ipv6_remote_peers_info.append(asn_data)

        # IPv4 remote peer information instance
        self.ipv4_remote_peers_info = ipv4_remote_peers_info

        # IPv6 remote peer information instance
        self.ipv6_remote_peers_info = ipv6_remote_peers_info



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
    t1.get_asn_prefixes(61138)
    # print(t1.ipv4_prefixes_info)
    # pprint(t1.ipv4_parent_prefixes)
    # print()
    # print(t1.ipv6_parent_prefixes)
    # pprint(t1.ipv6_prefixes_info)
    print(t1.ipv6_prefixes_info)

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
