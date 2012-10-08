#!/usr/bin/python

import sys
import os
import codecs

N_rules = ['+N+Sg:0', '+N+Pl:^s']
V_rules = ['+V:0']
A_rules = ['+A:0']

output = codecs.open('spanish.lexc', encoding='utf-8', mode='w+')

def print_header():
  output.write("""!!!spanish.lexc!!!

Multichar_Symbols +N +V +A +Sg +Pl

LEXICON Root

Noun ;
Verb ;
Adv  ;

""")

def parse_words(iterable):
  N = set()
  V = set()
  A = set()
  for line in iterable:
    (word, lemma, part) = line.split()
    if part == 'A':
      A.add(lemma)
    elif part == 'V':
      V.add(lemma)
    elif part == 'N':
      N.add(lemma)
    else:
      raise "Error"
  return (N, V, A)


def print_words(name, words, form):
  output.write("LEXICON " + name + "\n")
  for word in words:
    output.write(word.decode("ISO-8859-2"))
    output.write("\t" + form + ";\n")
  output.write("\n")

def print_rules(name, rules):
  output.write("LEXICON " + name + "\n\n")
  for rule in rules:
    output.write(rule + '\t#;\n')
  output.write("\n")

if __name__ == '__main__':
  print_header()
  (N, V, A) = parse_words(sys.stdin)
  print_words('Noun', N, 'Ninf')
  print_words('Verb', V, 'Vinf')
  print_words('Adv', A, 'Ainf')
  print_rules('Ninf', N_rules)
  print_rules('Vinf', V_rules)
  print_rules('Ainf', A_rules)
