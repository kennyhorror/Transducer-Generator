#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import codecs
import subprocess

from config import FOMA_PATH

N_rules = (
    '+N+Sg:0', '+N+Pl:*i', '+N+Pl:*e',
)

V_rules = (
    '+V:0',
    '+V+Presente+Sg+1:^o',    '+V+Presente+Sg+2:^i',   '+V+Presente+Sg+3:^e',
    '+V+Presente+Pl+1:^iamo', '+V+Presente+Pl+2:^te', '+V+Presente+Pl+3:^ono',

    u'+V+Futuro+Semplice+Sg+1:^ò', '+V+Futuro+Semplice+Sg+2:^ai',
    u'+V+Futuro+Semplice+Sg+3:^à', '+V+Futuro+Semplice+Pl+1:^emo',
    '+V+Futuro+Semplice+Pl+2:^ete','+V+Futuro+Semplice+Pl+3:^anno',

    '+V+Passato+Remoto+Sg+1:$i', '+V+Passato+Remoto+Sg+2:^sti',
    '+V+Passato+Remoto+Sg+3:^\'', '+V+Passato+Remoto+Pl+1:^mmo',
    '+V+Passato+Remoto+Pl+2:^ste', '+V+Passato+Remoto+Pl+3:^rono',

    '+V+Imperfetto+Sg+1:^vo', '+V+Imperfetto+Sg+2:^vi',
    '+V+Imperfetto+Sg+3:^va', '+V+Imperfetto+Pl+1:^vamo',
    '+V+Imperfetto+Pl+2:^vate', '+V+Imperfetto+Pl+3:^vano',

    '+V+Condizionale+Sg+1:^rei', '+V+Condizionale+Sg+2:^resti',
    '+V+Condizionale+Sg+3:^rebbe', '+V+Condizionale+Pl+1:^remmo',
    '+V+Condizionale+Pl+2:^reste', '+V+Condizionale+Pl+3:^rebbero',

    '+V+Congiuntivo+Imperfetto+Sg+1:^ssl', '+V+Congiuntivo+Imperfetto+Sg+2:^ssl',
    '+V+Congiuntivo+Imperfetto+Sg+2:^sse',
    '+V+Congiuntivo+Imperfetto+Sg+2:^ssimo',
    '+V+Congiuntivo+Imperfetto+Sg+1:^ste',
    '+V+Congiuntivo+Imperfetto+Sg+2:^ssero',

    '+V+Congiuntivo+Presente+Sg:^a', '+V+Congiuntivo+Presente+Pl+1:^iamo',
    '+V+Congiuntivo+Presente+Pl+2:^iate', '+V+Congiuntivo+Presente+Pl+3:^ano',
    
    '+V+Condizionale+Passato+Sg:^to', '+V+Condizionale+Passato+Pl:^ti',
    '+V+Gerundio:^ndo',
)

A_rules = (
    '+A+M+Sg:0', '+A+F+Sg:&a', '+A+M+Pl:&i', '+A+F+Pl:&e',
    '+A+Participio+Presente:&nte', '+A+Participio+Presente:&nti'
)

output = codecs.open('italian.lexc', encoding='utf-8', mode='w+')

def print_header():
  output.write(u"""!!!italian.lexc!!!

Multichar_Symbols +N +V +A +Sg +Pl +1 +2 +3 +F +M +Presente +Futuro +Semplice +Remoto +Passato +Part +Imperfetto +Condizionale +Congiuntivo +Participio +Gerundio

LEXICON Root

Noun ;
Verb ;
Adv  ;

""")

def print_foma(any_rules, lexicon = "Lexicon"):
  output = codecs.open('italian.foma', encoding='utf-8', mode='w+')
  output.write(u"""### italian.foma ###

define V [a | o | u | e | i] ;
define C [b | c | d | f | g | h | j | k | l | m | n | p | q | r | s | t | v | w | x | y | z];
define Cond [ r e i | r e s t i | r e b b e | r e m m o | r e s t e | r e b b e r o ];
# Rules for writing verbs
define VerbSolidK [..] -> [ h ] || [ c ] _ [ a r e ] [ "^" | "$" ] [ i | e ];
define VerbSolidKCond [..] -> [ h ] || [ c ] _ [ a r e ] [ "^" | "$" ] Cond;
define VerbPresenteSg12Pl1 [a r e | e r e | i r e] -> 0 || _ "^" [ o | i | i a m o ];
define VerbPresenteSg3First [ r e "^" e ] -> "^" || [ a ] _;
define VerbPresenteSg3SecondThird [ e r e | i r e ] -> 0 || _ "^" [ e ];
define VerbPresentePl2 [ r e ] -> 0 || [a | e | i ] _ "^" [ t e ];
define VerbPresentePl3First [ r e "^" o ] -> "^" || [ a ] _ [ n o ];
define VerbPresentePl3SecondThird [ e r e | i r e ] -> 0 || _ "^" [ o n o ];

define VerbFuturoSempliceFirst [ a r e ] -> [ e r ] ||  _ "^" [ ò | a i | à | e m o | e t e | a n n o]; 
define VerbFuturoSempliceSecondThird [ e ] -> 0 || [ i r | e r ]  _ "^" [ ò | a i | à | e m o | e t e | a n n o];

#Experimental
define VerbPassatoRemoto1 [ r e ] -> 0 || [ a | e | i ] _ "$" [ i ];
define VerbPassatoRemoto3First [ a r e ] "^" -> "ò" || _ "\'";
define VerbPassatoRemoto3Second [ r e ] "^" -> 0 || _ "\'";
define VerbPassatoRemoto3Third [ i r e ] "^" -> "ì" || _ "\'";
define VerbPassatoRemotoRest [ r e ] -> 0 || [ a | e | i ] _ "^" [ s t i | m m o | r o n o];

define VerbImperfetto [ r e ] -> 0 || [ a | e | i ] _ "^" [ v o | v i | v a ];
define VerbCondizionaleFirst [ a r e ] -> e || _ "^" Cond;
define VerbCondizionaleRest [ r e ] -> 0 || [ e | i ] _ "^" Cond;

define VerbCondizionalePassatoSecond [ e r e ] -> u ||  _ "^" [ t o ];
define VerbCondizionalePassatoRest [ r e ] -> 0 || [ a | i ] _ "^" [ t o | t i ];

define VerbCongiuntivoImperfetto [ r e ] -> 0 || [ a | e | i ] _ "^" [ s s l | s s e | s s i m o | s t e | s s e r o ];
define VerbGerundioFirstSecond [ r e ] -> 0 || [ a | e ] _ "^" [ n d o ];
define VerbGerundioThird [ i r e ] -> e || _ "^" [ n d o ];
define VerbCongiuntivoPresenteSgFirst [ a r e ] "^" [ a ] -> [ i ] || _;
define VerbCongiuntivoPresenteSgRest [ i | e ] [ r e ] -> 0 || _ "^" [ a ];
define VerbCongiuntivoPresentePl12 [ a | i | e ] [ r e ] -> 0 || _ "^" [ i a m o | i a t e];
define VerbCongiuntivoPresentePl3First [ a r e ] "^" [ a ] -> "^" [ i ] || _ [ n o ];
define VerbCongiuntivoPresentePl3Rest [[ i | e ] r e ] -> 0 || _ "^" [ a n o ];

# Rules for writing nouns
define NounMPl [o | e] -> 0 || _ "*" i ;
define NounFPl [a] -> 0 || _ "*" e ;
define NounCGoEndingPl [o] -> h || C [c | g] _ "*" i ;
define NounCGaEndingPl [a] -> h || [c | g] _ "*" e ;
define NounProfessionPl a -> 0 || i s t _ "*" [e | i] ;
define NounGreekPl a -> 0 || [m | t] _ "*" i ;
define NounIoEndingPl [i o] -> 0 || _ "*" i ;
define NounCiaEndingPl [i a] -> 0 || [c | g] _ "*" e ;
define NounUomini [o -> [i n] || u o m _ "*" i] .o.
                  [o -> [i n i] || u o m _ "-"] ;

# Rules for writing adjectives
define AdjFSg [o] -> 0 || _ "&" a ;
define AdjMPl [o | e] -> 0 || _ "&" i ;
define AdjFPl [o] -> 0 || _ "&" e ;
define AdjCGoEndingPl [o] -> h || C [c | g] _ "&" i ;
define AdjCGaEndingPl [o] -> h || [c | g] _ "&" e ;
define AdjProfessionPl a -> 0 || i s t _ "&" [e | i] ;
define AdjCioEndingPl [i o] -> 0 || [c | g] _ "&" i ;
define AdjCiaEndingPl [[i a] -> i || V [c | g] _ "&" e] |
                [[i a] -> 0 || C [c | g] _ "&" e];
define AdjPresenteParticipio [i -> e || _ r e "&" n t [e | i]] .o.
                            [[r e] -> 0 || _ "&" n t [e | i]] ;


#ii is not common in this language. So only i$i will remain.
define DoubleI [ i ] -> 0 || _ "^" i;

#Cleanup: remove morpheme boundaries
define Cleanup [ "^" | "$" | "\'" | "*" | "&" ] -> 0;

#This is required for guessing
define Stem [ C^<3 V C^<3]+;
define Any Stem [
%s |
%s |
%s ];

read lexc italian.lexc
define Lexicon

define Grammar %s                             .o.
               VerbSolidK                     .o.
               VerbSolidKCond                 .o.
               VerbPresenteSg3SecondThird     .o.
               VerbPresentePl2                .o.
               VerbPresentePl3First           .o.
               VerbPresentePl3SecondThird     .o.
               VerbFuturoSempliceFirst        .o.
               VerbFuturoSempliceSecondThird  .o.
               VerbPresenteSg3First           .o.
               VerbPresenteSg3SecondThird     .o.
               NounUomini                     .o.
               NounProfessionPl               .o.
               NounGreekPl                    .o.
               NounIoEndingPl                 .o.
               NounCiaEndingPl                .o.
               AdjProfessionPl                .o.
               AdjPresenteParticipio          .o.
               AdjCioEndingPl                 .o.
               AdjCiaEndingPl                 .o.
               VerbPassatoRemoto1             .o.
               VerbPassatoRemoto3First        .o.
               VerbPassatoRemoto3Second       .o.
               VerbPassatoRemoto3Third        .o.
               VerbPassatoRemotoRest          .o.
               VerbImperfetto                 .o.
               VerbCondizionaleFirst          .o.
               VerbCondizionaleRest           .o.
               VerbCondizionalePassatoSecond  .o.
               VerbCondizionalePassatoRest    .o.
               VerbCongiuntivoImperfetto      .o.
               VerbGerundioFirstSecond        .o.
               VerbGerundioThird              .o.
               VerbPresenteSg12Pl1            .o.
               NounCGoEndingPl                .o.
               NounCGaEndingPl                .o.
               AdjCGoEndingPl                 .o.
               AdjCGaEndingPl                 .o.
               VerbCongiuntivoPresenteSgRest   .o.
               VerbCongiuntivoPresentePl12     .o.
               VerbCongiuntivoPresentePl3First .o.
               VerbCongiuntivoPresentePl3Rest  .o.
               VerbCongiuntivoPresenteSgFirst  .o.
               NounMPl                        .o.
               NounFPl                        .o.
               AdjFSg                         .o.
               AdjFPl                         .o.
               AdjMPl                         .o.
               VerbPresenteSg3First           .o. #This rule is really stupid. Need to be fixed
               DoubleI                        .o.
               Cleanup;

regex Grammar;
save stack italian.bin
""" % (any_rules[0], any_rules[1], any_rules[2], lexicon))

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
    output.write(word.decode("ISO-8859-1"))
    output.write("\t" + form + ";\n")
  output.write("\n")

def print_rules(name, rules):
  output.write("LEXICON " + name + "\n\n")
  for rule in rules:
    output.write(rule + '\t#;\n')
  output.write("\n")

def get_any(rules):
  result = u''
  for rule in rules:
    if result:
      result += '|'
    result += '['
    [lpart, rpart] = rule.split(':')
    for word in lpart.split('+'):
      if not word:
        continue
      result += '"+'
      result += word
      result += '"'
    result += ']:'
    if rpart != u'0':
      result += '['
      for letter in rpart:
        result += '"'
        result += letter
        result += '"'
      result += ']'
    else:
      result += '0'
    result += '\n'
  return result

if __name__ == '__main__':
  (N, V, A) = parse_words(open('italian.txt.learn', 'r'))
  print_header()
  print_words('Noun', N, 'Ninf')
  print_words('Verb', V, 'Vinf')
  print_words('Adv', A, 'Ainf')
  print_rules('Ninf', N_rules)
  print_rules('Vinf', V_rules)
  print_rules('Ainf', A_rules)

  print_foma((get_any(N_rules), get_any(V_rules), get_any(A_rules)), 'Any')
  output.close()

  #foma = subprocess.Popen([FOMA_PATH + 'foma', '-f', 'italian.foma'])
  #foma.communicate()

