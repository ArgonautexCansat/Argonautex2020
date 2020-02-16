import pycom

print("Iniciando Argonautex II...")

# Disable unnecessary pycom features
pycom.wifi_on_boot(False) 
pycom.heartbeat(False)