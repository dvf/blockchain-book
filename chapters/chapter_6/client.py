import json
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 8888))
    s.sendall(json.dumps({"dan": "herro"}).encode())
