#!/usr/bin/python2
# encoding: utf-8

##################
# Description

##################
# Copyright 2021 Kazuya Fujimoto
# License: MIT
# Permission is hereby granted, free of charge, 
# to any person obtaining a copy of this software 
# and associated documentation files (the "Software"),
# to deal in the Software without restriction,
# including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons 
# to whom the Software is furnished to do so.
# The above copyright notice and this permission notice 
# hall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import time
import Adafruit_BBIO.SPI as SPI

from Adafruit_BBIO.SPI import SPI
import hal, argparse

# Process of the code
# - Read the parameters
#   - Params
#     - Heater num
#     - SPI ch to be used

class Heater:
    def __init__(self, id, h, default_out=0):
        self.id = id
        self.out = default_out
        self.current = 0
        self.assign_pin(h)

    def update_target(self, target):

        if target > 0 or target < 256:
            self.target = target
        else:
            raise ValueError("Target must be 0 to 255")
    
    def assign_pin(self, h):
        self.out_pin = h.newpin(self.id+".out", hal.HAL_FLOAT, hal.HAL_OUT)
        self.in_pin = h.newpin(self.id+".in", hal.HAL_FLOAT, hal.HAL_IN)
    
    def generate_spi_frame(self):
        duty = int(255 * self.out_pin)
        cmd0 = 0x20 + id
        cmd1 = 0x42 + (0x03 & (duty>>6))
        cmd2 = 0x80 + (duty & 0x3f) 
        cmd3 = 0xc0 
        print(hex(0xc0 + (self.out_pin & 0x3f)))
        return [cmd0, cmd1, cmd2, cmd3]

    def read_spi_frame(self, reply):
        val = ((reply[1] & 0x0f) <<6) + (reply[2] & 0x3f)
        self.in_pin = val

def generate_pin(heater_names, h):
    pins = []
    for heater in heater_names:
        pins.append(Heater(heater), h)
        
    return pins

def generate_spi_frame(pins):
    return [pin.out_pin.value for pin in pins]


    
def initialize(comp_name, heater_ids, spi_ch):
    # Initialize hal
    h = hal.component(comp_name)
    h.newpin("test", hal.HAL_FLOAT, hal.HAL_OUT)
    heaters = []
    #heater_split = heater_ids.split(",")
    
    for heater in heater_ids:
        heaters.append(Heater(heater, h))

    spi = SPI(1, int(spi_ch))
    
    return h, heaters, spi

parser = argparse.ArgumentParser(description='user comp for spin commun to pic')

parser.add_argument('-n', '--name', help='Component name')
parser.add_argument('-t', '--heaters', help='List of heaters, sample: h1,h2,h3')
parser.add_argument('-c', '--channel', help='Sample  chennel')

args = parser.parse_args()
print(args.channel)
print(args.heaters)
h, heaters, spi = initialize(args.name, args.heaters, args.channel)
print(heaters)
spi.mode = 0
count = 0
large = 1000
num = 100
txd = [i for i in range(num)]
while True:

    # debug: count up
    for heater in heaters:
        print(h.out_pin)
        cmd = heater.prepare_cmd()
        rep = spi.xfer(heater.generate_spi_frame(0))
        heater.read_spi_frame(rep)
        time.sleep(0.1)

    # print(spi.xfer2(txd))    
