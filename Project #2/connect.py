import subprocess
import socket

# Wait LIM seconds for a response
LIM = 1

if __debug__:
	host = 'github.com'
	ports = [ 21,22,23,25,80,443 ]
#	host = 'synprint.com'
#	ports = [ 21,22,23,25,80,110,139,443,445,3389 ]
else:
	host = input( "Please enter the target host: " )
	ports = [ int(x) for x in
			input( "Please enter the list of ports to scan: " ).split(',') ]

# Simple HTTP Request
request = "Get / HTTP/1.1\r\nHost:" + host + "\r\n\r\n"

for port in ports:

	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	s.settimeout(LIM)

	print( "Port " + "#" + str(port) + ": ", end="" )

	try:
		res = s.connect_ex( (host,port) )

		if res == 0:
			s.recv(4096)
			print( "SSH Successful." )
		else:
			print( "Connection failed." )

	except socket.error:
		try:
			s.send( request.encode() )
			print( "HTTP Request Successful." )
		except:
			print( "???" )

	finally:
		s.close()


