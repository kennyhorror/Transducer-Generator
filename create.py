#!/usr/bin/python

import sys
import os
import codecs

N_rules = (
    '+N+Sg:0', '+N+Pl:^i', '+N+Pl:^e',
)

V_rules = (
    '+V:0',
    '+V+Presente+Sg+1:^o',    '+V+Pr+Sg+2:^i',   '+V+Pr+Sg+3:^e',
    '+V+Presente+Pl+1:^iamo', '+V+Pr+Pl+2:^te', '+V+Pr+Pl+3:^ono',
)

A_rules = (
    '+A+Qual+Sg:0', '+A+Qual+Pl:^i', '+A+Qual+Pl:^e',
)

output = codecs.open('italian.lexc', encoding='utf-8', mode='w+')

def print_header():
  output.write("""!!!italian.lexc!!!

Multichar_Symbols +N +V +A +Sg +Pl +1 +2 +3 +Presente +Pa +Qual

LEXICON Root

Noun ;
Verb ;
Adv  ;

""")

def print_foma():
  output = codecs.open('italian.foma', encoding='utf-8', mode='w+')
  output.write("""### italian.foma ###

define V [a | o | u | e | i] ;

# Rules for writing verbs
define VerbPresenteSg12Pl1 [a r e | e r e | i r e] -> 0 || _ "^" [ o | i | i a m o ];
define VerbPresenteSg3First [ r e "^" e ] -> "^" || [ a ] _;
define VerbPresenteSg3SecondThird [ e r e | i r e ] -> 0 || _ "^" [ e ];
define VerbPresentePl2 [ r e ] -> 0 || [a | e | i ] _ "^" [ t e ];
define VerbPresentePl3First [ a r e ] -> a || _ "^" [ n o ];
define VerbPresentePl3SecondThird [ e r e | i r e ] -> 0 || _ "^" [ o n o ];

# Rules for writing nouns
define NounMPl [o | e] -> 0 || _ "^" i ;
define NounFPl [a] -> 0 || _ "^" e ;
define NounPresenteofPl a -> 0 || i s t _ "^" [e | i] ;
define NounGreekPl a -> 0 || [m | t] _ "^" i ;
define NounIOPl [i o] -> 0 || _ "^" i ;
define NounCiaPl [i a] -> 0 || [c | g] _ "^" e ;
define NounExceptions [{uomo} "+N" "+Sg" .x. {uomini} "+N" "+Pl"] |
                      [{zio} "+N" "+Sg" .x. {zii} "+N" "+Pl"]; 

# Rules for writing adjectives
define AdjMPl [o | e] -> 0 || _ "^" i ;
define AdjFPl [a] -> 0 || _ "^" e ;
define AdjCGoPl [o] -> h || [c | g] _ "^" i ;
define AdjCGaPl [a] -> h || [c | g] _ "^" e ;
define AdjCiOPl [i o] -> 0 || [c | g] _ "^" i ;
define AdjCiAPl [[i a] -> i || V [c | g] _ "^" e] |
                [[i a] -> 0 || [c | g] _ "^" e];

#Cleanup: remove morpheme boundaries
define Cleanup "^" -> 0;

read lexc italian.lexc
define Lexicon

define Grammar Lexicon              .o. 
               VerbPresenteSg12Pl1        .o.
               VerbPresenteSg3First       .o.
               VerbPresenteSg3SecondThird .o.
               VerbPresentePl2            .o.
               VerbPresentePl3First       .o.
               VerbPresentePl3SecondThird .o.
               Cleanup;

regex Grammar;

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

  print_foma()
