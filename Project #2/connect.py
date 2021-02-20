import subprocess
import socket

# Wait LIM seconds for a response
LIM = 1
#socket.settimeout(5)

if __debug__:
	host = 'github.com'
	ports = [ 21,22,23,25,80,443 ]
else:
	host = input( "Please enter the target host: " )
	ports = [ x for x in
			input( "Please enter the list of ports to scan: " ).split(',') ]

for port in ports:
	try:
		s = socket.create_connection( (host,port), timeout=LIM )
		print( "Port " + "#" + str(port) + ": " +
			s.recv(4096).decode().rstrip() )
		s.close()
	except:
		print( "Port " + "#" + str(port) + ": Connection failed." )
