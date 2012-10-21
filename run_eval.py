#!/usr/bin/env python

import codecs
import subprocess

from config import FOMA_PATH


if __name__ == '__main__':
    questions = []
    answers = []
    counts = {}

    for line in codecs.open('italian.txt.test.clean', encoding='ISO-8859-1', mode='r'):
        columns = line.split()
        questions.append(columns[0])
                                             
    process = subprocess.Popen([FOMA_PATH + 'flookup', 'italian.bin', '-x'], 
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    stdin = u'\n'.join(questions)
    (stdout, stderr) = process.communicate(stdin.encode('utf-8'))

    fomas = stdout.decode('utf-8').split('\n\n')[:-1]

    for results in fomas:
      for answer in results.split('\n'):
        lemma, part = answer.split('+')[0:2]

        # Avoid bad lemmas.
        if part == u'N' and not (lemma.endswith('a') or lemma.endswith('o') or
                                 lemma.endswith('i') or lemma.endswith('e')):
          continue
        elif part == u'A' and not (lemma.endswith('to') or lemma.endswith('re')):
          continue
        elif not lemma.endswith('re'):  # Need to be extended.
          continue

        key = '+'.join((lemma, part))
        weight = 1
        if answer.split('+')[1] == u'N':
          weight = 4
        elif answer.split('+')[1] == u'A':
          weight = 3
        if counts.has_key(key):
          counts[key] = counts[key] + weight
        else:
          counts[key] = weight

    output = codecs.open('lemmas.txt', encoding='utf-8', mode='w+')
    output2 = codecs.open('answer.txt', encoding='utf-8', mode='w+')
    words = set()
    for question, results in zip(questions, fomas):
      best = -1
      best_lemma = question + u'+N'
      for answer in results.split('\n'):
        key = '+'.join(answer.split('+')[0:2])
        if not counts.has_key(key):
          continue
        if counts[key] > best:
          best = counts[key]
          best_lemma = key
      output2.write("%s\t%s" % (question, best_lemma))
      words.add(best_lemma)

    lemmas = sorted(list(words))
    ioutput.write(u'\n'.join(lemmas))
