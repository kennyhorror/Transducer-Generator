#!/usr/bin/env python

import codecs
import subprocess

FOMA_PATH = "./"

try:
    from configlocal import *
except:
    pass

if __name__ == '__main__':
    questions = []
    answers = []

    for line in codecs.open('italian.txt.learn', encoding='ISO-8859-1', mode='r'):
        columns = line.split()
        questions.append(columns[0])
        answers.append(u''.join(columns[1:]))
                                             
    process = subprocess.Popen([FOMA_PATH + "flookup", "italian.bin", "-x"], 
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdin = u'\n'.join(questions)
    stdout, stderr = process.communicate(stdin.encode('utf-8'))

    fomas = stdout.decode('utf-8').split('\n\n')

    with codecs.open('italian.txt.result', encoding='utf-8', mode='w+') as output:
        for (word, results, answer) in zip(questions, fomas, answers):
            result = '\t'.join(results.split('\n'))
            output.write("%s\t%s\t%s\n" % (word, answer, result))

