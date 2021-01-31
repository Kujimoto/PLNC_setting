# About
This is a repository to host the machinekit setting for self-made 3d printer.
Contents of the files refer CRAMPS (https://github.com/machinekit/machinekit/blob/master/configs/ARM/BeagleBone/CRAMPS/CRAMPS.ini)
Settings is tentatively named as PLNC stands for plastic NC.

# Contents
- PLNC.hal: .hal file to set hardware abstraction layer
- PLNC.ini: .ini file for initialize machinekit
- PLNC.bbio: bbio files to set pinmux setup

# Current status
2021/1/31 created repository as a starting point.

# ToDos
- [ ] Establish minimal setup for stepping motor drive with pru.
- [ ] Run user defined python module from .ini
- [ ] Communicate with dauhter board via spi from python
