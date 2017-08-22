import struct
import serial
import time


ser = serial.Serial('/dev/ttyUSB0', 38400)

a = ''
a += ser.read(ser.inWaiting())
c = a.split('\xfe')
c_ = []
for i in range(len(c)):
    c_.append(struct.unpack('B'*len(c[i]), c[i]))


types = {
    0b0001: {'text': 'V AC',
             0b000: 3e-1,
             0b001: 3,
             0b010: 3e1,
             0b011: 3e2,
             0b100: 1e3},
    0b0010: {'text': 'V AC+DC',
             0b000: 3e-1,
             0b001: 3,
             0b010: 3e1,
             0b011: 3e2,
             0b100: 1e3},
    0b0011: {'text': 'V DC',
             0b000: 3e-1,
             0b001: 3,
             0b010: 3e1,
             0b011: 3e2,
             0b100: 1e3},
    0b0100: {'text': 'Ohm'},
    0b0101: {'text': 'Diode'},
    0b0110: {'text': 'degC'},
    0b0111: {'text': 'Farad'},
    0b1000: {'text': 'mA DC',
             0b000: 3e-4,
             0b001: 3e-3,
             0b010: 3e-2,
             0b011: 3e-1
             },
    0b1001: {'text': 'A DC'},
    0b1010: {'text': 'mA AC+DC'},
    0b1011: {'text': 'A AC+DC'},
    0b1100: {'text': 'Hz'},
    0b1101: {'text': 'dB'},
    0b1110: {'text': 'Events'},
    0b1111: {'text': 'Uhr'},
    0b0000: {'text': 'Leer'}
}


def decode_stream(list_of_packets_in_tuples_of_bytes):
    measurement_type = None
    measurement_range = None
    sign = 1
    for packet in list_of_packets_in_tuples_of_bytes:
        packet_length = len(packet)

        if packet_length > 0:
            packet_type = (packet[-1] & 0b00110000) >> 4
            if measurement_type:
                if packet_length == 6:
                    if packet_type == 2:  # measured data
                        measured_data = assemble_decimal_data(packet)

                        if ((packet[-1] & 0b00001000) >> 3) == 1:
                            sign = -1
                        else:
                            sign = 1

                        meassurement_range = (packet[-1] & 0b1111)

                    if packet_type == 0:
                        measured_data = assemble_decimal_data(packet)

                    print 'Numbers:', measured_data * sign, 'Packet header:', bin(packet[-1])

            if packet_length == 5:
                if packet_type == 1:
                    print 'Instrument settings:',
                    measurement_type = packet[-5] & 0b1111
                    print types[measurement_type]['text'],


                for k in packet:
                    print format(k, '#010b'), ' ',
                print (packet[-1] & 0b1111) == (packet[-2] & 0b1111),
                print ''


def assemble_decimal_data(data_packet):
    measured_data = 0
    for index in range(2, 7):
        measured_data += (data_packet[-index] & 0b1111) * 10 ** (6 - index)
    return measured_data


def read_saved_data(file_name):
    f = open(file_name, 'r')
    a = f.read()
    f.close()
    c = a.split('\xfe')
    c_ = []
    for i in range(len(c)):
        c_.append(struct.unpack('B'*len(c[i]), c[i]))
    return c_



b = struct.unpack('B'*len(a), a)
b
# for i in list(b):
#     if (i & 3) == 7:
#         print i

delim = struct.pack('BB', 0, 0)
vala = a.split(delim)
vala


vala = [
        '\x80\x80\x80\x80\xf8\xf8\xf8\x80\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x80\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x80\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xffx\xfe\x80\xf8\xf8\xf8\x80',
        '\x80\x80\x80\x80\xf8\xf8\xf8\x80\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xffx\xfe\x80\xf8\xf8\xf8\x80',
        '\x80\x80\x80\x80\xf8\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xffx\xfe\x80\xf8\xf8\xf8\x80',
        '\x80\x80\x80\x80\xf8\xf8\xf8\x80\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xffx\xfe\x80\xf8\xf8\xf8\x80',
        '\x80\x80\x80\x80\xf8\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x80\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xffx\xfe\x80\xf8\xf8\xf8\x80',
        '\x80\x80\x80\x80\xf8\xf8\xf8\x80\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x80\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xffx\xfe\x80\xf8\xf8\xf8\x80',
        '\x80\x80\x80\x80\xf8\xf8\xf8\x80\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x80\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\xf8\x80',
        '\x80\x80x\x00\xff\x80\x00\xf8\xf8\x00\xf8'
        ]

def vizgalodas(addr):
        for i in vala:
            baba = struct.unpack(len(i)*'B', i)
            for j in list(baba):
                if (j & 0b1111) == addr:
                    print i,j
                    print format(j, '#010b')



while True:
    try:
        a = ser.read(ser.inWaiting())
        print len(a)
        time.sleep(1)
    except KeyboardInterrupt:
        break


def addresses(b):
    addrs = []
    for i in b:
        bits_7_6 = (i & (0b11 << 6)) >> 6
        bits_5_4 = (i & (0b11 << 4)) >> 4
        bits_3_0 = i & 0b1111
        if bits_7_6 == 0b11:
            addr = bits_3_0
            print format(i, '#010b')
            if bits_3_0 not in addrs:
                addrs.append(bits_3_0)
    return addrs

addresses(b)


addrs = []
for i in b:
    # if (i & 0b11000000) == 0b11000000:
    # addr = i & 0b1111
    print format(i, '#010b')
        # if addr not in addrs:
        #     addrs.append(addr)


import minimalmodbus
import paho.mqtt.client as mqtt
import json
# instr = minimalmodbus.Instrument('/dev/ttyO4', 1)
# instr.serial.baudrate = 9600

error_codes = {
                16688: "A0  Error of external protection device",
                16689: "A1  Defect of printed circuit board",
                16691: "A3  Malfunction of drain level control system",
                16694: "A6  Fan Motor Lock",
                16695: "A7  Malfunction of swing flap motor",
                16697: "A9  Malfunction of electronic expansion valve",
                16712: "AH  Dirty air filter",
                16714: "AJ  Faulty capacity setting",
                16710: "AF  Drain level above limit",
                17204: "C4  Malfunction of liquid pipe temperature sensor",
                17205: "C5  Malfunction of gas pipe temperature sensor",
                17209: "C9  Malfunction of return air temperature sensor",
                17226: "CJ  Malfunction of controllerr temperature sensor",
                17712: "E0  Actuation of safety device",
                17713: "E1  Defect of printed circuit board",
                17715: "E3  Actuation of high pressure switch",
                17716: "E4  Actuation of low pressure sensor",
                17721: "E9  Malfunction of electronic expansion valve",
                17971: "F3  Abnormal discharge pipe temperature",
                18483: "H3  High pressure switch failure",
                18484: "H4  Actuation of low pressure switch",
                18489: "H9  Malfunction of ambient air temperature sensor",
                18993: "J1  Malfunction of pressure sensor",
                18995: "J3  Malfunction of discharge pipe temperature sensor",
                18997: "J5  Mafunction of suction pipe temperature sensor",
                18998: "J6  Malfunction of heat exchanger temperature sensor",
                19009: "JA  Malfunction of discharge pipe pressure sensor",
                19016: "JH  Malfunction of oil line temperature sensor",
                19011: "JC  Malfunction of suction pipe pressure sensor",
                19504: "L0  Failure of inverter system",
                19508: "L4  Malfunction of inverter pcb overheat sensor",
                19509: "L5  Inverter over-current",
                19510: "L6  Compressor motor defect (inverter)",
                19512: "L8  Compressor overload (inverter)",
                19513: "L9  Compressor lock (inverter)",
                19521: "LA  Malfunction of power unit",
                19523: "LC  Malfunction of transmission between inverter pcb and control pcb",
                20528: "P0  Gas depletion",
                20529: "P1  Inverter over - ripple protection",
                20532: "P4  Malfunction of inverter pcb temperature sensor",
                21808: "U0  Refrigerant shortage",
                21809: "U1  Reversed phase connection or negative present",
                21810: "U2  Insufficient power supply",
                21812: "U4  Malfunction of transmission between indoor and outdoor units",
                21813: "U5  Malfunction of transmission between indoor unit and remote controller",
                21815: "U7  Malfunction of transmission between outdoor units",
                21816: "U8  Malfunction of transmission between master and slave remote controllers",
                21817: "U9  Malfunction of transmission between indoor and outdoor units",
                21825: "UA  Excessive numberr of indoor units",
                21832: "UH  System not ready to run due to test mode being performed",
                21827: "UC  Duplicate DIII net adress",
                21829: "UE  Malfunction of transimission between indoor unit and central control device",
                21830: "UF  Incompatible piping or wiring",
                0: "0Data Not Available",
                255: "--  No Fault",
                14384: "V80 V80: Waiting for unit data",
                14388: "V84 V84: Unit missing"
}
RTDs = {}


class daikin_rtd:
    def __init__(self, port, id):
        self.instr = minimalmodbus.Instrument(port, id)
        self.instr.serial.baudrate = 9600
        self.hold_reg = {}
        self.inp_reg = {}
        self.units = []
        try:
            self.discover_units()
            self.read_all_holding_registers()
            self.read_all_input_registers()
        except IOError as e:
            z = e
            print "WTFH ", z

    def read_single_holding_register(self,reg):
        try:
            val = self.instr.read_register(reg,0)
            return val
        except ValueError as e:
            z=e
            return z

    def read_single_input_register(self,reg):
        try:
            val = self.instr.read_register(reg,0,4)
            return val
        except ValueError as e:
            z=e
            return z

    def read_set_of_holding_registers(self, start_reg, num):
        try:
            list = self.instr.read_registers(start_reg, num)
        except ValueError as e:
            z = e
            print "WTFH ", z
        for i in range(len(list)):
            key = start_reg + i
            self.hold_reg[key] = list[i]

    def read_all_holding_registers(self):
        self.read_set_of_holding_registers(1,5)
        self.read_set_of_holding_registers(10,6)
        self.read_set_of_holding_registers(20, 5)
        self.read_set_of_holding_registers(30, 2)
        self.read_set_of_holding_registers(35, 1)
        self.read_set_of_holding_registers(37, 1)

    def read_set_of_input_registers(self, start_reg, num):
        try:
            list = self.instr.read_registers(start_reg, num, 4)
        except ValueError as e:
            z = e
            print "WTFH ", z
        for i in range(len(list)):
            key = start_reg + i
            self.inp_reg[key] = list[i]

    def read_all_input_registers(self):
        self.read_set_of_input_registers(20,7)
        self.read_set_of_input_registers(30,1)
        self.read_set_of_input_registers(35,3)
        for unit in self.units:
            prefix = unit * 100
            self.read_set_of_input_registers(prefix + 20, 5)
            self.read_set_of_input_registers(prefix + 30, 3)
            self.read_set_of_input_registers(prefix + 35, 3)

    def discover_units(self):
        units = []
        for i in range(1, 17):
            a = self.instr.read_register(i * 100 + 20, 0, 4)
            if a == 0:
                continue
            units.append(i)
        self.units = units

    def write_single_holding_register(self, reg, val, dec_places=0):
        self.instr.write_register(reg, val, dec_places)
        readback = self.instr.read_register(reg, dec_places)
        return val == readback

    def on(self):
        return self.write_single_holding_register(5,1)

    def off(self):
        return self.write_single_holding_register(5,0)

    def isFault(self):
        fault = self.instr.read_register(21,0,4)
        if fault == 0:
            return False
        else:
            return True

    def fault(self):
        return self.instr.read_register(22,0,4)

    def fault_txt(self):
        return error_codes[self.fault()]



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/OUT/DAIKIN/#")

def on_message(client, userdata, msg):
    msg.topic = msg.topic.replace('/OUT/DAIKIN/', '')
    payload = json.loads(msg.payload)
    print(msg.topic+" "+str(payload))
    if 'device' in payload.keys() and 'serialport' in payload.keys():
        key = (payload['serialport'], payload['device'])
        if key not in RTDs.keys():
            RTDs[key] = daikin_rtd(*key)
        if 'ON' in payload.keys():
            RTDs[key].on()
        if 'OFF' in payload.keys():
            RTDs[key].off()
        if 'GET_STATE' in payload.keys():
            RTDs[key].read_all_holding_registers()
            RTDs[key].read_all_input_registers()
            payload['hold_reg'] = RTDs[key].hold_reg
            payload['inp_reg'] = RTDs[key].inp_reg
            client.publish('/IN/DAIKIN', json.dumps(payload))



    # print payload

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('10.11.0.26', 18088, 60)

client.loop_start()


ADS_devices = [{'_START_PIN': "P9_23",
                '_RSTN_PIN': "P9_24",
                '_DRDY_PIN': "P9_16",
                '_spi': SPI(0, 0),
                'readconfigs': [
                    [0x11, 0x05, 0x00, 0x60, 0x07, 0x01, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x40, 0x8B, 0x60, 0x12, 0x00,
                     0x00, 0x00, 0x00, 0x00]
                ]
                }
               ]