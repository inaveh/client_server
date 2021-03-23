#   Ex. 2.7 template - server side
#   Israel Naveh 2021

import socket
from protocol_solution import *
import os
import glob
import shutil
import subprocess
import pyautogui

IP = '0.0.0.0'
PORT = 2280


# The path + filename where the screenshot at the server should be saved

def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    # Then make sure the params are valid

    # (6)
    if check_cmd(cmd):
        cmd = cmd.split(' ')
        if cmd[0] in ['EXIT', 'SEND_PHOTO', 'TAKE_SCREENSHOT']:
            return True, cmd[0], None
        elif cmd[0] == 'COPY':
            src = cmd[1]
            dst = cmd[2]
            tmp = dst[:dst.rfind('\\')]
            # check the params
            if os.path.isfile(src) and os.path.exists(tmp):
                return True, cmd[0], [src, dst]
        elif cmd[0] == 'DIR' and os.path.exists(cmd[1]):
            return True, cmd[0], [cmd[1]]
        elif cmd[0] in ['DELETE', 'EXECUTE'] and os.path.isfile(cmd[1]):
            return True, cmd[0], [cmd[1]]
    return False, None, None


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    # (7)
    if command == 'DIR':
        parm = params[0]
        path = parm + r'*.*'
        return glob.glob(path)
    elif command == 'DELETE':
        os.remove(params[0])
        return "The file was deleted"
    elif command == 'COPY':
        shutil.copy(params[0], params[1])
        return "The file was copied"
    elif command == 'EXECUTE':
        subprocess.call(params)
        return "The program is work"
    elif command == 'TAKE_SCREENSHOT':
        image = pyautogui.screenshot()
        image.save(SAVED_PHOTO_LOCATION)
        return "The picture saved"
    elif command == "SEND_PHOTO":
        return str(os.path.getsize(SAVED_PHOTO_LOCATION))
    elif command == 'EXIT':
        return "The session closed"
    return 'Error'


def main():
    # open socket with client
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen()

    (client_socket, client_address) = server_socket.accept()

    # (1)
    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                # (6)

                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)

                # add length field using "create_msg"
                response = create_msg(response)

                # send to client
                client_socket.send(response)

                if command == 'SEND_PHOTO':
                    file_size = str(response.decode())
                    file_size = int(file_size[4:])
                    print(file_size)
                    count = 0
                    # Send the data itself to the client
                    with open(SAVED_PHOTO_LOCATION, 'rb') as input_file:
                        while count < file_size:
                            packet = input_file.read(1)
                            client_socket.send(packet)
                            count += 1
                # (9)
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                response = create_msg(response)

                # send to client
                client_socket.send(response)

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            response = create_msg(response)

            # send to client
            client_socket.send(response)

            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")


if __name__ == '__main__':
    main()
