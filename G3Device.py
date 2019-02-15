###########################################
### FILE: PYTHON SERIAL DEVICE DRIVER  ####
### DATE: 219-02-14 
### DESCRIPTION: This is a serial device class
###              for comunication with:
### HW type:     Britespot
### HW ID:       G3 Powell
###########################################

#import modules
import struct
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer


class G3Device:

    """ this class is representing a G3Device device """

    # constants for G3Device device
    INVALID_TEMP = -999
    INVALID_TEMP_DEFAULT_CHAR = '-'
    RAW_TEMP_DIVIDE_BY = 100
    
    COMMAND_LIST = {
        # Populated with starting address of each section, and for the last four additional information for how many register it would read(18 ch and 9 ch respectively)
        "readTempRegister": 97,
        "readPwrRegister": 151,
        "readIntgARegister": 205,
        "readIntgBRegister": 223,
        "readIntgABRegister": 241,
        "readRawTempRegister": 259,
        "readCalibrationOffsetRegister": 295,
        "readGeneralParametersRegister": [4,4],
        "readBritespotSnRegister": [67,12,6],
        "readBritespotFwRegister": [313,6,3],
        "readBritespotHwRegister": [319,6,3]
    }



    def __init__(self, com, slaveid, channels):         # start with the constru contructor is used for initializing variables ONLY ONE CONSTRUCTOR PER CLASS !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.client = ModbusClient(method = "rtu", port = com)
        self.connection = None
        self.slaveId = slaveid
        self.channels = channels

    def openConnection(self):      # every method OF CLASS MUST HAVE self AS FIRST PARAMETER !!!!!!!!!!!!!!!!!
        """this opens up com port with device"""
        self.connection = self.client.connect()
        if self.connection is False:
            print("Error connecting to the unit, exiting the program")
            exit(1)
        

    def closeConnection(self):
        """this closes connection with device"""
        if self.connection:
            self.client.close()

    

    def readData(self, command ):
        "Reads register from starting address (parameter), num of reg to read and slave id "
        if command not in G3Device.COMMAND_LIST:
            print("WRONG COMMAND PLEASE REFER TO COMMAND LIST: ")
            self.printDictionary()
            return None
        if isinstance( G3Device.COMMAND_LIST[command], int):
            response = self.client.read_input_registers( G3Device.COMMAND_LIST[command], self.channels, unit = self.slaveId)
        elif len( G3Device.COMMAND_LIST[command] ) == 2:
            response = self.client.read_input_registers( G3Device.COMMAND_LIST[command][0], G3Device.COMMAND_LIST[command][1], unit = self.slaveId)
        else:
            response = self.client.read_input_registers( G3Device.COMMAND_LIST[command][0], count = G3Device.COMMAND_LIST[command][1] if self.channels == 18 else G3Device.COMMAND_LIST[command][2], unit = self.slaveId)
        return response.registers

    
    def dashChannelsWithNoProbes( self, tempReg, rawTempReg, powerReg):
        for x in range( 0, len( tempReg ) ):
            if tempReg[x] == G3Device.INVALID_TEMP:
                tempReg[x] = G3Device.INVALID_TEMP_DEFAULT_CHAR
                rawTempReg[x] = G3Device.INVALID_TEMP_DEFAULT_CHAR
                powerReg[x] = G3Device.INVALID_TEMP_DEFAULT_CHAR
  
    
    def convertToSignedIntRegister(self, aregister ):
        "Simple conversion from unsigned to signed int when valid"
        reg = []
        for x in aregister: 
            unpack = struct.unpack( 'h', struct.pack('H', x ) )
            value = unpack[0]
            reg.append( value )
        return reg

    
    def divideRawTemp100( self, rawTemp ):
        "Gets the raw temperature the way it should be displayed"
        if rawTemp != G3Device.INVALID_TEMP_DEFAULT_CHAR:
            return rawTemp / G3Device.RAW_TEMP_DIVIDE_BY

    def concatenateLowAndHigh(self, low, high, register):
        "Concatenate high and low word from input register to get serial number"
        highToInt = int(register[high])
        lowToInt = int(register[low])
        hex_high = hex(highToInt)
        hex_low = hex(lowToInt)
        sn = int( hex_high + hex_low[2:], 0 )
        return sn


    def formatChannelValuesDisplay(self, temp, rawTemp, pwr ):
        rawTemperaturesDividedBy100AndSigned = []
        rawTemperaturesSigned = self.convertToSignedIntRegister(rawTemp)
        for x in range(0, self.channels):
            rawTemperaturesDividedBy100AndSigned.append( self.divideRawTemp100( rawTemperaturesSigned[x] ) )
        temperaturesSigned = self.convertToSignedIntRegister(temp)
        self.dashChannelsWithNoProbes(temperaturesSigned, rawTemperaturesDividedBy100AndSigned, pwr)
        myChannelsFormatted = []
        myChannelsFormatted.append(temperaturesSigned)
        myChannelsFormatted.append(rawTemperaturesDividedBy100AndSigned)
        myChannelsFormatted.append(pwr)
        return myChannelsFormatted

    def formatSerialNumbers(self, generalParam, britespotSn):
        generalParametersWithConcatenatedSn = []
        serialNumbersForBs = []
        high = 12 if self.channels == 18 else 6
        for x in range(0, high, 2):
            serialNumbersForBs.append( self.concatenateLowAndHigh(x,x+1, britespotSn ) )
        generalParametersWithConcatenatedSn.extend( [ self.concatenateLowAndHigh(0,1, generalParam ),  generalParam[2], generalParam[3] ] )
        mySnFormatted = []
        mySnFormatted.append(generalParametersWithConcatenatedSn)
        mySnFormatted.append(serialNumbersForBs)
        return mySnFormatted

    def printDictionary(self):
        print("List of available commands: ")
        for key in G3Device.COMMAND_LIST:
            print(key)


    














        
        

