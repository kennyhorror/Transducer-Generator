#!/usr/bin/python

import codecs
import subprocess

if __name__ == '__main__':
  words = [u'source italian.foma\nup\n']
  questions = []
  answers = []
  for line in open('italian.txt.learn', 'r'):
    columns = line.split()
    questions.append(columns[0].decode("ISO-8859-2"))
    words.append(columns[0].decode("ISO-8859-2") + u'\n')
    answers.append(u''.join(map(lambda x:x.decode("ISO-8859-2"), columns[1:])))
  stdin = u''.join(words)
  process = subprocess.Popen("./foma", stdin = subprocess.PIPE,
      stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = process.communicate(stdin.encode('utf-8'))
  output = codecs.open('italian.txt.result', encoding='utf-8', mode='w+')
  for word, result, answer in zip(questions,
                                  stdout.decode('utf-8').split('\n')[26:-3],
                                  answers):
    output.write(word)
    output.write('\t')
    output.write(result.split('> ')[-1])
    output.write('\t')
    output.write(answer)
    output.write('\n')
  output.close()
