from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import *

#Socket Information
HOST = "127.0.0.1"
PORT = 1234
BUFF = 1024
ADDR = (HOST, PORT)

C = socket(AF_INET, SOCK_STREAM)
C.connect(ADDR)

##when clients wants to leave the chat
def Leave(event=None):
    input.set("[exit]")
    send()

#Handles the recieving of a msg
def receive():
    while True:
        try:
            msg = C.recv(BUFF).decode("utf8")
            MsgScript.insert(tk.END, msg)
        except OSError:
            break

#Handles the sending of a msg
def send(event=None):
    msg = input.get()
    input.set("")
    C.send(bytes(msg, "utf8"))
    if msg == "[exit]":
        C.close()
        root.quit()



##The GUI side of the app

root = tk.Tk()
root.title("Elrond")
#The Top Section

MsgWindow = tk.Frame(root)
root.configure(background="burlywood4")
input = tk.StringVar()
input.set(" ")
NavBar = tk.Scrollbar(MsgWindow, bg="DarkOliveGreen4")
MsgScript = tk.Listbox(MsgWindow, height=15, width=50, yscrollcommand=NavBar.set, bg="DarkSeaGreen4")
NavBar.pack(side=tk.RIGHT, fill=tk.Y)# navigate through messages
MsgScript.pack(side=tk.LEFT, fill=tk.BOTH)
MsgScript.pack()
MsgWindow.pack()

#the bottom section
TypeMsg = tk.Entry(root, textvariable=input)
TypeMsg.bind("<Return>", send) ## Press enter to send MSG
TypeMsg.pack(side=LEFT, anchor=N, padx=5, pady=5)
SendBtn = tk.Button(root, text="Send", command=send)
SendBtn.pack(side=tk.LEFT)

root.protocol("WM_DELETE_WINDOW", Leave)
#Handles Threading

RcvThread = Thread(target=receive)
RcvThread.start()

tk.mainloop()  
