import pyfirmata
import socket

host = "localhost"
port = 4444

pins = {
-1 : [0,0,0,0,0,0,0],
1113938 : [0,1,1,0,0,1,1],
1113940 : [1,0,1,0,1,0,1],
1113937 : [1,0,1,0,0,1,1],
1113939 : [0,1,1,0,1,0,1]
}
def set_pins(pins):
        for i in range(7):
                if (i != 3):
                        b.digital[i+6].write(pins[i])


b = pyfirmata.Arduino('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_6413138333135120A251-if00')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
while True:
	result = s.recv(1024)
	
	if result == "exit":
		break
	elif key in pins:
		set_pins(pins[key])
s.close()
