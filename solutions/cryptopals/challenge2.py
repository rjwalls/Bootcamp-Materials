
result = ''

in1 = '1c0111001f010100061a024b53535009181c'.decode('hex')
in2 = '686974207468652062756c6c277320657965'.decode('hex')

result = [format(ord(a) ^ ord(b), 'x') for (a,b) in zip(in1, in2)]
result = ''.join(result)
print result

assert result == '746865206b696420646f6e277420706c6179'
