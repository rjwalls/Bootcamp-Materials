Flag: "daddy! I just managed to create a hash collision :)"

We can use pwntools and `python solve.py` or we can ssh in and use the
following:

```
python -c "import sys; sys.stdout.write('\xc8\xce\xc5\x06'*4 + '\xcc\xce\xc5\x06')" | xargs ./col
```
