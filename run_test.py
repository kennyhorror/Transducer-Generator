#!/usr/bin/python

import codecs
import subprocess

if __name__ == '__main__':
  words = [u'source italian.foma\nup\n']
  questions = []
  answers = []
  for line in open('italian.txt.learn', 'r'):
    columns = line.split()
    questions.append(columns[0].decode("ISO-8859-1"))
    words.append(columns[0].decode("ISO-8859-1") + u'\n')
    answers.append(u''.join(map(lambda x:x.decode("ISO-8859-1"), columns[1:])))
  stdin = u''.join(words[:1000])
  process = subprocess.Popen("./foma", stdin = subprocess.PIPE,
      stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = process.communicate(stdin.encode('utf-8'))
  output = codecs.open('italian.txt.result', encoding='utf-8', mode='w+')

  fomas = stdout.decode('utf-8').split('apply up> ')[1:-1]

  for word, results, answer in zip(questions,
                                   fomas,
                                   answers):
    output.write(word)
    output.write('\t')
    for result in results.split('\n'):
      output.write(result)
      output.write('\t')
    output.write(answer)
    output.write('\n')
  output.close()
