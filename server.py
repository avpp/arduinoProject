import socket
import threading

c = []

class client (threading.Thread):
	def __init__(self, sock, addr):
		self.pair = None
		self.sock = sock
		self.addr = addr
		threading.Thread.__init__(self)
	def send(self, msg):
		try:
			self.sock.send(msg)
		except:
			print "client ", self, " disconnected"
			if (self.pair != None):
				self.pair.set_pair(None)
	def set_pair(self, pair):
		if (self.pair != pair):
			self.pair = pair
			if (pair != None):
				self.send("pair")
			else:
				self.send("no pair")
			if (pair != None):
				pair.set_pair(self)
	def run(self):
		while (True):
			buf = self.sock.recv(1024)
			print "accept '", buf, "'"
			if (buf == "exit"):
				print "client ", self, " exit"
				if (self.pair != None):
					self.pair.set_pair(None)
				break
			if (self.pair != None):
				print "send to pair"
				self.pair.send(buf)
			else:
				print "no pair"
				self.send("no pair")
		print "delete client"
		c.remove(self)
		self.sock.close()
host = "localhost"
port = 4444
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
while True:
	print "listen for new Client"
	sock, addr = s.accept()
	print "connected ", sock, " ", addr
	newC = client(sock, addr)
	newC.start()
	for i in range(len(c)):
		if (c[i].pair == None):
			print "find pair for"
			c[i].set_pair(newC)
			break
	c.append(newC)
#for i in range(len(c)):
#	c[i].close()
s.close()
