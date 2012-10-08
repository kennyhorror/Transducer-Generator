#!/usr/bin/python

import sys
import os
import codecs

N_rules = ['+N+Sg:0', '+N+Pl:^s']
V_rules = ['+V:0']
A_rules = ['+A:0']

output = codecs.open('italian.lexc', encoding='utf-8', mode='w+')

def print_header():
  output.write("""!!!italian.lexc!!!

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
    columns = line.split()
    wordform, lemmas = columns[0], columns[1:]
    for lemma_with_tag in lemmas:
      lemma, tag = lemma_with_tag.split('+')
      if tag == 'A':
        A.add(lemma)
      elif tag == 'V':
        V.add(lemma)
      elif tag == 'N':
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
  (N, V, A) = parse_words(open('italian.txt.learn', 'r'))
  print_header()
  print_words('Noun', N, 'Ninf')
  print_words('Verb', V, 'Vinf')
  print_words('Adv', A, 'Ainf')
  print_rules('Ninf', N_rules)
  print_rules('Vinf', V_rules)
  print_rules('Ainf', A_rules)
