import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from ConfigFileGenerator import Settings

configFile = Settings()
print( configFile.read("G3", "sectionsToLog") )
print( configFile.read("G3", "numberOfChannels") )