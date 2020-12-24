import threading
import logging
import time
import random
import numpy as np
import struct
import binascii

class Project(threading.Thread):

    def __init__(self, name, cfg, loraObj):
        threading.Thread.__init__(self)        
        self.name = name
        self.config = cfg
        self.lora = loraObj        

    def run(self):
        # Waits for a random time to unsynchronize the threads
        time.sleep(random.randint(0,10))

        # Start thread
        logging.info("Starting %s project thread", self.name)
        print("\t\tStarting {} project thread".format(self.name))                
        
        # Process looping
        joined = False
        while True:            
            # Lock LoRa object
            self.lora.lock.acquire()
            logging.info("Running %s project thread", self.name)

            # Configure LoRa/TTN project parameters
            self.lora.setDevEUI(self.config.get("dev_eui"))
            self.lora.setAppEUI(self.config.get("app_eui"))
            if self.lora.auth_mode == "LWABP":
                self.lora.setDevAddr(self.config.get("dev_addr"))
                self.lora.setNwkSKey(self.config.get("nwks_key"))
                self.lora.setAppSKey(self.config.get("apps_key"))
            elif self.lora.auth_mode == "LWOTAA":
                self.lora.setAppKey(self.config.get("app_key"))
                if joined == False:
                    while self.lora.sendJoinRequest() == False:
                        pass
                    joined = True
            
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
                if (count + size <= self.lora.max_payload):
                    count += size
                else:                    
                    tx_queue.append(payload)
                    payload = ""
                    count = size
                
                if self.config[id]["data_type"] == "uint8":
                    value = random.randint(self.config[id]["min_value"], self.config[id]["max_value"])                    
                    payload += "{:02x}".format(value)
                elif self.config[id]["data_type"] == "uint16":
                    value = random.randint(self.config[id]["min_value"], self.config[id]["max_value"])                    
                    payload += "{:04x}".format(value)   
                elif self.config[id]["data_type"] == "float_uint16":
                    value = round(random.uniform(self.config[id]["min_value"], self.config[id]["max_value"]), 2)
                    value = int(value * 100)
                    payload += "{:04x}".format(value)
                elif self.config[id]["data_type"] == "float3_2compressed":
                    # Generates random value between [min_value] and [max_value]
                    value = round(random.uniform(self.config[id]["min_value"], self.config[id]["max_value"]), 2)
                    # Check if it is positive or negative
                    if value >= 0:
                        payload += "AA"
                        # From 0 to 655.35
                        value = int(value * 100)
                    else:
                        payload += "AF"
                        # From 0 to 655.35 and convert to positive
                        value = value * -100                       
                    payload += "{:04x}".format(value)
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
            port = self.lora.initial_port
            for msg in tx_queue:
                # self.lora.sendNoAckMsgHex(port, msg)
                self.lora.sendAckMsgHex(port, msg)
                port += 1

            # Release LoRa object
            self.lora.lock.release()

            # Awaits the sampling period
            time.sleep(self.config.get("sampling_period"))
            # break
    
    