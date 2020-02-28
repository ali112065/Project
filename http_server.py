from socket import *
from select import *


class HTTPserver:
    def __init__(self, host="0.0.0.0", port=8000, dir=None):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.dir = dir
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.sockfd = socket()
        self.sockfd.setblocking(False)
        self.sockfd.bind(self.address)

    def server_forever(self):
        self.sockfd.listen(3)
        print("Listen the port %d" % self.port)
        self.rlist.append(self.sockfd)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sockfd:
                    c, addr = r.accept()
                    c.setblocking(False)
                    self.rlist.append(c)
                else:
                    self.handel(r)

    def handel(self, connfd):
        request = connfd.recv(4096)
        if not request:
            connfd.close()
            self.rlist.remove(connfd)
            return

        info = request.decode().split(' ')[1]
        print("请求内容：", info)

        if info == "/":
            info = "/index.html"

        try:
            f = open(self.dir + info)
        except:
            data = "HTTP/1.1 404 Not Found\r\n"
            data += "Content-Type:text/html\r\n"
            data += "\r\n"
            data += "Sorry...."
        else:
            f = open('index.html')
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type:text/html\r\n"
            data += "\r\n"
            data += f.read()
            f.close()
        connfd.send(data.encode())


if __name__ == '__main__':
    HOST = "0.0.0.0"
    PORT = 8888
    DIR = "./static"
    httpd = HTTPserver(HOST, PORT, DIR)
    httpd.server_forever()
