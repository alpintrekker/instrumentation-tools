import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI
# from ADS126x_constants import *

spi = SPI(0,0)

# class ADS126x():


START_PIN = "P9_23"
RSTN_PIN = "P9_24"
DRDY_PIN = "P9_26"

GPIO.setup(RSTN_PIN, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
GPIO.output(RSTN_PIN, GPIO.HIGH)

GPIO.setup(START_PIN, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(START_PIN, GPIO.LOW)

GPIO.setup(DRDY_PIN, GPIO.IN)


R0 = 100.0
A = 3.9083e-3
B = -5.775e-7
C = -4.183e-12

def R2C(R):
    if R >= 100.0:
        return (-R0*A
                +(R0**2 * A**2
                  - 4 * R0 * B * (R0 - R))**0.5)\
               /(2*R0*B)

def C2R(C):
    if C >= 0.0:
        return R0 * (1 + A * C + B * C**2)


c = 0


while True:
    try:
        GPIO.wait_for_edge(DRDY_PIN, GPIO.FALLING)
        # rp = spi.xfer2([0, 0, 0, 0, 0, 0])
        # data = (rp[1] << 24) | (rp[2] << 16) | (rp[3] << 8) | rp[4]
        print   data * 5000.0 / 2**32 # R2C(data * 5000.0 / 2**32)

    except KeyboardInterrupt:
        break


def ADS126xReadRegister(StartAddress, pdata):
    cmd = [0x20 + StartAddress, len(pdata) - 1]
    return spi.xfer2(cmd + pdata)[2:]

def ADS126xWriteRegister(StartAddress, pdata):
    cmd = [0x40 + StartAddress, len(pdata) - 1]
    return spi.xfer2(cmd + pdata)[2:]


def ADS126xReadData(self, NumBytes, DataByteStartNum):
    raise NotImplementedError



a12 = [0x11,0x06,0x00,0x60,0x87,0x12,0x18,0x06,
       0x00,0x00,0x00,0x40,0xB0,0x06,0x00,0x00,
       0x00,0x00,0x00,0x00]


a34 = [0x11,0x06,0x00,0x60,0x87,0x34,0x18,0x06,
       0x00,0x00,0x00,0x40,0xB0,0x06,0x00,0x00,
       0x00,0x00,0x00,0x00]

# IDAC-1mA-AIN4__AIN0-AIN1_cal_sinc4_100sps


r.write_register(1,a01)
r.write_register(1,a23)

a01 = [0x11,0x05,0x10,0x00,0x08,0x01,0x00,0x00,
       0x00,0x00,0x00,0x40,0x7B,0x60,0x00,0x00,
       0x00,0x00,0x00,0x00]

a23 = [0x11,0x05,0x10,0x00,0x08,0x23,0x00,0x00,
       0x00,0x00,0x00,0x40,0x7B,0x60,0x00,0x00,
       0x00,0x00,0x00,0x00]

while True:
    try:
        GPIO.wait_for_edge(r.DrdyPin, GPIO.FALLING)
        # rp = spi.xfer2([0, 0, 0, 0, 0, 0])
        # data = (rp[1] << 24) | (rp[2] << 16) | (rp[3] << 8) | rp[4]
        print   r.read_adc_data()* 5000.0 / 2**32 # R2C(data * 5000.0 / 2**32)

    except KeyboardInterrupt:
        break