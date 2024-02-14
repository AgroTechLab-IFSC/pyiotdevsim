## @file lora.py
#  @author Robson Costa (<mailto:robson.costa@ifsc.edu.br>)
#  @brief LoRa class.
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
    """! The LoRa class.
    Manages the LoRa operations communicating with LoRa modules.
    """
    def __init__(self, _loraModule, _serialPortObj):
        """! The class constructor.
        @param _loraModule The type of LoRa module.
        @param _serialPortObj The serial port object.
        @return  An instance of the LoRa class based on a specified lora module initialized at specified serial port.
        """  
        ## Semaphore to use LoRa object
        self.lock = threading.Lock()        

        ## LoRa module type
        self.loraModule = _loraModule

        ## Serial object
        self.serialPort = _serialPortObj

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
       
    
        
    def checkLoRa(self):
        """! Check if LoRa module is connected and ready to use.
        @return True - if successfuly
        @return False - if failed
        """
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
        """! Get the maximum payload size based on base band and uplink data rate.
        @param loraBaseBand base band
        @param loraUPDatarate uplink data rate
        @return Maximum payload size.        
        """
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
        """! Enable RX window 1.                
        """
        logging.debug("Enabling LoRa receive window 1")
        cmd = "AT+RXWIN1=ON\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "RXWIN1: ON" in response:            
            pass
        else:
            logging.warning("RX window 1 at LoRa module not enabled") 

    def setLoRaRX2Win(self, loraRX2Frequency, loraRX2Datarate):
        """! Sets the RX window 2 parameters.
        @param loraRX2Frequency RX window 2 frequency
        @param loraRX2Datarate RX window 2 data rate        
        """
        logging.debug("Setting LoRa receive window 2 to %s and %s", loraRX2Frequency, loraRX2Datarate)
        cmd = "AT+RXWIN2="+str(loraRX2Frequency)+","+loraRX2Datarate+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if loraRX2Datarate in response:            
            pass
        else:
            logging.warning("Response window 2 at LoRa module not configured") 

    def setLoRaAuthMode(self, loraAuthMode):
        """! Sets the authentication mode.
        @param loraAuthMode authentication mode        
        """
        logging.debug("Setting LoRa authentication mode to %s", loraAuthMode)
        cmd = "AT+MODE="+loraAuthMode+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")       
        if loraAuthMode in response:            
            pass
        else:
            logging.warning("Authentication mode at LoRa module not configured")   
    
    def setLoRaADR(self, loraADR):
        """! Enable or disable ADR (Automatic Data Rate).
        @param loraADR enable (ON) or disable (OFF)
        """
        logging.debug("Setting LoRa ADR to %s", loraADR)
        cmd = "AT+ADR="+loraADR+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if loraADR in response:            
            pass
        else:
            logging.warning("ADR at LoRa module not configured")

    def setLoRaUPDatarate(self, loraUPDatarate):
        """! Sets the uplink data rate.
        @param loraUPDatarate uplink data rate
        """
        logging.debug("Setting LoRa uplink data rate to %s", loraUPDatarate)
        cmd = "AT+DR="+loraUPDatarate+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if loraUPDatarate in response:            
            pass
        else:
            logging.warning("Uplink data rate at LoRa module not configured")

    def setLoRaTXPower(self, loraTXPower):
        """! Sets the transmission power (in dBm).
        @param loraTXPower transmission power (in dBm)
        """
        logging.debug("Setting LoRa transmission power to %s dBm", loraTXPower)
        cmd = "AT+POWER="+str(loraTXPower)+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if str(loraTXPower) in response:            
            pass
        else:
            logging.warning("Transmission power at LoRa module not configured")

    def setLoRaClass(self, loraClass):
        """! Sets the LoRa class
        @param loraClass LoRa class
        """
        logging.debug("Setting LoRa class to %s", loraClass)
        cmd = "AT+CLASS="+loraClass+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")
        if loraClass in response:            
            pass
        else:
            logging.warning("Class at LoRa module not configured")

    def setLoRaSubBand(self, loraSubBand):
        """! Sets the sub-band. This will disable all channels not belonging to the specified sub-band.
        @param loraSubBand sub-band
        """
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
        """! Sets the base-band.
        @param loraBaseBand base-band
        """
        logging.debug("Setting LoRa base band to %s", loraBaseBand)
        cmd = "AT+DR="+loraBaseBand+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if loraBaseBand in response:            
            pass
        else:
            logging.warning("Base band at LoRa module not configured")

    def setDevEUI(self, devEUI):
        """! Sets the device EUI.
        @param devEUI device EUI
        """
        logging.debug("Setting TTN device EUI to %s", devEUI)
        cmd = "AT+ID=DevEui,"+devEUI+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "DevEui," in response:            
            pass
        else:
            logging.warning("Device EUI at LoRa module not configured")
    
    def setAppEUI(self, appEUI):
        """! Sets the application EUI.
        @param appEUI application EUI
        """
        logging.debug("Setting TTN application EUI to %s", appEUI)
        cmd = "AT+ID=AppEui,"+appEUI+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "AppEui," in response:            
            pass
        else:
            logging.warning("Application EUI at LoRa module not configured")
    
    def setDevAddr(self, devAddr):
        """! Sets the device address.
        @param devAddr device address
        """
        logging.debug("Setting TTN device address to %s", devAddr)
        cmd = "AT+ID=DevAddr,"+devAddr+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "DevAddr," in response:            
            pass
        else:
            logging.warning("Device address at LoRa module not configured")
    
    def setNwkSKey(self, nwkSKey):
        """! Sets the network session key.
        @param nwkSKey network session key.
        """
        logging.debug("Setting TTN network session key to %s", nwkSKey)
        cmd = "AT+KEY=NwkSKey,"+nwkSKey+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "NWKSKEY" in response:            
            pass
        else:
            logging.warning("Network session key at LoRa module not configured")
    
    def setAppSKey(self, appSKey):
        """! Sets the application session key.
        @param appSKey application session key.
        """
        logging.debug("Setting TTN application session key to %s", appSKey)
        cmd = "AT+KEY=AppSKey,"+appSKey+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "APPSKEY" in response:            
            pass
        else:
            logging.warning("Application session key at LoRa module not configured")

    def setAppKey(self, appKey):
        """! Sets the application key.
        @param appKey application key.
        """
        logging.debug("Setting TTN application key to %s", appKey)
        cmd = "AT+KEY=AppKey,"+appKey+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")        
        if "AppKey," in response:            
            pass
        else:
            logging.warning("Application key at LoRa module not configured")
    
    def sendJoinRequest(self):
        """! Sends a join request.
        @return True - if successfuly joined.
        @return False - if joined failed.
        """
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
        """! Sends unconfirmed hexadecimal messages.
        @param _loraPort port
        @param _loraMsg hexadecimal message        
        """
        logging.debug("Setting Lora port to %s", _loraPort)
        cmd = "AT+PORT="+str(_loraPort)+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")                
        if "PORT" in response:            
            pass
        else:
            logging.warning("LoRa port at LoRa module not configured")
        logging.info("Sending no ack hexadecimal message: %s", _loraMsg)
        cmd = "AT+MSGHEX=\""+_loraMsg+"\"\n"              
        self.serialPort.write(cmd.encode("UTF-8"))
        while True:
            response = self.serialPort.readline().decode("UTF-8")
            # print(response)
            if "Done" in response:            
                break

    def sendAckMsgHex(self, _loraPort, _loraMsg):
        """! Sends confirmed hexadecimal messages.
        @param _loraPort port
        @param _loraMsg hexadecimal message        
        """
        logging.debug("Setting Lora port to %s", _loraPort)
        cmd = "AT+PORT="+str(_loraPort)+"\n"
        self.serialPort.write(cmd.encode("UTF-8"))
        response = self.serialPort.readline().decode("UTF-8")                
        if "PORT" in response:            
            pass
        else:
            logging.warning("LoRa port at LoRa module not configured")
        logging.info("Sending ack hexadecimal message: %s", _loraMsg)
        cmd = "AT+CMSGHEX=\""+_loraMsg+"\"\n"        
        self.serialPort.write(cmd.encode("UTF-8"))
        while True:
            response = self.serialPort.readline().decode("UTF-8")
            # print(response)
            if "Done" in response:            
                break    