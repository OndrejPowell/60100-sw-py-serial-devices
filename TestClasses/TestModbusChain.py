import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from ModbusChain import ModbusChain


myModbusChain = ModbusChain('COM7', 2)
myModbusChain.openConnection()
myModbusChain.addG3DeviceToChain( 9, 1 )
myModbusChain.addG3DeviceToChain( 9, 2 )
print( myModbusChain.readData ( myModbusChain.deviceList[0], "readTempRegister" ) )
print( myModbusChain.readData ( myModbusChain.deviceList[1], "readTempRegister" ) )
myModbusChain.closeConnection()
myModbusChain.cleanDeviceList()