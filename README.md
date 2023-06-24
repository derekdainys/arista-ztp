# arista-ztp-ideas

Different ideas for building scalable solutions for Arista ZTP process.
No requirements to identify devices based on Serial or System MAC.
Files should be given to every switch during ZTP process via DHCP option 67.

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