Flag: "Mommy, I thought libc random is unpredictable..."

This challenge is pretty easy because they use the stdlib rand function without
providing a seed. As a result, the variable `random` is actually the same each
time. The solution is to write a bit of C code to find out that value---it is
1804289383 by the way---and then XOR with the value 0xdeadbeef to figure out
what the input key needs to be.

