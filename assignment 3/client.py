#Mark Galesi UCID:mjg64 section:101
# Echo Client
import sys
import socket
import struct
import time
import random
#from typing import Any

try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
    hostName = sys.argv[3]
except socket.gaierror:
    ip='12.0.0.1'
    print("invalid ip address, using default:12.0.0.1")

messageType = 1
retCode  = 0
messageID = random.randint(1,100)
answerLen = 0
question = (hostName + ' A IN').encode()
questionLen = len(question)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


request=struct.pack('!hhihh',messageType,retCode,messageID,questionLen,answerLen)+question

print('Sending Request to ' + str(ip) + ', ' + str(port)+':')
print('Message ID:\t' + str(messageID))
print('Question Length: ' + str(questionLen) + 'bytes')
print('Answer Length:' + str(answerLen) + 'bytes')
print('Question:' + str(question.decode()) + '\n')

for x in range(3):
    try:
        if(x>0):
            print('Sending Request to ' + str(ip) + ', ' + str(port)+':')
        clientsocket.sendto(request,(ip, port))
        clientsocket.settimeout(1)
        response, address = clientsocket.recvfrom(1024)

        message = struct.unpack('!hhihh',response[:12])
        messageType=message[0]
        retCode=message[1]
        messageID=message[2]
        questionLen=message[3]
        answerLen=message[4]
        answer=response[12+questionLen:].decode()

        print('\n\nRecieved Response from ' + str(address[0]) + ', ' + str(address[1]) + ":")
        print('Return Code: ' + str(retCode))
        print('Message ID:\t' + str(messageID))
        print('Question Length: ' + str(questionLen) + ' bytes')
        print('Answer Length:' + str(answerLen) + ' bytes')
        print('Question:' + str(question.decode()))
        if retCode==0:
            print('Answer: ' + str(answer))

        break
    except socket.timeout:
        print('Request timed out ...')
        if(x==2):
            print('Request timed out ... Exiting Program')

clientsocket.close()