#
# WIP Script to Log the availability of devices on a network
#


import sys
import os
import nmap
from datetime import datetime
from time import sleep

# Actual scanning is done by this function
def scan():
    # Define an array to hold  our results in. Fill with 0s
    scan_results = [0] * len(tracked_mac_addrs)
    # Repeat scan three times with a 10s gap between all scans. Some devices arnt seen on every scan, so you can increace the number as some devices wont be seen otherwise
    for x in range(0, 3): 
        # Perform the scan
        nm = nmap.PortScanner()
        nm.scan("192.168.x.x/xx", arguments='-sn') # most home wifi subnets start with 192.168.... You need to find out your full subnet address and put it here
        # Search for our target MAC addresses in the scan results 
        for h in nm.all_hosts():
            if 'mac' in nm[h]['addresses']: # MAC address doesn't always exist
                mac_addr = nm[h]['addresses']['mac']
                if mac_addr in tracked_mac_addrs:
                    scan_results[tracked_mac_addrs.index(mac_addr)] |= 1
        # Sleep 10 seconds if not the last loop
        if x != 2: sleep(10)
    return scan_results

# Check we are root
if os.geteuid() != 0:
    print("Must be run as root!")
    exit(-1)

# Check we have the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: %s [logfile]" % (sys.argv[0]))
    exit(-1)

###### Options that can be changed ######
subnet = "192.168.x.x/xx" # Define the subnet to scan here, same as above, put in your full subnet address
tracked_mac_addrs = [ # List the MAC addresses to track here - must be uppercase!
    "FF:FF:FF:FF:FF:FF", #Device A
    "FF:FF:FF:FF:FF:FF", #Device B
    "FF:FF:FF:FF:FF:FF", #Device C
    "FF:FF:FF:FF:FF:FF"  #Device D......You can put as many mac addresses that you want to track here as you like
]
scan_interval = 300 # In seconds. Scan every 5 minutes
###### End of options to be changed ######

# Setup our log file
log_file = None
if not (os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1])):
    # Create the file and write the headers to it
    print("Logfile does not exist. Creating it")
    try:
        log_file = open(sys.argv[1], 'w')
        log_file.write("time")
        for mac in tracked_mac_addrs:
            log_file.write(", %s" % (mac))
        log_file.write("\n")
    except:
        print("Failed to open log file %s" % (sys.argv[1]))
        exit(-1)
else:
    # Just open the log file and append to it
    print("Opening already created log file")
    try:
        log_file = open(sys.argv[1], 'a')
    except:
        print("Failed to open log file %s" % (sys.argv[1]))
        exit(-1)


# Main loop
while True:
    try:
        # Perform the scan
        print("Performing scan... ")
        scan_result = scan()
        print("done.")
        # Write a line to the logfile
        log_file.write("%s" % (datetime.now().strftime("%d-%m-%y %H:%M:%s")))
        for res in scan_result:
            log_file.write(", %s" % (res))
        log_file.write("\n")
        log_file.flush()
        print("Logfile written")
        # Sleep until the next scan
        print("Sleeping for %d seconds" % (scan_interval))
        sleep(scan_interval)
    except KeyboardInterrupt:
        # Gracefully shut down
        log_file.close()
        exit(0)