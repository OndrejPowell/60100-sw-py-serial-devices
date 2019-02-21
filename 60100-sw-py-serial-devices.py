#Clean Main

# Main application functional blocks:
#
# 1) initialization of application from Settings.ini file
#    including  - serail devices
#               - modbus devices
#               - log file name
# intend:
# this file 
#
# this exampole application will have following functionality:
#  - control Thermotron evironmental chamber and cycle through defined setpoints
#  - measure reference temperaure using Fluke 1523 
#  - collect the data from 2G3 units

# to do:
# initit the devices
# read the devices first

# import modules
from G3Device import G3Device
from ThermatronDevice import Thermotron
from Fluke1523Device import Fluke1523
from time import sleep






















