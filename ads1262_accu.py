import Adafruit_BBIO.GPIO as GPIO

GPIO.setup("P9_13", GPIO.IN)
c = 0


while True:
    GPIO.wait_for_edge("P9_13", GPIO.FALLING)
    print "#",
    c += 1
    if c % 25 == 0:
        print "\n"