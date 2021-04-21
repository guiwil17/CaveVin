# coding: utf-8

import socket
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("93.7.175.167", 1111))

m ={"fonction": "login", "paramètres": ["Test","Test"]}
data = json.dumps(m)

s.sendall(bytes(data,encoding="utf-8"))

r = s.recv(9999999)
r = r.decode("utf-8")

print(r)