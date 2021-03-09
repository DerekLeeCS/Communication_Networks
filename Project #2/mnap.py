import subprocess
import time

if __debug__:
	host = 'github.com'
	ports = [ 21,22,23,25,80,443 ]
	pcapOut = 'out.pcap'
else:
	host = input( "Please enter the name of the target host: " )
	ports = [ int(x) for x in
		input( "Please enter the list of ports to scan: " ).split(',') ]
	pcapOut = input( "Please enter the name of the pcap file: " )
	print( '-'*50 )

# -O flag is to enable inputs to the scripts
#	b/c the scripts use __DEBUG__
capture = [ 'tcpdump', '-w', pcapOut, 'tcp' ]
connect = [ 'python3', '-O', 'connect.py' ]
parse = [ 'python3', '-O', 'parse.py' ]

# ports: List[T] -> str
ports = ','.join( [ str(x) for x in ports ] )

# Start capturing packets
print( "Capturing packets..." )
procCapture = subprocess.Popen( args=capture, stderr=subprocess.DEVNULL )

# Ensure tcpdump is running before connecting to ports
time.sleep(0.5)

# Connect to the given ports
print( "Connecting to ports..." )
procPort = subprocess.Popen( args=connect, stdout=subprocess.PIPE,
				stdin=subprocess.PIPE )
procPort.communicate( input=host.encode() + '\n'.encode() +
			ports.encode() )[0]

# Stop capturing packets
procCapture.terminate()
print( "Finished capturing packets.\n" )

# Parse the packets
print( "Parsing packets..." )
procParse = subprocess.Popen( args=parse, stdout=subprocess.PIPE,
				stdin=subprocess.PIPE )
procParse.communicate( input=pcapOut.encode() + '\n'.encode() +
			'out.txt'.encode() )[0]
print( "Finished parsing packets." )
