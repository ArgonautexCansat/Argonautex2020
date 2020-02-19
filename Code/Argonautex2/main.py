import time
import pycom
import machine
import socket
import _thread
import struct
import crypto

from crypto import AES
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
lora = LoRa(mode = LoRa.LORA, region = LoRa.EU868, frequency = 868000000,
            tx_power = 14, bandwidth = LoRa.BW_125KHZ, sf = 7, preamble = 8,
            coding_rate = LoRa.CODING_4_5, power_mode = LoRa.ALWAYS_ON,
            tx_iq = False, rx_iq = False, adr = False, public = True, 
            tx_retries = 1, device_class = LoRa.CLASS_A)

# Create raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Sensor objects
py  = Pysense()

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
        mp  = MPL3115A2(py,mode=ALTITUDE)
        packet.temperature = mp.temperature()  
        packet.altitude = mp.altitude()

        mpp = MPL3115A2(py,mode=PRESSURE)
        packet.pressure = mpp.pressure()
        packet.humidity = si.humidity()

        packet.roll = li.roll()
        packet.pitch = li.pitch()

        time.sleep_ms(delay)

def send_data(delay, id):
    while True:
        if packet.temperature == None or packet.altitude == None or packet.pressure == None or packet.humidity == None:
            continue

        print("Temperature: " + str(packet.temperature))
        print("Altitude: " + str(packet.altitude))
        print("Pressure: " + str(packet.pressure))
        print("Humidity: " + str(packet.humidity))

        f = open("sym_keyfile.key")
        pk = f.read()
        f.close()

        pac = struct.pack('fffff', packet.temperature, packet.altitude, packet.pressure, packet.humidity, 2.32)
        print(len(pac))
        iv = crypto.getrandbits(128)
        cipher = AES(pk, AES.MODE_CFB, iv)
        msg = iv + cipher.encrypt(pac)
        print(len(msg))

        s.send(msg)

        print("Sent packet.\n")

        time.sleep_ms(delay)

_thread.start_new_thread(read_sensors, (0, 0))
_thread.start_new_thread(send_data, (250, 0))

