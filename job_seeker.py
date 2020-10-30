
import socket


def seeker_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    # types of jobs/services: 1=ICMP request, 2=Craft and Send IP packet, 3=Craft and Send TCP packet
    while True:
        client_socket.send("Hello".encode())
        data = client_socket.recv(1)  # receive response
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
