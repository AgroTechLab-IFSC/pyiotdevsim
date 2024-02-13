#  pyIoTDevSim 
It is a IoT device simulator that uses a real LoRaWAN&reg; module (connected to serial port) to sent simulated IoT data to TTN&reg; (<a href="https://www.thethingsnetwork.org" target="_blank">The Things Network</a>) infrastructure.<br>

![SCHEME schematic connection](./docs/figs/scheme.png "Connection scheme")<br>
 

## <b>Version 0.2.0 (26/02/2021):</b>
   - Added RHF0M003 module compatibility;
   - Moved LoRa session to Project session as a subsession (like TTN);
   - Included sub-band parameter;
   - Change module configuration (disable all channels of sub-bands not used);
 
## <b>Version 0.1.0 (16/11/2020):</b>
   - Added RHF72-056 module compatibility;
   - Multiproject capability (one thread by project);
   - Configuration by YAML file;
     - Project session (with TTN subsession);
     - LoRa session;
     - Serial session;
   - Payload sent using HEX format;
   - Data types:
     - UINT8;
     - UINT16;
     - FLOAT_UINT16;
     - FLOAT_COMPRESSED;
     - FLOAT32;
   - LOG generation;

## Configuration file details
 The pyIoTDevSim.yml is the configuration file searched by pyIoTDevSim to sets system, LoRa and projects parameters.<br>
 It uses a YAML format and all sections and keys parameters must be defined in lower case mode.<br>
 Two main sections are defined:
   - <code>system</code> (defines common LoRa parameters, LoRa module interface and the debug level used);
   - <code>projects</code> (list the projects enabled to run);

 Each project listed into the <code>projects</code> section must have a section with its name and the following parameters:
 @include projectA.yml
 Into subsection <code>sensor_list</code> must be defined the sensor list used by project. Each sensor must have a subsection with its name.
 This subsection must have <code>data_type</code>, <code>min_value</code> and <code>max_value</code>. Sensor values are randomly generated
 between values defines into <code>min_value</code> and <code>max_value</code>. The <code>data_type</code> will define the data type and size
 used to compose LoRa message (all messages are sent using hexadecimal format). The following data types can be used:
   - <code>uint8</code>
      - <b>range:</b> 0 to 255
      - <b>size:</b> 1 byte
   - <code>uint16</code>
      - <b>range:</b> 0 to 65535
      - <b>size:</b> 2 bytes
   - <code>float_uint16</code>
      - <b>range:</b> 0 to 655.35
      - <b>size:</b> 2 bytes
      - <b>limitation:</b> only 2 digits of precision
      - <b>operation:</b> value * 100
   - <code>float32_compressed</code>
      - <b>range:</b> 0 to 655.35
      - <b>size:</b> 3 bytes
      - <b>limitation:</b> byte 0 is the sign (AA = + / AF = -); only 2 digits of precision
      - <b>operation:</b> value * 100
   - <code>float32</code>
      - <b>range:</b> -3.4E+38 to +3.4E+38
      - <b>size:</b> 4 bytes
      - <b>operation:</b> sign bit, 8 bits exponent, 23 bits mantissa

---
AgroTechLab (*Laboratório de Desenvolvimento de Tecnologias para o Agronegócio*)  
IFSC (*Instituto Federal de Santa Catarina*) - Câmpus Lages  
Rua Heitor Vila Lobos, 225 - São Francisco  
Lages/SC - Brazil  
CEP: 88.506-400  
https://agrotechlab.lages.ifsc.edu.br
