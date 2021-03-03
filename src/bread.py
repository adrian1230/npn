import spacy as sp
from bake import *

nlp = sp.load('en_core_web_sm')

data = output()

package = []

'''
New Label:  FIN, SEG FIN, PRODUCT, FORECAST, BU Business Unit, ACQ, INV, PRESSURE
'''

def extract(point):
    for d, u in enumerate(point):
        if len(u) != 6:
            script = nlp(u)
            pack = []
            noun, verb, obej, adv, adj = [], [], [], [], []
            splited = u.split(' ')
            print(u,'\n')
            for j in range(len(script)):
                if script[j].dep_ == "xcomp" or script[j].dep_ == "ccomp" or script[j].dep_ == "pcomp" or script[j].dep_ == "ROOT" or script[j].dep_ == "aux" or script[j].dep_ == "auxpass" or script[j].dep_ == "neg":
                    verb.append(script[j].text)
                elif script[j].dep_ == "nsubj" or script[j].dep_ == "nsubjpass":
                    noun.append(script[j].text)
                elif script[j].dep_ == "pobj" or script[j].dep_ == "dobj" or script[j].dep_ == "quantmod" or script[j].dep_ == "compound" or script[j].dep_ == "nummod":
                    obej.append(script[j].text)
                elif script[j].dep_ == "amod" or script[j].dep_ == "acomp":
                    adj.append((script[j].text))
                elif script[j].dep_ == "advmod":
                    adv.append((script[j].text))
                elif script[j].dep_ == "conj":
                    if script[j].pos_ == "PRON" or script[j].pos_ == "PROPN" or script[j].pos_ == "NOUN":
                        noun.append(script[j].text)
                    elif script[j].pos_ == "ADJ":
                        adj.append(script[j].text)
                    elif script[j].pos_ == "VERB":
                        verb.append(script[j].text)
                elif script[j].dep_ == "relcl":
                    if script[j].pos_ == "VERB":
                        verb.append(script[j].text)
                else:
                    pass
            for q in range(len(adv)):
                verb.append(adv[q])
            if len(verb) == 0:
                pass
            if len(verb) != 0:
                if len(obej) > 0:
                    tup = []
                    def loca(array):
                        for i in range(len(array)):
                            word = array[i]
                            length = len(word)
                            count = array.count(word)
                            pos_start = None
                            c = 0
                            while c != count:
                                try:
                                    if pos_start is not None:
                                        pos_start = u.index(word,pos_start+length)
                                        pos_end = pos_start + length - 1
                                    else:
                                        pos_start = u.index(word)
                                        pos_end = pos_start + length - 1
                                except:
                                    pass
                                tup.append((word,pos_start,pos_end))
                                c += 1
                    loca(adj)
                    loca(verb)
                    loca(noun)
                    loca(obej)
                    tup = list(set(tup))
                    for j in range(len(tup)):
                        print(tup[j])
                    print('\n')

extract(data)