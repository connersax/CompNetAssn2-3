
import socket
import time
import os
from scapy.all import ARP, Ether, srp

def live_ip(target_ip):
    arp = ARP(pdst=target_ip) # create ARP packet
    ether = Ether(dst="ff:ff:ff:ff:ff:ff") # create the Ether broadcast packet. If it has a MAC address it means the IP is broadcasting
    packet = ether/arp # put the ARP and Ether packet together
    result = srp(packet, timeout=3, verbose=0)[0] #
    ip_addrs = "" # the string that will contain all the IP addresses

    for sent, received in result:
        ip_addrs += str(received.psrc + '\n') # add all the live IPs to the string that will be sent back to the creator

    return ip_addrs

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

    service = bytes([4])
    print("job_seeker: I am offering live IP service")
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
        return_to_creator = live_ip(data) # job data is processing

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
