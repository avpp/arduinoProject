import socket
import threading
import sys

c = []

class client (threading.Thread):
	def __init__(self, sock, addr):
		self.pair = None
		self.sock = sock
		self.addr = addr
		self.isContinue = True
		threading.Thread.__init__(self)
	def stop(self):
		self.isContinue = False
	def send(self, msg):
		try:
			self.sock.send(msg)
		except:
			print "client ", self.pair, " disconnected"
			self.stop()
			if (self.pair != None):
				self.pair.set_pair(None)
	def set_pair(self, pair):
		if (self.pair != pair):
			self.pair = pair
			if (pair != None):
				print "set pair:", self.addr, " -> ", pair.addr
				self.send("pair"+pair.addr[0])
				pair.set_pair(self)
			else:
				print "delete pair for", self.addr
				self.send("no pair")
	def run(self):
		while (self.isContinue):
			try:
				buf = self.sock.recv(1024)
			except socket.error:
				print "socket exception by:", self.addr
			except KeyboardInterrupt:
				print "keyboard interrupt"
				break
			print "accept from client ", self.addr, " : '", buf, "'"
			if (buf == "exit"):
				print "client ", self.addr, " exit"
				if (self.pair != None):
					self.pair.set_pair(None)
				break
			if (self.pair != None):
				print "transmit message:",self.addr, "--'", buf, "'-->", self.pair.addr
				self.pair.send(buf)
			else:
				print "can't transmit message for client", self.addr, "becouse no pair"
				self.send("no pair")
		print "delete client ", self.addr
		c.remove(self)
		self.sock.close()

host = "0.0.0.0"
port = 4444

if __name__ == "__main__":
	if (len(sys.argv)>1):
		port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
while True:
	print "listen for new Client"
	try:
		sock, addr = s.accept()
	except KeyboardInterrupt:
		for i in range(len(c)):
			c[i].stop()
		break
	print "connected ", sock, " ", addr
	newC = client(sock, addr)
	newC.start()
	for i in range(len(c)):
		if (c[i].pair == None):
			print "find pair for ", newC.addr
			c[i].set_pair(newC)
			break
	c.append(newC)
s.close()
