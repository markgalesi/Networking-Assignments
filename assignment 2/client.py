#Mark Galesi UCID:mjg64 section:101
# Echo Client
import sys
import socket
import struct
import time
import statistics
#from typing import Any

try:
    host = sys.argv[1]
    port = int(sys.argv[2])
except socket.gaierror:
    host='12.0.0.1'
    print("invalid ip address, using default:12.0.0.1")

numSeq = 0
messageType = 1

packets=[]
RTT=[]

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('Pinging ' + str(host) + ', ' + str(port)+':')
for x in range(10):
    try:
        data=struct.pack('!ii',numSeq,messageType)
        start=time.time()
        clientsocket.sendto(data,(host, port))
        clientsocket.settimeout(2)
        numSeq=numSeq+1
        dataEcho, address = clientsocket.recvfrom(1024)
        stop=time.time()
        timer=stop-start
        message = struct.unpack('!ii',dataEcho)
        print("Ping message number " + str(numSeq) + ' RTT:' + str(timer))
        RTT.append(timer)
        packets.append(1)
    except socket.timeout:
        print("Ping message number " + str(numSeq) + ' timed out')
        packets.append(0)

clientsocket.close()
numSent=10
numRec=len(RTT)
LR=((10-len(RTT))/10)*100
min=min(RTT)
max=max(RTT)
avg=statistics.mean(RTT)
print("---------Statistics---------")
print("Packets Sent:"+str(numSent))
print("Packets Recieved:"+str(numRec))
print("Packet Loss Rate:"+str(LR)+"%")
print("Minimum Round Trip Time:"+str(min))
print("Maximum Round Trip Time:"+str(max))
print("Average Round Trip Time:"+str(avg))