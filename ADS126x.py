import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time

class Ads126x():
    def __init__(self, START_PIN, PWDN_PIN, DRDY_PIN, x = 2):
        GPIO.setup(START_PIN, GPIO.OUT)
        GPIO.output(START_PIN, GPIO.LOW)


#  Function Prototypes */

	# Low level

    def set_adc_CS(self, state):                              # CS pin control
        raise NotImplementedError

    def set_adc_START(self, state):                                 # START pin control
        raise NotImplementedError

    def ADS126xXferByte(self, cData):
        raise NotImplementedError
        # receive byte, simultaneously send data - this function realizes all
        # necessary functionality, the other Send/Receive methods are only
        # designed to improve readability of the code



	# Higher level

    def ADS126xReadData(self, NumBytes, DataByteStartNum):
        raise NotImplementedError

# int32_t ADS126xREADandWRITE(int NumDatBytes, int StartAddress, int NumRegs, unsigned char * pdata;
# unsigned char ADS126xReadADC2Data(bufferType_t *readbuffer;

# read a number of consecutive registers to a given array pointer
    def ADS126xReadRegister(self, StartAddress, NumRegs, pdata):
        raise NotImplementedError


# write a number of consecutive registers from a given array pointer
    def ADS126xWriteRegister(self, StartAddress, NumRegs,  pdata):
        raise NotImplementedError

# Reset by command (alternative to pin
    def ADS126xSendResetCommand(self):
        raise NotImplementedError

# Start by command (alternative to pin
    def ADS126xSendStartCommand(self):
        raise NotImplementedError

    def ADS126xSendStopCommand(self):
        raise NotImplementedError

    def ADS126xSendADC2StartCommand(self):
        raise NotImplementedError

    def ADS126xSendADC2StopCommand(self):
        raise NotImplementedError
