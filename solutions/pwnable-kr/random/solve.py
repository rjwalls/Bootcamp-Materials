from pwn import *

s = ssh(host='pwnable.kr', user='random', password='guest', port=2222)
proc = s.process('/home/random/random')
proc.sendline('3039230856')
print proc.recv(1024)
