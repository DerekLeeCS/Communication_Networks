import subprocess
import socket

# Wait LIM seconds for a response
LIM = 1
#socket.settimeout(5)

if __debug__:
	host = 'github.com'
	ports = [ 21,22,23,25,80,443 ]
#	host = 'synprint.com'
#	ports = [ 21,22,23,25,80,110,139,443,445,3389 ]
else:
	host = input( "Please enter the target host: " )
	ports = [ x for x in
			input( "Please enter the list of ports to scan: " ).split(',') ]

for port in ports:

	try:
		s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		s.settimeout(LIM)
		res = s.connect_ex( (host,port) )

		if res == 0:
			print( "Port " + "#" + str(port) + ": " +
				s.recv(4096).decode().rstrip() )
		else:
			print( "Port " + "#" + str(port) + ": Connection failed." )

		s.close()

	except socket.error:
		print( "Port " + "#" + str(port) + ": ???" )
