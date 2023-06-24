#!/bin/python3
import subprocess
import json
import ipaddress

lldpOutput = subprocess.getoutput("Cli -p 15 -c 'show lldp neighbors | json'")
jsonOutput = json.loads(lldpOutput)

for neighbor in jsonOutput["lldpNeighbors"]:
    if neighbor["port"] == "Management1":
        portOutput = neighbor["neighborPort"]

        portNumber = int(list(filter(str.isdigit, portOutput))[0])
        number = portNumber + 100
        subnet = ""  # SPECIFY SUBNET TO BE GIVEN TO SWITCHES IN THE FOLLOWING FORMAT xxx.xxx.xxx. EX: 10.0.0.
        netmask = ""  # SPECIFY NETMASK TO BE GIVEN TO THE SWITCHES IN THE FOLLOWING FORMAT xx EX: 24
        ipAddress = f"{subnet}{number}/{netmask}"
        password = ""  # SPECIFY PASSWORD TO BE USED FOR THE ADMIN ACCOUNT ON SWITCHES

        network = ipaddress.ip_network(ipAddress, strict=False)
        gateway = str(network[1])

        config = f"""
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
management ssh
    no shutdown
    !
    vrf MGMT
        no shutdown
    !
!
"""


with open("/mnt/flash/startup-config", "w") as file:
    file.write(config)
