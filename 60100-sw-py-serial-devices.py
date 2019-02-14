from ThermatronDevice import Thermotron
from Fluke1523Device import Fluke1523
import time


# test code below
print('Python driver tester')
myFluke1523ComPort = input("Enter COM port >>>")
logInterval = int(input("Enter log interval in seconds >>>"))
myFluke1523Device1 = Fluke1523(myFluke1523ComPort)        # this is an object
myFluke1523Device1.openConnection()           # connection is open
myFluke1523Id = myFluke1523Device1.readData("readId")
print ("Fluke Reference Identificationi : " , myFluke1523Id)

for i in range (0,10):
    myDataRead = myFluke1523Device1.readData("readTemperature")
    print("Test 1: data recieved from Fluke setpoint one", i, myDataRead)
    time.sleep(logInterval)


myFluke1523Device1.closeConnection()










