import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI
import Adafruit_BBIO.PWM as PWM
import time
from datetime import datetime
import numpy as np
import logging
import threading
import Queue

from ws4py.client.threadedclient import WebSocketClient

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
dataQueue = Queue.Queue()
spQueue = Queue.Queue()
cvQueue = Queue.Queue(maxsize = 1)

class Heater:
    def __init__(self, pin, freq, inv = 0):
        self.pin = pin
        PWM.start(self.pin, 0, freq, inv)

    def set_duty(self, duty):
        PWM.set_duty_cycle(self.pin, duty)

class Oven:
    def __init__(self):
        self.psu_pin = "P9_15"
        self.fan_pin = "P9_14"
        self.H1_pin = "P8_13"
        self.H2_pin = "P9_42"
        self.H1 = Heater(self.H1_pin, 1)
        self.H2 = Heater(self.H2_pin, 1)
        self.fan_init()
        self.psu_on()



    def oven_cleanup(self):
        PWM.cleanup()
        GPIO.cleanup()

    def fan_init(self):
        PWM.start(self.fan_pin, 9, 100)

    def fan_duty(self, duty):
        if 9.55 <= duty <= 18.0:
            PWM.set_duty_cycle(self.fan_pin, duty)

    def fan_min(self):
        self.fan_duty(9.7)
        time.sleep(0.5)
        self.fan_duty(9.55)

    def fan_off(self):
        PWM.set_duty_cycle(self.fan_pin, 9)

    def psu_on(self):
        GPIO.setup(self.psu_pin, GPIO.OUT)
        GPIO.output(self.psu_pin, GPIO.HIGH)

    def psu_off(self):
        GPIO.output(self.psu_pin, GPIO.LOW)

class Ads126x:
    def __init__(self, start_pin, rstn_pin, drdy_pin, spi, x=2):

        self.StartPin = start_pin
        self.RstnPin = rstn_pin
        self.DrdyPin = drdy_pin
        self.Spi = spi
        self.chip = x
        self.gpio_init()

    def gpio_init(self):
        GPIO.setup(self.RstnPin, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.RstnPin, GPIO.LOW)

        GPIO.setup(self.StartPin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
        GPIO.output(self.StartPin, GPIO.LOW)

        GPIO.setup(self.DrdyPin, GPIO.IN)

    def power_up(self):
        GPIO.output(self.RstnPin, GPIO.HIGH)

    def power_down(self):
        GPIO.output(self.RstnPin, GPIO.LOW)

    def start_conversion(self):
        GPIO.output(self.StartPin, GPIO.HIGH)

    def stop_conversion(self):
        GPIO.output(self.StartPin, GPIO.LOW)

    def read_adc_data(self, num_bytes=6, dbsn=1):
        a = []
        for i in range(num_bytes):
            a.append(0)
        rp = self.Spi.xfer2(a)
        data = (rp[dbsn + 0] << 24) | \
               (rp[dbsn + 1] << 16) | \
               (rp[dbsn + 2] << 8) | \
               (rp[dbsn + 3])
        return data

    def read_register(self, start_address, num_bytes):
        a = []
        for i in range(num_bytes):
            a.append(0)
        cmd = [0x20 + start_address, num_bytes -1]
        return self.Spi.xfer2(cmd + a) [2:]

    def write_register(self, start_address, data):
        cmd = [0x40 + start_address, len(data) - 1]
        return self.Spi.xfer2(cmd + data)[2:]

    def read_n_sample_w_config(self, n, conf):
        self.stop_conversion()
        self.write_register(1,conf)
        self.start_conversion()
        read_data = []
        read_timestamps = []
        for i in range(n):
            GPIO.wait_for_edge(r.DrdyPin, GPIO.FALLING)
            read_timestamps.append(datetime.utcnow().isoformat())
            read_data.append(self.read_adc_data())
        return read_timestamps, read_data

class DdClient(WebSocketClient):
    parent = None

    def opened(self):
        self.send('Hi, from ADS1262!')

    def closed(self, code, reason=None):
        logging.debug("Closed down " + str(code) + ' ' + str(reason))

    def received_message(self, m):
        logging.debug(m)


def R2C(R):
    if R >= 100.0:
        return (-R0 * A
                + (R0 ** 2 * A ** 2
                   - 4 * R0 * B * (R0 - R)) ** 0.5) \
               / (2 * R0 * B)

def C2R(C):
    if C >= 0.0:
        return R0 * (1 + A * C + B * C ** 2)

class AdcReader(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, adc, config):
        super(AdcReader, self).__init__()
        self._stop = threading.Event()
        self.adc = adc
        self.config = config

    # def start(self):
    #     self._stop.clear()
    #     self.run()

    def stop(self):
        self._stop.set()


    def stopped(self):
        return self._stop.isSet()


    def run(self):
        logging.debug('Starting')
        buff = ''
        while not self._stop.isSet():
            try:
                for key in self.config.keys():
                    timestamps, data = \
                        self.adc.read_n_sample_w_config(20, self.config[key])
                    a = np.array(data, np.dtype('float'))

                    # dataQueue.put( str(key)[0:3] + ' ' + \
                    #       str(np.round(R2C(np.mean(a / 2 ** 31) * 1000 / K), decimals=3)) + \
                    #       ' +- ' + \
                    #       str(np.round(R2C(100 + np.std(a / 2 ** 31) * 1000 / K), decimals=3)))
                    pkt = {'channel': str(key)[0:3],
                           'timstp': timestamps,
                           'data': data,
                           'mean': R2C(np.mean(a / 2 ** 31) * 1000 / K),
                           'std' : R2C(100 + np.std(a / 2 ** 31) * 1000 / K)}
                    # ws.send(json.dumps(pkt))
                    dataQueue.put(pkt)
                    eV.set()
            except KeyboardInterrupt:
                self.stop()
            except:
                errMsg = "Reader thread is terminated."
                logging.debug(errMsg)
                break

        logging.debug('Stopping')

class PID_calc(threading.Thread):

    def __init__(self):
        super(PID_calc, self).__init__()
        self._stop = threading.Event()
        self.currentSetpoint = None
        self.I = 0.0

        self.kP = 11
        self.kI = 0.1
        self.kD = 1200

        self.CV = 0.0
        self.last_10_errors = np.array([], np.dtype('float'))

    # def start(self):
    #     self._stop.clear()
    #     self.run()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        logging.debug('Starting')
        de_dt = 0.0
        err_h = 3
        x = range(err_h)

        while not self._stop.isSet():
            while not spQueue.empty():
                self.currentSetpoint = spQueue.get()
                self.I = 0.0
            eV.wait()
            while not dataQueue.empty():
                reading = dataQueue.get()
                print reading
                if self.currentSetpoint:
                    e = self.currentSetpoint - reading['mean']
                    self.I += e
                    self.last_10_errors = np.append(self.last_10_errors, e)
                    if np.shape(self.last_10_errors)[0] > err_h:
                        self.last_10_errors = self.last_10_errors[-err_h:]
                        de_dt = np.polyfit(x, self.last_10_errors, 1)[0]

                    if (self.CV + self.kI * self.I) > 100:
                        self.CV = 100
                    elif (self.CV + self.kI * self.I) < 0:
                        self.CV = 0
                    else:
                        self.CV += self.kI * self.I

                    if (self.CV + self.kD * de_dt) > 100:
                        self.CV = 100
                    elif (self.CV + self.kD * de_dt) < 0:
                        self.CV = 0
                    else:
                        self.CV += self.kD * de_dt


                    if (self.CV + self.kP * e) > 100:
                        self.CV = 100
                    elif (self.CV + self.kP * e) < 0:
                        self.CV = 0
                    else:
                        self.CV += self.kP * e
                    print self.CV
                    try:
                        cvQueue.put_nowait(self.CV)
                    except Queue.Full:
                        cvQueue.get()
                        cvQueue.put_nowait(self.CV)

            eV.clear()


        logging.debug('Stopping')


class CV_setter(threading.Thread):
    def __init__(self):
        super(CV_setter, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        logging.debug('Starting')

        while not self._stop.isSet():
            while not cvQueue.empty():
                cv = cvQueue.get()
                o.H1.set_duty(cv)
            time.sleep(1)


        logging.debug('Stopping')

if __name__ == "__main__":

    R0 = 100.0
    A = 3.9083e-3
    B = -5.775e-7
    C = -4.183e-12
    K = .999379



    _START_PIN = "P9_23"
    _RSTN_PIN = "P9_24"
    _DRDY_PIN = "P9_26"

    _spi = SPI(0,0)

    readconfig = {'A01_IDAC2_1mA_A4_REF_A23':
                      [0x11, 0x05, 0x00, 0x60, 0x07, 0x01, 0x00, 0x00,
                       0x00, 0x00, 0x00, 0x40, 0x4B, 0x60, 0x12, 0x00,
                       0x00, 0x00, 0x00, 0x00]}  # ,
                  # 'A67_IDAC2_1mA_A4_REF_A23':
                  #     [0x11, 0x05, 0x00, 0x60, 0x07, 0x67, 0x00, 0x00,
                  #      0x00, 0x00, 0x00, 0x40, 0x4B, 0x60, 0x12, 0x00,
                  #      0x00, 0x00, 0x00, 0x00]}

    r = Ads126x(_START_PIN, _RSTN_PIN, _DRDY_PIN, _spi)
    r.power_up()
    o = Oven()
    time.sleep(5)
    o.fan_min()
    eV = threading.Event()
    pr = PID_calc()
    pr.start()
    ar = AdcReader(r, readconfig)
    ar.start()
    cvs = CV_setter()
    cvs.start()

    spQueue.put(120)








    # try:
    #     ws = DdClient('ws://192.168.0.54:18080/Si', protocols=['http-only', 'chat'])
    #     ws.connect()
    #     # ws.run_forever()
    # except:
    #     ws = None
    #     logging.warning('Connecting to ws was unsuccesful')

