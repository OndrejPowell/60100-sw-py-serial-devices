###########################################
### FILE: PYTHON SERIAL DEVICE DRIVER  ####
### DATE: 219-02-08 
### DESCRIPTION: This is a serial device class
###              for comunication with:
### HW type:     Fluke reference thermometer 
### HW ID:       Fluke 1523
###########################################

#import modules
from time import sleep
from serial import Serial, SerialException, SerialTimeoutException


class Fluke1523:

    """ this class is representing a Fluke1523 device """

    # constants for Fluke1523 device
    BAUDRATE = 9600                # DEFAULT BAUDRATE
    TIMEOUT = 0.5                  # time out in seconds
    
    COMMAND_LIST = {
        "readTemperature" : b'FETC?\r\n'
    }



    def __init__(self, com):         # start with the constru contructor is used for initializing variables ONLY ONE CONSTRUCTOR PER CLASS !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.connection = None
        self.comPort = com 
    

    def openConnection(self):      # every method OF CLASS MUST HAVE self AS FIRST PARAMETER !!!!!!!!!!!!!!!!!
        """this opens up com port with device"""
        try:
            self.connection = Serial(port=self.comPort, baudrate=Fluke1523.BAUDRATE, timeout=Fluke1523.TIMEOUT )    #open com port
        except SerialException:
            print("Com port cannot open")
        

    def closeConnection(self):
        """this closes connection with device"""
        if self.connection != None:
            if self.connection.isOpen():  # this is a getter, there is a variab le is_open .... 
                self.connection.close()


    def readData(self, command, size=50):
        """reads data from Thermatron"""
        self.writeData( command )
        data_read = self.connection.read(size)
        return data_read.decode('utf-8')        # returns decoded data
        


    def writeData(self, command):
        """ writes command to Thermatron"""
        if command not in Fluke1523.COMMAND_LIST:
            print("WRONG COMMAND PLEASE REFER TO COMMAND LIST: ")
            self.printDictionary()
            return
        try:
            self.connection.write( Fluke1523.COMMAND_LIST[command] )
        except SerialTimeoutException:
            print("COULD NOT READ THE DATA")
        except SerialException:
            print("DEVICE DISCONNECTED")


    def printDictionary(self):
        print("List of available commands: ")
        for key in Fluke1523.COMMAND_LIST:
            print(key)


    














        
        

