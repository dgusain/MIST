# MIST

The Mechanized Inhaling Smoking Tool (MIST) is a human vape simulation device, designed and developed at the Hawk Behavioral Health Lab, Department of Clinical Psychology, University at Buffalo.  
Link to website: [Hawk Behavioral Health Lab](https://ubwp.buffalo.edu/hawklab/)

The device was developed to enable biomedical research investigators to autonomously test vapes/cigarettes for participants, hence enabling them to work much more efficiently.

The MIST works in congruency with the currently in development FRIENDS device - an electromagnetic puff detection device, for electronic nicotine delivery systems research study.

The v3 is an improvement on the original v2 version, which makes the process completely autonomous. The v3 replaces the mechanical pneumatic pedal valve with a solenoid valve, which increases the accuracy and speed of the opening/closing of the valve. The solenoid valve is powered by a grounded AC supply and functions with a Raspberry Pi 4 Model B chip.

The device is hooked up with a Cambridge filter to collect the e-liquid from the smoke released by the vape, and avoid it from getting jammed in the rotameter and the solenoid valves.

## Components

| Component                | Purpose                                                                 |
|--------------------------|-------------------------------------------------------------------------|
| Pneumatic tubing (1/4" diameter)           | Connects the vape adapter to the rotameter, to solenoid valve, and pump.       |
| Aquarium pump (20W)           | Provides suction for vape device       |
| Solenoid Valve           | Controls the opening/closing of the valve with increased accuracy       |
| Raspberry Pi 4 Model B   | Powers the solenoid valve and controls the device functions. Stores the program code.             |
| Cambridge Filter         | Collects e-liquid from the smoke to prevent jamming in the rotameter    |
| Rotameter (0 to 5 LPM)               | Measures the flow rate of the smoke, from the inlet-vape to the solenoid valve                                     |
| Relay Switch             | Controls the electrical connection for the solenoid valve               |
| Male adapters           | Connection from 1/4" OD to 1/4" NPT - to create vape adapters      |
| Vape adapters           | A set of tubing adapters to suit various vape mouth sizes and attach them to the MIST       |

