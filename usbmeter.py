#!/usr/bin/python3

# sudo systemctl start bluetooth
# echo "power on" | bluetoothctl

import collections
from bluetooth import *
import sys
import argparse
import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import matplotlib
import time
import pickle

parser = argparse.ArgumentParser(description="CLI for USB Meter")
parser.add_argument("--addr", dest="addr",type=str,help="Address of USB Meter")
parser.add_argument("--graph", dest="graph",help="Live graphing",action='store_true')

args = parser.parse_args()

addr = None

if args.addr:
    addr = args.addr
    sock=BluetoothSocket( RFCOMM )
    res = sock.connect((addr, 1))
else:
    nearby_devices = discover_devices(lookup_names = True)
    
    for v in nearby_devices:
        if "UM25C" in v[1]:
            print("Found",v[0])
            addr = v[0]
            break

    service_matches = find_service(address=addr)

    if len(service_matches) == 0:
        print("No services found for address ",addr)
        quit()

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("connecting to \"%s\" on %s:%d" % (name, host, port))

    sock=BluetoothSocket( RFCOMM )
    res = sock.connect((host, port))

leng = 20

volts = collections.deque(maxlen=leng)
currents = collections.deque(maxlen=leng)
watts = collections.deque(maxlen=leng)
times = collections.deque(maxlen=leng)

if args.graph is not None:
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    f, (ax1, ax2, ax3) = plt.subplots(3,sharex=True)
    plt.show(block=False)

sock.send((0xF0).to_bytes(1,byteorder='big'))

pickle_file = open('data.pickle', 'wb')

d = b""
while True:

    d += sock.recv(130)

    if len(d) != 130:
        continue

    data = {}

    data['Volts'] = struct.unpack(">h",d[2:3+1])[0]/1000.0  # volts
    data['Amps'] = struct.unpack(">h",d[4:5+1])[0]/10000.0  # amps
    data['Watts'] = struct.unpack(">I",d[6:9+1])[0]/1000.0  # watts
    data['temp_C'] = struct.unpack(">h",d[10:11+1])[0]      # temp in C
    data['temp_F'] = struct.unpack(">h",d[12:13+1])[0]      # temp in F

    volts.append(data['Volts'])
    currents.append(data['Amps'])
    watts.append(data['Watts'])

    utc_dt = datetime.datetime.now(datetime.timezone.utc) # UTC time
    dt = utc_dt.astimezone() # local time
    times.append(dt)
    data['time'] = dt

    g = 0
    for i in range(16,95,8):
        ma, mw = struct.unpack(">II",d[i:i+8])              # mAh,mWh respectively
        gs = str(g)
        data[gs+'_mAh'] = ma
        data[gs+'_mWh'] = mw
        g+=1

    data['data_line_pos_volt'] = struct.unpack(">h",d[96:97+1])[0]/100.0 # data line pos voltage
    data['data_line_neg_volt'] = struct.unpack(">h",d[98:99+1])[0]/100.0 # data line neg voltage
    data['resistance'] = struct.unpack(">I",d[122:125+1])[0]/10.0        # resistance
    
    if args.graph is not None and plt.get_fignums():
        ax1.clear()
        ax1.plot(times, volts)
        ax2.clear()
        ax2.plot(times, currents)
        ax3.clear()
        ax3.plot(times, watts)

        ax1.title.set_text("Voltage")
        ax1.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        ax1.fmt_xdata = DateFormatter('%H:%M:%S')
        f.autofmt_xdate()

        ax2.title.set_text("Current")
        ax3.title.set_text("Wattage")

        f.canvas.draw()
        f.canvas.flush_events()
        plt.pause(0.001)

    print(data)
    pickle.dump(data,pickle_file)

    d=b""
    sock.send((0xF0).to_bytes(1,byteorder='big'))


    time.sleep(0.01)
    
sock.close()


