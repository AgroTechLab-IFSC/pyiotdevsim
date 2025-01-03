import threading
import logging
import time
import random
import numpy as np
import struct
import binascii

class Project(threading.Thread):
    """Project class.
    
    Manages the project operations. It's created a thread to each project configured.

    Attributes:
        name (str): The project name.
        config (dict): The project configuration.
        lora (LoRa): The LoRa object.
        baseBand (str): The LoRa base-band.
        authMode (str): The LoRa authentication mode.
    """

    def __init__(self, name, cfg, loraObj, loraBaseBand, loraAuthMode):
        """Project class constructor.
        
        Parameters:
            name (str): The project name.
            cfg (dict): The project configuration.
            loraObj (LoRa): The LoRa object.
            loraBaseBand (str): The LoRa base-band.
            loraAuthMode (str): The LoRa authentication mode.
        """  
        
        threading.Thread.__init__(self)        
        
        # Projec name
        self.name = name

        # Projec configuration
        self.config = cfg

        # LoRa object
        self.lora = loraObj

        # LoRa base band
        self.baseBand = loraBaseBand  

        # LoRa authentication mode
        self.authMode = loraAuthMode      


    def set_bit(self, number, position):
        """Create a mask with a bit setted to 1 at a desired position.
        
        Parameters:
            number (int): The number to set the bit.
            position (int): The bit position to set.

        Returns:
            int: The number with the bit setted.
        """
        
        mask = 1 << position
        result = number | mask

        return result


    def run(self):
        """Run method."""  
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
                if self.config[id]["data_type"] == "int8" or self.config[id]["data_type"] == "uint8":
                    size = 1
                elif self.config[id]["data_type"] == "int16" or self.config[id]["data_type"] == "uint16" or self.config[id]["data_type"] == "float_int15" or self.config[id]["data_type"] == "float_uint16":
                    size = 2
                elif self.config[id]["data_type"] == "int32" or self.config[id]["data_type"] == "uint32" or self.config[id]["data_type"] == "float":
                    size = 4

                # Check if data is putted into the same message or a new is created
                if (count + size <= self.lora.getLoRaMaxPayload(self.baseBand, self.config.get("uplink_dr"))):
                    count += size
                else:                    
                    tx_queue.append(payload)
                    payload = ""
                    count = size
                
                # INT8 (-128 ~ 127)
                # UINT8 (0 ~ 255)
                if self.config[id]["data_type"] == "int8" or self.config[id]["data_type"] == "uint8":
                    min_value = self.config[id]["min_value"]
                    max_value = self.config[id]["max_value"]
                    if self.config[id]["data_type"] == "int8":
                        if min_value < -128:
                            min_value = -128
                        if max_value > 127:
                            max_value = 127
                    if self.config[id]["data_type"] == "uint8":
                        if min_value < 0:
                            min_value = 0
                        if max_value > 255:
                            max_value = 255
                    value = random.randint(min_value, max_value)                    
                    payload += "{:02x}".format(value)
                    # print("Value {:d} = {:02x}".format(value, value))
                
                # INT16 (-32768 ~ 32767)
                # UINT16 (0 ~ 65535)
                elif self.config[id]["data_type"] == "int16" or self.config[id]["data_type"] == "uint16":
                    min_value = self.config[id]["min_value"]
                    max_value = self.config[id]["max_value"]
                    if self.config[id]["data_type"] == "int16":
                        if min_value < -32768:
                            min_value = -32768
                        if max_value > 32767:
                            max_value = 32767
                    if self.config[id]["data_type"] == "uint16":
                        if min_value < 0:
                            min_value = 0
                        if max_value > 65535:
                            max_value = 65535
                    value = random.randint(min_value, max_value)                    
                    payload += "{:04x}".format(value)
                    # print("Value {:d} = {:04x}".format(value, value))   
                
                # INT32 (-2147483648 ~ 2147483647)
                # UINT32 (0 ~ 4294967295)
                elif self.config[id]["data_type"] == "int32" or self.config[id]["data_type"] == "uint32":
                    min_value = self.config[id]["min_value"]
                    max_value = self.config[id]["max_value"]
                    if self.config[id]["data_type"] == "int32":
                        if min_value < -2147483648:
                            min_value = -2147483648
                        if max_value > 2147483647:
                            max_value = 2147483647
                    if self.config[id]["data_type"] == "uint32":
                        if min_value < 0:
                            min_value = 0
                        if max_value > 4294967295:
                            max_value = 4294967295
                    value = random.randint(min_value, max_value)                    
                    payload += "{:08x}".format(value)
                    # print("Value {:d} = {:08x}".format(value, value))

                # FLOAT_INT15 (-327.67 ~ 327.67)
                elif self.config[id]["data_type"] == "float_int15":
                    min_value = self.config[id]["min_value"]
                    max_value = self.config[id]["max_value"]
                    if min_value < -327.67:
                        min_value = -327.67
                    if max_value > 327.67:
                        max_value = 327.67
                    valueb = round(random.uniform(min_value, max_value), 2)
                    if valueb >= 0:
                        value = int(valueb * 100)
                    else:
                        value = int(valueb * -100)
                        value = self.set_bit(value, 15)

                    payload += "{:04x}".format(value)
                    # print("Value {} -> {} = {:04x}".format(valueb, value, value))

                # FLOAT_UINT16 (0 ~ 655.35)
                elif self.config[id]["data_type"] == "float_uint16":
                    min_value = self.config[id]["min_value"]
                    max_value = self.config[id]["max_value"]
                    if min_value < 0:
                        min_value = 0
                    if max_value > 655.35:
                        max_value = 655.35
                    valueb = round(random.uniform(min_value, max_value), 2)
                    value = int(valueb * 100)
                    payload += "{:04x}".format(value)
                    # print("Value {} -> {:d} = {:04x}".format(valueb, value, value))                
                
                elif self.config[id]["data_type"] == "float":
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
    
    