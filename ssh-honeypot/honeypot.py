import socket
import threading
import paramiko
from config import *
from logger import write_log

HOST_KEY = paramiko.RSAKey.generate(2048)
attempt_tracker = {}

class SSHServer(paramiko.ServerInterface):

    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        ip = self.client_ip

        if ip not in attempt_tracker:
            attempt_tracker[ip] = 0

        attempt_tracker[ip] += 1

        write_log(LOG_FILE, f"{ip} | USER: {username} | PASS: {password}")

        if attempt_tracker[ip] > BRUTE_FORCE_THRESHOLD:
            write_log(ALERT_LOG, f"BRUTE FORCE DETECTED from {ip}")

        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return "password"

def handle_connection(client_socket, addr):
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(HOST_KEY)
        server = SSHServer(addr[0])
        transport.start_server(server=server)

        channel = transport.accept(20)
        if channel is None:
            return

        channel.send("Welcome to Ubuntu 20.04 LTS\n")
        channel.send("Last login: {}\n\n".format(paramiko.util.format_binary(b'fake')))
        channel.send("$ ")

        while True:
            command = channel.recv(1024).decode("utf-8").strip()

            if not command:
                continue

            write_log(COMMAND_LOG, f"{addr[0]} | COMMAND: {command}")

            if command.lower() == "exit":
                channel.send("Bye!\n")
                break

            channel.send("Command not found\n")
            channel.send("$ ")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(100)

    print(f"[+] SSH Honeypot running on port {PORT}")

    while True:
        client, addr = sock.accept()
        print(f"[+] Connection from {addr[0]}")
        threading.Thread(target=handle_connection, args=(client, addr)).start()

if __name__ == "__main__":
    start_server()
