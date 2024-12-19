import sys
import logging
from ruamel.yaml import YAML

class Config:
    """Config class.
    
    Get and validate configuration parameters from a configuration file based on YAML.
    """

    def __init__(self, cfgFile):
        """Config class constructor.

        Get and validate configuration parameters from a configuration file based on YAML. These parameters will be saved as class attributes.
    
        Parameters:
            cfgFile (str): Configuration file path.

        Attributes:
            tree (dict): Configuration file tree (from YAML object).
        """              

        # A tree with configuration project
        self.tree = self.readConfigFile(cfgFile)

        # Getting SYSTEM session
        logging.debug("Getting 'system' key information")
        if "system" not in self.tree:
            logging.error("Not 'system' key found on configuration file")
            sys.exit("ERROR: Not 'system' key found on configuration file!!!")            
            if "serial" not in self.tree:
                logging.error("Not 'serial' key found on configuration file")
                sys.exit("ERROR: Not 'serial' key found on configuration file!!!")
        # Debug level
        self.debugLevel = self.tree["system"]["debug_level"]

        # LoRa module type
        self.loraModule = self.tree["system"]["lora_module"]

        # Serial port path
        self.serialPort = self.tree["system"]["serial"]["port"]

        # Serial baudrate
        self.serialBaudrate = self.tree["system"]["serial"]["baudrate"]

        # LoRa base band
        self.loraBaseBand = self.tree["system"]["lora"]["base_band"]

        # LoRa sub band
        self.loraSubBand = self.tree["system"]["lora"]["sub_band"]

        # LoRa class
        self.loraClass = self.tree["system"]["lora"]["class"]

        # LoRa RX window 2 frequency
        self.loraRXWin2Freq = self.tree["system"]["lora"]["rxwin2_freq"]

        # LoRa RX window 2 data rate
        self.loraRXWin2DR = self.tree["system"]["lora"]["rxwin2_dr"]

        # LoRa authentication mode
        self.loraAuthMode = self.tree["system"]["lora"]["auth_mode"]

        # Getting PROJECTS session
        logging.debug("Getting 'projects' key information")
        if "projects" not in self.tree:
            logging.error("Not 'projects' key found on configuration file")
            sys.exit("ERROR: Not 'projects' key found on configuration file!!!")
        # Projects list
        self.projects = self.tree["projects"]
        logging.info("%s project(s) found: %s", len(self.projects), self.projects)        

    def readConfigFile(self, configFile):
        """Read the configuration file.
        
        Parameters:
            configFile (str): Configuration file path.
        
        Returns:
            (dict): Configuration tree (from YAML object).
        """
        try:
            with open(configFile, 'r') as _f:
                yaml = YAML(typ='safe')
                tree = yaml.load(_f)
                return tree
        except FileNotFoundError:
            logging.error("Configuration file not found!!!")
            sys.exit("ERROR: Configuration file not found!!!")
    
    def getLoRaModule(self):
        """Get LoRa module type.
        
        Parameters:
            None

        Returns:
            str: LoRa module type.
        """
        return self.loraModule


    def getSerialPort(self):
        """Get serial port path.
        
        Parameters:
            None

        Returns:
            str: Serial port path.
        """
        return str(self.serialPort)
    
    
    def getSerialBaudrate(self):
        """Get serial baudrate.
        
        Parameters:
            None

        Returns:
            int: Serial baudrate.
        """
        return self.serialBaudrate
    

    def getDebugLevel(self):
        """Get debug level.
        
        Parameters:
            None
        
        Returns:
            int: Debug level.
        """
        return self.debugLevel
    
    
    def getLoRaBaseBand(self):
        """Get LoRa base band.
        
        Parameters:
            None
        
        Returns:
            str: LoRa base band.
        """
        return self.loraBaseBand

    
    def getLoRaSubBand(self):
        """Get LoRa sub band.
        
        Parameters:
            None

        Returns:
            str: LoRa sub band.
        """
        return self.loraSubBand
    
    
    def getLoRaClass(self):
        """Get LoRa class.
        
        Parameters:
            None
        
        Returns:
            str: LoRa class.
        """
        return self.loraClass

    
    def getLoRaRXWin2Freq(self):
        """Get LoRa RX window 2 frequency.
        
        Parameters:
            None
        
        Returns:
            int: LoRa RX window 2 frequency.
        """
        return self.loraRXWin2Freq
    
    
    def getLoRaRXWin2DR(self):
        """Get LoRa RX window 2 data rate.
        
        Parameters:
            None

        Returns:
            int: LoRa RX window 2 data rate.
        """
        return self.loraRXWin2DR

    
    def getLoRaAuthMode(self):
        """Get LoRa authentication mode.
        
        Parameters:
            None
        
        Returns:
            str: LoRa authentication mode.
        """
        return self.loraAuthMode


    def getProjectConfig(self, projectName):
        """Get project configuration.

        Parameters:
            projectName (str): Project name.
        
        Returns:
            dict: Project configuration.   
        """
        projectConfig = {            
            "sampling_period": self.tree[projectName]["sampling_period"],
            "sensor_list": self.tree[projectName]["sensor_list"],
            "dev_eui": self.tree[projectName]["ttn"]["dev_eui"],
            "app_eui": self.tree[projectName]["ttn"]["app_eui"],
            "app_key": self.tree[projectName]["ttn"]["app_key"],
            "apps_key": self.tree[projectName]["ttn"]["apps_key"],
            "nwks_key": self.tree[projectName]["ttn"]["nwks_key"],
            "dev_addr": self.tree[projectName]["ttn"]["dev_addr"],            
            "tx_power": self.tree[projectName]["lora"]["tx_power"],
            "uplink_dr": self.tree[projectName]["lora"]["uplink_dr"],
            "chan0_freq": self.tree[projectName]["lora"]["chan0_freq"],
            "chan0_dr": self.tree[projectName]["lora"]["chan0_dr"],
            "chan1_freq": self.tree[projectName]["lora"]["chan1_freq"],
            "chan1_dr": self.tree[projectName]["lora"]["chan1_dr"],            
            "adr": self.tree[projectName]["lora"]["adr"],            
            "repeat": self.tree[projectName]["lora"]["repeat"],
            "retry": self.tree[projectName]["lora"]["retry"],
            "initial_port": self.tree[projectName]["lora"]["initial_port"]
        }        
        for id in self.tree[projectName]["sensor_list"]:
            projectConfig[id] = {                
                "data_type": self.tree[projectName][id]["data_type"],
                "min_value": self.tree[projectName][id]["min_value"],
                "max_value": self.tree[projectName][id]["max_value"]                
            }                    
        return projectConfig