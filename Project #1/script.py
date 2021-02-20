import subprocess

# Get input file
if __debug__:
	fileIn = "out.pcap"
else:
	fileIn = input( "Please enter the name of the pcap file: " )

# Constants
commands = [	'tshark', '-r', fileIn, '-Y', 'tls.handshake.type==1',
		'-T', 'fields', '-e', 'ip.src', '-e', 'ip.dst',
		'-e', 'tls.handshake.extensions_server_name' ]
getOrg = [ 'whois', '-H' ]
TYPE_ORG = 'OrgName:'


# Run Process
proc = subprocess.run( args=commands, capture_output=True )

# Convert byte output to str
output = proc.stdout.decode().split()
print( "Finished parsing with tshark." )

# Split into a set of tuples to remove duplicates
# [ Src IP, Dst IP, Server Name ]
websites = { tuple(output[i:i+3]) for i in range(0,len(output),3) }

# Get organization for each
completed = []
for site in websites:

	# Run whois command
	tempProc = subprocess.run( args=getOrg+[site[1]], capture_output=True )
	tempOut = tempProc.stdout.decode()

	# Slice organization name
	locBegin = tempOut.find( TYPE_ORG )
	locEnd = tempOut.find( "\n", locBegin )

	# Append to final list
	completed += [ site + ( tempOut[ locBegin+len(TYPE_ORG):locEnd ].lstrip(), ) ]

print( "Finished getting organization." )

# Get output file
if __debug__:
	fileOut = "out.txt"
else:
	fileOut = input( "Please enter the name of the output file: " )

# Write to output
with open( fileOut, 'w' ) as f:
	for siteInfo in completed:
		sentence = ' '.join( siteInfo )
		f.write( sentence + '\n' )
