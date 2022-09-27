import time
from random import random as rand 
from pylsl import StreamInfo, StreamOutlet,local_clock


def main():
    srate=280
    name = 'Aurora'
    type = 'NIRS'
    n_channels = 8
    
    stream_info = StreamInfo(name,type,n_channels,srate,'float32','12334')
    stream_outlet  = StreamOutlet(stream_info)
    start_time = local_clock()
    sent_sampels = 0

    while True:
        elapsed_time = local_clock()- start_time
        required_sampels = int(srate* elapsed_time)-sent_sampels
        for index in range(required_sampels):
            ssample =[rand() for _ in range(n_channels)]
            # print(ssample)
            stream_outlet.push_sample(ssample)
        sent_sampels+=required_sampels



main()