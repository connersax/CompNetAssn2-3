from re import VERBOSE
import socket
import time
import os
import sys
from scapy.all import IP, ICMP, sr1

def host_online(target_ip):
    icmp = IP(dst=target_ip)/ICMP()
    response = sr1(icmp,timeout=10, verbose=0)
    if response == None:
        return(target_ip + " is down")
    else:
        return(target_ip + " is up")

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

    service = bytes([3])
    print("job_seeker: I am offering host online service")
    client_socket.send(service)    # send service/skill
    data = int.from_bytes(client_socket.recv(1), "big")    # receive job or no job available
    if data == 1:
        print("job_creator: I have corresponding job " + str(int.from_bytes(service, "big")) )

# send back accept or deny response
        print("job_seeker: I accept " + str(int.from_bytes(service, "big")) + " job")
        client_socket.send(bytes([1]))

# RECEIVE JOB DATA
        data = client_socket.recv(1024).decode()
        print("job_creator: Job data sent\n")

        client_socket.close()  # close the connection

        print("job data: " + data + '\n')
        return_to_creator = host_online(data) # job data is processing

        # reconnecting to give result
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server

        print("job_seeker: My IP;UID is " + ip_uid)
        client_socket.send(ip_uid.encode()) # send ip

        data = client_socket.recv(1024).decode()    # creator ip
        print("job_creator: My IP;UID is " + data + " waiting for return status of job")

        print("job_seeker: Job completed with code 0")
        client_socket.send(bytes([0]))

        print("job_seeker: Sending result data\n")
        client_socket.send(return_to_creator.encode()) # sending result
    else:
        print("job_creator: I do not have corresponding job " + str(int.from_bytes(service, "big")))
        client_socket.close()  # close the connection


if __name__ == '__main__':
    seeker_program()