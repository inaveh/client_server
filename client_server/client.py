#   Ex. 2.7 template - client side
#   Israel Naveh 2021

import socket
from protocol_solution import *

IP = "127.0.0.1"
PORT = 2280
FILE_PATH = r"C:\Users\israel\Desktop\sscopy.jpg"

# The path + filename where the copy of the screenshot at the client should be saved


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO

    valid, response = get_msg(my_socket)
    if valid:
        # (10) treat SEND_PHOTO
        if cmd == "SEND_PHOTO":
            file_size = int(response)
            count = 0
            file_name = FILE_PATH
            with open(file_name, 'wb') as input_file:
                while count < file_size:
                    packet = my_socket.recv(1)
                    input_file.write(packet)
                    count += 1
            print("The file was send")
        else:
            print(response)
    else:
        print("Error")


def main():
    # open socket with the server
    my_socket = socket.socket()
    my_socket.connect((IP, PORT))
    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if check_cmd(cmd):  # check validation
            packet = create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                my_socket.close()
                break
        else:
            print("Not a valid command, or missing parameters\n")
    my_socket.close()


if __name__ == '__main__':
    main()
