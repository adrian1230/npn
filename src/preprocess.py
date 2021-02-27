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

print("token.text, token.lemma_, token.pos_, token.tag_, token.dep_")
for j in range(len(data)):
    chunk = nlp(data[j])
    for h in chunk:
        print(h.text, h.lemma_, h.pos_, h.tag_, h.dep_)