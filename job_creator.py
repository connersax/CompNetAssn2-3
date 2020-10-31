
import socket
import time
from array import *


def creator_program():
    # get the hostname
    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)
    ip_uid = str(host_ip) + ";1234"
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
        data = conn.recv(1024).decode() # IP;UID
        print("job_seeker: My IP;UID is " + str(data))
        conn.send(ip_uid.encode()) # My IP:UID
        print("job_creator: My IP;UID is " + ip_uid)
        data = int.from_bytes(conn.recv(1), "big") # seeker service
        print("job_seeker: I am offering " + str(data) + "service")

        is_available = False
        available_index = 0
        for job in available: # testing if job is available
            if job[0] == data and job[1] != 0: # job has to match and have a size greater then 0
                is_available = True
                break

            available_index += 1 # only increments when not available since index starts at 0

        if is_available == True:
            conn.send(bytes([1])) # if the job is available send a 1
            print("job_creator: I have corresponding job " + str(data))

            data = int.from_bytes(conn.recv(1), "big") # seeker accepting or denying job
            if data == 1:
                available[available_index][1] -= 1
                print("job_seeker: I accept job")
                conn.send("job_data".encode()) # creator sending job data
                print("job_creator: Job data sent")
            else:
                print("job_seeker: I deny job")
        else:
            conn.send(bytes([0])) # if the job is not available send a 0
            print("job_creator: I do not have corresponding job " + str(data))
            conn.close()
            print("Connection closed with seeker")




        time.sleep(5)



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
