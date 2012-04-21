import socket
import sys
import cv2
import threading
import videoStream
##
## control by opencv window
## press ESC for disconnect from server and close window
## press ENTER to change type of input (fixed/not fixed)
## press UP to send move forward command
## press DOWN to send move back command
## press LEFT to send turn left command
## press RIGHT to send turn right command
## press SPACE to send stop command (important in fixrd type of control)
##
class listener (threading.Thread):
	def __init__(self, sock):
		self.sock = sock
		self.alive = True
		threading.Thread.__init__(self)
	def run(self):
		while (self.alive):
			buf = self.sock.recv(1024)
			print "accept ", buf
			if (buf.startwith("caps")):
				CAPSparam = buf[4:len(buf)]
				print "we have caps = ", CAPSparam
				stream = videoStream.client(CAPSparam)
				stream.start()
				print "vido create"
host = 'localhost'
port = 4444
if __name__ == "__main__":
	print sys.argv
	if len(sys.argv) > 1:
		host = sys.argv[1]
	if len(sys.argv) > 2:
		port = int(sys.argv[2])
print "connect to", host,":",port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
l = listener(s)
l.start()
buttons = {1113937 : 'a',
	   1113938 : 'w',
	   1113939 : 'd',
	   1113940 : 's',
	   1048608 : 'x'}
pressState = True
changeButton = 1048586
escapeButton = 1048603
lastState='x'
count = 0
cv2.namedWindow("Control")
print "create window"
while True:
	checkTime = 0
	if pressState:
		checkTime = 1000
	key = cv2.waitKey(checkTime)
	print "key= ", key
	newState = lastState
	if key == escapeButton:
		s.send("exit")
		break
	elif key in buttons:
		newState = buttons[key]
	elif key == changeButton:
		pressState = not pressState
	elif key == -1 and pressState:
		newState = 'x'
	if newState != lastState :
		print "now_send", newState
		s.send(newState)
		lastState = newState
#	c = raw_input()
#	print "now send ", c
#	s.send(c)
#	if (c == 'exit'):
#		break
s.close()
