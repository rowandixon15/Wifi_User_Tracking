# Wifi_User_Tracking
#A python script that monitors specific MAC addresses and logs them.
#N.B. -  This .py file has been heavily commented on to help beginner coders understand how it works and guide them through.
        #It is not intended for moderate

Recomendations:
    -Run on a raspberry pi (With wifi already up and running)
    -Dont run on windows as installing the 'nmap' module required is difficult

Run from cmd prompt: $ sudo python3 /address/of/the/file/Wifi_MAC_logger_basic.py 123.csv
    (123.csv can be called anything. It is just the file that will be created to store the logging data)
    
Other:
    - It must be run with root permissions (ie sudo) as nmap wont run 
