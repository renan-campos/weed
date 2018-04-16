import Adafruit_DHT
import time
import logging
import logging.handlers

import RPi.GPIO as GPIO

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# DHT-11 Power Pin
dht11_power = 17
# DHT-11 Data Pin 
dht11_data = 3

# MCP3008 & Vegetronix power pin
mcp3008_power = 27
# ADC channel vegatronix is on
veg_chan =  0
# Software SPI Configuration
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(dht11_power, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(mcp3008_power, GPIO.OUT, initial=GPIO.LOW)

def getTempHum():
    """
    Returns Temperature and Humidity
    """
    humidity  = 0.0
    temperature = 0.0

    # Set up logger
    logger = logging.getLogger(__name__)
    handler = logging.handlers.RotatingFileHandler(
                filename='logs/sensors.log',
                maxBytes=16992,
                backupCount=7
                )
    handler.setFormatter(
                logging.Formatter(fmt="%(asctime)s %(levelname)s:%(message)s")
                )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # Turn sensor on
    GPIO.output(dht11_power, GPIO.HIGH)
    
    # Calculate average temperature and humidity
    for i in range(10):
        # Get data from DHT 11 on pin 3
        h, t = Adafruit_DHT.read_retry(11, dht11_data)

        if h == None or t == None:
            logger.error("DHT11 sensor failure")
            i = i - 1
            if (i == -1):
                # Turn sensor off.
                GPIO.output(dht11_power, GPIO.LOW)
                return (-1, -1)
            break

        humidity    = humidity    + h
        temperature = temperature + t

    humidity    = humidity    / (i+1)
    temperature = temperature / (i+1)

    # Convert to F
    temperature = temperature * 9/5.0 + 32
    logger.info(
            'Temp: {0:0.1f} F Humidity: {1:0.1f} %'.format(temperature, humidity))
    
    # Turn sensor off.
    GPIO.output(dht11_power, GPIO.LOW)

    # Add information to web app.
    return (temperature, humidity)


def getSoilMoisture():
    # Set up logger
    logger = logging.getLogger(__name__)
    handler = logging.handlers.RotatingFileHandler(
                filename='logs/sensors.log',
                maxBytes=16992,
                backupCount=7
                )
    handler.setFormatter(
                logging.Formatter(fmt="%(asctime)s %(levelname)s:%(message)s")
                )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    # Turn sensor on.
    GPIO.output(mcp3008_power, GPIO.HIGH)

    # Sleep to give the ADC and sensor time to power on.
    time.sleep(0.5)
    
    value = mcp.read_adc(veg_chan)
    
    if value == None:
        logger.error("Vegatronix sensor failure")
        # Turn sensor off.
        GPIO.output(mcp3008_power, GPIO.LOW)
        return -1
    
    percent = float(value)/931 * 100
    if percent > 100:
        percent = 100
    logger.info("Soil moisture at %3.1f%%" % (percent))
    
    # Turn sensor off.
    GPIO.output(mcp3008_power, GPIO.LOW)
    
    return percent
