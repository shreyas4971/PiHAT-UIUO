# PiHAT-UIUO (Universal Industrial I/O)
This repository contains the official Python driver scripts, test utilities, and automation examples for the WIN-PiHAT Industrial I/O series. Designed to transform the Raspberry Pi into a robust Programmable Logic Controller (PLC) alternative, these HATs provide optically isolated inputs, heavy-duty relay switching, and high-speed solid-state control for harsh industrial environments. 

The codebase provides clean, deployable examples for reading sensor states, driving actuators, and integrating physical I/O with cloud telemetry (MQTT).

---

 **Currently Supported Modules**

 **1. WIN-PiHAT-16DI (16-Channel Digital Input)**
A high-density input expansion board featuring 16 optically isolated digital input channels. 
* **Use Case:** Perfect for reading industrial sensors, limit switches, machine fault states, and standard 24V control logic. 
* **Key Feature:** Full galvanic isolation ensures that high-voltage industrial spikes cannot back-feed and destroy the Raspberry Pi's sensitive 3.3V GPIO pins.

 **2. WIN-PiHAT-8DO Relay (8-Channel Electromechanical Output)**
An output board equipped with 8 heavy-duty mechanical relays. 
* **Use Case:** Designed for switching high-power AC/DC loads, controlling contactors, running solenoid valves, and managing heavy machinery.
* **Key Feature:** Provides true physical air-gap isolation between the Raspberry Pi and the high-voltage load.

 **3. WIN-PiHAT-8DO MOSFET (8-Channel Solid-State Output)**
A solid-state output board utilizing high-speed, high-current MOSFETs for 8 channels of digital switching. 
* **Use Case:** Ideal for fast-acting DC loads, PWM (Pulse Width Modulation) generation, LED lighting arrays, and precision motor control.
* **Key Feature:** Zero moving parts. Solves the issue of mechanical relay degradation (wear and arcing) in applications that require rapid, continuous switching.

---

 **Future Expansion Roadmap**
The PiHAT-UIUO ecosystem is actively growing. Future updates to this repository will include driver support and Python examples for:
* **Analog I/O (ADC/DAC):** For reading continuous 4-20mA or 0-10V industrial sensors.
* **Temperature Monitoring:** RTD and Thermocouple interfaces for precision thermal tracking.
* **Industrial Protocols:** RS485/Modbus RTU expansion boards for daisy-chaining legacy factory equipment.
