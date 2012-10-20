#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import codecs

N_rules = (
    '+N+Sg:0', '+N+Pl:^i', '+N+Pl:^e',
)

V_rules = (
    '+V:0',
    '+V+Presente+Sg+1:^o',    '+V+Presente+Sg+2:^i',   '+V+Presente+Sg+3:^e',
    '+V+Presente+Pl+1:^iamo', '+V+Presente+Pl+2:^te', '+V+Presente+Pl+3:^ono',

    u'+V+FuturoSemplice+Sg+1:^ò', '+V+FuturoSemplice+Sg+2:^ai',
    u'+V+FuturoSemplice+Sg+3:^à', '+V+FuturoSemplice+Pl+1:^emo',
    '+V+FuturoSemplice+Pl+2:^ete','+V+FuturoSemplice+Pl+3:^anno',

    '+V+PassatoRemoto+Sg+1:$i', '+V+PassatoRemoto+Sg+2:^sti',
    '+V+PassatoRemoto+Sg+3:^\'', '+V+PassatoRemoto+Pl+1:^mmo',
    '+V+PassatoRemoto+Pl+2:^ste', '+V+PassatoRemoto+Pl+3:^rono',

    '+V+Imperfetto+Sg+1:^vo', '+V+Imperfetto+Sg+2:^vi',
    '+V+Imperfetto+Sg+3:^va', '+V+Imperfetto+Pl+1:^vamo',
    '+V+Imperfetto+Pl+2:^vate', '+V+Imperfetto+Pl+3:^vano',

    '+V+Condizionale+Sg+1:^rei', '+V+Condizionale+Sg+2:^resti',
    '+V+Condizionale+Sg+3:^rebbe', '+V+Condizionale+Pl+1:^remmo',
    '+V+Condizionale+Pl+2:^reste', '+V+Condizionale+Pl+3:^rebbero',

    '+V+CondizionalePassato:^to',
)

A_rules = (
    '+A:0', '+A+Pl:^i', '+A+Pl:^e',
    '+A+Part+Presente:^nte', '+A+Part+Presente:^nti',
    '+A+Part+Passato:^ti', '+A+Part+Passato:^ta', '+A+Part+Passato:^te'
)

output = codecs.open('italian.lexc', encoding='utf-8', mode='w+')

def print_header():
  output.write(u"""!!!italian.lexc!!!

Multichar_Symbols +N +V +A +Sg +Pl +1 +2 +3 +Presente +FuturoSemplice +PassatoRemoto +Passato +Part +Imperfetto +Condizionale +CondizionalePassato

LEXICON Root

Noun ;
Verb ;
Adv  ;

""")

def print_foma():
  output = codecs.open('italian.foma', encoding='utf-8', mode='w+')
  output.write(u"""### italian.foma ###

define V [a | o | u | e | i] ;
define C [b | c | d | f | g | h | j | k | l | m | n | p | q | r | s | t | v | w | x | y | z];

# Rules for writing verbs
define VerbPresenteSg12Pl1 [a r e | e r e | i r e] -> 0 || _ "^" [ o | i | i a m o ];
define VerbPresenteSg3First [ r e "^" e ] -> "^" || [ a ] _;
define VerbPresenteSg3SecondThird [ e r e | i r e ] -> 0 || _ "^" [ e ];
define VerbPresentePl2 [ r e ] -> 0 || [a | e | i ] _ "^" [ t e ];
define VerbPresentePl3First [ r e "^" o ] -> "^" || [ a ] _ [ n o ];
define VerbPresentePl3SecondThird [ e r e | i r e ] -> 0 || _ "^" [ o n o ];

define VerbFuturoSempliceFirst [ a r e ] -> [ e r ] ||  _ "^" [ ò | a i | à | e m o | e t e | a n n o]; 
define VerbFuturoSempliceSecondThird e -> 0 || [ i r | e r ]  _ "^" [ ò | a i | à | e m o | e t e | a n n o];

#Experimental
define VerbPassatoRemoto1 [ r e ] -> 0 || [ a | e | i ] _ "$" [ i ];
define VerbPassatoRemoto3First [ a r e ] "^" -> "ò" || _ "\'";
define VerbPassatoRemoto3Second [ r e ] "^" -> 0 || _ "\'";
define VerbPassatoRemoto3Third [ i r e ] "^" -> "ì" || _ "\'";
define VerbPassatoRemotoRest [ r e ] -> 0 || [ a | e | i ] _ "^" [ s t i | m m o | r o n o];

define VerbImperfetto [ r e ] -> 0 || [ a | e | i ] _ "^" [ v o | v i | v a ];
define VerbCondizionaleFirst [ a r e ] -> e || _ "^" [ r e i | r e s t i | r e b b e | r e m m o | r e s t e | r e b b e r o ];
define VerbCondizionaleRest [ r e ] -> 0 || [ e | i ] _ "^" [ r e i | r e s t i | r e b b e | r e m m o | r e s t e | r e b b e r o ];

define VerbCondizionalePassatoSecond [ e r e ] -> u ||  _ "^" [ t o ];
define VerbCondizionalePassatoRest [ r e ] -> 0 || [ a | i ] _ "^" [ t o ];

# Rules for writing nouns
define NounMPl [o | e] -> 0 || _ "^" i ;
define NounFPl [a] -> 0 || _ "^" e ;
define NounProfessionPl a -> 0 || i s t _ "^" [e | i] ;
define NounGreekPl a -> 0 || [m | t] _ "^" i ;
define NounIoEndingPl [i o] -> 0 || _ "^" i ;
define NounCiaEndingPl [i a] -> 0 || [c | g] _ "^" e ;
define NounExceptions [{uomo} "+N" "+Sg" .x. {uomini} "+N" "+Pl"] |
                      [{zio} "+N" "+Sg" .x. {zii} "+N" "+Pl"]; 

# Rules for writing adjectives
define AdjMPl [o | e] -> 0 || _ "^" i ;
define AdjFPl [a] -> 0 || _ "^" e ;
define AdjCGoEndingPl [o] -> h || [c | g] _ "^" i ;
define AdjCGaEndingPl [a] -> h || [c | g] _ "^" e ;
define AdjCioEndingPl [i o] -> 0 || [c | g] _ "^" i ;
define AdjCiaEndingPl [[i a] -> i || V [c | g] _ "^" e] |
                [[i a] -> 0 || C [c | g] _ "^" e];
define AdjPresenteParticipio [i -> e || _ r e "^" n t [e | i]] .o.
                            [[r e] -> 0 || _ "^" n t [e | i]] ;
define AdjPassatoParticipio [t o] -> 0 || [a | u | i] _ "^" t [e | i | a] ;

#Cleanup: remove morpheme boundaries
define Cleanup [ "^" | "$" | "\'" ] -> 0;

read lexc italian.lexc
define Lexicon

define Grammar Lexicon                        .o. 
               VerbPresenteSg3SecondThird     .o.
               VerbPresentePl2                .o.
               VerbPresentePl3First           .o.
               VerbPresentePl3SecondThird     .o.
               VerbFuturoSempliceFirst        .o.
               VerbFuturoSempliceSecondThird  .o.
               VerbPresenteSg3First           .o.
               VerbPresenteSg3SecondThird     .o.
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
               NounMPl                        .o.
               NounFPl                        .o.
               AdjMPl	                      .o.
               AdjFPl	                      .o.
               VerbPresenteSg12Pl1            .o.
               VerbPresenteSg3First           .o. #This rule is really stupid. Need to be fixed
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
    output.write(word.decode("ISO-8859-1"))
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
