import logging
import threading
import lora_constants
import sys


class LoRa:
    def __init__(self, _loraCfg, _serialPort):
        self.lock = threading.Lock()

        # Get and check LoRa base band
        self.base_band = _loraCfg.get("base_band")
        if self.base_band not in lora_constants.lora_baseband_ref:
            logging.error("Base band parameter in LoRa configuration file is not valid")
            sys.exit("\tERROR: Base band parameter in LoRa configuration file is not valid!!!")

        # Get and check LoRa class
        self.lora_class = _loraCfg.get("lora_class")
        if self.lora_class not in lora_constants.lora_class_ref:
            logging.error("Class parameter in LoRa configuration file is not valid")
            sys.exit("\tERROR: Class parameter in LoRa configuration file is not valid!!!")

        # Get and check LoRa transmission power
        self.tx_power = _loraCfg.get("tx_power")
        if self.base_band == "EU434" or self.base_band == "EU868":
            if self.tx_power not in lora_constants.lora_tx_power_868_ref:
                logging.error("Transmission power parameter in LoRa configuration file is not valid")
                sys.exit("\tERROR: Transmission power parameter in LoRa configuration file is not valid!!!")
        elif self.base_band == "US915" or self.base_band == "AU920":
            if self.tx_power not in lora_constants.lora_tx_power_915_ref:
                logging.error("Transmission power parameter in LoRa configuration file is not valid")
                sys.exit("\tERROR: Transmission power parameter in LoRa configuration file is not valid!!!")

        # Get and check LoRa uplink DR
        self.uplink_dr = _loraCfg.get("uplink_dr")
        if self.base_band == "EU434" or self.base_band == "EU868":
            if self.uplink_dr not in lora_constants.lora_dr_868_ref:
                logging.error("Uplink data rate parameter in LoRa configuration file is not valid")
                sys.exit("\tERROR: Uplink data rate parameter in LoRa configuration file is not valid!!!")
            
            # Define the maximum payload based on DR and base band
            if (self.uplink_dr == "DR0" or self.uplink_dr == "DR1" or self.uplink_dr == "DR2"):
                self.max_payload = 51
            elif (self.uplink_dr == "DR3"):
                self.max_payload = 115
            if (self.uplink_dr == "DR4" or self.uplink_dr == "DR5" or self.uplink_dr == "DR6" or self.uplink_dr == "DR7"):
                self.max_payload = 242                

        if self.base_band == "US915" or self.base_band == "AU920":
            if self.uplink_dr not in lora_constants.lora_dr_915_ref:
                logging.error("Uplink data rate parameter in LoRa configuration file is not valid")
                sys.exit("\tERROR: Uplink data rate parameter in LoRa configuration file is not valid!!!")       

            # Define the maximum payload based on DR and base band
            if (self.uplink_dr == "DR0"):
                self.max_payload = 11
                self.initial_port = 1
            elif (self.uplink_dr == "DR1"):
                self.max_payload = 53
                self.initial_port = 10
            elif (self.uplink_dr == "DR2"):
                self.max_payload = 126
                self.initial_port = 20
            elif (self.uplink_dr == "DR3" or self.uplink_dr == "DR4"):
                self.max_payload = 242
                self.initial_port = 30

        self.chan0_freq = _loraCfg.get("chan0_freq")
        self.chan0_dr = _loraCfg.get("chan0_dr")
        self.chan1_freq = _loraCfg.get("chan1_freq")
        self.chan1_dr = _loraCfg.get("chan1_dr")
        self.rxwin2_freq = _loraCfg.get("rxwin2_freq")
        self.rxwin2_dr = _loraCfg.get("rxwin2_dr")

        # Get and check ADR (Automatic Data Rate)
        self.adr = _loraCfg.get("adr")
        if self.adr not in lora_constants.lora_adr_ref:
            logging.error("ADR parameter in LoRa configuration file is not valid")
            sys.exit("\tERROR: ADR parameter in LoRa configuration file is not valid!!!")

        # Get and check Authentication Mode
        self.auth_mode = _loraCfg.get("auth_mode")
        if self.auth_mode not in lora_constants.lora_auth_mode_ref:
            logging.error("Authentication mode parameter in LoRa configuration file is not valid")
            sys.exit("\tERROR: Authentication mode parameter in LoRa configuration file is not valid!!!")

        self.repeat = _loraCfg.get("repeat")
        self.retry = _loraCfg.get("retry")
        self.serialPort = _serialPort        
    

    def checkLoRa(self):
        self.serialPort.write(b"AT\n")
        response = self.serialPort.readline().decode("UTF-8")        
        if "OK" in response:
            self.serialPort.write(b"AT+VER\n")
            response = self.serialPort.readline().decode("UTF-8")
            response = response.split(": ")
            response = response[1]            
            response = response[0:len(response)-2]            
            logging.info("Connected to LoRa module with firmware version %s", response)
            return True
        else:
            logging.error("LoRa module is not connected")
            return False
            
    def setupLoRa(self):
        # Setup LoRa base band
        logging.debug("Setting LoRa base band to %s", self.base_band)
        cmd = "AT+DR="+self.base_band+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")
        if self.base_band in response:            
            pass
        else:
            logging.warning("Base band at LoRa module not configured")

        # Setup LoRa class
        logging.debug("Setting LoRa class to %s", self.lora_class)
        cmd = "AT+CLASS="+self.lora_class+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")
        if self.lora_class in response:            
            pass
        else:
            logging.warning("Class at LoRa module not configured")
        
        # Setup LoRa transmission power
        logging.debug("Setting LoRa transmission power to %s dBm", self.tx_power)
        cmd = "AT+POWER="+str(self.tx_power)+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if str(self.tx_power) in response:            
            pass
        else:
            logging.warning("Transmission power at LoRa module not configured")
        
        # Setup LoRa uplink data rate
        logging.debug("Setting LoRa uplink data rate to %s", self.uplink_dr)
        cmd = "AT+DR="+self.uplink_dr+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if self.uplink_dr in response:            
            pass
        else:
            logging.warning("Uplink data rate at LoRa module not configured")

        # Setup LoRa channel 0
        logging.debug("Setting LoRa channel 0 to %s and %s", self.chan0_freq, self.chan0_dr)
        cmd = "AT+CH=0,"+str(self.chan0_freq)+","+self.chan0_dr+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if self.chan0_dr in response:            
            pass
        else:
            logging.warning("Channel 0 at LoRa module not configured")

        # Setup LoRa channel 1
        logging.debug("Setting LoRa channel 1 to %s and %s", self.chan1_freq, self.chan1_dr)
        cmd = "AT+CH=1,"+str(self.chan1_freq)+","+self.chan1_dr+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if self.chan1_dr in response:            
            pass
        else:
            logging.warning("Channel 1 at LoRa module not configured")
        
        # Setup LoRa receive window 2
        logging.debug("Setting LoRa receive windows 2 to %s and %s", self.rxwin2_freq, self.rxwin2_dr)
        cmd = "AT+RXWIN2="+str(self.rxwin2_freq)+","+self.rxwin2_dr+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if self.rxwin2_dr in response:            
            pass
        else:
            logging.warning("Response window 2 at LoRa module not configured")
        
        # Setup LoRa ADR (Automatic Data Rate)
        logging.debug("Setting LoRa ADR to %s", self.adr)
        cmd = "AT+ADR="+self.adr+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if self.adr in response:            
            pass
        else:
            logging.warning("ADR at LoRa module not configured")
        
        # Setup LoRa authentication mode
        logging.debug("Setting LoRa authentication mode to %s", self.auth_mode)
        cmd = "AT+MODE="+self.auth_mode+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")       
        if self.auth_mode in response:            
            pass
        else:
            logging.warning("Authentication mode at LoRa module not configured")
    
    def setDevEUI(self, devEUI):
        logging.debug("Setting TTN device EUI to %s", devEUI)
        cmd = "AT+ID=DevEui,"+devEUI+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "DevEui," in response:            
            pass
        else:
            logging.warning("Device EUI at LoRa module not configured")
    
    def setAppEUI(self, appEUI):
        logging.debug("Setting TTN application EUI to %s", appEUI)
        cmd = "AT+ID=AppEui,"+appEUI+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "AppEui," in response:            
            pass
        else:
            logging.warning("Application EUI at LoRa module not configured")
    
    def setDevAddr(self, devAddr):
        logging.debug("Setting TTN device address to %s", devAddr)
        cmd = "AT+ID=DevAddr,"+devAddr+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "DevAddr," in response:            
            pass
        else:
            logging.warning("Device address at LoRa module not configured")
    
    def setNwkSKey(self, nwkSKey):
        logging.debug("Setting TTN network session key to %s", nwkSKey)
        cmd = "AT+KEY=NwkSKey,"+nwkSKey+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "NWKSKEY" in response:            
            pass
        else:
            logging.warning("Network session key at LoRa module not configured")
    
    def setAppSKey(self, appSKey):
        logging.debug("Setting TTN application session key to %s", appSKey)
        cmd = "AT+KEY=AppSKey,"+appSKey+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "APPSKEY" in response:            
            pass
        else:
            logging.warning("Application session key at LoRa module not configured")

    def setAppKey(self, appKey):
        logging.debug("Setting TTN application key to %s", appKey)
        cmd = "AT+KEY=AppKey,"+appKey+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "AppKey," in response:            
            pass
        else:
            logging.warning("Application key at LoRa module not configured")
    
    def sendJoinRequest(self):
        logging.debug("Sending Lora JOIN request")
        cmd = "AT+Join\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")                
        print(response)
        while True:
            response = self.serialPort.readline().decode("UTF-8")
            print(response)
            if "failed" in response:
                logging.warning("Join failed")
                return False
            elif "DevAddr" in response:
                logging.info("Network joined")            
                return True
            elif "Joined" in response:
                logging.info("Joined already")            
                return True

    def sendNoAckMsgHex(self, _loraPort, _loraMsg):
        logging.debug("Setting Lora port to %s", _loraPort)
        cmd = "AT+PORT="+str(_loraPort)+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")                
        if "PORT" in response:            
            pass
        else:
            logging.warning("LoRa port at LoRa module not configured")
        logging.debug("Sending no ack hexadecimal message: %s", _loraMsg)
        cmd = "AT+MSGHEX=\""+_loraMsg+"\"\n"        
        self.serialPort.write(cmd.encode("UTF-8"))
        while True:
            response = self.serialPort.readline().decode("UTF-8")
            print(response)
            if "Done" in response:            
                break

    def sendAckMsgHex(self, _loraPort, _loraMsg):
        logging.debug("Setting Lora port to %s", _loraPort)
        cmd = "AT+PORT="+str(_loraPort)+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")                
        if "PORT" in response:            
            pass
        else:
            logging.warning("LoRa port at LoRa module not configured")
        logging.debug("Sending ack hexadecimal message: %s", _loraMsg)
        cmd = "AT+CMSGHEX=\""+_loraMsg+"\"\n"        
        self.serialPort.write(cmd.encode("UTF-8"))
        while True:
            response = self.serialPort.readline().decode("UTF-8")
            print(response)
            if "Done" in response:            
                break    