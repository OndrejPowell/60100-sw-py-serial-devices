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
# this example application will have following functionality:
#  - control Thermotron evironmental chamber and cycle through defined setpoints
#  - measure reference temperaure using Fluke 1523 
#  - collect the data from 2G3 units

# to do:
# initit the devices
# read the devices first


# import modules
from ConfigFileGenerator import Settings
from ThermatronDevice import Thermatron
from Fluke1523Device import Fluke1523
from G3Device import G3Device
from time import sleep
import csv


def formatList( alist, start, end ):
    "Formats the line with constant spacing"
    line_new = ''
    for i in range(start,end):
        if isinstance( alist[i], list):
            for data in alist[i]:
                line_new += str(data) + ','
        else:
            line_new += str(alist[i]) + ','  
    return line_new

# read settings.ini
def main():
# open the file for logging
    logfile = open ('test.csv', mode='w', newline='')
    logfile_writer = csv.writer(logfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    settings = Settings()
    COMMAND_WAIT_TIME = 1.5
# create instance of Thermatron
    thermatron = Thermatron(settings.read("Thermatron", "comport"))
    thermatron.openConnection()
    thermatron.sendCommand("sendRunCommand")
# create instance of Fluke1523
    fluke1523 = Fluke1523(settings.read("Fluke1523", "comport"))
    fluke1523.openConnection()

# create instance of multiple G3 units
    nrOfG3s = int( settings.read("G3","numberofunits") )
    g3ChannelsToList = settings.read("G3","numberofchannels").split(',')
    g3ComPort = settings.read("G3","comports")
    g3SectionsToLogToList = settings.read("G3","sectionstolog").split(',')
    listOfG3Devices = []

    #instanciating and opening connection from all devices 
    for i in range(0, nrOfG3s):
        
        listOfG3Devices.append( G3Device( g3ComPort, i+1, int( g3ChannelsToList[i] ) ) )
        listOfG3Devices[i].openConnection()
        print( g3ComPort, i+1)
        deviceInfoId = listOfG3Devices[i].getFormattedDeviceInfo()
        print("Device:", i+1, g3ComPort ,"General Parameters: ", deviceInfoId[0], "Britespot SerialNumbers", deviceInfoId[1])
        # listOfG3Devices[i].closeConnection()

    #reading from all devices

    # main loop
    setpointToList = settings.read("Thermatron","setpoints").split(',')
    dataSample = []
    # LOOP 1 - highest loop, gets repeated as per "number of cycles" in the settings.ini
    for currentCycle in range(0, int(settings.read("Main-Log-Settings","numberofcycles") ) ):
        
        

        # LOOP 2 - Thermatron cycles through temperature setpoints
        for setpoint in setpointToList:
            thermatron.setTemperature( str(setpoint).strip() )
            sleep(COMMAND_WAIT_TIME)
            

            # LOOP 3 - for collecting the data at each Thermatron setpoints    
            for sampleNr in range(0, int( settings.read("Main-Log-Settings", "numberofsamplespersetpoint") ) ): # 
                deviceCounter = 0
                # data from Fluke reference
                dataFromFluke1523 = fluke1523.readData("readTemperature")
                dataSample.append(setpoint)
                dataSample.append(currentCycle+1)
                dataSample.append(sampleNr+1)
                dataSample.append( str( dataFromFluke1523 ).strip() )

                # LOOP 4 - collects the data from the connected devices           
                
                for device in listOfG3Devices:   
                    for i in range(0, len(g3SectionsToLogToList)):
                        if g3SectionsToLogToList[i] == "readTempRegister":
                            sectionLogged = device.convertToSignedIntRegister( device.readData(g3SectionsToLogToList[i]) )
                        elif g3SectionsToLogToList[i] == "readRawTempRegister":
                            sectionLogged = device.convertRawTempRegister( device.readData(g3SectionsToLogToList[i]) )
                        else:
                            sectionLogged = device.readData(g3SectionsToLogToList[i])
                        dataSample.append(sectionLogged)    
                        
                        # print ("Sample #:", sampleNr+1, "Device:", deviceCounter+1, g3ComPortsToList[deviceCounter] , "Section: " + g3SectionsToLogToList[i] + ":", sectionLogged)
                    deviceCounter += 1
                aline = formatList( dataSample, 0, len(dataSample) )
                formatDataSampleList = aline[:len(aline)-1].split(',') # FROM aline start to end (which is length of string - 1)
                print(formatDataSampleList)
                logfile_writer.writerow(formatDataSampleList)
                print()
                print("-------------------------------------------------------------------------")
                print()
                dataSample.clear()
                sleep( float( settings.read("Main-Log-Settings", "polltime") ) )

    #closing connection from all devices
    for i in range(0, nrOfG3s):    
        listOfG3Devices[i].closeConnection()
    fluke1523.closeConnection()
    thermatron.sendCommand("sendStopCommand")
    sleep(COMMAND_WAIT_TIME)
    thermatron.closeConnection()
    logfile.close()



if __name__ == "__main__":
    main()



















