import pyfirmata
import socket
import sys
import videoStream

host = "localhost"
port = 4444

if __name__ == "__main__":
	if (len(sys.argv)>1):
		host = sys.argv[1]
	if (len(sys.argv)>2):
		port = int(sys.argv[2])
	print "connect to ", host,":",port

out_p = [10,9,8,7,6,5]
pins = {
'x' : [0,0,0,0,0,0], 
'w' : [1,0,1,1,1,0], 
'a' : [1,1,0,1,1,0], 
's' : [1,1,0,1,0,1], 
'd' : [1,0,1,1,0,1]  
}
def set_pins(pins):
        for i in range(len(out_p)):
		b.digital[out_p[i]].write(pins[i])


b = pyfirmata.Arduino('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_6413138333135120A251-if00')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
while True:
	result = s.recv(1024)
	print result
	if result == "exit":
		break
	elif result.startwith("pair"):
		hostip = result[4:len(result)]
		print "pair avaiilable on ip ", hostip
		videostream = videoStream.Server(hostip)
		print "caps = ", videostream.emmiter.get_property("caps")
		s.send("caps"+videostream.emmiter.get_property("caps"))
		videostream.start()
		print "stream start"
	elif result[0] in pins:
		set_pins(pins[result[0]])
s.close()
