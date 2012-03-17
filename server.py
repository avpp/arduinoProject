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
		if (not pair):
			pair.set_pair(self)
	def run(self):
		while (True):
			buf = self.sock.recv(1024)
			print "accept '", buf, "'"
			if (self.pair != None):
				print "send to pair"
				self.pair.sock.send(buf)
			else:
				print "no pair"
				self.sock.send("no pair")
			if (buf == "exit"):
				self.pair.set_pair(None)
				break
		self.sock.close()
host = "localhost"
port = 4444
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
c = []
while True:
	print "listen for new Client"
	sock, addr = s.accept()
	print "connected ", sock, " ", addr
	newC = client(sock, addr)
	print "try run new Thread"
	newC.start()
	print "next work"
	for i in range(len(c)):
		if (not c[i].pair):
			c[i].set_pair(newC)
			break
	c.append(newC)
#for i in range(len(c)):
#	c[i].close()
s.close()
