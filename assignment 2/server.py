#Mark Galesi UCID:mjg64 section:101
# Echo Server
import sys
import socket
import struct
import random
import time

try:
    serverIP = sys.argv[1]
    serverPort = int(sys.argv[2])
except socket.gaierror:
    serverIP='12.0.0.1'
    print("invalid ip address, using default:12.0.0.1")

messageType = 2
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

while True:
    data, address = serverSocket.recvfrom(1024)
    message=struct.unpack('!ii',data)
    data=struct.pack('!ii',message[0],messageType)
    rand=random.uniform(0.05,0.5)
    time.sleep(rand)
    print(str(rand))
    if(random.randint(0,10)>4):
        print("Responding to ping request with sequence number "+ str(message[0]+1))
        serverSocket.sendto(data,address)
    else:
        print("Message with sequence number "+ str(message[0]+1) + " dropped")