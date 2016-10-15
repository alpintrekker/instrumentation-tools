from mcp2210 import MCP2210

dev = MCP2210(0x04D8, 0x00DE)
curr_spi = dev.transfer_settings
