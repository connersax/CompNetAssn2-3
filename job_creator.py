
import socket
from array import *


def creator_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    # types of jobs/services: 1=ICMP request, 2=Craft and Send IP packet, 3=Craft and Send TCP packet
    available = [[1,1],[2,2],[1,2]] # defined as [job,size]


    while True:
        data = conn.recv(1024).decode()
        print("job_seeker: " + str(data))
        conn.send(bytes([4]))

    # while True:
    #     # receive data stream. it won't accept data packet greater than 1024 bytes
    #     data = conn.recv(1024).decode()
    #     if not data:
    #         # if data is not received break
    #         break
    #     print("from connected user: " + str(data))
    #     data = input(' -> ')
    #     conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    creator_program()
