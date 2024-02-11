#  pyIoTDevSim 
It is a IoT device simulator that uses a real LoRaWAN&reg; module (connected to serial port) to sent simulated IoT data to TTN&reg; (<a href="https://www.thethingsnetwork.org" target="_blank">The Things Network</a>) infrastructure.<br>

![SCHEME schematic connection](https://github.com/AgroTechLab-IFSC/pyiotdevsim/tree/master/docs/figs/scheme.png "Connection scheme")<br>
 

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
   - <code>system</code>
   - <code>projects</code>
 
 The <code>system</code> section layout defines common LoRa parameters, LoRa module interface and the debug level used. An example is showed bellow: 
 @include system.yml

 The <code>projects</code> section will list the projects enabled to run. An example is showed bellow (in this case Project C is defined but not will be enabled):
 @include projects.yml

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

## License
  @author Robson Costa (<mailto:robson.costa@ifsc.edu.br>)
  @brief Project main file.
  @version 0.2.0
  @since 16/11/2020
  @date 01/03/2021
  @copyright Copyright &copy; 2020 - 2021 <a href="https://agrotechlab.lages.ifsc.edu.br" target="_blank">AgroTechLab</a>.\n
  ![LICENSE license](../figs/license.png)<br>
  Licensed under the CC BY-NC-SA (<i>Creative Commons Attribution-NonCommercial-ShareAlike</i>) 4.0 International Unported License (the <em>"License"</em>). You may not
  use this file except in compliance with the License. You may obtain a copy of the License <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode" target="_blank">here</a>.
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an <em>"as is" basis, 
  without warranties or  conditions of any kind</em>, either express or implied. See the License for the specific language governing permissions 
  and limitations under the License.
