#!/bin/python3
import subprocess
import json
import requests
import ipaddress

lldpOutput = subprocess.getoutput("Cli -p 15 -c 'show lldp neighbors | json'")
jsonOutput = json.loads(lldpOutput)

for neighbor in jsonOutput["lldpNeighbors"]:
    if neighbor["port"] == "Management1":
        portId = neighbor["neighborPort"]
        neighborId = neighbor["neighborDevice"]

nautobotServer = ""  # ADD IN YOUR NAUTOBOT SERVER
readOnlyToken = ""  # ADD IN YOUR NAUTOBOT READ-ONLY TOKEN

headers = {
    "Authorization": f"Token {readOnlyToken}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

url = f"https://{nautobotServer}/api/dcim/interfaces?device={neighborId}&name={portId}"

response = requests.get(url, headers=headers, verify=False).json()
deviceUrl = response["results"][0]["cable_peer"]["device"]["url"]

deviceResponse = requests.get(deviceUrl, headers=headers, verify=False).json()
hostname = deviceResponse["name"]

ipUrl = f"https://{nautobotServer}/api/ipam/ip-addresses?device={hostname}&interface=Management1"
ipResponse = requests.get(ipUrl, headers=headers, verify=False).json()
ipAddress = ipResponse["results"][0]["address"]

network = ipaddress.ip_network(ipAddress, strict=False)
gateway = str(network[1])

password = ""  # SPECIFY THE PASSWORD TO BE USED ON SWITCHES


config = f"""
service routing protocols model multi-agent
!
hostname {hostname}
!
terminal width 32767
!
vrf instance MGMT
!
username admin secret {password}
!
interface Management1
vrf MGMT
    ip address {ipAddress}
!
ip route vrf MGMT 0.0.0.0/0 {gateway}
!
management api http-commands
    protocol http
    no shutdown
    !
    vrf MGMT
        no shutdown
        protocol http
    !
!
management ssh
    no shut
    !
    vrf MGMT
        no shut
    !
!
"""


with open("/mnt/flash/startup-config", "w") as file:
    file.write(config)
