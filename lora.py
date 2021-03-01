# Limitações: o base_band deve ser o mesmo para todos os projetos, se a cada projeto for redefinido, o contador de frames sempre irá reiniciar,
# neste caso, em modo ABP sempre enviará o frame com o contador em 1, resultando na seguinte mensagem no TTN:
# "cluster failed to handle message: device not found"
# o modo de autenticação segue o mesmo comportamento
# a frequencia e DR do RXWin2 e os canais RXWin1 são padronizados pelo TTN e amarrados com a baseband e subband
# O comportamento em modo OTAA deve ser testado.
import logging
import threading
import lora_constants
import sys


class LoRa:
    def __init__(self, _loraModule, _serialPortObj):
        self.lock = threading.Lock()        

        # # Get and check LoRa base band
        # self.base_band = _loraCfg.get("base_band")
        # if self.base_band not in lora_constants.lora_baseband_ref:
        #     logging.error("Base band parameter in LoRa configuration file is not valid")
        #     sys.exit("\tERROR: Base band parameter in LoRa configuration file is not valid!!!")

        # # Get and check LoRa class
        # self.lora_class = _loraCfg.get("lora_class")
        # if self.lora_class not in lora_constants.lora_class_ref:
        #     logging.error("Class parameter in LoRa configuration file is not valid")
        #     sys.exit("\tERROR: Class parameter in LoRa configuration file is not valid!!!")

        # # Get and check LoRa transmission power
        # self.tx_power = _loraCfg.get("tx_power")
        # if self.base_band == "EU434" or self.base_band == "EU868":
        #     if self.tx_power not in lora_constants.lora_tx_power_868_ref:
        #         logging.error("Transmission power parameter in LoRa configuration file is not valid")
        #         sys.exit("\tERROR: Transmission power parameter in LoRa configuration file is not valid!!!")
        # elif self.base_band == "US915" or self.base_band == "AU920":
        #     if self.tx_power not in lora_constants.lora_tx_power_915_ref:
        #         logging.error("Transmission power parameter in LoRa configuration file is not valid")
        #         sys.exit("\tERROR: Transmission power parameter in LoRa configuration file is not valid!!!")

           

        # # Get and check ADR (Automatic Data Rate)
        # self.adr = _loraCfg.get("adr")
        # if self.adr not in lora_constants.lora_adr_ref:
        #     logging.error("ADR parameter in LoRa configuration file is not valid")
        #     sys.exit("\tERROR: ADR parameter in LoRa configuration file is not valid!!!")

        # # Get and check Authentication Mode
        # self.auth_mode = _loraCfg.get("auth_mode")
        # if self.auth_mode not in lora_constants.lora_auth_mode_ref:
        #     logging.error("Authentication mode parameter in LoRa configuration file is not valid")
        #     sys.exit("\tERROR: Authentication mode parameter in LoRa configuration file is not valid!!!")

        # self.repeat = _loraCfg.get("repeat")
        # self.retry = _loraCfg.get("retry")
        self.loraModule = _loraModule
        self.serialPort = _serialPortObj
    

    def checkLoRa(self):
        self.serialPort.write(b"AT\n")
        response = self.serialPort.readline().decode("UTF-8")        
        if "OK" in response:
            self.serialPort.write(b"AT+VER\n")
            response = self.serialPort.readline().decode("UTF-8")
            response = response.split(": ")
            response = response[1]            
            response = response[0:len(response)-2]            
            logging.info("Connected to %s LoRa module with firmware version %s", self.loraModule, response)
            return True
        else:
            logging.error("LoRa module is not connected")
            return False
            
    
        
    
        
    def getLoRaMaxPayload(self, loraBaseBand, loraUPDatarate):
        max_payload = 0
        if loraBaseBand == "EU434" or loraBaseBand == "EU868":
            if loraUPDatarate not in lora_constants.lora_dr_868_ref:
                logging.error("Uplink data rate parameter in LoRa configuration file is not valid")
                sys.exit("\tERROR: Uplink data rate parameter in LoRa configuration file is not valid!!!")
                        
            if (loraUPDatarate == "DR0" or loraUPDatarate == "DR1" or loraUPDatarate == "DR2"):
                max_payload = 51
            elif (loraUPDatarate == "DR3"):
                max_payload = 115
            if (loraUPDatarate == "DR4" or loraUPDatarate == "DR5" or loraUPDatarate == "DR6" or loraUPDatarate == "DR7"):
                max_payload = 242                

        if loraBaseBand == "US915" or loraBaseBand == "AU915" or loraBaseBand == "AU920":
            if loraUPDatarate not in lora_constants.lora_dr_915_ref:
                logging.error("Uplink data rate parameter in LoRa configuration file is not valid")
                sys.exit("\tERROR: Uplink data rate parameter in LoRa configuration file is not valid!!!")                   
            
            if (loraUPDatarate == "DR0"):
                max_payload = 11                
            elif (loraUPDatarate == "DR1"):
                max_payload = 53                
            elif (loraUPDatarate == "DR2"):
                max_payload = 126                
            elif (loraUPDatarate == "DR3" or loraUPDatarate == "DR4"):
                max_payload = 242

        return max_payload

    #     # Setup LoRa channel 0
    #     logging.debug("Setting LoRa channel 0 to %s and %s", self.chan0_freq, self.chan0_dr)
    #     cmd = "AT+CH=0,"+str(self.chan0_freq)+","+self.chan0_dr+"\n"
    #     self.serialPort.write(cmd.encode("UTF-8"))
    #     response = self.serialPort.readline().decode("UTF-8")        
    #     if self.chan0_dr in response:            
    #         pass
    #     else:
    #         logging.warning("Channel 0 at LoRa module not configured")

    #     # Setup LoRa channel 1
    #     logging.debug("Setting LoRa channel 1 to %s and %s", self.chan1_freq, self.chan1_dr)
    #     cmd = "AT+CH=1,"+str(self.chan1_freq)+","+self.chan1_dr+"\n"
    #     self.serialPort.write(cmd.encode("UTF-8"))
    #     response = self.serialPort.readline().decode("UTF-8")        
    #     if self.chan1_dr in response:            
    #         pass
    #     else:
    #         logging.warning("Channel 1 at LoRa module not configured")
        
    def setLoRaRX1Win(self):
        logging.debug("Enabling LoRa receive window 1")
        cmd = "AT+RXWIN1=ON\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "RXWIN1: ON" in response:            
            pass
        else:
            logging.warning("RX window 1 at LoRa module not enabled") 

    def setLoRaRX2Win(self, loraRX2Frequency, loraRX2Datarate):
        logging.debug("Setting LoRa receive window 2 to %s and %s", loraRX2Frequency, loraRX2Datarate)
        cmd = "AT+RXWIN2="+str(loraRX2Frequency)+","+loraRX2Datarate+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if loraRX2Datarate in response:            
            pass
        else:
            logging.warning("Response window 2 at LoRa module not configured") 

    def setLoRaAuthMode(self, loraAuthMode):
        logging.debug("Setting LoRa authentication mode to %s", loraAuthMode)
        cmd = "AT+MODE="+loraAuthMode+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")       
        if loraAuthMode in response:            
            pass
        else:
            logging.warning("Authentication mode at LoRa module not configured")   
    
    def setLoRaADR(self, loraADR):
        logging.debug("Setting LoRa ADR to %s", loraADR)
        cmd = "AT+ADR="+loraADR+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if loraADR in response:            
            pass
        else:
            logging.warning("ADR at LoRa module not configured")

    def setLoRaUPDatarate(self, loraUPDatarate):
        logging.debug("Setting LoRa uplink data rate to %s", loraUPDatarate)
        cmd = "AT+DR="+loraUPDatarate+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if loraUPDatarate in response:            
            pass
        else:
            logging.warning("Uplink data rate at LoRa module not configured")

    def setLoRaTXPower(self, loraTXPower):
        logging.debug("Setting LoRa transmission power to %s dBm", loraTXPower)
        cmd = "AT+POWER="+str(loraTXPower)+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if str(loraTXPower) in response:            
            pass
        else:
            logging.warning("Transmission power at LoRa module not configured")

    def setLoRaClass(self, loraClass):
        logging.debug("Setting LoRa class to %s", loraClass)
        cmd = "AT+CLASS="+loraClass+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")
        if loraClass in response:            
            pass
        else:
            logging.warning("Class at LoRa module not configured")

    def setLoRaSubBand(self, loraSubBand):
        if (self.loraModule == "RHF76-052"):
            if loraSubBand == 1:                
                for ch in range(8, 72):
                    logging.debug("Disabling LoRa channel %s", ch)
                    cmd = "AT+CH="+str(ch)+", 0\n"
                    self.serialPort.write(cmd.encode("UTF-8"))
                    response = self.serialPort.readline().decode("UTF-8")        
                    if str(ch) in response:            
                        pass
                    else:
                        logging.warning("Failed disabling LoRa channel %s", ch)
            elif loraSubBand == 2:                
                for ch in range(0, 8):
                    logging.debug("Disabling LoRa channel %s", ch)
                    cmd = "AT+CH="+str(ch)+", 0\n"
                    self.serialPort.write(cmd.encode("UTF-8"))
                    response = self.serialPort.readline().decode("UTF-8")        
                    if str(ch) in response:            
                        pass
                    else:
                        logging.warning("Failed disabling LoRa channel %s", ch)
                for ch in range(16, 65):
                    logging.debug("Disabling LoRa channel %s", ch)
                    cmd = "AT+CH="+str(ch)+", 0\n"
                    self.serialPort.write(cmd.encode("UTF-8"))
                    response = self.serialPort.readline().decode("UTF-8")        
                    if str(ch) in response:            
                        pass
                    else:
                        logging.warning("Failed disabling LoRa channel %s", ch)
                for ch in range(66, 72):
                    logging.debug("Disabling LoRa channel %s", ch)
                    cmd = "AT+CH="+str(ch)+", 0\n"
                    self.serialPort.write(cmd.encode("UTF-8"))
                    response = self.serialPort.readline().decode("UTF-8")        
                    if str(ch) in response:            
                        pass
                    else:
                        logging.warning("Failed disabling LoRa channel %s", ch)
        # elif (self.loraModule == "RHF03M003"):
      
    def setLoRaBaseBand(self, loraBaseBand):
        logging.debug("Setting LoRa base band to %s", loraBaseBand)
        cmd = "AT+DR="+loraBaseBand+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if loraBaseBand in response:            
            pass
        else:
            logging.warning("Base band at LoRa module not configured")

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