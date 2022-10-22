import time
import Adafruit_BBIO.SPI as SPI

from Adafruit_BBIO.SPI import SPI
# spi = SPI(bus, device) #/dev/spidev<bus>.<device>
def prepare_cmd(id, duty):
    cmd0 = 0x20 + id
    cmd1 = 0x42 + (0x03 & (duty>>6))
    cmd2 = 0x80 + (duty & 0x3f) 
    cmd3 = 0xc0 
    return [cmd0, cmd1, cmd2, cmd3]

def parse_reply(rep):
    return ((rep[1] & 0x0f) <<6) + (rep[2] & 0x3f)
# /dev/spidev0.0

spi = SPI(1, 0)
spi.mode = 0 
spi.cshigh = False 
spi.msh = 50000
c = 0
for i in range(1000000):
#while True:
    rep = []
    print(prepare_cmd(0, c*50)) 
    rep = spi.xfer2(prepare_cmd(0, c*50))

    c +=1
    c = c%4
    temp = parse_reply(rep)
    print([hex(r) for r in rep])
    print("temp="+str(temp))
    
    time.sleep(0.1)

spi.close()
