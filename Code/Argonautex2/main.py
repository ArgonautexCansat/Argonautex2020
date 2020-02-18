import time
import pycom
import machine
import socket
import _thread

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

# Sensor objects
py  = Pysense()

mp  = MPL3115A2(py,mode=ALTITUDE)
mpp = MPL3115A2(py,mode=PRESSURE)
si  = SI7006A20(py)
lt  = LTR329ALS01(py)
li  = LIS2HH12(py)

# Sensor values
class DataPacket(object):
    # Battery percentage
    battery_percent = None

    # Atmospheric values
    temperature = None
    altitude    = None
    pressure    = None
    humidity    = None

    # Gyro rotation
    roll  = None
    pitch = None
    yaw   = None

packet = DataPacket()

def read_sensors(delay, id):
    while True:
        packet.temperature = mp.temperature()
        packet.altitude = mp.altitude()
        packet.pressure = mpp.pressure()
        packet.humidity = si.humidity()

        packet.roll = li.roll()
        packet.pitch = li.pitch()

def send_data(delay, id):
    while True:
        print("Temperature: " + str(packet.temperature))
        print("Altitude: " + str(packet.altitude))
        print("Pressure: " + str(packet.pressure))
        print("Humidity: " + str(packet.humidity))

        time.sleep(3)

_thread.start_new_thread(read_sensors, (0, 0))
_thread.start_new_thread(send_data, (0, 0))

