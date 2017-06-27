import enchant
import string

from collections import Counter


dictionary = enchant.Dict('en_US')
printable = set(string.printable)


def xor(in1str, keystr):
  """
  Assumes the inputs are hex strings, e.g., 'DEADBEEF', and
  returns a hex string.
  """
  keystr = keystr[:len(in1str)]
  keystr *= len(in1str) / len(keystr)
  keystr += keystr[:len(in1str)%len(keystr)]

  in1 = in1str.decode('hex')
  in2 = keystr.decode('hex') 

  result = [format(ord(a) ^ ord(b), '02x') for (a,b) in zip(in1, in2)]

  return ''.join(result)


def num_english_words(instr):
  # Make sure all of the characters are printable,  because enchant will raise an
  # exception on strange characters 

  if not set(instr).issubset(printable):
    return 0
  try:
    # TODO: this will only split on whitespace (not punctuation)
    # a more robust approach might be to use regex.
    words = [w for w in instr.split(' ') if dictionary.check(w)] 
    return len(words)
  except:
    return 0


def freq_letters(instr):
  """
  Calculates the frequency of each letter in a string
  Returns a Counter object.

  Operation is case insensitive
  """
  count = Counter() 

  for c in instr:
    count[c.lower()] += 1 

  return count


def freq_score(instr):
  """
  Returns a simple score based on English letter freq.
  source: https://inventwithpython.com/hacking/chapter20.html
  """
  count = freq_letters(instr)  
  return len([l for l, freq in count.most_common(6) if l in 'etaoin'])


def break_single_byte_xor(instr, metric):
  """
  metric is a function pointer: int metric(str)
  """

  results = []

  for x in xrange(256):
    decrypted = xor(instr, format(x, '02x')).decode('hex')
    score = metric(decrypted)

    results.append((score, decrypted))

  return sorted(results, key=lambda s: s[0], reverse=True) 

 

def main():
  in1str = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

  print break_single_byte_xor(in1str, num_english_words)[0]
  print break_single_byte_xor(in1str, freq_score)[0] 


if __name__ == "__main__":
  main()
