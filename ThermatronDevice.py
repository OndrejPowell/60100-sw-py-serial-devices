###########################################
### FILE: PYTHON SERIAL DEVICE DRIVER  ####
### DATE: 219-02-08 
### DESCRIPTION: This is a serial device class
###              for comunication with:
### HW type:     Enironmental chamber
### HW ID:       Thermotron 3200 controller
###########################################

#import modules
from time import sleep
from serial import Serial, SerialException, SerialTimeoutException


class Thermotron:

    """ this class is representing a Thermotron device """

    # constants for Thermotron device
    BAUDRATE = 19200                # DEFAULT BAUDRATE
    TIMEOUT = 0.5                   # time out in seconds
    
    COMMAND_LIST = {
        "readSetPoint": b'setp1?\r\n',
        "setPointTemperature" : 'setp{0},{1}\r\n',
        "sendRunCommand" : b'RUNM\r\n',
        "sendStopCommand" : b'STOP\r\n'

    }



    def __init__(self, com):         # start with the constru contructor is used for initializing variables ONLY ONE CONSTRUCTOR PER CLASS !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.connection = None
        self.comPort = com 
    

    def openConnection(self):      # every method OF CLASS MUST HAVE self AS FIRST PARAMETER !!!!!!!!!!!!!!!!!
        """this opens up com port with device"""
        try:
            self.connection = Serial(port=self.comPort, baudrate=Thermotron.BAUDRATE, timeout=Thermotron.TIMEOUT )    #open com port
        except SerialException:
            print("Com port cannot open")
        

    def closeConnection(self):
        """this closes connection with device"""
        if self.connection != None:
            if self.connection.isOpen():  # this is a getter, there is a variab le is_open .... 
                self.connection.close()


    def readData(self, command, size=50):
        """reads data from Thermatron"""
        self.sendCommand( command )
        data_read = self.connection.read(size)
        return data_read.decode('utf-8')        # returns decoded data
        


    def sendCommand(self, command):
        """ writes command to Thermatron"""
        if command not in Thermotron.COMMAND_LIST:
            print("WRONG COMMAND PLEASE REFER TO COMMAND LIST: ")
            self.printDictionary()
            return
        try:
            self.connection.write( Thermotron.COMMAND_LIST[command] )
        except SerialTimeoutException:
            print("COULD NOT READ THE DATA")
        except SerialException:
            print("DEVICE DISCONNECTED")

    def setTemperature(self, setpointNumber, value):
        command = ( Thermotron.COMMAND_LIST["setPointTemperature"].format(setpointNumber, value)).encode('utf-8')
        try:
            self.connection.write( command )
        except SerialTimeoutException:
            print("COULD NOT READ THE DATA")
        except SerialException:
            print("DEVICE DISCONNECTED")

    def printDictionary(self):
        print("List of available commands: ")
        for key in Thermotron.COMMAND_LIST:
            print(key)


    














        
        

