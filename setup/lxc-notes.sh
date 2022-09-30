USB Passthrough
===============
$ lsusb
Bus 002 Device 003: ID 0451:8041 Texas Instruments, Inc. 
Bus 002 Device 002: ID 0451:8041 Texas Instruments, Inc. 
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 021: ID 17ef:6047 Lenovo 
Bus 001 Device 031: ID 046d:082d Logitech, Inc. HD Pro Webcam C920
Bus 001 Device 004: ID 0451:8043 Texas Instruments, Inc. 
Bus 001 Device 005: ID 046d:0a01 Logitech, Inc. USB Headset
Bus 001 Device 033: ID 0fce:51da Sony Ericsson Mobile Communications AB 
Bus 001 Device 003: ID 0451:8043 Texas Instruments, Inc. 
Bus 001 Device 002: ID 072f:90cc Advanced Card Systems, Ltd ACR38 SmartCard Reader
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

$ lxc config device add c1 sony usb vendorid=0fce productid=51da

