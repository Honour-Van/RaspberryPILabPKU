import smbus
import time

address = 0x48
A0 = 0x40
bus = smbus.SMBus(1)

while True:
    for value in range(256):
        bus.write_byte_data(address, A0, value)
        print(value)
    for value in range(255, -1, -1):
        bus.write_byte_data(address, A0, value)
        print(value)