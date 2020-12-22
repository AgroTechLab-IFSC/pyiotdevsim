import sys
import logging
from ruamel.yaml import YAML

class Config:
    def __init__(self, _cfgFile):
        self.configFile = _cfgFile
        self.tree = self._readConfigFile()

        # Getting PROJECTS information
        logging.debug("Getting 'projects' key information")
        if "projects" not in self.tree:
            logging.error("Not 'projects' key found on configuration file")
            sys.exit("ERROR: Not 'projects' key found on configuration file!!!")
        self.projects = self.tree["projects"]
        logging.info("%s project(s) found: %s", len(self.projects), self.projects)

        # Getting LoRa information
        logging.debug("Getting 'lora' key information")
        if "lora" not in self.tree:
            logging.error("Not 'lora' key found on configuration file")
            sys.exit("ERROR: Not 'lora' key found on configuration file!!!")
        self.configLoRa = self._loadLoRaConfig()
        
        # Getting SERIAL information
        logging.debug("Getting 'serial' key information")
        if "serial" not in self.tree:
            logging.error("Not 'serial' key found on configuration file")
            sys.exit("ERROR: Not 'serial' key found on configuration file!!!")
        self.serialPort = self.tree["serial"]["port"]
        self.serialBaudrate = self.tree["serial"]["baudrate"]

    def _readConfigFile(self):
        try:
            with open(self.configFile, 'r') as _f:
                yaml = YAML(typ='safe')
                tree = yaml.load(_f)
                return tree
        except FileNotFoundError:
            logging.error("Configuration file not found!!!")
            sys.exit("ERROR: Configuration file not found!!!")
    
    def _loadLoRaConfig(self):
        # Get LoRa configuration parameters from file
        _loraCfg = {
            "base_band": self.tree["lora"]["base_band"],
            "lora_class": self.tree["lora"]["class"],
            "tx_power": self.tree["lora"]["tx_power"],
            "uplink_dr": self.tree["lora"]["uplink_dr"],
            "chan0_freq": self.tree["lora"]["chan0_freq"],
            "chan0_dr": self.tree["lora"]["chan0_dr"],
            "chan1_freq": self.tree["lora"]["chan1_freq"],
            "chan1_dr": self.tree["lora"]["chan1_dr"],
            "rxwin2_freq": self.tree["lora"]["rxwin2_freq"],
            "rxwin2_dr": self.tree["lora"]["rxwin2_dr"],
            "adr": self.tree["lora"]["adr"],
            "auth_mode": self.tree["lora"]["auth_mode"],
            "repeat": self.tree["lora"]["repeat"],
            "retry": self.tree["lora"]["retry"]
        }       
        return _loraCfg    

    def getLoRaConfig(self):
        return self.configLoRa
    
    def getSerialPort(self):
        return str(self.serialPort)
    
    def getSerialBaudrate(self):
        return self.serialBaudrate
    
    def getProjectConfig(self, _projectName):
        projectConfig = {
            "dev_eui": self.tree[_projectName]["dev_eui"],
            "app_eui": self.tree[_projectName]["app_eui"],
            "app_key": self.tree[_projectName]["app_key"],
            "apps_key": self.tree[_projectName]["apps_key"],
            "nwks_key": self.tree[_projectName]["nwks_key"],
            "dev_addr": self.tree[_projectName]["dev_addr"],
            "sampling_period": self.tree[_projectName]["sampling_period"],
            "sensor_list": self.tree[_projectName]["sensor_list"]                    
        }        
        for id in self.tree[_projectName]["sensor_list"]:
            projectConfig[id] = {                
                "data_type": self.tree[_projectName][id]["data_type"],
                "min_value": self.tree[_projectName][id]["min_value"],
                "max_value": self.tree[_projectName][id]["max_value"]                
            }                    
        return projectConfig