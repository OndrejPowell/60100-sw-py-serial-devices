from configparser import SafeConfigParser
from pathlib import Path

class Settings:
    """ Class that sets up a default Settings.ini if not there yet """
    def __init__(self):
        self.config = SafeConfigParser()
        my_file = Path('.\\Settings.ini')
        #If file doesn't exists, create it.
        if not my_file.is_file():
            self.setupIniFile()
        self.config.read('Settings.ini')

    def setupIniFile(self):

        self.config.add_section('G3')
        self.config.set('G3', 'numberOfChannels', '')
        self.config.set('G3', 'numberOfUnits', '')
        self.config.set('G3', 'comPort', '')
        self.config.set('G3', 'sectionsToLog', 'readTempRegister,readPwrRegister')
        
        self.config.add_section('EEM')
        self.config.set('EEM', 'numberOfUnits' , '') 
        self.config.set('EEM', 'comPort' , '')
        self.config.set('EEM', 'sectionsToLog' , '') 
        
        
        self.config.add_section('Thermatron')
        self.config.set('Thermatron', 'setpoints', '-40,-20,0,20,40,60') 
        self.config.set('Thermatron', 'numberOfLoops', '10')
        self.config.set('Thermatron', 'soakTime', '60')
        
        self.config.add_section('Main-Log-Settings') 
        self.config.set('Main-Log-Settings', 'numberOfSamplesPerSetpoint', '100')
        self.config.set('Main-Log-Settings', 'numberOfCycles', '3')
        self.config.set('Main-Log-Settings', 'pollTime', '3.5')

        with open('Settings.ini', 'w') as f:
            self.config.write(f)

    def read(self, section, key):
        return self.config.get(section, key)