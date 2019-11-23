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




serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

while True:
    messageType = 2
    retCode  = 0
    messageID = 0
    answerLen = 0
    question = ''
    answer = ''
    questionLen = 0
    data, address = serverSocket.recvfrom(1024)
    message=struct.unpack('!hhihh',data[:12])
    hostName=data[12:]
    hostName = hostName.decode()
    f=open("dns-master.txt","r")
    lines=f.readlines()
    for x in lines[5:]:
        host=x.split(' ')[0] + ' ' + x.split(' ')[1] + ' ' + x.split(' ')[2]
        if host==hostName:
            answer = x
            retCode=0
            break
        retCode=1
    answer=answer.encode()
    hostName=hostName.encode()
    answerLen=len(answer)
    response=struct.pack('!hhihh',messageType,retCode,message[2],message[3],answerLen)+hostName+answer
    serverSocket.sendto(response,address)