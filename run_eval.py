#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        if part == u'N' and not (lemma.endswith(u'a') or lemma.endswith(u'o') or
                                 lemma.endswith(u'i') or lemma.endswith(u'e') or
                                 lemma.endswith(u'à') or lemma.endswith(u'r')):
          continue
        elif part == 'A' and not (lemma.endswith('to') or lemma.endswith('e') or
                                   lemma.endswith('o') or lemma.endswith('a') or lemma.endswith(u'ista')):
          continue
        elif part == u'V' and not lemma.endswith(u're'):  # Need to be extended.
          continue
        

        key = '+'.join((lemma, part))
        weight = 1
        if part == u'N':
          weight = 7
          if lemma.endswith(u'e') or lemma.endswith(u'i'):
            weight = 8
        elif part == u'A':
          weight = 6
        if counts.has_key(key):
          counts[key] = counts[key] + weight
        else:
          counts[key] = weight

    output = codecs.open('lemmas.txt', encoding='utf-8', mode='w+')
    output2 = codecs.open('answer.txt', encoding='ISO-8859-1', mode='w+')
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
      output2.write("%s\t%s\n" % (question, best_lemma))
      words.add(best_lemma)

    lemmas = sorted(list(words))
    output.write(u'\n'.join(lemmas))
