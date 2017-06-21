Flag: "Sorry mom.. I got confused about scanf usage :("

We want to exploit the Global Offset Table (GOT) to make the call to `fflush`
(in the login function) actually call the line `system("/bin/cat flag")`.
Fortunately, the program's use of scanf allows us to write to an arbitrary
location in memory. This is because the value of passcode1 is interpreted as a
pointer by scanf. 

To make passcode1 point where we want it, we have to use residual data on the
stack left by the call to the welcome function. After some stack examination we
see that the location of the last 4 bytes of the name array are the same
location used for password one. Thus, we need to put our pointer there.

But what should we point to? Here's where the GOT comes in. We use the
following command to figure out the dynamic relocations of the fflush function:
`objdump -R passcode`. In this case, it is at `0x804a004`. We want to write a
new value to this address (done as part of the vulnerable scanf) to cause the
call to exit to jump to a different bit of code. A bit of disassembly
examination tells use that 0x80485e3 would be a good location as that is the
start of the call to system in the login function. 

Tricky bit: scanf uses the format specifier `%d` so we have to input the target
address as an ascii decimal string. So we convert 0x80485e3 (the address that
begins the call to system in the login function) to decimal 134514147.

