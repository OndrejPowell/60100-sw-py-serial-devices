import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# now this works, even when a2.py is run directly
from G3Device import G3Device


# def formatList( self, alist, start, end, width ):
#     "Formats the line with constant spacing"
#     line_new = ''
#     for i in range(start,end):
#         line_new += str(alist[i]).ljust(width)
#     return line_new
# MIGHT BE USEFUL TO FORMAT OUR OUTPUT FOR TESTING

myG3Device = G3Device('COM6', 1, 9)
myG3Device.openConnection()
formattedChannels = myG3Device.formatChannelValuesDisplay(myG3Device.readData("readTempRegister"), myG3Device.readData("readRawTempRegister"),  myG3Device.readData("readTempRegister"))
formatTemps = formattedChannels[0] 
formatRawTemps = formattedChannels[1] 
formatPowers = formattedChannels[2] 
print( "Temperatures: ", formatTemps)
print( "Raw Temperatures : ", formatRawTemps)
print( "Powers: ", formatPowers)
print( "Integral A: ", myG3Device.readData("readIntgARegister"))
print( "Integral B: ", myG3Device.readData("readIntgBRegister"))
print( "Integral AB: ", myG3Device.readData("readIntgABRegister"))
print( "Calibration Offsets: ", myG3Device.readData("readCalibrationOffsetRegister"))
print(  "FW REV For Britespots: ", myG3Device.readData("readBritespotFwRegister"))
print( "HW REV For Britespots: ", myG3Device.readData("readBritespotHwRegister"))
formattedSn = myG3Device.formatSerialNumbers( myG3Device.readData("readGeneralParametersRegister"), myG3Device.readData("readBritespotSnRegister") )
formattedGeneralParams = formattedSn[0]
formattedBritespotSn = formattedSn[1]
print("Unit SN, HW-REV, FW-REV: ", formattedGeneralParams)
print("Britespots Serial Numbers: ", formattedBritespotSn)
myG3Device.closeConnection()
