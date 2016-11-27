import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
psu_pin = "P9_15"
fan_pin = "P9_14"
H1_pin = "P8_13"
H2_pin = "P9_42"

def oven_init():
    # H1 = Heater(H1_pin, 1)
    # H2 = Heater(H2_pin, 1)
    fan_init()
    psu_on()

def oven_cleanup():
    PWM.cleanup()
    GPIO.cleanup()

def fan_init():
    PWM.start(fan_pin, 9, 100)

def fan_duty(duty):
    if 9.55 <= duty <= 18.0:
        PWM.set_duty_cycle(fan_pin, duty)

def fan_min():
    fan_duty(9.7)
    time.sleep(0.5)
    fan_duty(9.55)

def fan_off():
    PWM.set_duty_cycle(fan_pin, 9)

def psu_on():
    GPIO.setup(psu_pin, GPIO.OUT)
    GPIO.output(psu_pin, GPIO.HIGH)

def psu_off():
    GPIO.output(psu_pin, GPIO.LOW)

class Heater():
    def __init__(self, pin, freq, inv = 0):
        self.pin = pin
        PWM.start(self.pin, 0, freq, inv)

    def set_duty(self, duty):
        PWM.set_duty_cycle(self.pin, duty)



