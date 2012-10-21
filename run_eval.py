#!/usr/bin/env python

import codecs
import subprocess

from config import FOMA_PATH


if __name__ == '__main__':
    questions = []
    answers = []
    counts = {}

    for line in codecs.open('italian.txt.learn', encoding='ISO-8859-1', mode='r'):
        columns = line.split()
        questions.append(columns[0])
                                             
    process = subprocess.Popen([FOMA_PATH + 'flookup', 'italian.bin', '-x'], 
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    stdin = u'\n'.join(questions)
    (stdout, stderr) = process.communicate(stdin.encode('utf-8'))

    fomas = stdout.decode('utf-8').split('\n\n')

    for results in fomas:
      for answer in results.split('\n'):
        key = '+'.join(answer.split('+')[0:2])
        if counts.has_key(key):
          counts[key] = counts[key] + 1
        else:
          counts[key] = 1

    output = codecs.open('lemmas.txt', encoding='utf-8', mode='w+')
    words = set()
    for question, results in zip(questions, fomas):
      best = -1
      best_lemma = ""
      for answer in results.split('\n'):
        key = '+'.join(answer.split('+')[0:2])
        if counts[key] > best:
          best = counts[key]
          best_lemma = key
#      output.write("%s %s %d\n" % (question, results, best))
      words.add(best_lemma)

    lemmas = sorted(list(words))
    output.write(u'\n'.join(lemmas))
