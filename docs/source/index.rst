.. pyIoTDevSim documentation master file, created by
   sphinx-quickstart on Thu Dec 19 15:23:37 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyIoTDevSim
===========

**pyIoTDevSim** is a IoT device simulator developed by `AgroTechLab <https://agrotechlab.lages.ifsc.edu.br>`_ (*Technology Development 
Laboratory for Agribusiness*) of `IFSC <https://www.ifsc.edu.br>`_ (*Federal Institute of Santa Catarina*). 

It uses a real LoRaWAN module (connected to serial port) to sent simulated IoT data to `TTN (The Things Network) 
<https://www.thethingsnetwork.org>`_ infrastructure. Its objective is to accelerate the development of IoT solutions, allowing the 
validation of the communication infrastructure, data validation/formatting and storage and visualization system in parallel to the 
development of hardware and firmware projects.

.. image:: _static/scheme.png

.. important::
   
   **pyIoTDevSim** uses UART and the AT protocol to communicate with LoRaWAN modules. Therefore, it is only compatible with 
   LoRaWAN modems, i.e. it does not implement the LoRaWAN (L2) protocol.
   
   Currently **pyIoTDevSim** is compatible with following LoRaWAN modules:

     - RisingHF `RHF76-052x <https://wiki.risinghf.com/en/01/01/04/01/#description>`_;
     - RisingHF `RHF0M003 <https://wiki.risinghf.com/en/01/01/06/01/>`_;
   
**pyIoTDevSim** can be configured using a YAML file (``pyIoTDevSim.yml``), where the system and projects parameters are defined. More
information about the configuration file can be found `Configuration file <config_file.html>`_ section.

When **pyIoTDevSim** is executed, it reads the configuration file and starts the communication with the LoRaWAN module. All operations
are logged in the console and in a log file (``pyIoTDevSim.log``).

Versions support
----------------

Updates and new features are constantly being added to **pyIoTDevSim**. The following table shows the supported versions:

.. table::
   :align: center
   :widths: 20 20 20   

   +---------+------------+--------------+
   | Version |  Security  | New features |
   +=========+============+==============+
   |  0.x.x  |     Yes    |     Yes      |
   +---------+------------+--------------+


.. toctree::
   :name: mastertoc
   :maxdepth: 2
   :caption: Table of Contents:

   authors_license
   changelog
   config_file
   modules