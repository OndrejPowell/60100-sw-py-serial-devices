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
from pymodbus.transaction import ModbusIOException



class ModbusChain:

    """ this class is representing a ModbusChain """

    # constants for ModbusChain 
    INVALID_TEMP = -999
    INVALID_TEMP_DEFAULT_CHAR = '-'
    RAW_TEMP_DIVIDE_BY = 100
    
    G3_COMMAND_LIST = {
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



    def __init__(self, com, numOfDevices):       # start with the constru contructor is used for initializing variables ONLY ONE CONSTRUCTOR PER CLASS !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.comPort = com
        self.client = ModbusClient(method = "rtu", port = self.comPort)
        self.connection = None
        self.deviceList = []  #it's gonna contain a list of tuples nrOfChannels, slaveID

    def addG3DeviceToChain( self, nrOfChannels, slaveId ) :
        self.deviceList.append( ( nrOfChannels, slaveId )  )

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

    

    def readData(self, deviceTuple, command ):
        "Reads register from starting address (parameter), num of reg to read and slave id "
        try:
            nrOfChannels = deviceTuple[0]
            slaveId = deviceTuple[1]
            if command not in ModbusChain.G3_COMMAND_LIST:
                print("WRONG COMMAND PLEASE REFER TO COMMAND LIST: ")
                self.printDictionary()
                return None
            if isinstance( ModbusChain.G3_COMMAND_LIST[command], int):
                response = self.client.read_input_registers( ModbusChain.G3_COMMAND_LIST[command], nrOfChannels, unit = slaveId)
            elif len( ModbusChain.G3_COMMAND_LIST[command] ) == 2:
                response = self.client.read_input_registers( ModbusChain.G3_COMMAND_LIST[command][0], ModbusChain.G3_COMMAND_LIST[command][1], unit = slaveId)
            else:
                response = self.client.read_input_registers( ModbusChain.G3_COMMAND_LIST[command][0], count = ModbusChain.G3_COMMAND_LIST[command][1] if nrOfChannels == 18 else ModbusChain.G3_COMMAND_LIST[command][2], unit = slaveId)
            return response.registers
        except ModbusIOException:
            return 'NO-DATA'
    
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
        if rawTemp != ModbusChain.INVALID_TEMP_DEFAULT_CHAR:
            return rawTemp / ModbusChain.RAW_TEMP_DIVIDE_BY

    def concatenateLowAndHigh(self, low, high, register):
        "Concatenate high and low word from input register to get serial number"
        highToInt = int(register[high])
        lowToInt = int(register[low])
        hex_high = hex(highToInt)
        hex_low = hex(lowToInt)
        sn = int( hex_high + hex_low[2:], 0 )
        return sn


    def convertRawTempRegister(self, rawTemp ):
        """This function gets raw temp register and converts it in a way that data is meaningful to the user. See test class for usage"""
        rawTemperaturesDividedBy100AndSigned = []
        rawTemperaturesSigned = self.convertToSignedIntRegister(rawTemp)
        for x in range(0, len(rawTemp) ):
            rawTemperaturesDividedBy100AndSigned.append( self.divideRawTemp100( rawTemperaturesSigned[x] ) )
        return rawTemperaturesDividedBy100AndSigned

    def getG3FormattedDeviceInfo(self, deviceTuple):
        """This function gets the 2 registers with Serial Numbers and concatenates low and high words to make up the serial number needed. See test class for usage"""
        generalParam = self.readData(deviceTuple, "readGeneralParametersRegister")
        britespotSn = self.readData(deviceTuple, "readBritespotSnRegister")
        generalParametersWithConcatenatedSn = []
        serialNumbersForBs = []
        high = 12 if deviceTuple[0] == 18 else 6
        for x in range(0, high, 2):
            serialNumbersForBs.append( self.concatenateLowAndHigh(x,x+1, britespotSn ) )
        generalParametersWithConcatenatedSn.extend( [ self.concatenateLowAndHigh(0,1, generalParam ),  generalParam[2], generalParam[3] ] )
        mySnFormatted = []
        mySnFormatted.append(generalParametersWithConcatenatedSn)
        mySnFormatted.append(serialNumbersForBs)
        return mySnFormatted

    def cleanDeviceList(self):
        del self.deviceList[:]

    def printDictionary(self):
        print("List of available commands: ")
        for key in ModbusChain.G3_COMMAND_LIST:
            print(key)


    














        
        

