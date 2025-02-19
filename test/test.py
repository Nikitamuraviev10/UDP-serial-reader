import socket
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from support import c_deserial

import time
import random

IP = 'localhost'
PORT = 40000


DST_IP = 'localhost'
DST_PORT = 41000

SLEEP = 0.001

data_struct = '''
struct Data{
    u32 time;
    f32 power_voltage;
    f32 power_current;
    f32 signal_voltage;
    f32 signal_current;
    f32 target_angle;
    f32 angle;
};
'''

start_time = time.time()

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# sock.bind((IP, PORT))

deserial = c_deserial.Deserial(data_struct)
data = deserial.get_struct()
data.fill_by_zero()

while True:
    data.time = int(1000 * (time.time() - start_time))
    data.power_voltage = 20 + random.random()

    sock.sendto(data.serial(), (DST_IP, DST_PORT))
    print(f"Sent data: time={data.time}, power_voltage={data.power_voltage}")
    time.sleep(SLEEP)
