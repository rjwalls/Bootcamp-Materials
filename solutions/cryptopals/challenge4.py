from challenge3 import break_single_byte_xor, num_english_words


def test_line(line):
  strings = []
  word_count = []

  for x in xrange(256):
    hexstr = xor(line, format(x, 'x'))
    strings.append(hexstr.decode('hex'))
    word_count.append(num_english_words(strings[-1]))
   
  results = sorted(zip(word_count, strings), key=lambda s: s[0], reverse=True)

  return results[0]

def main():
  with open('4.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]

  results = []

  for line in lines:
    score, decrypted = break_single_byte_xor(line, num_english_words)[0]  
    
    if score > 0:
      results.append((score, decrypted))

  for score, decrypted in sorted(results, key=lambda s: s[0], reverse=True)[:3]:
    print decrypted 


if __name__ == "__main__":
  main()
