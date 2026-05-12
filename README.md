# PiHAT-UIUO (Universal Industrial I/O)
This repository contains the official Python driver scripts, test utilities, and automation examples for the WIN-PiHAT Industrial I/O series. Designed to transform the Raspberry Pi into a robust Programmable Logic Controller (PLC) alternative, these HATs provide high-density input expansion, heavy-duty relay switching, and high-speed solid-state control for industrial environments. 

The codebase provides clean, deployable examples for reading sensor states, driving actuators, and integrating physical I/O with cloud telemetry (MQTT).

---

### **Currently Supported Modules**

#### **1. WIN-PiHAT-16DI (16-Channel Digital Input)**
A high-density input expansion board featuring 16 digital input channels. 
* **Use Case:** Perfect for reading logic-level sensors, limit switches, machine fault states, and button panels. 
* **Key Feature:** Provides massive input expansion via a single HAT, significantly reducing wiring complexity and GPIO footprint for large-scale monitoring applications.

#### **2. WIN-PiHAT-8DO Relay (8-Channel Electromechanical Output)**
An output board equipped with 8 heavy-duty mechanical relays. 
* **Use Case:** Designed for switching high-power AC/DC loads, controlling contactors, running solenoid valves, and managing heavy machinery.
* **Key Feature:** Provides true physical air-gap isolation between the Raspberry Pi and the high-voltage load, keeping the Pi's sensitive GPIO pins completely safe.

#### **3. WIN-PiHAT-8DO MOSFET (8-Channel Solid-State Output)**
A solid-state output board utilizing high-speed, high-current MOSFETs for 8 channels of digital switching. 
* **Use Case:** Ideal for fast-acting DC loads, PWM (Pulse Width Modulation) generation, LED lighting arrays, and precision motor control.
* **Key Feature:** Features isolated output stages to protect the Pi, while offering zero moving parts. This solves the issue of mechanical relay degradation (wear and arcing) in applications that require rapid, continuous switching.

### **4. WIN-PiHAT-8AI (8-Channel Analog Input)**
A high-resolution data acquisition board featuring 8 independent analog input channels.
* **Use Case:** Perfect for reading continuous industrial sensors, pressure transducers, temperature transmitters, flow meters, and variable frequency drive (VFD) feedback signals.
* **Key Feature:** Provides precise signal measurement with an onboard ADC supporting selectable 12-bit or 16-bit resolution. With jumper-configurable input ranges (0-5V, 0-10V, 4-20mA), it enables highly accurate digitization of real-world analog conditions directly to the Pi's I2C/SPI bus.

### **5. WIN-PiHAT-8AO (8-Channel Analog Output)**
A precision control board featuring 8 independent analog output channels.
* **Use Case:** Ideal for driving proportional valves, variable frequency drives (VFDs), servo motor speed references, and industrial dimming systems.
* **Key Feature:** Utilizes an onboard Digital-to-Analog Converter (DAC) with selectable 12-bit or 16-bit resolution to generate precise 0-10V programmable control signals, seamlessly translating digital commands from the Pi into smooth, real-world proportional control

---

### **Future Expansion Roadmap**
The PiHAT-UIUO ecosystem is actively growing. Future updates to this repository will include driver support and Python examples for:
* **Temperature Monitoring:** RTD and Thermocouple interfaces for precision thermal tracking.
* **Industrial Protocols:** RS485/Modbus RTU expansion boards for daisy-chaining legacy factory equipment.
