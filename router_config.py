import subprocess
import os
from dotenv import load_dotenv


load_dotenv()
device = os.getenv("ROUTER")
login_id = os.getenv("ROUTER_USER")
login_password = os.getenv("ROUTER_PASSWORD")

# print(device, login_id, login_password)

ssh_cmd = "ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes128-cbc {val1}@{val2}".format(val1=login_id, val2=device)

print(ssh_cmd)

ssh_connect = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
"""
The authenticity of host 'skip' can't be established.
RSA key fingerprint is SHA256:Ba7+8JUUQM1O124owV/PIHPbnovlMsJyE+55+LRJaTc.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'skip' (RSA) to the list of known hosts.
(skip) Password: 
"""

# Didn't work. The output stops at "ssh_connect" and don't get to "ssh_authenciate"
ssh_authenticate = subprocess.run(input=login_password, shell=True)