import sys
import telnetlib
import argparse
import re
from socket import *

parser = argparse.ArgumentParser(description='HTTP over Telnet over Telnet Proxy')
parser.add_argument('hostname', help='Telnet host',action='store')
parser.add_argument('password', help='Telnet password',action='store')
parser.add_argument('destination', help='Telnet over Telnet Destination',action='store')
args = parser.parse_args()


s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
s.bind(('', 23238))            # bind it to the server port
s.listen(10)                         # allow 10 simultaneous pending connections

tn = telnetlib.Telnet(args.hostname)

tn.read_until("Password: ")
tn.write(args.password + "\n")
# Wait for a Cisco ">" prompt
print tn.read_until(">")
print "Connected"
tn.write("term len 0\n")
print tn.read_until(">")
while 1:
    # wait for next client to connect
	connection, address = s.accept() # connection is a new socket
	print "Accepted new connection"
	buffer = ""
	while 1:
		data = connection.recv(102400) # receive up to 10K bytes
		data = re.sub("Accept-Encoding.*[gzip|deflate].*\n","",data) # Strip unwanted headers
		data = re.sub("Referer.*\n","",data)
		if data:
			# Open telnet connection to detination
			tn.write("telnet "+args.destination+" 80\n")
			# Wait 1 sec ... Ugly hack
			tn.read_until("Open")
			# Push data from browser to dest
			tn.write(data+"\n")
			# Wait for HTTP Headers in reply -- Ugly again
			tn.read_until("\nHTTP")
			#Detected connection closed 
			buffer = tn.read_until("[Connection to "+args.destination+" closed by foreign host]")
			buffer = buffer[:-(len("[Connection to "+args.destination+" closed by foreign host]"))]
			# Send reponse back to browser
			connection.send("HTTP"+buffer)
			break
		else:
			break
	connection.close()     

