from machine import SD
from machine import UART
import pycom
import os

uart = UART(0, 115200)
os.dupterm(uart)

print("Starting Argonautex II ground station...")

# Disable unnecessary pycom features
pycom.wifi_on_boot(False) 
pycom.heartbeat(False)
pycom.rgbled(0)

# SD Card header
try:       
    sd = SD()
    os.mount(sd, '/sd')

    files = os.listdir('/sd')

    # data.csv doesn't exist
    if 'DATA.CSV' not in files:
        f = open('/sd/data.csv', 'w')
        f.write('Test Header')
        f.close()

        print('Created data.csv')

    print('SD Card initialised.')
except:
    print('SD Card error!')
