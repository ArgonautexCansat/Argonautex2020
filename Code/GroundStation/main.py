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
s.setblocking(False)

f = open("sym_keyfile.key")
pk = f.read()
f.close()

while True: 
    data = s.recv(64)

    if len(data) > 0:
        iv = crypto.getrandbits(128)
        cipher = AES(pk, AES.MODE_CFB, data[:16])
        msg = cipher.decrypt(data[16:])

        print(struct.unpack('ffff', msg))

    time.sleep_ms(100)

