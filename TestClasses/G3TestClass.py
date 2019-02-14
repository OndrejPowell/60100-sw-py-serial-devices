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
print ( "Temperatures: ", myG3Device.readData("readTempRegister"))
generalParameters = myG3Device.readData("readGeneralParametersRegister")
print (  "FW REV For Britespots: ", myG3Device.readData("readBritespotFwRegister"))
print ( "HW REV For Britespots: ", myG3Device.readData("readBritespotHwRegister"))
britespotSn = myG3Device.readData("readBritespotSnRegister")
serialNumbersForBs = []
generalParametersWithConcatenatedSn = []
for x in range(0, 6,2):
    serialNumbersForBs.append( myG3Device.concatenateLowAndHigh(x,x+1, britespotSn ) )
print("Britespots Serial Numbers: ", serialNumbersForBs)
generalParametersWithConcatenatedSn.extend( [ myG3Device.concatenateLowAndHigh(0,1, generalParameters ),  generalParameters[2], generalParameters[3] ] )
print("Unit SN, HW-REV, FW-REV: ", serialNumbersForBs)