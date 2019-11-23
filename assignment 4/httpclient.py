#Mark Galesi UCID:mjg64 section:101
# Echo Client
import sys
import socket
import shutil
import time
import os
#from typing import Any
def cache(existingCache,filename,fileContents,lastMod):
    open(existingCache,'w').close()
    file=open(existingCache,'a')
    file.write("cached " + filename + " " + lastMod + "\n" + fileContents)
    file.close()

def check(cache,filename):
    if str("cached " + filename) in open(cache).read():
        return True
    else:
        return False


def GET(filename,host,port):
    message = "GET /" + filename + " HTTP/1.1" + "\\r\\n\n" + "Host: " + host + ":" + str(port) + "\\r\\n\n" + "\\r\\n"
    print(message + "\n")
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))
    clientsocket.send(message.encode())
    response, address = clientsocket.recvfrom(1024)
    clientsocket.close()
    return response

def conditionalGet(filename,host,port):
    f=open("cache.txt","r")
    date=f.readlines()[1].split(": ")[1]
    f.close()
    message = "GET /" + filename + " HTTP/1.1" + "\\r\\n\n" + "Host: " + host + ":" + str(port) + "\\r\\n\n" + "If-Modified-Since: " + date[:-1] + "\\r\\n\n" + "\\r\\n"
    print(message + "\n")
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))
    clientsocket.send(message.encode())
    response, address = clientsocket.recvfrom(1024)
    clientsocket.close()
    return response



argv = sys.argv
url = argv[1]
host = url.split(":")[0]
port = url.split("/")[0].split(":")[1]
filename = url.split("/")[1]
port = int(port)

"""if os.path.isfile(filename):
    data = "GET /" + filename + " HTTP/1.1" + "\\r\\n\n" + "Host: " + host + ":" + port + "\\r\\n\n" + "\\r\\n"
    print(data)
    if os.path.isfile("./cache.txt") and not check("cache.txt", filename):
        cache("cache.txt",filename)
else:
    print("unable to cache")"""
if os.path.isfile("./cache.txt"):

    f=open("cache.txt","r+")
    f.close()
if check("cache.txt", filename):
    response=conditionalGet(filename,host,port)
    if "Not Modified" not in response.decode():
        data=response.decode().split("\\r\\n")
        fileContents=data[-1]
        del data[-1]
        temp=""
        cache("cache.txt",filename,fileContents,data[1])
        for i in data:
            temp += i + "\\r\\n"
        print(temp + "\n" + fileContents)
    else:
        print(response.decode())


else:
    response=GET(filename,host,port)
    data=response.decode().split("\\r\\n")
    fileContents=data[-1]
    del data[-1]
    temp=""
    cache("cache.txt",filename,fileContents,data[1])
    for i in data:
        temp += i + "\\r\\n"
    print(temp + "\n" + fileContents)


#clientsocket= socket(AF_INET, SOCK_STREAM)
#clientsocket.sendto(request,(ip, port))
#clientsocket.settimeout(1)
#response, address = clientsocket.recvfrom(1024)
#clientsocket.close()