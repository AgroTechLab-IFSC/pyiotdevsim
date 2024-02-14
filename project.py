## @file project.py
#  @author Robson Costa (<mailto:robson.costa@ifsc.edu.br>)
#  @brief Project class.
#  @version 0.2.0
#  @since 2020/11/16
#  @date 2024/02/14
#  @copyright Copyright &copy; since 2020 <a href="https://agrotechlab.lages.ifsc.edu.br" target="_blank">AgroTechLab</a>.\n
#  ![LICENSE license](../figs/license.png)<br>
#  Licensed under the CC BY-NC-SA (<i>Creative Commons Attribution-NonCommercial-ShareAlike</i>) 4.0 International Unported License (the <em>"License"</em>). You may not
#  use this file except in compliance with the License. You may obtain a copy of the License <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode" target="_blank">here</a>.
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an <em>"as is" basis, 
#  without warranties or  conditions of any kind</em>, either express or implied. See the License for the specific language governing permissions 
#  and limitations under the License.
import threading
import logging
import time
import random
import numpy as np
import struct
import binascii

class Project(threading.Thread):
    """! The Project class.
    Manages the project operations. It's created a thread to each project configured.
    """

    def __init__(self, name, cfg, loraObj, loraBaseBand, loraAuthMode):
        """! The class constructor.
        @param name The project name.
        @param cfg The project configuration.
        @param loraObj The LoRa object.
        @param loraBaseBand The LoRa base-band.
        @param loraAuthMode The LoRa authentication mode.
        @return An instance of the Project class.
        """  
        threading.Thread.__init__(self)        
        
        ## Projec name
        self.name = name

        ## Projec configuration
        self.config = cfg

        ## LoRa object
        self.lora = loraObj

        ## LoRa base band
        self.baseBand = loraBaseBand  

        ## LoRa authentication mode
        self.authMode = loraAuthMode      

    def run(self):
        """! The run method.        
        """  
        # Waits for a random time to unsynchronize the threads
        time.sleep(random.randint(5,10))

        # Start thread
        logging.info("Starting %s project thread", self.name)
        print("\t\tStarting {} project thread".format(self.name))                
        
        # Process looping
        joined = False
        while True:            
            # Lock LoRa object
            self.lora.lock.acquire()
            logging.info("Running %s project thread", self.name)
            
            # Configure TTN project parameters
            self.lora.setDevEUI(self.config.get("dev_eui"))
            self.lora.setAppEUI(self.config.get("app_eui"))            
            if self.authMode == "LWABP":
                self.lora.setDevAddr(self.config.get("dev_addr"))
                self.lora.setNwkSKey(self.config.get("nwks_key"))
                self.lora.setAppSKey(self.config.get("apps_key"))
            elif self.authMode == "LWOTAA":
                self.lora.setAppKey(self.config.get("app_key"))
                if joined == False:
                    while self.lora.sendJoinRequest() == False:
                        pass
                    joined = True
            
            # Configure LoRa project parameters                        
            self.lora.setLoRaTXPower(self.config.get("tx_power"))
            self.lora.setLoRaUPDatarate(self.config.get("uplink_dr"))
            self.lora.setLoRaADR(self.config.get("adr"))                                

            # Create a list of messages payloads
            tx_queue = []
            payload = ""
            count = 0
            for id in self.config.get("sensor_list"):
                # Define the data size             
                if self.config[id]["data_type"] == "uint8":
                    size = 1
                elif self.config[id]["data_type"] == "uint16" or self.config[id]["data_type"] == "float_uint16":
                    size = 2
                elif self.config[id]["data_type"] == "float32_compressed":
                    size = 3
                elif self.config[id]["data_type"] == "float32":
                    size = 4

                # Check if data is putted into the same message or a new is created
                if (count + size <= self.lora.getLoRaMaxPayload(self.baseBand, self.config.get("uplink_dr"))):
                    count += size
                else:                    
                    tx_queue.append(payload)
                    payload = ""
                    count = size
                
                if self.config[id]["data_type"] == "uint8":
                    value = random.randint(self.config[id]["min_value"], self.config[id]["max_value"])                    
                    payload += "{:02x}".format(value)
                    # print("Value {:d} = {:02x}".format(value, value))
                elif self.config[id]["data_type"] == "uint16":
                    value = random.randint(self.config[id]["min_value"], self.config[id]["max_value"])                    
                    payload += "{:04x}".format(value)
                    # print("Value {:d} = {:04x}".format(value, value))   
                elif self.config[id]["data_type"] == "float_uint16":
                    valueb = round(random.uniform(self.config[id]["min_value"], self.config[id]["max_value"]), 2)
                    value = int(valueb * 100)
                    payload += "{:04x}".format(value)
                    # print("Value {} -> {:d} = {:04x}".format(valueb, value, value))                
                elif self.config[id]["data_type"] == "float32_compressed":
                    # Generates random value between [min_value] and [max_value]
                    valueb = round(random.uniform(self.config[id]["min_value"], self.config[id]["max_value"]), 2)

                    # Check if it is positive or negative
                    if valueb >= 0:
                        payload += "AA"
                        # From 0 to 655.35
                        value = int(valueb * 100)
                    else:
                        payload += "AF"
                        # From 0 to 655.35 and convert to positive
                        value = int(valueb * -100)
                    payload += "{:04x}".format(value)
                    # print("Value {} -> {} = {:04x}".format(valueb, value, value))
                elif self.config[id]["data_type"] == "float32":
                    # Generates random value between [min_value] and [max_value]
                    value = round(random.uniform(self.config[id]["min_value"], self.config[id]["max_value"]), 6)
                    # Convert float64 of Python to float32
                    value = np.float32(value)                                                              
                    payload += str(binascii.hexlify(struct.pack('<f', value)), "UTF-8")                                          

            # Put the last payload into the message queue            
            tx_queue.append(payload)
            logging.debug("%s message(s) putted into the transmission queue", len(tx_queue))    

            # Sent messages putted into the queue
            port = self.config.get("initial_port")
            for msg in tx_queue:                
                self.lora.sendNoAckMsgHex(port, msg)
                # self.lora.sendAckMsgHex(port, msg)
                port += 1

            # Release LoRa object
            self.lora.lock.release()

            # Awaits the sampling period
            time.sleep(self.config.get("sampling_period"))            
    
    