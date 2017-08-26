import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import threading


class Ads126x:
    def __init__(self, start_pin, rstn_pin, drdy_pin, spi, x=2):

        self.StartPin = start_pin
        self.RstnPin = rstn_pin
        self.DrdyPin = drdy_pin
        self.Spi = spi
        self.chip = x
        self.gpio_init()
        self.free = threading.Event()
        self.free.set()
        self.current_config = None

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
        cmd = [0x20 + start_address, num_bytes - 1]
        return self.Spi.xfer2(cmd + a)[2:]

    def write_register(self, start_address, data):
        cmd = [0x40 + start_address, len(data) - 1]
        return self.Spi.xfer2(cmd + data)[2:]

    def sfo_cal(self):
        self.write_register(6, [0xff])
        self.Spi.xfer2([0x19])

    def sio_cal(self, mux):
        self.power_down()
        self.power_up()
        self.write_register(6, [mux])
        self.Spi.xfer2([0x16])

    def read_n_sample_w_config(self, n, conf):
        self.stop_conversion()
        self.write_register(1, conf)
        self.start_conversion()
        read_data = []
        for i in range(n):
            GPIO.wait_for_edge(self.DrdyPin, GPIO.FALLING)
            tst = datetime.utcnow().isoformat()
            read_data.append((tst, self.read_adc_data()))
        self.stop_conversion()
        return read_data


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ADS_controller/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic.split('/')
    dev_id = int(topic[2])
    if dev_id not in ads_s.keys():
        if dev_id in known_ADS_devices.keys():
            ads_s[dev_id] = Ads126x(known_ADS_devices[dev_id]['_START_PIN'],
                                    known_ADS_devices[dev_id]['_RSTN_PIN'],
                                    known_ADS_devices[dev_id]['_DRDY_PIN'],
                                    known_ADS_devices[dev_id]['_spi'])
            ads_s[dev_id].power_up()
            ads_s[dev_id].sfo_cal()


    if topic[1] == 'READ':
        # wait for device become available
        ads_s[dev_id].free.wait()
        ads_s[dev_id].free.clear()
        print(topic)
        c = int(topic[3])
        msg.topic = msg.topic.replace('ADS_controller/', '')
        # print(msg.topic+" "+str(msg.payload))
        # print(dev_id, c)
        n = int(msg.payload)
        s = ads_s[dev_id].read_n_sample_w_config(n, known_ADS_devices[dev_id]['readconfigs'][c])
        ads_s[dev_id].free.set()
        t = "ADS_controller/DATA/" + str(dev_id) + '/' + str(c)
        client.publish(t, json.dumps(s))

#
# _START_PIN = "P9_23"
# _RSTN_PIN = "P9_24"
# _DRDY_PIN = "P9_16"
# _spi = SPI(0, 0)
#
# readconfig = [
#         [0x11, 0x05, 0x00, 0x60, 0x07, 0x01, 0x00, 0x00,
#          0x00, 0x00, 0x00, 0x40, 0x8B, 0x60, 0x12, 0x00,
#          0x00, 0x00, 0x00, 0x00]
# ]
# r = Ads126x(_START_PIN, _RSTN_PIN, _DRDY_PIN, _spi)
# r.power_up()
# r.sfo_cal()


known_ADS_devices = {0:{'_START_PIN': "P9_23",
                        '_RSTN_PIN': "P9_24",
                        '_DRDY_PIN': "P9_16",
                        '_spi': SPI(0, 0),
                        'readconfigs': [
                            [0x11, 0x05, 0x00, 0x60, 0x07, 0x01, 0x00, 0x00,
                             0x00, 0x00, 0x00, 0x40, 0x8B, 0x60, 0x12, 0x00,
                             0x00, 0x00, 0x00, 0x00]
                        ]
                        }
                     }

ads_s = {}






client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('192.168.0.51', 18088, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()
# client.loop_forever()