## @file config.py
#  @author Robson Costa (<mailto:robson.costa@ifsc.edu.br>)
#  @brief Config class.
#  @version 0.2.0
#  @since 16/11/2020
#  @date 01/03/2021
#  @copyright Copyright &copy; 2020 - 2021 <a href="https://agrotechlab.lages.ifsc.edu.br" target="_blank">AgroTechLab</a>.\n
#  ![LICENSE license](../figs/license.png)<br>
#  Licensed under the CC BY-NC-SA (<i>Creative Commons Attribution-NonCommercial-ShareAlike</i>) 4.0 International Unported License (the <em>"License"</em>). You may not
#  use this file except in compliance with the License. You may obtain a copy of the License <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode" target="_blank">here</a>.
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an <em>"as is" basis, 
#  without warranties or  conditions of any kind</em>, either express or implied. See the License for the specific language governing permissions 
#  and limitations under the License.
import sys
import logging
from ruamel.yaml import YAML

class Config:
    """! The Config class.
    Get and validate configuration parameters from a configuration file based on YAML.
    """
    def __init__(self, _cfgFile):
        """! The Config class initializer.
        @param _cfgFile Configuration file path.
        @return  An instance of the Config class initialized based on a specified configuration file.
        """                
        
        ## Configuration file
        self.configFile = _cfgFile

        ## A tree with configuration project
        self.tree = self._readConfigFile()

        # Getting SYSTEM session
        logging.debug("Getting 'system' key information")
        if "system" not in self.tree:
            logging.error("Not 'system' key found on configuration file")
            sys.exit("ERROR: Not 'system' key found on configuration file!!!")            
            if "serial" not in self.tree:
                logging.error("Not 'serial' key found on configuration file")
                sys.exit("ERROR: Not 'serial' key found on configuration file!!!")
        ## Debug level
        self.debugLevel = self.tree["system"]["debug_level"]

        ## LoRa module type
        self.loraModule = self.tree["system"]["lora_module"]

        ## Serial port path
        self.serialPort = self.tree["system"]["serial"]["port"]

        ## Serial baudrate
        self.serialBaudrate = self.tree["system"]["serial"]["baudrate"]

        ## LoRa base band
        self.loraBaseBand = self.tree["system"]["lora"]["base_band"]

        ## LoRa sub band
        self.loraSubBand = self.tree["system"]["lora"]["sub_band"]

        ## LoRa class
        self.loraClass = self.tree["system"]["lora"]["class"]

        ## LoRa RX window 2 frequency
        self.loraRXWin2Freq = self.tree["system"]["lora"]["rxwin2_freq"]

        ## LoRa RX window 2 data rate
        self.loraRXWin2DR = self.tree["system"]["lora"]["rxwin2_dr"]

        ## LoRa authentication mode
        self.loraAuthMode = self.tree["system"]["lora"]["auth_mode"]

        # Getting PROJECTS session
        logging.debug("Getting 'projects' key information")
        if "projects" not in self.tree:
            logging.error("Not 'projects' key found on configuration file")
            sys.exit("ERROR: Not 'projects' key found on configuration file!!!")
        ## Projects list
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
    
    ## @fn getLoRaModule
    #  @brief Return the LoRa module type.
    #  @return LoRa module type. 
    def getLoRaModule(self):
        return self.loraModule

    ## @fn getSerialPort
    #  @brief Return the serial port path.
    #  @return Serial port path.
    def getSerialPort(self):
        return str(self.serialPort)
    
    ## @fn getSerialBaudrate
    #  @brief Return the serial baudrate.
    #  @return Serial baudrate.
    def getSerialBaudrate(self):
        return self.serialBaudrate
    
    ## @fn getDebugLevel
    #  @brief Return the debug level.
    #  @return Debug level.
    def getDebugLevel(self):
        return self.debugLevel
    
    ## @fn getLoRaBaseBand
    #  @brief Return LoRa base band.
    #  @return LoRa base band.
    def getLoRaBaseBand(self):
        return self.loraBaseBand

    ## @fn getLoRaSubBand
    #  @brief Return LoRa sub band.
    #  @return LoRa sub band.
    def getLoRaSubBand(self):
        return self.loraSubBand
    
    ## @fn getLoRaClass
    #  @brief Return LoRa class.
    #  @return LoRa class.
    def getLoRaClass(self):
        return self.loraClass

    ## @fn getLoRaRXWin2Freq
    #  @brief Return LoRa RX window 2 frequency.
    #  @return LoRa RX window 2 frequency.
    def getLoRaRXWin2Freq(self):
        return self.loraRXWin2Freq
    
    ## @fn getLoRaRXWin2DR
    #  @brief Return LoRa RX window 2 data rate.
    #  @return LoRa RX window 2 data rate.
    def getLoRaRXWin2DR(self):
        return self.loraRXWin2DR

    ## @fn getLoRaAuthMode
    #  @brief Return LoRa authentication mode.
    #  @return LoRa authentication mode.
    def getLoRaAuthMode(self):
        return self.loraAuthMode

    def getProjectConfig(self, _projectName):
        """! Get project configuration
        @param _projectName project name
        @return project configuration        
        """
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