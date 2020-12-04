
import socket
import time
import os
from array import *


def creator_program():
    # get the hostname
    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)
    ip_uid = str(host_ip) + ";" + str(os.getpid())
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)


    # types of jobs/services: 1=ICMP flood, 2=TCP flood, 3=Craft and Send TCP packet
    available = [[1,10,'192.168.1.1'],[2,10,'192.168.1.1'],[3,2,'192.168.1.1']] # defined as [job, size, data]
    stored_seekers = [] # will be used when there is a job available it can do
    current_job_seekers = [] # seekers currently doing jobs from this creator


    while True:
        conn, address = server_socket.accept()  # accept new connection

        data = conn.recv(1024).decode() # seeker IP;UID
        seeker_id = data

        seeker_with_result = False
        for seeker in current_job_seekers: # testing to see if this seeker is back with the result of a previous job
            if seeker == seeker_id:
                seeker_with_result = True

        if seeker_with_result == False:
            print("job_seeker: My IP;UID is " + str(data))
            conn.send(ip_uid.encode()) # creator IP:UID
            print("job_creator: My IP;UID is " + ip_uid)
            data = int.from_bytes(conn.recv(1), "big") # seeker service
            seeker_service = data
            print("job_seeker: I am offering " + str(data) + " service")

            stored_seekers.append([seeker_id, seeker_service]) # storing seeker and the service it does

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
                    conn.send(available[available_index][2].encode()) # creator sending job data
                    print("job_creator: Job data sent\n")
                    current_job_seekers.append(seeker_id)

                else:
                    print("job_seeker: I deny job")
            else:
                conn.send(bytes([0])) # if the job is not available send a 0
                print("job_creator: I do not have corresponding job " + str(data))
                conn.close()
                print("Connection closed with seeker\n")

        else:
            #job seeker response here
            conn.send(ip_uid.encode()) # creator IP:UID
            print("job_creator: My IP;UID is " + ip_uid + " waiting for return status of job")
            data = int.from_bytes(conn.recv(1), "big") # return code of job
            print("job_seeker: Job completed with code " + str(data))
            data = conn.recv(1024).decode() # result data
            print("job_seeker: result: " + data)
            current_job_seekers.remove(seeker_id)

            for job in available:
                if job[1] == 0:
                    available.remove(job) # removes a job from available once it is completed

            print("\n")



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
