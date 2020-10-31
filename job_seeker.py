
import socket
import time
import os


def seeker_program():
    host = socket.gethostname()  # as both code is running on same pc
    hostip = socket.gethostbyname(host) # gets the ip address
    ip_uid = str(hostip) + ";" + str(os.getpid())
    port = 5000  # socket server port number




    for i in range(1,3):
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server

        print("job_seeker: My IP;UID is " + ip_uid)
        client_socket.send(ip_uid.encode()) # send ip
        data = client_socket.recv(1024).decode()    # receive ip
        print("job_creator: My IP;UID is " + str(data))  # show in terminal

# types of jobs/services: 1=ICMP request, 2=Craft and Send IP packet, 3=Craft and Send TCP packet
        service = bytes([i])
        print("job_seeker: I am offering" + str(i) + "service")
        client_socket.send(service)    # send service/skill
        data = int.from_bytes(client_socket.recv(1), "big")    # receive job or no job available
        if data == 1:
            print("job_creator: I have corresponding job " + str(int.from_bytes(service, "big")) )
        else:
            print("job_creator: I do not have corresponding job " + str(int.from_bytes(service, "big")) )

# send back accept or deny response
        print("job_seeker: I accept " + str(int.from_bytes(service, "big")) + " job")
        client_socket.send(bytes([1]))

# RECEIVE JOB DATA
        data = client_socket.recv(1024).decode()
        job_data = data # this would later be saved and used
        print("job_creator: Job data sent\n")

        client_socket.close()  # close the connection

        time.sleep(2) # job data is processing

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
        client_socket.send("completed".encode()) # sending result

if __name__ == '__main__':
    seeker_program()
