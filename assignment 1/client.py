#Mark Galesi UCID:mjg64 section:101
# Echo Client
import sys
import socket

# Get the server hostname, port and data length as command line arguments
try:
    host = sys.argv[1]
    port = int(sys.argv[2])
    count = int(sys.argv[3])
except ValueError:
    count=10
    print("third argument must be an integer, using default:10")
except socket.gaierror:
    host='12.0.0.1'
    print("invalid ip address, using default:12.0.0.1")

#except socket.gaierror
#except ValueError
data = 'X' * count # Initialize data to be sent

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send data to server
for x in range(3):
    try:
        print("Sending data to   " + host + ", " + str(port) + ": " + data + "(" + str(count) + " characters)")
        clientsocket.sendto(data.encode(),(host, port))
        clientsocket.settimeout(1)

        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(count)
        print("Receive data from " + address[0] + ", " + str(address[1]) + ": " + dataEcho.decode())
        break
    except socket.timeout:
            print('no response from server, request timed out')

#Close the client socket
clientsocket.close()