# arista-ztp-ideas

Different ideas for building scalable solutions for zero touch provisioning process.

There are couple things I dislike specifically around the idea of manipulating DHCP as it is quite manual or as I like to call up-front-provisioning.
This process usually involves identifying devices based on serial number or system MAC address and handing them the right configuration file.

Here I added some solutions that could be extended upon but would serve as one universal way of provisioning Arista devices.

When Arista devices download file via DHCP option 67/143 the first line in the file will specificy which shell it should run in.
Most typically people specify CLI commands up front, as it selects CLI shell by default, but this can be changed and these ideas will take advantage of this.

#!/bin/bash -> Will run the script via bash shell
#!/bin/python3 -> Will run the script via python3 shell


