from smbus import SMBus
import paho.mqtt.client as mqtt
import json


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/OUT/I2C/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    msg.topic = msg.topic.replace('/OUT/I2C/', '')
    print(msg.topic+" "+str(msg.payload))
    payload = json.loads(msg.payload)
    # print payload
    if msg.topic == 'setbit':
        pass
    try:
        if payload['bus'] not in [0,1,2]:
            raise ValueError
        if payload['bit'] not in range(8):
            raise ValueError
        if payload['register'] not in range(256):
            raise ValueError
        if payload['device'] not in range(256):
            raise ValueError
        if payload['value'] not in [0,1]:
            raise ValueError

        bus = SMBus(payload['bus'])
        current_reg_value = bus.read_byte_data(payload['device'],
                                               payload['register'])
        if payload['value'] == 1:
            new_reg_value = current_reg_value | (1 << payload['bit'])

        if payload['value'] == 0:
            new_reg_value = current_reg_value & ~(1 << payload['bit'])

        bus.write_byte_data(payload['device'],
                            payload['register'],
                            new_reg_value)
    except IOError:
        print "Device IO error"
    except KeyError:
        print "Some of required parameters are not present"
    except ValueError:
        print "Some of required parameters are not valid"
    # except:
    #     print "Unknown error occured"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('10.11.0.26', 18088, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
b2 = SMBus(2)
b2.write_byte_data(0x23, 0x03,0x0)

client.loop_start()
#   client.loop_forever()
