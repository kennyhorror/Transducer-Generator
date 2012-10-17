#!/usr/bin/python

import codecs
import subprocess

if __name__ == '__main__':
  words = []
  for line in open('italian.txt.learn', 'r'):
    columns = line.split()
    words.append(columns[0].decode("ISO-8859-2") + u'\n')
  stdin = u'source italian.foma\nup\n'.join(words)

  process = subprocess.Popen("./foma", stdin = subprocess.PIPE,
      stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = process.communicate(stdin.encode('utf-8'))
  output = codecs.open('italian.txt.result', encoding='utf-8', mode='w+')
  itr = 0
  for line in stdout.decode('utf-8').split('\n')[:-3]:
    itr += 1
    if itr < 27:
      continue
    output.write(line.split('> ')[-1])
    output.write('\n')
  output.close()
