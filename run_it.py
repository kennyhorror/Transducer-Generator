#!/usr/bin/env python

import codecs
import subprocess

from config import FOMA_PATH


if __name__ == '__main__':
    questions = []
    for line in codecs.open('italian.txt.test.clean', encoding='ISO-8859-1', mode='r'):
        questions.append(line.split()[0])
                                             
    process = subprocess.Popen([FOMA_PATH + 'flookup', 'italian.bin', '-x'], 
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    stdin = u'\n'.join(questions)
    (stdout, stderr) = process.communicate(stdin.encode('utf-8'))

    fomas = stdout.decode('utf-8').split('\n\n')

    with codecs.open('italian.txt.result', encoding='ISO-8859-1', mode='w+') as output:
        for (word, results) in zip(questions, fomas):
          if results != '+?':
            answers = set()
            for answer in results.split('\n'):
              lemma, part = answer.split('+')[0:2]
              answers.add(u'+'.join([lemma, part]))
            ranswers = list(answers)
            if len(answers) > 1:
              ranswers = []
              for lemma in answers:
                if not lemma.endswith('+N'):
                  ranswers.append(lemma)
            result = u' '.join(sorted(ranswers))
          else:
            result = word + u'+N'
          output.write('%s %s\n' % (word, result))

