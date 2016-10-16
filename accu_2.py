from Adafruit_BBIO.SPI import SPI
import struct
import time

spi = SPI(0,0)
spi.mode = 1
spi.msh = 300000
spi.xfer([0b00011000, 0x02])


def decode_sent_command(ser_cmd):
    cmd_bits = (ser_cmd & (((1<<6) - 1)<<10))>>10
    data_bits = ser_cmd & ((1<<10)-1)
    return bin(cmd_bits)[2:], data_bits


def send_cmd(cmd,data):
    ser_cmd = (cmd << 10) | (data & ((1<<10)-1))
    w0 = ser_cmd >> 8
    w1 = ser_cmd & ((1<<8)-1)
    return [w0, w1]

 # write to RDAC
spi.xfer(list(struct.unpack('BB', struct.pack('>H', 1 << 10 | 0))))

 # read RDAC
spi.xfer(list(struct.unpack('BB', struct.pack('>H', 0b10 << 10 | 0))))

 # read Control register
spi.xfer(list(struct.unpack('BB', struct.pack('>H', 0b111 << 10 | 0))))
spi.readbytes(2)

for i in range(1024):
    spi.xfer(list(struct.unpack('BB', struct.pack('>H', 1 << 10 | i))))
    time.sleep(.2)


spi.writebytes([0x0,0x0])
spi.writebytes([0x18,0x02])
spi.writebytes([0x05,0x00])
spi.writebytes([0x08,0x0])
spi.writebytes([0x0,0x0])
spi.writebytes([0x0,0x0])
spi.writebytes([0x0,0x0])

spi.xfer([0x0,0x0])
spi.xfer([0x18,0x02])
spi.xfer([0x05,0x00])
spi.xfer([0x08,0x0])
spi.xfer([0x0,0x0])


class voltage_divider:
    def __init__(self):
        self.R1 = 1e20
        self.R2 = 1e20
