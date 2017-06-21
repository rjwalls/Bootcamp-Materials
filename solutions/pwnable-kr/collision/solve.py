from pwn import *

shell = ssh('col', 'pwnable.kr', password='guest', port=2222)

col = shell.run('./col ' + '\xc8\xce\xc5\x06'*4 + '\xcc\xce\xc5\x06')
print col.recvall()
