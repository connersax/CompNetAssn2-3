
import socket


def seeker_program():
    host = socket.gethostname()  # as both code is running on same pc
    hostip = socket.gethostbyname(host) # gets the ip address
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server



    for i in range(1,2):
        print("job_seeker: My IP;UID is " + hostip)
        client_socket.send(hostip.encode()) # send ip
        data = client_socket.recv(1024).decode()    # receive ip
        print("job_creator: My IP;UID is " + str(data))  # show in terminal

# types of jobs/services: 1=ICMP request, 2=Craft and Send IP packet, 3=Craft and Send TCP packet
        service = bytes([2])
        print("job_seeker: I am offering 2 service")
        client_socket.send(service)    # send service/skill
        data = int.from_bytes(client_socket.recv(1), "big")    # receive job or no job available
        if data == 1:
            print("job_creator: I have corresponding job " + str(int.from_bytes(service, "big")) )
        else:
            print("job_creator: I do not have corresponding job " + str(int.from_bytes(service, "big")) )

# send back accept or deny response
        print("job_seeker: I accept " + str(int.from_bytes(service, "big")) + " job")
        client_socket.send(bytes([1]))

        #RECEIVE JOB DA


    # while message.lower().strip() != 'bye':
    #     client_socket.send(message.encode())  # send message
    #     data = client_socket.recv(1024).decode()  # receive response
    #
    #     print('Received from server: ' + data)  # show in terminal
    #
    #     message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    seeker_program()
