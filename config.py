import sys
import logging
from ruamel.yaml import YAML

class Config:
    def __init__(self, _cfgFile):
        self.configFile = _cfgFile
        self.tree = self._readConfigFile()

        # Getting SYSTEM session
        logging.debug("Getting 'system' key information")
        if "system" not in self.tree:
            logging.error("Not 'system' key found on configuration file")
            sys.exit("ERROR: Not 'system' key found on configuration file!!!")            
            if "serial" not in self.tree:
                logging.error("Not 'serial' key found on configuration file")
                sys.exit("ERROR: Not 'serial' key found on configuration file!!!")
        self.debugLevel = self.tree["system"]["debug_level"]
        self.loraModule = self.tree["system"]["lora_module"]
        self.serialPort = self.tree["system"]["serial"]["port"]
        self.serialBaudrate = self.tree["system"]["serial"]["baudrate"]
        self.loraBaseBand = self.tree["system"]["lora"]["base_band"]
        self.loraSubBand = self.tree["system"]["lora"]["sub_band"]
        self.loraClass = self.tree["system"]["lora"]["class"]
        self.loraRXWin2Freq = self.tree["system"]["lora"]["rxwin2_freq"]
        self.loraRXWin2DR = self.tree["system"]["lora"]["rxwin2_dr"]
        self.loraAuthMode = self.tree["system"]["lora"]["auth_mode"]

        # Getting PROJECTS session
        logging.debug("Getting 'projects' key information")
        if "projects" not in self.tree:
            logging.error("Not 'projects' key found on configuration file")
            sys.exit("ERROR: Not 'projects' key found on configuration file!!!")
        self.projects = self.tree["projects"]
        logging.info("%s project(s) found: %s", len(self.projects), self.projects)        

    def _readConfigFile(self):
        try:
            with open(self.configFile, 'r') as _f:
                yaml = YAML(typ='safe')
                tree = yaml.load(_f)
                return tree
        except FileNotFoundError:
            logging.error("Configuration file not found!!!")
            sys.exit("ERROR: Configuration file not found!!!")
    
    def getLoRaModule(self):
        return self.loraModule

    def getSerialPort(self):
        return str(self.serialPort)
    
    def getSerialBaudrate(self):
        return self.serialBaudrate
    
    def getDebugLevel(self):
        return self.debugLevel
    
    def getLoRaBaseBand(self):
        return self.loraBaseBand

    def getLoRaSubBand(self):
        return self.loraSubBand
    
    def getLoRaClass(self):
        return self.loraClass

    def getLoRaRXWin2Freq(self):
        return self.loraRXWin2Freq
    
    def getLoRaRXWin2DR(self):
        return self.loraRXWin2DR

    def getLoRaAuthMode(self):
        return self.loraAuthMode

    def getProjectConfig(self, _projectName):
        projectConfig = {            
            "sampling_period": self.tree[_projectName]["sampling_period"],
            "sensor_list": self.tree[_projectName]["sensor_list"],
            "dev_eui": self.tree[_projectName]["ttn"]["dev_eui"],
            "app_eui": self.tree[_projectName]["ttn"]["app_eui"],
            "app_key": self.tree[_projectName]["ttn"]["app_key"],
            "apps_key": self.tree[_projectName]["ttn"]["apps_key"],
            "nwks_key": self.tree[_projectName]["ttn"]["nwks_key"],
            "dev_addr": self.tree[_projectName]["ttn"]["dev_addr"],            
            "tx_power": self.tree[_projectName]["lora"]["tx_power"],
            "uplink_dr": self.tree[_projectName]["lora"]["uplink_dr"],
            "chan0_freq": self.tree[_projectName]["lora"]["chan0_freq"],
            "chan0_dr": self.tree[_projectName]["lora"]["chan0_dr"],
            "chan1_freq": self.tree[_projectName]["lora"]["chan1_freq"],
            "chan1_dr": self.tree[_projectName]["lora"]["chan1_dr"],            
            "adr": self.tree[_projectName]["lora"]["adr"],            
            "repeat": self.tree[_projectName]["lora"]["repeat"],
            "retry": self.tree[_projectName]["lora"]["retry"],
            "initial_port": self.tree[_projectName]["lora"]["initial_port"]
        }        
        for id in self.tree[_projectName]["sensor_list"]:
            projectConfig[id] = {                
                "data_type": self.tree[_projectName][id]["data_type"],
                "min_value": self.tree[_projectName][id]["min_value"],
                "max_value": self.tree[_projectName][id]["max_value"]                
            }                    
        return projectConfig