#!/usr/bin/python3

# sudo systemctl start bluetooth
# echo "power on" | bluetoothctl

from bluetooth import *
import sys
import time
import argparse

parser = argparse.ArgumentParser(description="CLI for USB Meter")
parser.add_argument("--addr", dest="addr",type=str,help="Address of USB Meter")
args = parser.parse_args()

addr = None
if args.addr:
    addr = args.addr
else:
    nearby_devices = discover_devices(lookup_names = True)
    addr = None
    for v in nearby_devices:
        if v[1] == "UM25C":
            print("Found",v[0])
            addr = v[0]
            break

service_matches = find_service(address=addr)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

sock=BluetoothSocket( RFCOMM )
res = sock.connect((host, port))

sock.send((0xF0).to_bytes(1,byteorder='big'))

d = b""
while True:

    d += sock.recv(130)

    if len(d) != 130:
        continue

    data = {}

    data['Volts'] = struct.unpack(">h",d[2:3+1])[0]/1000.0 # volts
    data['Amps'] = struct.unpack(">h",d[4:5+1])[0]/1000.0 # amps
    data['Watts'] = struct.unpack(">I",d[6:9+1])[0]/1000.0 # watts
    data['temp_C'] = struct.unpack(">h",d[10:11+1])[0]      # temp in C
    data['temp_F'] = struct.unpack(">h",d[12:13+1])[0]      # temp in F

    g = 0
    for i in range(16,95,8):
        ma, mw = struct.unpack(">II",d[i:i+8]) # mAh,mWh respectively
        gs = str(g)
        data[gs+'_mAh'] = ma
        data[gs+'_mWh'] = mw
        g+=1

    data['data_line_pos_volt'] = struct.unpack(">h",d[96:97+1])[0]/100.0 # data line pos voltage
    data['data_line_neg_volt'] = struct.unpack(">h",d[98:99+1])[0]/100.0 # data line neg voltage
    data['resistance'] = struct.unpack(">I",d[122:125+1])[0]/10.0 # resistance
    
    print(data)

    d=b""
    sock.send((0xF0).to_bytes(1,byteorder='big'))

    time.sleep(0.01)
    
sock.close()


