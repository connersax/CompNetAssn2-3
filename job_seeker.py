
import socket


def seeker_program():
    host = socket.gethostname()  # as both code is running on same pc
    hostip = socket.gethostbyname(host) # gets the ip address
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server



    for i in range(1,5):
        # client_socket.send("Hello".encode()) # send message
        client_socket.send(hostip.encode()) # send ip
        data = client_socket.recv(1)    # receive ip
        print('job_creator: ' + str(data)  # show in terminal

# types of jobs/services: 1=ICMP request, 2=Craft and Send IP packet, 3=Craft and Send TCP packet
        client_socket.send(bytes[2])    # send service/skill
        data = client_socket.recv(1)    # receive job or no job available
        print('job_creator: ' + str(int.from_bytes(data, "big")))  # show in terminal


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
