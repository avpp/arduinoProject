import socket

host = 'localhost'
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
while True:
	c = raw_input()
	print "now send ", c
	s.send(c)
	if (c == 'exit'):
		break
s.close()
