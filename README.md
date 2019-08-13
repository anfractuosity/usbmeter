# usbmeter

Extracts and graphs data from UM25C etc. USB power meters in Linux.

Based on the excellent reverse engineering found here - https://sigrok.org/wiki/RDTech_UM24C.  

To view a live graph of voltage/current/wattage:

```
./usbmeter.py --graph
```

# Install on arch

```
sudo pacman -S bluez
sudo pacman -S bluez-utils 
sudo pacman -S python-pybluez
```

# Todo

* Store data to a user specified file
* Tidy code

# Licence

MIT

