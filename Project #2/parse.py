import subprocess
from collections import defaultdict

PORT_INFO = "/etc/services"

# Get input file
if __debug__:
	fileIn = '2-20_nmap.pcap'
else:
	fileIn = input( "Please enter the name of the pcap file: " )

parse = [	'tshark', '-r', fileIn, '-Y', 'tcp',
		'-T', 'fields', '-e', 'tcp.srcport',
		'-e', 'tcp.dstport', '-e', 'tcp.ack'	]

# Run Process
proc = subprocess.run( args=parse, capture_output=True )

# Convert byte output to str
out = proc.stdout.decode().split()

# Split into a list of tuples for easier parsing
out = [ out[i:i+3] for i in range(0,len(out),3) ]

# Map source ports to ( destination ports to responses )
ports = defaultdict( lambda:defaultdict(int) )
for src,dst,ack in out:
	ports[src][dst] += int(ack)
	ports[dst] # Ensure the dst port is initialized

states = dict()
for src in ports.keys():
	for dst in ports[src]:
		# Response
		if src in ports[dst].keys():
			if ports[src][dst] > 0:
				states[src] = "Open"
				states[dst] = "Open"

		# No response
		else:
			states[src] = "Filtered"
			states[dst] = "Filtered"

# Filter the source ports
# Looks like the real ports are <10000?
filtered = dict()
for k,v in states.items():
	if int(k) < 10000:
		filtered[int(k)] = v

# Sort ports from low to high
portSorted = sorted( filtered.items() )

# Read in port descriptions
with open( PORT_INFO, 'r' ) as f:
	info = f.read()

# Append port descriptions
portInfoSorted = []
for k,v in portSorted:
	tempInfo = info.split( str(k) + "/tcp" )[0]
	tempInfo = tempInfo.rstrip().split()
	portInfoSorted.append( (k,v,tempInfo[-1]) )

# Get output file
if __debug__:
	fileOut = "out.txt"
else:
	fileOut = input( "Please enter the name of the output file: " )

# Write to file
with open( fileOut, 'w' ) as f:
	f.write( "Port\t" + "State\t" + "Service" + "\n" )
	for k,v,s in portInfoSorted:
		f.write( str(k) + "/tcp " + v + " " + s + "\n" )
