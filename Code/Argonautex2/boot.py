from machine import SD
import pycom
import os

print("Starting Argonautex II...")

# Disable unnecessary pycom features
pycom.wifi_on_boot(False) 
pycom.heartbeat(False)

# SD Card header
try:       
    sd = SD()
    os.mount(sd, '/sd')

    files = os.listdir('/sd')

    # data.csv doesn't exist
    if 'data.csv' not in files:
        f = open('/sd/data.csv', 'w')
        f.write('Test Header')
        f.close()

        print('Created data.csv')
except:
    print('SD Card error!')
