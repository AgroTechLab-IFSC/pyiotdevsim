## @mainpage
#  pyIoTDevSim is a IoT device simulator. It uses a real LoRa interface (connected to serial port) to sent simulated
#  IoT data to Thingsboard server throw TTN infrastructure.<br>
# ![SCHEME schematic connection](../figs/scheme.png)<br>
# 
#  The following LoRa interfaces are supported:
#   - <b>\subpage rhf76_052</b>
# 
#  <br><br>
#  <b>AgroTechLab (<i>Laboratory for the Development of Technologies for Agrobusiness</i>)</b><br>
#  <b>IFSC (<i>Instituto Federal de Santa Catarina</i>)</b><br>
#  Rua Heitor Vila Lobos, 222 - São Francisco<br>
#  Lages/SC - Brazil<br>
#  CEP: 88.506-400

## \page rhf76_052 RHF76-052
#  RisingHF LoRaWAN module based on RHF76-052AM chip. It is a low power，low cost and small size module embedded with LoRa® chip SX1276 
# of Semtech, and ultra-low power MCU STM32L051/052xx of ST. The application of LoraWAN® module is targeted at wireless sensor network，
# AMR and others IoT devices powered by battery which need low power consumption to extend the battery life.<br>
# RHF76-052AM key features are listed below, details can be found into [datasheet](../datasheets/rhf76052_datasheet.pdf):
#  - Supply voltage: 3.3V; 
#  - Operating voltage: 3.3V;
#  - Low power consumption: 1.45uA sleep current in WOR mode;
#  - Dual band design:
#   - Low frequency band: 434MHz/470MHz;
#   - High frequency band: 868MHz/915MHz;
#  - User-friendly interface: 
#   - AT commands (documentations [here](../datasheets/ATCommands_v31.pdf) and [here](../datasheets/ATCommands_v42.pdf));
#   - SPI/USART/I2C/USB, 2 × ADC，10 × GPIOs;
#  - Support LoRaWAN® protocol;
#  
#  ![PROMINI schematic connection](../figs/rhf76052_pinout.png)

## @file pyiotdevsim.py
#  @author Robson Costa (robson.costa@ifsc.edu.br)
#  @brief Project main file.
#  @version 1.0.0
#  @since 2020-11-16 
#  @date 2020-11-16

#  @copyright Copyright (c) 2020 - AgroTechLab. \n
#  Licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License (the <em>"License"</em>). You may not
#  use this file except in compliance with the License. You may obtain a copy of the License <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode" target="_blank">here</a>.
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an <em>"as is" basis, 
#  without warranties or  conditions of any kind</em>, either express or implied. See the License for the specific language governing permissions 
#  and limitations under the License.

import sys
import logging
logging.basicConfig(filename="pyIoTDevSim.log", format='%(asctime)s %(levelname)s - %(message)s', level=logging.DEBUG)
import serial
import config
import lora
import project
import time
import threading

# SYSTEM INFORMATION
pyLoRa_version = "1.0.0"
pyLoRa_configFile = 'pyIoTDevSim.yml'

def main():
    print("Starting pyLoRa", pyLoRa_version)
    logging.info("Starting pyLoRa %s", pyLoRa_version)    
    logging.info("Opening configuration file %s", pyLoRa_configFile)
    print("\tReading configuration file... ", end='')
    cfgObj = config.Config(pyLoRa_configFile)    
    print("[OK]")
    print("\t\t{:d} project(s) found: {}".format(len(cfgObj.projects), cfgObj.projects))

    # Open a serial port to communicate with LoRa module
    logging.info("Opening serial port at %s with baudrate %s",cfgObj.getSerialPort(), cfgObj.getSerialBaudrate())    
    serialPort = serial.Serial(cfgObj.getSerialPort(), cfgObj.getSerialBaudrate())

    # Create LoRa communication object and setup basic settings
    loraObj = lora.LoRa(cfgObj.getLoRaConfig(), serialPort)
    print("\tChecking LoRa module... ", end='')
    if loraObj.checkLoRa() is True:
        print("[OK]")
        print("\tConfiguring LoRa basics settings... ", end='')
        loraObj.setupLoRa()
        print("[OK]")
    else:
        sys.exit("[ERROR]\n\t\tLoRa module not connected!!!")
    
    # Create project(s) objects in thread format and start
    print("\tCreating and launching projects threads...")
    projVect = []
    i = 0
    for id in cfgObj.projects:
        projVect.append(project.Project(id, cfgObj.getProjectConfig(id), loraObj))
        projVect[i].start()
        i += 1    
                
if __name__ == "__main__":    
    main()