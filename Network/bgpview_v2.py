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


class RequestBGPapi:
    """ Replace as_number with number.
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

    # Replace ix_id with number.
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

        self.data_from_api = None
        # self.api_status = None
        # self.api_status_message = None

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

        self.web_url = bgpview_url

        """ When API request fails, retry it 3 times with 3 seconds wait """
        query_try = 0
        while query_try != 3:
            # print(query_try)
            try:
                web_request = requests.get(f"{bgpview_url}", verify=False)
                time.sleep(0.5)
                print(bgpview_url)
                print(web_request)

                if web_request.status_code == 200:
                    meta_data = web_request.json()
                    self.data_from_api = meta_data
                    # "ok" or "error""
                    self.api_status = meta_data["status"]
                    # "Query was successful" means good and has data
                    self.api_status_message = meta_data["status_message"]
                    break

            except Exception as e:
                print(f"===> ERROR: {e.args} <===")
                # print(e.message)
                traceback.print_exc()
                print()

            query_try += 1
            print("Sleep 3 seconds")
            print(f"Query Try: {query_try}")
            time.sleep(1)
        else:
            print(f"===> ERROR: Query request to {bgpview_url} three times but failed. <===")
            print(f"===> ERROR: {bgpview_url} status code {web_request} <===\n")

        """ Return as tupble(dict, str, str)
        dict = self.data_from_api
        str = self.api_status
        str = self.api_status_message """
        return self.data_from_api, self.api_status, self.api_status_message
        # return self.api_status, self.api_status_message


class RequestASN(RequestBGPapi):
    """ Get ASN information such as owner, country, and more..."""
    def __init__(self, api_endpoint, asn_ip_var):
        api_endpoint = "https://api.bgpview.io/asn/as_number"
        self.asn = None
        self.asn_name = None
        self.asn_location = None
        self.asn_date_allocated = None
        self.asn_date_updated = None
        super().__init__(api_endpoint, asn_ip_var)

    def get_asn_info(self):
        raw_data = self.run_bgpview_api()
        # print(type(data), f">>>>>> {data}")
        # pprint(data)
        # status = self.run_bgpview_api()["status"]
        # print(status)
        # status_message = self.run_bgpview_api()["status_message"]
        # print(status_message)
        meta_data = raw_data[0]
        # print(meta_data)
        status = raw_data[1]
        status_message = raw_data[2]
        try:
            # "ok" or "error""
            # status = meta_data["status"]
            # print(status)

            # "Malformed input" or ""Query was successful""
            # status_message = meta_data["status_message"]
            # print(status_message)

            if status == "error" or "Malformed input" in status_message:
                print(f"===> ERROR: {self.asn_ip_var} is NOT a valid AS number. <===\n")
            elif status == "ok" and "Query was successful" in status_message:
                data = meta_data["data"]
                # print(data)
                asn = data["asn"]
                asn_name = data["description_short"]
                asn_location = data["country_code"]
                asn_date_allocated = data["rir_allocation"]["date_allocated"]
                # asn_date_allocated = str(data["rir_allocation"]["date_allocated"]).split()
                # asn_date_allocated = str(list(asn_date_allocated[0]))
                asn_date_updated = data["date_updated"]
                # print(type(asn_date_allocated))
                # print(asn, asn_name, asn_location, asn_date_allocated, asn_date_updated)

                # "assigned", "allocated", "available", "reserved", "unknown"
                rir_allocation_status = data["rir_allocation"]["allocation_status"]
                # print(rir_allocation_status)

                # "assigned", "reserved", "unknown" 
                iana_assignment_status = data["iana_assignment"]["assignment_status"]
                # print(iana_assignment_status)

                # if rir_allocation_status == "assigned" and iana_assignment_status == "assigned":
                # if rir_allocation_status == "assigned" or rir_allocation_status == "allocated":
                if iana_assignment_status == "assigned":
                    if "unknown" not in rir_allocation_status:
                        # if rir_allocation_status == "assigned":
                        self.asn = str(asn)
                        self.asn_name = asn_name
                        self.asn_location = asn_location
                        self.asn_date_allocated = asn_date_allocated
                        self.asn_date_updated = asn_date_updated
                    # elif rir_allocation_status == "allocated":
                # elif rir_allocation_status == "available":
                # # if rir_allocation_status == "available":
                #     self.asn = f"{asn} (FREE)"
                #     self.asn_name = asn_name
                #     self.asn_location = asn_location
                #     self.asn_date_allocated = asn_date_allocated
                #     self.asn_date_updated = asn_date_updated
                # elif rir_allocation_status == "reserved" and iana_assignment_status == "reserved":
                elif "reserved" in iana_assignment_status and rir_allocation_status:
                    self.asn = str(asn)
                    self.asn_name = "Private AS Number (RFC6996)"
                    self.asn_location = "Use within the Organization Network"
                    self.asn_date_allocated = "N/A"
                    self.asn_date_updated = "N/A"
                # elif rir_allocation_status == "unknown" and iana_assignment_status == "unknown":
                elif "unknown" in iana_assignment_status and rir_allocation_status:
                    self.asn = str(asn)
                    self.asn_name = "Not a valid AS Number"
                    self.asn_location = "N/A"
                    self.asn_date_allocated = "N/A"
                    self.asn_date_updated = "N/A"
                else:
                    self.asn = asn
                    self.asn_name = "NEED VALIDATION FROM HUMAN"
                    self.asn_location = "NEED VALIDATION FROM HUMAN"
                    self.asn_date_allocated = "NEED VALIDATION FROM HUMAN"
                    self.asn_date_updated = "NEED VALIDATION FROM HUMAN"

                # print(f"TESTINGGGGG {self.web_url}")
            else:
                print(f"===> REVIEW: {self.web_url} has no data. <===\n")

            # return self.asn, self.asn_name, self.asn_location, self.asn_date_allocated, self.asn_date_updated

        except Exception as e:
            print(f"===> ERROR: {e.args} <===")
            traceback.print_exc()
            print()

        # Sample return ('1', 'Level 3 Parent, LLC', 'US', '2001-09-20 00:00:00', '2021-05-15 07:42:08')
        return self.asn, self.asn_name, self.asn_location, self.asn_date_allocated, self.asn_date_updated

class RequestASNprefixes(RequestBGPapi):
    """ Get prefixes IPv4 and IPv6 from the AS number """
    def __init__(self, api_endpoint, asn_ip_var):
        api_endpoint = "https://api.bgpview.io/asn/as_number/prefixes"
        # self.api_endpoint = api_endpoint
        self.ipv4_prefixes = None
        self.ipv4_parent_prefixes = None
        self.ipv6_prefixes = None
        self.ipv6_parent_prefixes = None
        super().__init__(api_endpoint, asn_ip_var)

    def get_asn_prefixes(self):
        raw_data = self.run_bgpview_api()
        # print(type(raw_data))
        # print(raw_data[1])
        meta_data = raw_data[0]
        # print(type(meta_data))
        # print(meta_data)
        status = raw_data[1]
        # print(type(status))
        # print(status)
        status_message = raw_data[2]
        # print(type(status_message))
        # print(status_message)

        try:
            # "ok" or "error"
            # status = meta_data["status"]
            # "Query was successful" or "Malformed input"
            # status_message = data["status_message"]
            ipv4_prefixes = []
            ipv4_parent_prefixes = []
            ipv6_prefixes = []
            ipv6_parent_prefixes = []

            # if status == "error" or "Malformed" in status_message:
            # if "error" in meta_data["status"] or "Malformed" in data["status_message"]:
            # if "error" in status or "Malformed" in status_message:
            #     print(f"===> ERROR: {self.asn_ip_var} is NOT a valid AS number. <===\n")
            if status == "ok" and "Query was successful" in status_message:
                data = meta_data["data"]
                ipv4_prefixes_list = data["ipv4_prefixes"]
                ipv6_prefixes_list = data["ipv6_prefixes"]
                # print(ipv4_prefixes_list)
                # print(ipv6_prefixes_list)
                
                # if len(ipv4_prefixes_list) != 0:
                for line in ipv4_prefixes_list:
                    for k, v in line.items():
                        # print(k)
                        if type(v) == dict:
                            if v["prefix"] is not None:
                                parent = v["prefix"]
                                ipv4_parent_prefixes.append(parent)
                            # else:
                            #     ipv4_parent_prefixes.append("No IPv4")
                        elif k == "prefix":
                            ip = v
                        elif k == "description":
                            name = v
                        elif k == "country_code":
                            location = v

                            ipv4_info = f"{ip} {name} ({location})"
                            # print(ipv4_info)
                            ipv4_prefixes.append(ipv4_info)
                # else:
                #     ipv4_parent_prefixes.append("No IPv4")
                #     ipv4_prefixes.append("No IPv4 Prefixes")

                # if len(ipv6_prefixes_list) != 0:
                for line in ipv6_prefixes_list:
                    for k, v in line.items():
                        if type(v) == dict:
                            if v["prefix"] is not None:
                                parent = v["prefix"]
                                print(parent)
                                ipv6_parent_prefixes.append(parent)
                            # else:
                            #     ipv6_parent_prefixes.append("No IPv6")
                        elif k == "prefix":
                            ip = v
                        elif k == "description":
                            name = v
                        elif k == "country_code":
                            location = v

                            ipv6_info = f"{ip} {name} ({location})"
                            # print(ipv4_info)
                            ipv6_prefixes.append(ipv6_info)
                # else:
                #     ipv6_parent_prefixes.append("No IPv6")
                #     ipv6_prefixes.append("No IPv6 Prefixes")

                # a = self.web_url
                # print(a)

                # print(f"===> REVIEW: {self.web_url} has no data. <===\n")
                # print(f"===> ERROR: {self.asn_ip_var} is NOT a valid AS number. <===\n")

            elif status == "error" or "Malformed" in status_message:
                print(f"===> ERROR: {self.asn_ip_var} is NOT a valid AS number. <===\n")
            else:
                print(f"===> REVIEW: {self.api_endpoint} has no data. <===\n")

            # Return None when there is no IPv4 or IPv6 prefixes
            # self.ipv4_prefixes = ipv4_prefixes
            # self.ipv4_parent_prefixes = list(dict.fromkeys(ipv4_parent_prefixes))
            # self.ipv6_prefixes = ipv6_prefixes
            # self.ipv6_parent_prefixes = list(dict.fromkeys(ipv6_parent_prefixes))


            # print(f"ipv4_prefixes ----> {ipv4_prefixes}\n")
            # print(f"ipv4_parent_prefixes ----> {ipv4_prefixes}\n")
            # print(f"ipv6_prefixes ----> {ipv6_prefixes}\n")
            # print(f"ipv6_parent_prefixes -----> {ipv6_parent_prefixes}\n")

            # Return None when there is no IPv4 or IPv6 prefixes
            if len(ipv4_prefixes) == 0:
                # ipv4_pref = None
                # self.ipv4_prefixes = ipv4_pref
                self.ipv4_prefixes = "No IPv4 Prefixes"
            else:
                self.ipv4_prefixes = ipv4_prefixes

            if len(ipv4_parent_prefixes) == 0:
                self.ipv4_parent_prefixes = "No IPv4 Parent Prefixes"
            else:
                self.ipv4_parent_prefixes = list(dict.fromkeys(ipv4_parent_prefixes))

            if len(ipv6_prefixes) == 0:
                self.ipv6_prefixes = "No IPv6 Prefixes"
            else:
                self.ipv6_prefixes = ipv6_prefixes

            if len(ipv6_parent_prefixes) == 0:
                self.ipv6_parent_prefixes = "No IPv6 Parent Prefixes"
            else:
                self.ipv6_parent_prefixes = list(dict.fromkeys(ipv6_parent_prefixes))

            # if len(ipv4_prefixes) != 0:
            #     self.ipv4_prefixes = ipv4_prefixes
            # elif len(ipv4_parent_prefixes) != 0:
            #     self.ipv4_parent_prefixes = list(dict.fromkeys(ipv4_parent_prefixes))
            # elif len(ipv6_prefixes) != 0:
            #     self.ipv6_prefixes = ipv6_prefixes
            # elif len(ipv6_parent_prefixes) != 0:
            #     self.ipv6_parent_prefixes = list(dict.fromkeys(ipv6_parent_prefixes))
            # else:
            #     # self.ipv4_prefixes = ipv4_prefixes
            #     # self.ipv4_parent_prefixes = list(dict.fromkeys(ipv4_parent_prefixes))
            #     # self.ipv6_prefixes = ipv6_prefixes
            #     # self.ipv6_parent_prefixes = list(dict.fromkeys(ipv6_parent_prefixes))

            #     self.ipv4_prefixes = None
            #     self.ipv4_parent_prefixes = None
            #     self.ipv6_prefixes = None
            #     self.ipv6_parent_prefixes = None

        except Exception as e:
            print(f"===> ERROR: {e.args} <===")
            traceback.print_exc()

        return self.ipv4_parent_prefixes, self.ipv4_prefixes, self.ipv6_parent_prefixes, self.ipv6_prefixes



if __name__ == "__main__":
    a = "https://api.bgpview.io/asn/as_number"
    # a = "https://api.bgpview.io/asn/as_number/prefixes"
    b = "1"
    t1 = RequestASNprefixes(a, b)
    # t1.get_asn_info()
    pprint(t1.get_asn_prefixes())
    print(t1.api_endpoint)
    print(t1.web_url)

    # import datetime
    # d1 = datetime.datetime.now()
    # t2 = RequestASN(a, b)
    # print(t2.api_endpoint)
    # # print(t2.get_asn_info())

    # for i in range(65555):
    # # for i in range(64000, 65555):
    #     d2 = datetime.datetime.now()
    #     t2 = RequestASN(a, i)
    #     print(f"Count #{i}:")
    #     print(t2.get_asn_info())
    #     d3 = datetime.datetime.now()
    #     print(d2 - d1)
    #     print(d3 - d2)
    #     print()

    
