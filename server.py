import socket
import threading

class client (threading.Thread):
	def __init__(self, sock, addr):
		self.pair = None
		self.sock = sock
		self.addr = addr
		threading.Thread.__init__(self)
	def set_pair(self, pair):
		if (self.pair != pair):
			self.pair = pair
			self.sock.send("pair")
		if (!pair):
			pair.set_pair(self)
	def run(self):
		while (true):
			buf = self.sock.recv(1024)
			if (self.pair):
				self.pair.sock.send(buf)
			else:
				self.sock.send("no pair")
			if (buf == "exit"):
				self.pair.set_pair(None)
				break
		self.sock.close()
host = "localhost"
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
c = []
while True:
	sock, addr = s.accept()
	newC = client(sock, addr)
	for i in range(len(c)):
		if (!c[i].pair):
			c[i].set_pair(newC)
			break
	c.append(newC)
