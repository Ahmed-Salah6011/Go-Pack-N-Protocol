import socket
import threading
import sys
import select
import time
from protocol import *




global frame_expected
frame_expected=0


####DEVICE B


HOST = "localhost"
PORT = 12000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
###########################

frame_expected=0
r=frame()

network_layer=list()

ack_frame=frame()


while True:
    r=from_physical_layer(s)
    if (r=="`"):
        break
    if r:
        if (r.seq == frame_expected) :
            to_network_layer(network_layer,r.info)
            frame_expected=inc(frame_expected)
            print("Recieved {}".format(r.info))

            ack_frame.seq=-1
            ack_frame.ack=r.seq
            ack_frame.info="ack"

            to_physical_layer(s,ack_frame)
        
        else:
            print("Discarded")
    






    

