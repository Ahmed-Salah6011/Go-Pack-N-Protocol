import socket
import threading
import sys
import select
from protocol import *

#1 .... network_layer_available
#2 .... frame_arrival
#3 .... timeout




global next_frame_to_send
global ack_expected
global nbuffered
global network_layer
next_frame_to_send=0
ack_expected=0
nbuffered=0

###DEVICE A


HOST = "localhost"
PORT = 12000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
###########################################
print("Enter 9 packets to send")
network_layer=list()
for i in range(9):
    network_layer.append(input())

# network_layer = ["ABC#","DEF#","GHI#","JKL#","MNO#","PQR#","STU#","VWX#","YZA#"]
counter=0
###########################################
##THREAD FUNCTIONS



###########################################
next_frame_to_send=0
ack_expected=0
r=frame()
buffer= dict()
nbuffered=0
no_ack=0
recieved_frame=frame()

event=enable_network_layer()


####
frame_expected=-1
curr=0
########
first_time=1

#########
enable_timer=0
timer=0
#########
while curr <len(network_layer):
    n_first=1
    recieved_frame = from_physical_layer(conn)
    if recieved_frame:
        r=recieved_frame
        while (between(ack_expected, r.ack, next_frame_to_send)):
            nbuffered = nbuffered - 1
            stop_timer(ack_expected)
            ack_expected=inc(ack_expected)
            curr+=1

    elif timer==4:
        timer=0
        next_frame_to_send = ack_expected
        n=curr
        for i in range(nbuffered):
            send_data(conn,next_frame_to_send, frame_expected, buffer,n)
            next_frame_to_send=inc(next_frame_to_send)
            n+=1


    else:
        if next_frame_to_send == 2 and first_time==1:
            first_time=0
            enable_timer=1
            ####
            buffer[next_frame_to_send]= from_network_layer(network_layer ,counter)
            counter+=1
            nbuffered = nbuffered + 1
            start_timer(next_frame_to_send)
            # send_data( conn,next_frame_to_send, frame_expected, buffer)
            next_frame_to_send=inc(next_frame_to_send)
        else:
            buffer[next_frame_to_send]= from_network_layer(network_layer ,counter)
            nbuffered = nbuffered + 1
            send_data( conn,next_frame_to_send, frame_expected, buffer,counter)
            counter+=1
            next_frame_to_send=inc(next_frame_to_send)
        
    
    if enable_timer ==1:
        timer+=1

    if (nbuffered >= MAX_SEQ):
        continue






