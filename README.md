# arista-ztp-ideas

Different ideas for building scalable solutions for zero touch provisioning process.
No requirements to identify devices based on Serial or System MAC

lldp-increment
---------------------
- Read LLDP data from switch
- Assign IP to the management port based on oob switch port number
- Activate API and SSH in the management VRF

nautobot
-----------
- Read LLDP data from switch
- Pass the data to DCIM/IPAM solution (Nautobot in this case)
- Read IP data from Nautobot and Assign to Management interface
- Activate API and SSH in the management VRF