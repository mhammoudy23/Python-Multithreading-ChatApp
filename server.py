from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

HOST = "127.0.0.1"
PORT = 1234
BUFF = 1024
ADDR = (HOST, PORT)

S = socket(AF_INET, SOCK_STREAM)
S.bind(ADDR)
clients = {}
addr = {}

def broadcast(msg, prefix=""):  # Displays the messages for all to see
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

#Handles new users registering

def UserReg():
    while True:
        client, client_addr = S.accept()
        print("%s:%s is in the room." % client_addr)
        client.send(bytes("Please start by entering your username", "utf8"))
        addr[client] = client_addr
        Thread(target=UserIn, args=(client,)).start()

#Handles New users entering the chat
def UserIn(client):

    name = client.recv(BUFF).decode("utf8")
    welcome = 'You have now joined the council %s' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the council" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFF)
        if msg != bytes("[exit]", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("[exit]", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the council" % name, "utf8"))
            break


if __name__ == "__main__": #Handles the multi-threading
    S.listen(5)
    print("Connecting....")
    ACCEPT_THREAD = Thread(target=UserReg)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()

    S.close()
