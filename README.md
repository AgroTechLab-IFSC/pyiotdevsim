

#  pyIoTDevSim 
It is a IoT device simulator that uses a real LoRaWAN&reg; module (connected to serial port) to sent simulated IoT data to TTN&reg; (<a href="https://www.thethingsnetwork.org">The Things Network</a>) infrastructure.<br>

![SCHEME schematic connection](./docs/figs/scheme.png "Connection scheme")<br>

## Configuration file details
 The pyIoTDevSim.yml is the configuration file searched by pyIoTDevSim to sets system, LoRa and projects parameters.<br>
 It uses a YAML format and all sections and keys parameters must be defined in lower case mode.<br>
 Two main sections are defined:
   - <code>system</code> - defines common LoRa parameters, LoRa module interface and the debug level used;
   - <code>projects</code> - list the projects enabled to run;

 The <code>system</code> parameters are the same to all projects:
   - <code>debug_level</code> - pyIoTDevSim debug level (ie: DEBUG);
   - <code>lora_module</code> - LoRa module (ie: RHF76-052);
   - <code>serial</code> - subsection with serial parameters:
     - <code>port</code> - serial port (ie: /dev/ttyUSB0);
     - <code>baudrade</code> - serial baudrate (ie: 9600);
   - <code>lora</code> - subsection with LoRa parameters:
     - <code>base_band</code> - LoRa base band (ie: AU920);
     - <code>sub_band</code> - LoRa sub-band (ie: 2);
     - <code>class</code> - LoRa class (ie: A);
     - <code>rxwin2_freq</code> - LoRa RX window 2 frequency (ie: 923.3);
     - <code>rxwin2_dr</code> - LoRa RX window 2 data ratio (ie.: DR8);
     - <code>auth_mode</code> - LoRa authentication mode (ie: LWABP);

 The <code>projects</code> section list the name of projects enabled to run. An example is showed bellow (in this case Project C is defined but not will be enabled):<pre>projects:<br>&#9;- Project_A<br>&#9;- Project_B<br>&#9;# - Project_C</pre>

 Ater, to each project listed at <code>projects</code> section a new section must be created with the following parameters:   
   - <code>project_name</code> - section with the project name (the same used at <code>projects</code> section);
     - <code>sampling_period</code> - sampling period (in seconds) of sensor list (ie: 300);
     - <code>ttn</code> - subsection with TTN (The Things Network) parameters:
       - <code>dev_eui</code> - device EUI;
       - <code>app_eui</code> - application EUI;
       - <code>dev_addr</code> - device address;
       - <code>nwks_key</code> - network session key;
       - <code>apps_key</code> - application session key;
       - <code>app_key</code> - application key;
     - <code>lora</code> - subsection with LoRa parameters:
       - <code>tx_power</code> - transmission power in dB (ie: 20);
       - <code>uplink_dr</code> - uplink data ratio (ie: DR1);
       - <code>chan0_freq</code> - channel 0 frequency (ie: 917.2);
       - <code>chan0_dr</code> - channel 0 data ratio (ie: DR1);
       - <code>chan1_freq</code> - channel 1 frequency (ie: 917.9);
       - <code>chan1_dr</code> - channel 1 data ratio (ie: DR1);
       - <code>adr</code> - automatic data ratio (ie: OFF);
       - <code>repeat</code> - transmission repeat (ie: 2);
       - <code>retry</code> - transmission retry (ie: 2);
       - <code>initial_port</code> - initial port number to transmission sensor values (ie: 10);
     - <code>sensor_list</code> - subsection with a list of sensors;
     - <code>sensor_name</code> - subsection with sensor parameters (one to each sensor listed at <code>sensor_list</code>):
       - <code>data_type</code> - sensor data type (ie: float32);
       - <code>min_value</code> - sensor minimum value (ie: -27.803293);
       - <code>max_value</code> - sensor maximum value (ie: -27.804540);

 Sensor values are randomly generated between values defines at <code>min_value</code> and <code>max_value</code>. To fixed values both parameters must be the same. The <code>data_type</code> will define the data type and payload size used to compose LoRa message (all messages are sent using hexadecimal format). The following data types can be used:
   - <code>int8</code>
      - <b>range:</b> -128 to 127
      - <b>size:</b> 1 byte
   - <code>uint8</code>
      - <b>range:</b> 0 to 255
      - <b>size:</b> 1 byte
   - <code>int16</code>
      - <b>range:</b> -32768 to 32767
      - <b>size:</b> 2 bytes
   - <code>uint16</code>
      - <b>range:</b> 0 to 65535
      - <b>size:</b> 2 bytes
   - <code>int32</code>
      - <b>range:</b> -2147483648 to 2147483647
      - <b>size:</b> 4 bytes
   - <code>uint32</code>
      - <b>range:</b> 0 to 4294967295
      - <b>size:</b> 4 bytes
   - <code>float_uint16</code>
      - <b>range:</b> 0 to 655.35
      - <b>size:</b> 2 bytes
      - <b>limitation:</b> only 2 digits of precision
      - <b>operation:</b> value * 100
   - <code>float_int15</code>
      - <b>range:</b> -327.67 to 327.67
      - <b>size:</b> 2 bytes
      - <b>limitation:</b> 1 bit of sign and 15 bits of value; only 2 digits of precision
      - <b>operation:</b> value * 100
   - <code>float</code>
      - <b>range:</b> -3.4E+38 to +3.4E+38
      - <b>size:</b> 4 bytes
      - <b>operation:</b> sign bit, 8 bits exponent, 23 bits mantissa

## Release Notes

### <b>Version 0.4.0 (19/12/2024):</b>
   - Documentation updated;

### <b>Version 0.3.0 (02/10/2024):</b>
   - Updated data types;

### <b>Version 0.2.0 (26/02/2021):</b>
   - Added RHF0M003 module compatibility;
   - Moved LoRa session to Project session as a subsession (like TTN);
   - Included sub-band parameter;
   - Change module configuration (disable all channels of sub-bands not used);
 
### <b>Version 0.1.0 (16/11/2020):</b>
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

<br><hr><p style="text-align: center;"><b><a href="https://agrotechlab.lages.ifsc.edu.br/">AgroTechLab (<i>Laboratório de Desenvolvimento de Tecnologias para o Agronegócio</i>)</a></b><br>
<b><a href="https://ifsc.edu.br/web/campus-lages">IFSC (<i>Instituto Federal de Santa Catarina</i>) - Câmpus Lages</a></b><br>
Rua Heitor Vila Lobos, 225 - São Francisco<br>
Lages/SC - Brazil<br>
CEP: 88.506-400</p>