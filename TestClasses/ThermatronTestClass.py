import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) 
from ThermatronDevice import Thermatron
from time import sleep
# test code below

print('Thermotron driver tester')

myThermatronDevice1 = Thermatron("COM5")        # this is an object
myThermatronDevice1.openConnection()            # connection is ope

sleep(1)

myThermatronDevice1.sendCommand('sendRunCommand')

myDataRead = myThermatronDevice1.readData("readSetPoint")
print("Test 1: dta recieved from thermatron setpoint one", myDataRead)

myThermatronDevice1.setTemperature(1,1)

sleep(1)

myDataRead1 = myThermatronDevice1.readData("readSetPoint")
print("Test 2: dta recieved from thermatron setpoint one", myDataRead1)

sleep(10)

myThermatronDevice1.sendCommand('sendStopCommand')


myThermatronDevice1.closeConnection()