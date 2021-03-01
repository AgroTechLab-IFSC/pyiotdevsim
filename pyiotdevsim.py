## @mainpage
#  pyIoTDevSim is a IoT device simulator that uses a real LoRaWAN&reg; module (connected to serial port) to sent simulated
#  IoT data to TTN&reg; (<a href="https://www.thethingsnetwork.org" target="_blank">The Things Network</a>) infrastructure.<br>
# ![SCHEME schematic connection](../figs/scheme.png)<br>
# 
#  A complete features list is found @subpage feature_list "here" and the configuration file it is detailed @subpage config_file "here".<br>
#  The following LoRaWAN modules are supported:
#   - <b>@subpage rhf76_052</b> (since v0.1.0)
#   - <b>@subpage rhf0m003</b> (since v0.2.0)
# 
#  <br><br>
#  <b>AgroTechLab (<i>Laboratório de Desenvolvimento de Tecnologias para o Agronegócio</i>)</b><br>
#  <b>IFSC (<i>Instituto Federal de Santa Catarina</i>)</b><br>
#  Rua Heitor Vila Lobos, 222 - São Francisco<br>
#  Lages/SC - Brazil<br>
#  CEP: 88.506-400<br>
#  <table style="width:100%">
#   <tr>
#       <td><a href="https://agrotechlab.lages.ifsc.edu.br/"><img src="../figs/agrotechlab_logo.png" alt="AgroTechLab"></a></td>
#       <td><a href="https://www.thethingsnetwork.org/community/lages/"><img src="../figs/ttn_lages.png" alt="TTN/Lages"></a></td>
#       <td><a href="https://www.ifsc.edu.br/web/campus-lages"><img src="../figs/ifsc_logo.png" alt="IFSC/Lages"></a></td>
#   </tr>

## @page feature_list Features list
# <b>Version 0.2.0 (26/02/2021):</b>
#   - Added RHF0M003 module compatibility;
#   - Moved LoRa session to Project session as a subsession (like TTN);
#   - Included sub-band parameter;
#   - Change module configuration (disable all channels of sub-bands not used);
# 
# <b>Version 0.1.0 (16/11/2020):</b>
#   - Added RHF72-056 module compatibility;
#   - Multiproject capability (one thread by project);
#   - Configuration by YAML file;
#     - Project session (with TTN subsession);
#     - LoRa session;
#     - Serial session;
#   - Payload sent using HEX format;
#   - Data types:
#     - UINT8;
#     - UINT16;
#     - FLOAT_UINT16;
#     - FLOAT_COMPRESSED;
#     - FLOAT32;
#   - LOG generation;
# 
#  <br><br>
#  <b>AgroTechLab (<i>Laboratório de Desenvolvimento de Tecnologias para o Agronegócio</i>)</b><br>
#  <b>IFSC (<i>Instituto Federal de Santa Catarina</i>)</b><br>
#  Rua Heitor Vila Lobos, 222 - São Francisco<br>
#  Lages/SC - Brazil<br>
#  CEP: 88.506-400<br>
#  <table style="width:100%">
#   <tr>
#       <td><a href="https://agrotechlab.lages.ifsc.edu.br/"><img src="../figs/agrotechlab_logo.png" alt="AgroTechLab"></a></td>
#       <td><a href="https://www.thethingsnetwork.org/community/lages/"><img src="../figs/ttn_lages.png" alt="TTN/Lages"></a></td>
#       <td><a href="https://www.ifsc.edu.br/web/campus-lages"><img src="../figs/ifsc_logo.png" alt="IFSC/Lages"></a></td>
#   </tr>

## @page config_file Configuration file details
# The pyIoTDevSim uses a YAML format configuration file.
#   - Added RHF0M003 module compatibility;
#   - Moved LoRa session to Project session as a subsession (like TTN);
#   - Included sub-band parameter;
#   - Change module configuration (disable all channels of sub-bands not used);
# 
# <b>Version 0.1.0 (16/11/2020):</b>
#   - Added RHF72-056 module compatibility;
#   - Multiproject capability (one thread by project);
#   - Configuration by YAML file;
#     - Project session (with TTN subsession);
#     - LoRa session;
#     - Serial session;
#   - Payload sent using HEX format;
#   - Data types:
#     - UINT8;
#     - UINT16;
#     - FLOAT_UINT16;
#     - FLOAT_COMPRESSED;
#     - FLOAT32;
#   - LOG generation;
# 
#  <br><br>
#  <b>AgroTechLab (<i>Laboratório de Desenvolvimento de Tecnologias para o Agronegócio</i>)</b><br>
#  <b>IFSC (<i>Instituto Federal de Santa Catarina</i>)</b><br>
#  Rua Heitor Vila Lobos, 222 - São Francisco<br>
#  Lages/SC - Brazil<br>
#  CEP: 88.506-400<br>
#  <table style="width:100%">
#   <tr>
#       <td><a href="https://agrotechlab.lages.ifsc.edu.br/"><img src="../figs/agrotechlab_logo.png" alt="AgroTechLab"></a></td>
#       <td><a href="https://www.thethingsnetwork.org/community/lages/"><img src="../figs/ttn_lages.png" alt="TTN/Lages"></a></td>
#       <td><a href="https://www.ifsc.edu.br/web/campus-lages"><img src="../figs/ifsc_logo.png" alt="IFSC/Lages"></a></td>
#   </tr>

## @page rhf76_052 RHF76-052
# RisingHF LoRaWAN module based on RHF76-052AM chip. It is a low power，low cost and small size module embedded with LoRa® chip SX1276 
# of Semtech, and ultra-low power MCU STM32L051/052xx of ST. The application of LoraWAN® module is targeted at wireless sensor network，
# AMR and others IoT devices powered by battery which need low power consumption to extend the battery life.<br>
# RHF76-052AM key features are listed below, details can be found into [datasheet](../datasheets/rhf76052_datasheet.pdf):
#  - Supply voltage: 3.3V; 
#  - Operating voltage: 3.3V;
#  - Low power consumption: 1.45uA sleep current in WOR mode;
#  - Dual band design:
#   - Low frequency band: 20 dBm @ 434MHz/470MHz;
#   - High frequency band: 14 dBm @ 868MHz/915MHz;
#  - User-friendly interface: 
#   - AT commands (documentations [here](../datasheets/ATCommands_v31.pdf) and [here](../datasheets/ATCommands_v42.pdf));
#   - SPI/USART/I2C/USB, 2 × ADC，10 × GPIOs;
#  - Support LoRaWAN® protocol;
# 
#  ![PROMINI schematic connection](../figs/rhf76052_pinout.png)
# 
#  <br><br>
#  <b>AgroTechLab (<i>Laboratório de Desenvolvimento de Tecnologias para o Agronegócio</i>)</b><br>
#  <b>IFSC (<i>Instituto Federal de Santa Catarina</i>)</b><br>
#  Rua Heitor Vila Lobos, 222 - São Francisco<br>
#  Lages/SC - Brazil<br>
#  CEP: 88.506-400<br>
#  <table style="width:100%">
#   <tr>
#       <td><a href="https://agrotechlab.lages.ifsc.edu.br/"><img src="../figs/agrotechlab_logo.png" alt="AgroTechLab"></a></td>
#       <td><a href="https://www.thethingsnetwork.org/community/lages/"><img src="../figs/ttn_lages.png" alt="TTN/Lages"></a></td>
#       <td><a href="https://www.ifsc.edu.br/web/campus-lages"><img src="../figs/ifsc_logo.png" alt="IFSC/Lages"></a></td>
#   </tr>

## @page rhf0m003 RHF0M003
#  RisingHF LoRaWAN module based on RHF0M003-HF20 chip. It is a low power，low cost and small size module embedded with LoRa® chip SX1276 
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
#  ![PROMINI schematic connection](../figs/rhf76052_pinout.png)
#  <br><br>
#  <b>AgroTechLab (<i>Laboratório de Desenvolvimento de Tecnologias para o Agronegócio</i>)</b><br>
#  <b>IFSC (<i>Instituto Federal de Santa Catarina</i>)</b><br>
#  Rua Heitor Vila Lobos, 222 - São Francisco<br>
#  Lages/SC - Brazil<br>
#  CEP: 88.506-400<br>
#  <table style="width:100%">
#   <tr>
#       <td><a href="https://agrotechlab.lages.ifsc.edu.br/"><img src="../figs/agrotechlab_logo.png" alt="AgroTechLab"></a></td>
#       <td><a href="https://www.thethingsnetwork.org/community/lages/"><img src="../figs/ttn_lages.png" alt="TTN/Lages"></a></td>
#       <td><a href="https://www.ifsc.edu.br/web/campus-lages"><img src="../figs/ifsc_logo.png" alt="IFSC/Lages"></a></td>
#   </tr>

## @file pyiotdevsim.py
#  @author Robson Costa (<mailto:robson.costa@ifsc.edu.br>)
#  @brief Project main file.
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
logging.basicConfig(filename="pyIoTDevSim.log", format='%(asctime)s %(levelname)s - %(message)s', level=logging.DEBUG)
import serial
import config
import lora
import project
import time
import threading

# SYSTEM INFORMATION
VERSION = "0.2.0"
CONFIG_FILE = 'pyIoTDevSim.yml'

def main():
    print("Starting pyLoRa", VERSION)
    logging.info("Starting pyLoRa %s", VERSION)    
    logging.info("Reading configuration file %s", CONFIG_FILE)
    print("\tReading configuration file... ", end='')
    cfgObj = config.Config(CONFIG_FILE)    
    print("[OK]")
    print("\t\t{:d} project(s) found: {}".format(len(cfgObj.projects), cfgObj.projects))

    # # Open a serial port to communicate with LoRa module
    logging.info("Opening serial port at %s with baudrate %s",cfgObj.getSerialPort(), cfgObj.getSerialBaudrate())    
    serialPortObj = serial.Serial(cfgObj.getSerialPort(), cfgObj.getSerialBaudrate())

    # Create LoRa communication object
    loraObj = lora.LoRa(cfgObj.getLoRaModule(), serialPortObj)    
    print("\tChecking LoRa module... ", end='')
    if loraObj.checkLoRa() is True:
        print("[OK]")    
    else:
        sys.exit("[ERROR]\n\t\tLoRa module not connected!!!")
    
    # Configuring LoRa common parameters
    loraObj.setLoRaBaseBand(cfgObj.getLoRaBaseBand())
    loraObj.setLoRaSubBand(cfgObj.getLoRaSubBand())
    loraObj.setLoRaClass(cfgObj.getLoRaClass())
    loraObj.setLoRaRX1Win()    
    loraObj.setLoRaRX2Win(cfgObj.getLoRaRXWin2Freq(), cfgObj.getLoRaRXWin2DR())
    loraObj.setLoRaAuthMode(cfgObj.getLoRaAuthMode())    

    # Create project(s) objects in thread format and start
    print("\tCreating and launching project(s) thread(s)...")
    projVect = []
    i = 0
    for id in cfgObj.projects:
        projVect.append(project.Project(id, cfgObj.getProjectConfig(id), loraObj, cfgObj.getLoRaBaseBand(), cfgObj.getLoRaAuthMode()))
        projVect[i].start()
        i += 1    
                
if __name__ == "__main__":    
    main()