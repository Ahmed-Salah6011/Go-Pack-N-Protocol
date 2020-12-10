import threading
import socket

#1 .... network_layer_available
#2 .... frame_arrival
#3 .... timeout
#4 .... checksum_error
#5 .... network_layer_not_available

global event
event=0
global MAX_SEQ
MAX_SEQ=7

##############TIMER PARAMS AND METHODS
global WAITING_TIME
WAITING_TIME=2

global sent_frames
sent_frames=dict()
################################3

def counting():
    global event
    event=3


class frame:
    seq=None
    ack=None
    info=None
    # kind=None
    def __str__(self):
        return "{} {} {}".format(self.seq,self.ack,self.info)
def wait_for_event():
    global event
    i=0
    while(event not in[1,2,3,4,5]):
        i+=1
    return event

def from_network_layer(network_layer, turn):
    return network_layer[turn]

def to_network_layer(network_layer, data):
    # n=list(network_layer).append(data)
    # return n
    network_layer.append(data)

def from_physical_layer(sockets):
    r=frame()
    sockets.settimeout(1)
    try:
        b=sockets.recv(1024)
    except socket.timeout:
        return None
    except socket.error:
        return "`"
    
    d=repr(b)[2:-1]
    if d=='': return "`"

    rec=d.split()
    r.seq=int(rec[0])
    r.ack=int(rec[1])
    r.info=rec[2]
    # print("Recieved" , d)
    return r

def to_physical_layer(sockets,data):
    sockets.sendall(str(data).encode())


def start_timer(seq_nr):
    global WAITING_TIME
    global sent_frames
    print("Frame with seq_nr {} is sent and waiting for acknowledgment".format(seq_nr))
    # t = threading.Timer(WAITING_TIME,counting)
    # sent_frames[seq_nr]=t
    # t.start()

def stop_timer(seq_nr):
    global sent_frames
    # sent_frames[seq_nr].cancel()
    print("Frame with seq {} is acknowledged".format(seq_nr))

def enable_network_layer():
    global event
    event = 1
    return 1

def disable_network_layer():
    global event
    event = 5
    return 5

def inc(x):
    global MAX_SEQ
    if x < MAX_SEQ-1:
        x+=1
    else:
        x=0
    return x


def between(a, b, c):
    if ( ( (a <= b) and (b < c) ) or ( (c < a) and (a <= b) ) or ( (b < c) and (c < a) ) ):
        return True
    else:
        return False


def send_data(sockets ,frame_nr, frame_expected, buffer,counter):
    global MAX_SEQ
    s=frame()
    s.info = buffer[counter % MAX_SEQ]
    s.seq = frame_nr
    s.ack =frame_expected
    to_physical_layer(sockets,s)
    start_timer(frame_nr)


    










