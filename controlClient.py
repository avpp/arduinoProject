import socket
import sys

host = 'localhost'
port = 4444
if __name__ == "__main__":
	print sys.argv
	if len(sys.argv) > 1:
		host = sys.argv[1]
	if len(sys.argv) > 2:
		port = int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
while True:
	c = raw_input()
	print "now send ", c
	s.send(c)
	if (c == 'exit'):
		break
s.close()
