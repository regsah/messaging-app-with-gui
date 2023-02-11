from tkinter import *
import socket


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "windows-1254"
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

class Instamess:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.my_window(myframe=frame)

    def my_window(self, myframe):

        scrollbar = Scrollbar(myframe)
        scrollbar.pack(side="right", fill=Y)

        text = Text(myframe, undo=True,  yscrollcommand=scrollbar.set, borderwidth=3)
        text.pack(side="top", fill=X)
        text.configure(state="disabled")
        scrollbar.config(command=text.yview)

        entry_frame = Frame(master=myframe)
        entry_frame.pack(side="bottom", fill=X)

        user_name_entry = Entry(entry_frame, borderwidth=3)
        user_name_entry.grid(column=0, sticky="wesn", row=0)

        entry = Entry(entry_frame, borderwidth=3)
        entry.grid(column=1, columnspan=4, sticky="wesn", row=0)
        entry.bind("<Return>", lambda event: self.take_message(entry, user_name_entry, text))

        send_button = Button(entry_frame, text="SEND", padx=2, borderwidth=3, command=lambda: self.take_message(entry, user_name_entry, text))
        send_button.grid(column=5, sticky="wesn", row=0)
        col_count, row_count = entry_frame.grid_size()

        for col in range(col_count):
            entry_frame.grid_columnconfigure(col, minsize=100)

        for row in range(row_count):
            entry_frame.grid_rowconfigure(row, minsize=10)

        self.send_message(msg="", user_name="", text=text)


    def take_message(self, entry, user_name_entry, text):
        msg = entry.get()
        if msg:
            user_name = f"[{user_name_entry.get()}] "
            msg = msg + "\n"
            self.send_message(msg, user_name, text)

    def send_message(self, msg, user_name, text):
        msg = f"{user_name}{msg}"
        message = msg.encode(FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

        self.get_message(text)

    def get_message(self, text):

        msg_length = client.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)

        if msg != text.get("1.0", END):
            text.configure(state="normal")
            text.delete("1.0", END)
            text.insert("1.0", msg)
            text.configure(state="disabled")

        text.after(1000, lambda: self.send_message(msg="", user_name="", text=text))


root = Tk()
App = Instamess(root)
root.mainloop()
