import spacy as sp
from download import *
import pickle as pk
import re
import os

alpha_1 = "abcdefghijklmnopqrstuvwxyz"

alpha_2 = alpha_1.upper()

nlp = sp.load('en_core_web_sm')

data = out

for p in range(len(data)):
    if "\\n" in data[p]:
        data[p] = ' '.join(data[p].split('\\n'))
    if "\"" in data[p]:
        data[p] = ' '.join(data[p].split('\"'))

marked = []

for g in range(len(data)):
    data[g] = data[g].strip()
    length = len(data[g])
    z = 0
    for f in data[g]:
        if  f not in alpha_1 and f not in alpha_2:
            z += 1
    if z == length:
        marked.append(g)

for p in range(len(data)):
    if p in marked:
        del data[p]

# Maria PROPN NNP nsubj
# is AUX VBZ ROOT
# reponsible ADJ JJ acomp
# for ADP IN prep
# planning VERB VBG pcomp
# the DET DT det
# activities NOUN NNS dobj
# and CCONJ CC cc
# venues NOUN NNS conj
# for ADP IN prep
# our DET PRP$ poss
# coming VERB VBG amod
# vacation NOUN NN pobj
# , PUNCT , punct
# which DET WDT dobj
# we PRON PRP nsubj
# want VERB VBP relcl
# to PART TO aux
# spend VERB VB xcomp
# our DET PRP$ poss
# 10th ADJ JJ amod
# anniversary NOUN NN dobj
# in ADP IN prep
# , PUNCT , punct
# and CCONJ CC cc
# I PRON PRP nsubj
# am AUX VBP aux
# looking VERB VBG conj
# for ADP IN prep
# it PRON PRP pobj
# . PUNCT . punct

# print("token.text, token.lemma_, token.pos_, token.tag_, token.dep_")
for j in range(len(data)):
    # print(data[j],'\n')
    chunk = nlp(data[j])
    sentences = []
    for h in chunk:
        print(h.pos_, h.tag_, h.dep_)
        if h.pos_ == "VERB":
            pass
    print("########################")
    # if h.pos_
    