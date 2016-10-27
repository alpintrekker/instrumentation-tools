from mcp2210 import MCP2210
from mcp2210 import commands
import struct
dev = MCP2210(0x04D8, 0x00DE)

class AD5292:
    def __init__(self, mcp_dev, cs_pin):
        if isinstance(mcp_dev, MCP2210):
            self.dev = mcp_dev
        self.cs = cs_pin
        self.spi_mode = 1
        self.bit_rate = 300000
        self.curr_chip_settings = commands.ChipSettings
        self.curr_transfer_settings = commands.SPISettings

    def _prepare_spi(self):
        self.curr_chip_settings = self.dev.chip_settings
        self.curr_chip_settings.pin_designations[self.cs] = 1
        self.dev.chip_settings = self.curr_chip_settings

        self.curr_transfer_settings = self.dev.transfer_settings
        self.curr_transfer_settings.bit_rate = self.bit_rate
        self.curr_transfer_settings.idle_cs = 1<<self.cs
        self.curr_transfer_settings.active_cs = 0
        self.dev.transfer_settings = self.curr_transfer_settings

    def set_wiper(self, pos):
        # self._prepare_spi()
        self.dev.transfer('\x00\x00')   # NoOp
        self.dev.transfer('\x18\x02')   # allow update of wiper position through digital Interface
        self.dev.transfer(
            struct.pack('>H',(1 << 10) | (pos & ((1<<10)-1))))   # convert to LE, aka > formatting character

        # self.dev.transfer('')
        # raise NotImplementedError

    def read_wiper(self):
        self.dev.transfer('\x08\x00')   # prepare read back of RDAC
        return struct.unpack('H', self.dev.transfer('\x00\x00'))
        # NoOp, last 10 bits of the returned 16 bit word is the actual wiper position


dgp = AD5292(dev, 5)
dgp._prepare_spi()