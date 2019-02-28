###########################################
### FILE: PYTHON SERIAL DEVICE DRIVER  ####
### DATE: 2019-02-26 
### DESCRIPTION: This class reads the:
###              Settings.ini and parses
###              the values,
###              it makes main code cleaner
###########################################


from ConfigFileGenerator import Settings

settings = Settings()

class G3SettingsParser:

    NR_OF_CHANNELS_LIST = []
    SLAVE_ID_LIST = []
    NR_OF_UNITS =  int( settings.read("G3","numberofunits") )
    COMPORT =  settings.read("G3","comport")
    SECTIONS_TO_LOG =  settings.read("G3","sectionstolog").split(',')

    tempList1 = settings.read("G3","slaveidlist").split(',')
    tempList2 = settings.read("G3","numberofchannels").split(',')
    
    for i  in range(0,len(tempList1)):
        SLAVE_ID_LIST.append( int( tempList1[i] ) )
        NR_OF_CHANNELS_LIST.append( int( tempList2[i] ) )

class EEMSettingsParser:

    SLAVE_ID_LIST = []
    NR_OF_UNITS =  int( settings.read("EEM","numberofunits") )
    COMPORT =  settings.read("EEM","comport")
    SECTIONS_TO_LOG =  settings.read("EEM","sectionstolog").split(',')

    tempList1 = settings.read("EEM","slaveidlist").split(',')
    
    for x in tempList1:
        SLAVE_ID_LIST.append( int( x ) )


class ThermatronSettingsParser:
   
    COMPORT =  settings.read("Thermatron","comport")
    SETPOINTS_LIST = []
    tempList1 = settings.read("Thermatron","setpoints").split(',')
    NR_OF_LOOPS =  int( settings.read("Thermatron","numberofloops") )
    SOAK_TIME =  int( settings.read("Thermatron","soaktime") )

    for x in tempList1:
        SETPOINTS_LIST.append( int( x ) )

class Fluke1523SettingsParser:
   
    COMPORT =  settings.read("Fluke1523","comport")


class MainLogSettingsParser:
   
    NR_OF_SAMPLES_PER_SETPOINT =  int( settings.read("Main-Log-Settings","numberofsamplespersetpoint" ) )
    NR_OF_CYCLES =  int( settings.read("Main-Log-Settings","numberofcycles" ) )
    POLLTIME =  float( settings.read("Main-Log-Settings","polltime" ) )

