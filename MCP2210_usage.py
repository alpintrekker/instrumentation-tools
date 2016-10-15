import hid
import numpy as np
import struct

mydev = hid.Device(0x04D8, 0x00DE)

buff = np.zeros(64,dtype = 'int8').tolist()

buff[0]=0x61
buff[1]=0x10

cmd = struct.pack('B'*64, *buff)
mydev.write(cmd)
resp = mydev.read(64)
ret = struct.unpack('B'*64, resp)


# GET SPI POWER-UP TRANSFER SETTINGS

class my_mcp2210:

    def __init__(self):
        self.dev = hid.Device(0x04D8, 0x00DE)
        self.SPI = {}

    def get_spi_powerup_transfer_settings(self):
        buff = np.zeros(64, dtype='int8').tolist()
        buff[0]=0x61
        buff[1]=0x10

        cmd = struct.pack('B'*64, *buff)
        self.dev.write(cmd)
        resp = self.dev.read(64)
        self.SPI['bit_rate'] = struct.unpack('<I', resp[4:8])[0]
        self.SPI['idle_CS'] = struct.unpack('H', resp[8:10])[0]
        self.SPI['active_CS'] = struct.unpack('H', resp[10:12])[0]
        self.SPI['delay_CS_2_data'] = struct.unpack('H', resp[12:14])[0]
        self.SPI['delay_data_2_CS'] = struct.unpack('H', resp[14:16])[0]
        self.SPI['delay_data_2_data'] = struct.unpack('H', resp[16:18])[0]
        self.SPI['bytes_to_transfer'] = struct.unpack('H', resp[18:20])[0]
        self.SPI['spi_mode'] = struct.unpack('B', resp[20:21])[0]


