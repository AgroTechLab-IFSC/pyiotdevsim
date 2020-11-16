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