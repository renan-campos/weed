# weed
Web Enhanced Environment Detection 

Description : A system to monitor the growing environment of an indoor plant.
SW Inventory: The following software is needed on the Raspberry Pi:
		- Python 2.7
		-- Flask
		-- SQL alchemy
		-- Adafruit DHT
HW Inventory: The following hardware is needed for this system:
		- Raspberry Pi
		- DHT11     (Temperature & Humidity Sensor)
		- MCP3008   (ADC)
		- VH400     (Soil moisture Sensor)
		- Pi Camera
Value Add   : This system allows user to monitor their plant remotley.
Install     : Wire the components in the following way:
		DHT11 Power  <=> Pi Pin 17
                DHT11 Data   <=> Pi Pin  3
                DHT11 GND    <=> GND
                MCP3008 VDD  <=> Pi Pin 27
                MCP3008 Vref <=> Pi Pin 27
                MCP3008 AGND <=> GND
                MCP3008 CLK  <=> Pi Pin 11
                MCP3008 Dout <=> Pi Pin 9
                MCP3008 Din  <=> Pi pin 10
                MCP3008 CS   <=> Pi Pin 8
                MCP3008 DGND <=> GND
                VH400 5V     <=> Pi Pin 27
                VH400 Data   <=> MCP3008 channel 0
                VH400 GND    <=> GND
                Pi camera    <=> Pi camera slot
              After powering on the Pi, go into the code's directory and run:
                $ python app.py & 
