#Mark Galesi UCID:mjg64 section:101
# Echo Server
import sys
import socket
import random
import time
import os
import codecs
from datetime import datetime

try:
    serverIP = sys.argv[1]
    serverPort = int(sys.argv[2])
except socket.gaierror:
    serverIP='127.0.0.1'
    print("invalid ip address, using default:127.0.0.1")

def GETresponse(file):
    t = time.gmtime()
    date = time.strftime("%a, %d %b %Y %H:%M:%S %Z", t)
    if os.path.isfile("./" + file):
        t2 = time.gmtime(os.path.getmtime(file))
        lastModif = time.strftime("%a, %d %b %Y %H:%M:%S %Z", t2)
        size = os.path.getsize(file)
        f=codecs.open(file, 'r', encoding='utf-8')
        temp=f.read()
        fileContents=""
        for line in temp.split("\n"):
            fileContents+=line
        response = "HTTP/1.1 200 OK" + "\\r\\n\n" + "Date: " + date + "\\r\\n\n" + "Last-Modified:" + lastModif + "\\r\\n\n" + "Content-Length:" + str(size) + " text/html; charset=UTF-8\r\n" + "\\r\\n"
        print(response + "\n")
        response = response + fileContents
    else:
        response = "HTTP/1.1 404 Not Found" + "\\r\\n\n" + "Date: " + date + "\\r\\n\n" + "\\r\\n"
        print(response + "\n")
    return response

def ConditionalGETresponse(file,modCheck):
    t = time.gmtime()
    date = time.strftime("%a, %d %b %Y %H:%M:%S %Z", t)
    if os.path.isfile("./" + file):
        t2 = time.gmtime(os.path.getmtime(file))
        lastModif = time.strftime("%a, %d %b %Y %H:%M:%S %Z", t2)
        fileOnRecord=int(time.mktime(time.strptime(lastModif, "%a, %d %b %Y %H:%M:%S %Z")))
        fileOnClient=int(time.mktime(time.strptime(modCheck, "%a, %d %b %Y %H:%M:%S %Z")))
        if(fileOnRecord>fileOnClient):
            response=GETresponse(file)
            return response
        else:
            response = "HTTP/1.1 304 Not Modified" +"\\r\\n\n" + "Date: " + date + "\\r\\n\n" + "\\r\\n"
            print(response + "\n")
            return response
    else:
        response = "HTTP/1.1 404 Not Found" + "\\r\\n\n" + "Date: " + date + "\\r\\n\n" + "\\r\\n"
        print(response + "\n")
    return response


response="hello"
print("The server is ready to receive on port:  " + str(serverPort) + "\n")
while True:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((serverIP, serverPort))
    serverSocket.listen(2)
    conn, address = serverSocket.accept()
    data = conn.recv(1024)
    arr=data.decode().split("\\r\\n")
    arr2=arr
    if("If-Modified-Since:" in data.decode()):
        print("Conditional GET")
        arr = arr[0].split("/")
        arr = arr[1].split(" ")
        file = arr[0]
        modifDate=arr2[2].split(": ")[1]
        conn.send(ConditionalGETresponse(file,modifDate).encode())
        conn.close()
    else:
        print("GET")
        arr = arr[0].split("/")
        arr = arr[1].split(" ")
        file = arr[0]
        conn.send(GETresponse(file).encode())
        conn.close()



serverSocket.close()