
crackme0x00a: Run strings and password is obvious

crackme0x00b: Run `strings -e L crackme0x00b` because the string is 32-bit
little endian.

crackme0x01: Use IDA to find the comparison instruction at 0x80842B which
compares the input to constant value 0x149a. Convert that value to decimal and
use as the password:
 - 5274
 - alternatively use `gobjdump -M intel -D ../challenges/crackme0x01 | grep -A 30 '<main>' 

crackme0x02: Easiest to solve using gdb. Just throw a breakpoint at the
comparision (0x0804844e) between the input password and the correct password.
Use `x/xw $ebp-0xc` to get the value of the password.
 - Note, you `disas main` to find the branch point  manually, or you can use
   IDA. The latter is easier. 
