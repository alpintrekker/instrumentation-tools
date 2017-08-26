import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI
import Adafruit_BBIO.PWM as PWM
import time
from datetime import datetime
import numpy as np
import pandas as pd
import logging
import threading
import Queue
import json

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

    def sfoCal(self):
        self.write_register(6, [0xff])
        self.Spi.xfer2([0x19])

    def sioCal(self,mux):
        self.power_down()
        self.power_up()
        self.write_register(6, [mux])
        self.Spi.xfer2([0x16])

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
        # logging.debug(m)
        pass


def R2C(R):
    if R >= 100.0:
        return (-R0 * A
                + (R0 ** 2 * A ** 2
                   - 4 * R0 * B * (R0 - R)) ** 0.5) \
               / (2 * R0 * B)
    else:
        return 0

def C2R(c):
    if c >= 0.0:
        return R0 * (1 + A * c + B * c ** 2)

def copy_curr_OFCAL_to_readconfig():
    for key in readconfig.keys():
        readconfig[key][6:9] = r.read_register(7,3)
        print key, '[', \
            ', '.join('{:02x}'.format(x) for x in readconfig[key]),\
            ']'

def twos_compl(val, bits=32):
    if (val & (1 << (bits -1))) != 0:
        val = val - (1 << bits)
    return val

tc = np.vectorize(twos_compl)

class AdcReader(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, adc, config, ws_=None, mqtt_=None):
        super(AdcReader, self).__init__()
        self._stop = threading.Event()
        self.ws = ws_
        self.mqtt = mqtt_
        self.adc = adc
        self.config = config
        self.datalog = None

    def stop(self):
        self._stop.set()
        self.adc.stop_conversion()

    def stopped(self):
        return self._stop.isSet()

    def save_log(self):
        if self.datalog is not None:
            self.datalog.to_pickle(datetime.utcnow().isoformat().replace(':', '-').replace('.', '-') + '.pkl')

    def clear_log(self):
        self.datalog = None


    def run(self):
        logging.debug('Starting')
        buff = ''
        while not self._stop.isSet():
            try:
                for key in self.config.keys():
                    timestamps, data = \
                        self.adc.read_n_sample_w_config(10, self.config[key])
                    a = np.array(data, np.dtype('float'))

                    # dataQueue.put( str(key)[0:3] + ' ' + \
                    #       str(np.round(R2C(np.mean(a / 2 ** 31) * 1000 / K), decimals=3)) + \
                    #       ' +- ' + \
                    #       str(np.round(R2C(100 + np.std(a / 2 ** 31) * 1000 / K), decimals=3)))
                    self.pkt = {'channel': str(key)[0:3],
                           'timstp': timestamps,
                           'data': data,
                           # 'mean': np.mean(tc(a)) ,
                           'mean': R2C(np.mean(a / 2 ** 31) * 1000 / K),
                           # 'std' : np.std(tc(a))}
                           'std' : R2C(100 + np.std(a / 2 ** 31) * 1000 / K)}
                    # ws.send(json.dumps(pkt))
                    dataQueue.put(self.pkt)

                    df = pd.DataFrame({'channel': self.pkt['channel'],
                                       'value': self.pkt['mean'],
                                       'std': self.pkt['std']},
                                      index = [pd.Timestamp(self.pkt['timstp'][5])])
                    self.datalog = pd.concat([self.datalog, df])

                    if self.pkt['channel'] == 'A01' and self.ws is not None:
                        try:
                            ws.send(json.dumps({'toIIf': '_',
                                                'cmd': 'data',
                                                'type': 'T',
                                                'T1': self.pkt['mean'],
                                                'Date': timestamps[5]
                                                }))
                        except:
                            logging.debug('Unable to send data via websocket')

                    eV.set()
            except KeyboardInterrupt:
                self.stop()
            # except:
            #     errMsg = "ADC Reader thread is terminated."
            #     logging.debug(errMsg)
            #     break

        logging.debug('Stopping')

class PID_calc(threading.Thread):

    def __init__(self):
        super(PID_calc, self).__init__()
        self._stop = threading.Event()
        self.currentSetpoint = None
        self.I = 0.0

        self.kP = 16 # 14
        self.kI = 0.1
        self.kD = 80 # at err_h = 5, 120, for fine balance: 60 even 40

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
        err_h = 50
        x = range(err_h)

        while not self._stop.isSet():
            while not spQueue.empty():
                self.currentSetpoint = spQueue.get()
                # self.I = 0.0
            eV.wait()
            while not dataQueue.empty():
                reading = dataQueue.get()
                print '\n', \
                    reading['channel'],  ': ', \
                    np.round(reading['mean'], decimals=3), ' +- ', \
                    np.round(reading['std'], decimals=3),
                # if reading['channel'] == 'A01':
                #     print ' '
                if reading['channel'] == 'A01':
                    if self.currentSetpoint:
                        e = self.currentSetpoint - reading['mean']
                        self.I += e
                        self.CV = 0
                        self.last_10_errors = np.append(self.last_10_errors, e)
                        if np.shape(self.last_10_errors)[0] > err_h:
                            self.last_10_errors = self.last_10_errors[-err_h:]
                            de_dt = np.polyfit(x, self.last_10_errors, 1)[0]

                        # if (self.CV + self.kI * self.I) > 100:
                        #     self.CV = 100
                        # elif (self.CV + self.kI * self.I) < 0:
                        #     self.CV = 0
                        # else:
                        #     self.CV += self.kI * self.I
                        #
                        # if (self.CV + self.kD * de_dt) > 100:
                        #     self.CV = 100
                        # elif (self.CV + self.kD * de_dt) < 0:
                        #     self.CV = 0
                        # else:
                        #     self.CV += self.kD * de_dt
                        #
                        #
                        # if (self.CV + self.kP * e) > 100:
                        #     self.CV = 100
                        # elif (self.CV + self.kP * e) < 0:
                        #     self.CV = 0
                        # else:
                        #     self.CV += self.kP * e
                        self.CV = self.kP * e + \
                                  self.kI * self.I + \
                                  self.kD * de_dt
                        if self.CV < 0:
                            self.CV = 0
                        if self.CV > 100:
                            self.CV = 100
                        print self.CV, self.kP * e, self.kI * self.I, self.kD * de_dt,
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
        logging.debug('Starting CV_setter')

        while not self._stop.isSet():
            while not cvQueue.empty():
                cv = cvQueue.get()
                o.H1.set_duty(cv)
                o.H2.set_duty(cv)
            time.sleep(1)


        logging.debug('Stopping CV setter')

if __name__ == "__main__":

    _START_PIN = "P9_26"
    _RSTN_PIN = "P9_27"
    _DRDY_PIN = "P9_25"
    _spi = SPI(1, 0)


R0 = 100.0
A = 3.9083e-3
B = -5.775e-7
C = -4.183e-12
K = .999379


_START_PIN = "P9_23"
_RSTN_PIN = "P9_24"
_DRDY_PIN = "P9_16"
_spi = SPI(0,0)

readconfig = {
            # 'A01_IDAC2_1mA_A4_REF_A23':
            #       [0x11, 0x05, 0x00, 0x60, 0x07, 0x01, 0x00, 0x00,
            #        0x00, 0x00, 0x00, 0x40, 0x7B, 0x60, 0x12, 0x00,
            #        0x00, 0x00, 0x00, 0x00],
              'A01_IDAC2_1mA_A8_REF_A23':
                  [0x11, 0x05, 0x00, 0x60, 0x07, 0x01, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x40, 0x8B, 0x60, 0x12, 0x00,
                   0x00, 0x00, 0x00, 0x00],
              # 'A67_IDAC2_1mA_A4_REF_A23':
              #     [0x11, 0x05, 0x00, 0x60, 0x07, 0x67, 0x00, 0x00,
              #      0x00, 0x00, 0x00, 0x40, 0x4B, 0x60, 0x12, 0x00,
              #      0x00, 0x00, 0x00, 0x00],
              # 'A67_IDAC2_1mA_A8_REF_A45':
              #     [0x11, 0x05, 0x00, 0x60, 0x07, 0x67, 0x00, 0x00,
              #      0x00, 0x00, 0x00, 0x40, 0x8B, 0x60, 0x1B, 0x00,
              #      0x00, 0x00, 0x00, 0x00],
              # 'TDAC':
              #     [0x11, 0x05, 0x00, 0x60, 0x07, 0xEE, 0x00, 0x00,
              #      0x00, 0x00, 0x00, 0x40, 0xBB, 0x00, 0x00, 0x17,
              #      0x18, 0x00, 0x00, 0x00]}
              }
r = Ads126x(_START_PIN, _RSTN_PIN, _DRDY_PIN, _spi)
r.power_up()
r.sfoCal()
    try:
        ws = DdClient('ws://192.168.0.51:18080/cC', protocols=['http-only', 'chat'])
        ws.connect()
        # ws.run_forever()
    except:
        ws = None
        logging.warning('Connecting to ws was unsuccesful')


    o = Oven()
    time.sleep(5)
    o.fan_min()

    eV = threading.Event()
    pr = PID_calc()
    pr.start()
    ar = AdcReader(r, readconfig)
    ar.start()

    o.H1.set_duty(0)
    o.H2.set_duty(0)

    ar.save_log()
    o.H1.set_duty(0)
    o.H2.set_duty(0)

    cvs = CV_setter()
    cvs.start()


    spQueue.put(75)

temp_sp = 45

while True:
    try:
        temp_sp += 1
        spQueue.put(temp_sp)
        print '\n\nNew setpoint', \
            temp_sp, \
            'at', \
            datetime.utcnow().isoformat(),
        time.sleep(10)
    except KeyboardInterrupt:
        break

pr.stop()
pr = PID_calc()
pr.start()

pr.kP =  10
pr.kD = 80
pr.kI = 0.025
pr.I = 30/ pr.kI

spQueue.put(0)
spQueue.put(191.56)
pr.I = 0





