import socket
import threading


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "windows-1254"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            data = open("data.txt", "a")
            data.write(msg)
            data.close()

            data = open("data.txt", "r")
            data = data.read()

            message = data.encode(FORMAT)
            msg_length = len(data)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))
            conn.send(send_length)
            conn.send(message)

    conn.close()


def send_message(conn):
    data = open("data.txt", "r")
    data = data.read()

    message = data.encode(FORMAT)
    msg_length = len(data)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("Server is starting...")
start()