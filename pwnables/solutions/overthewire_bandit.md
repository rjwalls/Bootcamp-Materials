# About


Solutions for the [Over the Wire Bandit challenges][bandit].

[bandit]:http://overthewire.org/wargames/bandit/bandit2.html

# Solutions

Level 1: `less ./-` because `-` is, by convention, interpreted to mean stdin.

Level 4: `less ./*`. Need to specify the directory because of the dash. Also,
less will let you know if the file "appears to be binary" so you can just
ignore it.

Level 5: `find inhere/ -size 1033c \! -executable -exec file {} \;` finds a
file that is 1033 bytes, not executable, and checks the file type with `file`.
This will tell us if the found files are human readable.

Level 6: `find / -size 33c -group bandit6 -user bandit7 2> /dev/null`. We
redirect stderr to dev/null to clean up the output. 

Level 8: `sort data.text | uniq -c | sort | less`

Level 9: `strings data.txt | grep -E "^=="`

Level 10: `base64 -d data.txt`

Level 11: `cat data.txt | tr '[A-Za-z]' '[N-ZA-Mn-za-m]'` Basically, a rot13
cipher.

Level12: Lots of usage of tar, gzip, bzip2, mv, and file. The `file` command is
useful because it tells you how the current working file is compressed. The
final file name is data8.
 - 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL

Level13: `ssh localhost -i ./sshkey.private -p 2220 -l bandit14`. Then `cat
/etc/bandit_pass/bandit14`
 - 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e

Level 14: `echo 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e | nc localhost 30000`
 - BfMYroe26WYalil77FoDi9qh59eK5xNr

Level 15: `echo BfMYroe26WYalil77FoDi9qh59eK5xNr | openssl s_client -connect
localhost:30001 -ign_eof`
 - cluFn7wTiGryunymYOu4RcffSxQluehd

Level 16: `echo  cluFn7wTiGryunymYOu4RcffSxQluehd| openssl s_client -connect
localhost:31790 -ign_eof`. Have to save the return private key (into a tmpdir)
and use it like level 15. Need to also set the permissions of the key file:
`chmod 600 ./tmp.key`

Level 17: `diff passwords.new passwords.old`
 - kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd

Level 18: `ssh bandit.labs.overthewire.org -p 2220 -l bandit18 'cat readme'`
 - IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x

Level 19: `./bandit20-do cat /etc/bandit_pass/bandit20`
 - GbKksEFF4yrVs6il55v6gwY5aVje5f0j

Level 20: On session 1: `./suconnect 34555`. On session 2: `echo GbKksEFF4yrVs6il55v6gwY5aVje5f0j | nc -l 34555`
 - gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr

Level 21: `less cronjob_bandit22; cat /usr/bin/cronjob_bandit22.sh; cat
/tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv`
 - Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI

Level 22: `cat /usr/bin/cronjob_bandit23.sh` and then follow the script.
 - jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n

Level 23: Copy the following script into /var/spool/bandit24/: `mkdir
/tmp/muffin1/
cat /etc/bandit_pass/bandit24 > /tmp/muffin1/bandit24`
 - UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ

Level 24: Just use a python script and the following: `python script.py | nc
localhost 30002`
 - uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG

Level 25--26: Look in the `/etc/passwd` file to find the user's default shell,
it points to `/usr/bin/showtext`. If we read the contents of `showtext` we see
the line `more ~/text.txt` and not much else. This is the line we need to
exploit. 

Our goal is to trigger the interactive mode of more, which will give us the
ability to execute additional commands from inside of `more`. You can trigger
this mode when size of your terminal isn't big enough to display all of the
lines in the file. At first, I tried to make the file bigger.  To do this, I
would need to modify the home directory to point someplace we have write access
too. So I tried passing the environment variables using `ssh -o SendEnv=HOME`
to modify the home directory , but only limited environment passing is allowed.
From the

`/etc/ssh/sshd_config`:

```
# Allow client to pass locale environment variables
AcceptEnv LANG LC_* WECHALL*
```

The easier solution is to simply make your terminal window smaller, i.e., drag
the bottom edge of your terminal window to make it as short as possible. Once
you are in interactive mode, press `v` to open up the file in VI. Once in VI,
you are free to open and read any file accessible with the current user's
permissions: `:e /etc/bandit_pass/bandit26`
 - 5czgV9L3Xx8JPOyRbXh6lQbmIOWvPT6Z

You can also launch a shell from inside of vi:

```
:set shell=/bin/bash
:sh
```

By default, the `:sh` command in Vi uses the SHELL environment variable. That
won't work for us in this case so we have to set it manually.
