#   Ex. 2.7 template - protocol

LIST_OF_COMMANDS = ['TAKE_SCREENSHOT', 'SEND_PHOTO', 'DIR', 'DELETE', 'COPY', 'EXECUTE', 'EXIT']
LENGTH_FIELD_SIZE = 4
PORT = 8820
SAVED_PHOTO_LOCATION = r"C:\Users\israel\Desktop\ss.jpg"


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    # (3)
    cmd = data.split(' ')
    if cmd[0] in ['EXIT', 'SEND_PHOTO', 'TAKE_SCREENSHOT'] and len(cmd) == 1:
        return True
    elif cmd[0] == 'COPY' and len(cmd) == 3:
        return True
    elif cmd[0] in ['DIR', 'DELETE', 'EXECUTE'] and len(cmd) == 2:
        return True
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    # (4)
    if len(data) > 9999:
        return "Length of your request too longer".encode()
    # padding the length
    cmd_length = str(len(str(data))).zfill(4)
    protocol_message = cmd_length + str(data)
    return protocol_message.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    # (5)
    length = str(my_socket.recv(LENGTH_FIELD_SIZE).decode())
    if length.isdigit():
        data = my_socket.recv(int(length)).decode()
        return True, data
    return False, "Error"
