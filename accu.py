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
                    measurement_type = packet[-5] & 0b1111
                    print types[measurement_type]['text'],

                print '5 byte of something:',
                for k in packet:
                    print format(k, '#010b'), ' ',
                print ''


def assemble_decimal_data(data_packet):
    measured_data = 0
    for index in range(2, 7):
        measured_data += (data_packet[-index] & 0b1111) * 10 ** (6 - index)
    return measured_data






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