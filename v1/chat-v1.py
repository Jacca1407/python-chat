import socket
import threading

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static, Input

print("\033[31m-------------------------------------------------- CHAT --------------------------------------------------\033[0m")

while True:
    REMOTE_IP = input("Remote IP address: ")
    try:
        int(REMOTE_IP.replace(".", ""))
        break
    except:
        print("\033[38;5;208mIP address is not valid. Try again\033[0m")

while True:
    try:
        REMOTE_PORT = int(input("Remote port: "))
        break
    except:
        print("\033[38;5;208mRemote port is not valid. Try again\033[0m")

while True:
    try:
        LOCAL_PORT = int(input("Listening port: "))
        break
    except:
        print("\033[38;5;208mListening port is not valid. Try again\033[0m")

class Chat(App):
    CSS_PATH = "style.tcss"
    theme = "nord"

    def compose(self) -> ComposeResult:
        self.chat_log = Static("Waiting for connection...", id="log")
        yield Header()
        yield Footer()
        yield Vertical(self.chat_log, id="chat-box")
        yield Input(placeholder="Message...", id="input")

    def on_mount(self) -> None:
        threading.Thread(target=self.server, daemon=True).start()
        threading.Thread(target=self.client, daemon=True).start()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        msg = event.value.strip()
        if msg and self.peer_socket:
            try:
                self.peer_socket.send(msg.encode())
                self.append_message(r"\[You] " + msg)
            except:
                self.append_message(r"[orange]\[Not sent!][/] " + msg)
        self.query_one("#input", Input).value = ""

    def append_message(self, message: str):
        self.chat_log.update(self.chat_log.renderable + f"\n{message}")

    def server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', LOCAL_PORT))
        sock.listen(1)
        conn, addr = sock.accept()
        self.append_message(f"Connection established with {addr[0]}:{REMOTE_PORT}\n")
        self.peer_socket = conn
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode()
                self.call_from_thread(lambda: self.append_message(r"\[Peer] " + msg))
            except Exception as e:
                print("Server error" + str(e))
                break

    def client(self):
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((REMOTE_IP, REMOTE_PORT))
                self.peer_socket = sock
                while True:
                    msg = sock.recv(1024).decode()
                    if msg:
                        self.call_from_thread(lambda: self.append_message(r"\[Peer] " + msg))
            except Exception as e:
                print("Server error" + str(e))

    peer_socket = None

if __name__ == "__main__":
    Chat().run()
