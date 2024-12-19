Configuration file
------------------

 The ``pyIoTDevSim.yml`` is the configuration file searched by **pyIoTDevSim** to sets system, LoRa and projects parameters.
 It uses a YAML format and all sections and keys parameters must be defined in lower case mode.
 Two main sections are defined:
   - ``system`` - common LoRa parameters, LoRa module interface and the debug level used;
   - ``projects`` - list the projects enabled to run;

 The ``system`` parameters are the same to all projects:

   - ``debug_level`` - pyIoTDevSim debug level (ie: DEBUG);
   - ``lora_module`` - LoRa module (ie: RHF76-052);
   - ``serial`` - subsection with serial parameters:

     - ``port`` - serial port (ie: /dev/ttyUSB0);
     - ``baudrade`` - serial baudrate (ie: 9600);
   - ``lora`` - subsection with LoRa parameters:

     - ``base_band`` - LoRa base band (ie: AU920);
     - ``sub_band`` - LoRa sub-band (ie: 2);
     - ``class`` - LoRa class (ie: A);
     - ``rxwin2_freq`` - LoRa RX window 2 frequency (ie: 923.3);
     - ``rxwin2_dr`` - LoRa RX window 2 data ratio (ie.: DR8);
     - ``auth_mode`` - LoRa authentication mode (ie: LWABP);

 The ``projects`` section list the name of projects enabled to run. An example is showed 
 bellow (in this case Project C is defined but not will be enabled)::
 
   projects:
      - Project_A
      - Project_B
      # - Project_C

 Ater, to each project listed at ``projects`` section a new section must be created with the following parameters:

   - ``project_name`` - section with the project name (the same level used at ``projects`` section);

     - ``sampling_period`` - sampling period (in seconds) of sensor list (ie: 300);
     - ``ttn`` - subsection with TTN (The Things Network) parameters:

       - ``dev_eui`` - device EUI;
       - ``app_eui`` - application EUI;
       - ``dev_addr`` - device address;
       - ``nwks_key`` - network session key;
       - ``apps_key`` - application session key;
       - ``app_key`` - application key;
     - ``lora`` - subsection with LoRa parameters:

       - ``tx_power`` - transmission power in dB (ie: 20);
       - ``uplink_dr`` - uplink data ratio (ie: DR1);
       - ``chan0_freq`` - channel 0 frequency (ie: 917.2);
       - ``chan0_dr`` - channel 0 data ratio (ie: DR1);
       - ``chan1_freq`` - channel 1 frequency (ie: 917.9);
       - ``chan1_dr`` - channel 1 data ratio (ie: DR1);
       - ``adr`` - automatic data ratio (ie: OFF);
       - ``repeat`` - transmission repeat (ie: 2);
       - ``retry`` - transmission retry (ie: 2);
       - ``initial_port`` - initial port number to transmission sensor values (ie: 10);
     - ``sensor_list`` - subsection with a list of sensors;
     - ``sensor_name`` - subsection with sensor parameters (one to each sensor listed at ``sensor_list``):

       - ``data_type`` - sensor data type (ie: float32);
       - ``min_value`` - sensor minimum value (ie: -27.803293);
       - ``max_value`` - sensor maximum value (ie: -27.804540);

 Sensor values are randomly generated between values defines at ``min_value`` and ``max_value``. To fixed values both parameters 
 must be the same. The ``data_type`` will define the data type and payload size used to compose LoRa message (all messages are sent 
 using hexadecimal format). The following data types can be used:

   - ``int8``

      - **range:** -128 to 127
      - **size:** 1 byte
   - ``uint8``

      - **range:** 0 to 255
      - **size:** 1 byte
   - ``int16``
      - **range:** -32768 to 32767
      - **size:** 2 bytes
   - ``uint16``
      - **range:** 0 to 65535
      - **size:** 2 bytes
   - ``int32``

      - **range:** -2147483648 to 2147483647
      - **size:** 4 bytes
   - ``uint32``

      - **range:** 0 to 4294967295
      - **size:** 4 bytes
   - ``float_uint16``

      - **range:** 0 to 655.35
      - **size:** 2 bytes
      - **limitation:** only 2 digits of precision
      - **operation:** value * 100
   - ``float_int15``

      - **range:** -327.67 to 327.67
      - **size:** 2 bytes
      - **limitation:** 1 bit of sign and 15 bits of value; only 2 digits of precision
      - **operation:** value * 100
   - ``float``

      - **range:** -3.4E+38 to +3.4E+38
      - **size:** 4 bytes
      - **operation:** sign bit, 8 bits exponent, 23 bits mantissa
   
.. toctree::
   :name: config_file
   :maxdepth: 2
   :caption: Configuration file