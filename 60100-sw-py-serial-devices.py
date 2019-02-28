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
from SettingsParser import G3SettingsParser as g3sp
#from SettingsParser import EEMSettingsParser as eemsp
from SettingsParser import ThermatronSettingsParser as thermatronsp
from SettingsParser import Fluke1523SettingsParser as flukesp
from SettingsParser import MainLogSettingsParser as mainlogsp
from ThermatronDevice import Thermatron
from Fluke1523Device import Fluke1523
from ModbusChain import ModbusChain as Mc
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
    COMMAND_WAIT_TIME = 1.5
# create instance of Thermatron
    thermatron = Thermatron(thermatronsp.COMPORT)
    thermatron.openConnection()
    thermatron.sendCommand("sendRunCommand")
# create instance of Fluke1523
    fluke1523 = Fluke1523(flukesp.COMPORT)
    fluke1523.openConnection()

# create instance of multiple G3 units
    

    mc1 = Mc(g3sp.COMPORT, g3sp.NR_OF_UNITS)
    mc1.openConnection()

    #instanciating and opening connection from all devices 
    for i in range(0, g3sp.NR_OF_UNITS):
        mc1.addG3DeviceToChain( g3sp.NR_OF_CHANNELS_LIST[i]  , g3sp.SLAVE_ID_LIST[i] )
        print(mc1.deviceList)
        deviceInfoId = mc1.getG3FormattedDeviceInfo ( mc1.deviceList[i] )
        print("Device:", g3sp.SLAVE_ID_LIST[i], g3sp.COMPORT ,"General Parameters: ", deviceInfoId[0], "Britespot SerialNumbers", deviceInfoId[1])

    #reading from all devices

    # main loop
    dataSample = []
    totalSampleNumber = 0
    # LOOP 1 - highest loop, gets repeated as per "number of cycles" in the settings.ini
    for currentCycle in range(0, mainlogsp.NR_OF_CYCLES):
        
        # LOOP 2 - Thermatron cycles through temperature setpoints
        for setpoint in thermatronsp.SETPOINTS_LIST:
            thermatron.setTemperature( str(setpoint).strip() )
            sleep(thermatronsp.SOAK_TIME)
            

            # LOOP 3 - for collecting the data at each Thermatron setpoints    
            for sampleNr in range(0, mainlogsp.NR_OF_SAMPLES_PER_SETPOINT ): # 
                deviceCounter = 0
                totalSampleNumber += 1
                                
                # data from Fluke reference
                dataFromFluke1523 = fluke1523.readData("readTemperature")

                # append the sample IDs and data

                dataSample.append(totalSampleNumber)
                dataSample.append(currentCycle+1)
                dataSample.append(setpoint)
                dataSample.append(sampleNr+1)
                dataSample.append( str( dataFromFluke1523 ).strip() )

                # LOOP 4 - collects the data from the connected devices
                
                for deviceTuple in mc1.deviceList:   
                    for i in range(0, len(g3sp.SECTIONS_TO_LOG)):
                        if g3sp.SECTIONS_TO_LOG[i] == "readTempRegister":
                            sectionLogged = mc1.convertToSignedIntRegister( mc1.readData(deviceTuple, g3sp.SECTIONS_TO_LOG[i]) )
                        elif g3sp.SECTIONS_TO_LOG[i] == "readRawTempRegister":
                            sectionLogged = mc1.convertRawTempRegister( mc1.readData(deviceTuple, g3sp.SECTIONS_TO_LOG[i]) )
                        else:
                            sectionLogged = mc1.readData(deviceTuple, g3sp.SECTIONS_TO_LOG[i])
                        dataSample.append(sectionLogged)    
                    deviceCounter += 1
                aline = formatList( dataSample, 0, len(dataSample) )
                formatDataSampleList = aline[:len(aline)-1].split(',') # FROM aline start to end (which is length of string - 1)
                print(formatDataSampleList)
                logfile_writer.writerow(formatDataSampleList)
                print()
                print("-------------------------------------------------------------------------")
                print()
                dataSample.clear()
                sleep(mainlogsp.POLLTIME)

    # closing connection from all devices
    print("Test finished, number of errors while getting data: ", mc1.errorCounter)
    mc1.closeConnection()
    mc1.cleanDeviceList()
    fluke1523.closeConnection()
    thermatron.sendCommand("sendStopCommand")
    sleep(COMMAND_WAIT_TIME)
    thermatron.closeConnection()
    logfile.close()



if __name__ == "__main__":
    main()



















