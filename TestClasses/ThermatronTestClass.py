from ThermatronDevice import Thermotron
# test code below

print('Thermotron driver tester')

myThermatronDevice1 = Thermotron("COM5")        # this is an object
myThermatronDevice1.openConnection()            # connection is ope

myDataRead = myThermatronDevice1.readData("readSetPoint", 50)
print("Test 1: dta recieved from thermatron setpoint one", myDataRead)


myThermatronDevice1.closeConnection()