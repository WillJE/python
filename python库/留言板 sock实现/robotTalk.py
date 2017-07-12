import socketserver

class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        conn.sendall(bytes("你好，我是机器人", encoding="utf-8"))
        while True:
            ret_bytes = conn.recv(1024)
            ret_str = str(ret_bytes, encoding="utf-8")
            if ret_str == "q":
                break
            conn.sendall(bytes(ret_str+"你好我好大家好", encoding="utf-8"))

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 8888), Myserver)
    server.serve_forever()


import socket
obj = socket.socket()
obj.connect(("127.0.0.1", 8888))
ret_bytes = obj.recv(1024)
ret_str = str(ret_bytes, encoding="utf-8")
print(ret_str)
while True:
    inp = input("你好请问您有什么问题？ \n >>>")
    if inp == "q":
        obj.sendall(bytes(inp, encoding="utf-8"))
        break
    else:
        obj.sendall(bytes(inp, encoding="utf-8"))
        ret_bytes = obj.recv(1024)
        ret_str = str(ret_bytes, encoding="utf-8")
        print(ret_str)

