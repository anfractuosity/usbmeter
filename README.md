# usbmeter

Extracts and graphs data from UM25C etc. USB power meters in Linux.

Based on the excellent reverse engineering found here - https://sigrok.org/wiki/RDTech_UM24C.  

# Install on arch

```
sudo pacman -S bluez
sudo pacman -S bluez-utils 
sudo pacman -S python-pybluez
pip3 install . --user
```

# Run on arch

Start the bluetooth service:

```
sudo systemctl start bluetooth
echo "power on" | bluetoothctl
```

It is then recommended to do the following, to view a live
graph of voltage, current and power:

```
usbmeter --addr <ADDRESS> --graph
```

You can also run without the --addr parameter, for the device
to be detected automatically, however some people have told 
me that this gives 'No services found for address ....' for them.

# Licence

MIT

