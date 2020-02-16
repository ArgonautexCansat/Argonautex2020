import time
import pycom
import machine
import socket

from pysense import Pysense
from network import LoRa
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

print("Starting LoRa...")

# Initialise LoRa in LORA mode
# Region = Europe (868MHz)
# More parameters need to be set
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# Create raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Sensor values
mp_temperature = 0
mp_altitude = 0
mp_pressure = 0

si_temperature = 0
si_humidity = 0

li_roll = 0
li_pitch = 0

battery_voltage = 0

pycom.heartbeat(False)
pycom.rgbled(0x000000)

py = Pysense()

mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
print("MPL3115A2 temperature: " + str(mp.temperature()))
print("Altitude: " + str(mp.altitude()))
mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
print("Pressure: " + str(mpp.pressure()))


si = SI7006A20(py)
print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
print("Dew point: "+ str(si.dew_point()) + " deg C")
t_ambient = 24.4
print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")


lt = LTR329ALS01(py)
print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))

li = LIS2HH12(py)
print("Acceleration: " + str(li.acceleration()))
print("Roll: " + str(li.roll()))
print("Pitch: " + str(li.pitch()))

print("Battery voltage: " + str(py.read_battery_voltage()))

time.sleep(3)
py.setup_sleep(10)
py.go_to_sleep()