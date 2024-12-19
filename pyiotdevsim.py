import sys
import logging
import serial
import config
import lora
import project

# SYSTEM INFORMATION
VERSION = "0.4.0"
CONFIG_FILE = 'pyIoTDevSim.yml'
LOG_FILE = 'pyIoTDevSim.log'

def main():
    """Main function."""
    logging.info(f"Starting pyIoTDevSim {VERSION}")
    print(f"Starting pyIoTDevSim {VERSION}", flush=True)
    logging.info(f"Reading configuration file {CONFIG_FILE}")
    print(f"\tReading configuration file... ", end='', flush=True)
    cfgObj = config.Config(cfgFile=CONFIG_FILE)    
    print("[OK]", flush=True)
    print(f"\t\t{len(cfgObj.projects)} project(s) found: {cfgObj.projects}", flush=True)

    # Open a serial port to communicate with LoRa module
    logging.info(f"Opening serial port at {cfgObj.getSerialPort()} with baudrate {cfgObj.getSerialBaudrate()}")
    print(f"\tOpening serial port at {cfgObj.getSerialPort()} with baudrate {cfgObj.getSerialBaudrate()}... ", end='', flush=True)
    try:
        serialPortObj = serial.Serial(cfgObj.getSerialPort(), cfgObj.getSerialBaudrate())
        print(f"[OK]", flush=True)
    except serial.SerialException:
        logging.error("Serial port not available!") 
        sys.exit("[ERROR]\n\t\tSerial port not available!!!")
    
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
    """Main function (entry point)."""

    # Set logging configuration
    logging.basicConfig(filename=LOG_FILE, format='%(asctime)s %(levelname)s - %(message)s', level=logging.INFO)
    
    # Call main function
    main()