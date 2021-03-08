import spacy as sp
from bye import *
from operator import itemgetter

nlp = sp.load('en_core_web_sm')

book = dry()

charge = "$%"

punct = ",.'!@#$%^&*()_-+=~`?/:;{}[]<>"

def extract(point):
    little = []
    for d, u in enumerate(point):
        if len(u) >= 5:
            splited = u.split(' ')
            script = nlp(u)
            subj, verb, obej, adv, adj = [], [], [], [], []
            def allocation(sentence_):
                for j in range(len(sentence_)):
                    if sentence_[j].dep_ == "ROOT":
                        if sentence_[j].pos_ == "VERB":
                            verb.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "NUM":
                            obej.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "AUX":
                            verb.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "xcomp" or sentence_[j].dep_ == "ccomp" or sentence_[j].dep_ == "pcomp" or sentence_[j].dep_ == "aux" or sentence_[j].dep_ == "auxpass" or sentence_[j].dep_ == "neg" or sentence_[j].dep_ == "attr" or sentence_[j].dep_ == "nmod":
                        verb.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "nsubj" or sentence_[j].dep_ == "nsubjpass":
                        subj.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "pobj" or sentence_[j].dep_ == "dobj" or sentence_[j].dep_ == "quantmod" or sentence_[j].dep_ == "nummod" or sentence_[j].dep_ == "npadvmod":
                        obej.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "amod" or sentence_[j].dep_ == "acomp":
                        adj.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "advmod" or sentence_[j].dep_ == "advcl":
                        adv.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "conj":
                        if sentence_[j].pos_ == "PRON" or sentence_[j].pos_ == "PROPN" or sentence_[j].pos_ == "NOUN":
                            subj.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "ADJ":
                            adj.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "VERB":
                            verb.append(sentence_[j].text)
                        else:
                            pass
                    elif sentence_[j].dep_ == "relcl":
                        if sentence_[j].pos_ == "VERB":
                            verb.append(sentence_[j].text)
                        else:
                            pass
                    elif sentence_[j].dep_ == "compound":
                        if sentence_[j].pos_ == "NOUN":
                            subj.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "PROPN":
                            obej.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "NUM":
                            obej.append(sentence_[j].text)
                        else:
                            pass
                    else:
                        pass
            allocation(script)
            for q in range(len(adv)):
                verb.append(adv[q])
            if len(verb) == 0:
                pass
            if len(verb) != 0:
                if len(obej) > 0:
                    tup = []
                    reconstructed = []
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
                                a = ''.join([word," "])
                                b = ''.join([word,"'"])
                                if u[pos_start:pos_end+2] == a or u[pos_start:pos_end+2] == b:
                                    tup.append((word,pos_start,pos_end))
                                c += 1
                    loca(adj)
                    loca(subj)
                    loca(obej)
                    loca(verb)
                    tup = sorted(list(set(tup)), key=itemgetter(1))
                    g = 0
                    while g != len(tup):
                        if tup[g][0] in adj:
                            pos_ = []
                            dis_ = []
                            for j in range(len(tup)):
                                if j == g:
                                    pass
                                elif j > g:
                                    if tup[j][0] in subj or tup[j][0] in obej:
                                        pos_.append(j)
                                        dis_.append(abs(tup[g][2] - tup[j][1]))
                                else:
                                    if tup[j][0] in subj or tup[j][0] in obej:
                                        pos_.append(j)
                                        dis_.append(abs(tup[g][1] - tup[j][2]))
                            if len(dis_) != 0:
                                min_ = dis_.index(min(dis_))
                                destination = tup[pos_[min_]]
                                if destination[0] in subj:
                                    subj.append(tup[g][0])
                                elif destination[0] in obej:
                                    obej.append(tup[g][0])
                                else:
                                    pass
                        g += 1
                    subj = list(set(subj))
                    for h in range(len(splited)):
                        a = splited[h].split('$')
                        if len(a) == 1:
                            a = None
                        elif len(a) == 2:
                            a = a[1]
                        b = splited[h].split('%')
                        if len(b) == 1:
                            b = None
                        elif len(b) == 2:
                            b = b[0]
                        c = splited[h].split('.')
                        if len(c) == 1:
                            c = None
                        elif len(c) == 2:
                            c = c[0]
                        d = splited[h].split(',')
                        if len(d) == 1:
                            d = None
                        elif len(d) == 2:
                            d = d[0]
                        if splited[h] in subj or a in subj or b in subj or c in subj or d in subj:
                            reconstructed.append(splited[h])
                        elif splited[h] in verb:
                            reconstructed.append(splited[h])
                        elif splited[h] in obej or a in obej or b in obej or c in obej or d in obej:
                            reconstructed.append(splited[h])
                        else:
                            pass
                    formulated = ' '.join(reconstructed)
                    doc = nlp(formulated)
                    refined = []
                    # for j in doc:
                    #     print(j,j.pos_,j.tag_,j.dep_,j.is_alpha,j.is_stop)
                    for i in doc:
                        if i.pos_ != "AUX":
                            if i.dep_ != "aux":
                                if i.is_stop == False:
                                    if i.is_alpha == True:
                                        refined.append(i.text)
                    refined = ' '.join(refined)
                    little.append([u,refined])

    final = []

    def again_(rose):
        for d in range(len(rose)):
            words = rose[d][1]
            last = nlp(words)
            ner = []
            for d in last.ents:
                ner.append([str(d), str(d.label_)])
            for j in range(len(ner)):
                ner[j] = list(set(ner[j]))
            left = ''
            if len(ner) != 0:
                print(words)
                print(ner)
                for e in range(len(ner)):
                    if e == 0:
                        for d in range(len(ner[e])):
                            if ner[e][d].isupper() != True:
                                left = ''.join(words.split(ner[e][d]))
                    else:
                        for d in range(len(ner[e])):
                            if ner[e][d].isupper() != True:
                                left = ''.join(left.split(ner[e][d]))
                print(left)
                lefted = nlp(left)
                subj, verb, obej, adv, adj = [], [], [], [], []
                def allocation(sentence_):
                    for j in range(len(sentence_)):
                        if sentence_[j].dep_ == "ROOT":
                            if sentence_[j].pos_ == "VERB":
                                verb.append(sentence_[j].text)
                            elif sentence_[j].pos_ == "NUM":
                                obej.append(sentence_[j].text)
                            elif sentence_[j].pos_ == "AUX":
                                verb.append(sentence_[j].text)
                        elif sentence_[j].dep_ == "xcomp" or sentence_[j].dep_ == "ccomp" or sentence_[j].dep_ == "pcomp" or sentence_[j].dep_ == "aux" or sentence_[j].dep_ == "auxpass" or sentence_[j].dep_ == "neg" or sentence_[j].dep_ == "attr" or sentence_[j].dep_ == "nmod":
                            verb.append(sentence_[j].text)
                        elif sentence_[j].dep_ == "nsubj" or sentence_[j].dep_ == "nsubjpass":
                            subj.append(sentence_[j].text)
                        elif sentence_[j].dep_ == "pobj" or sentence_[j].dep_ == "dobj" or sentence_[j].dep_ == "quantmod" or sentence_[j].dep_ == "nummod" or sentence_[j].dep_ == "npadvmod":
                            obej.append(sentence_[j].text)
                        elif sentence_[j].dep_ == "amod" or sentence_[j].dep_ == "acomp":
                            adj.append(sentence_[j].text)
                        elif sentence_[j].dep_ == "advmod" or sentence_[j].dep_ == "advcl":
                            adv.append(sentence_[j].text)
                        elif sentence_[j].dep_ == "conj":
                            if sentence_[j].pos_ == "PRON" or sentence_[j].pos_ == "PROPN" or sentence_[j].pos_ == "NOUN":
                                subj.append(sentence_[j].text)
                            elif sentence_[j].pos_ == "ADJ":
                                adj.append(sentence_[j].text)
                            elif sentence_[j].pos_ == "VERB":
                                verb.append(sentence_[j].text)
                            else:
                                pass
                        elif sentence_[j].dep_ == "relcl":
                            if sentence_[j].pos_ == "VERB":
                                verb.append(sentence_[j].text)
                            else:
                                pass
                        elif sentence_[j].dep_ == "compound":
                            if sentence_[j].pos_ == "NOUN":
                                subj.append(sentence_[j].text)
                            elif sentence_[j].pos_ == "PROPN":
                                obej.append(sentence_[j].text)
                            elif sentence_[j].pos_ == "NUM":
                                obej.append(sentence_[j].text)
                            else:
                                pass
                        else:
                            pass
                allocation(lefted)
                for q in range(len(adv)):
                    verb.append(adv[q])
                print(subj)
                print(verb)
                print(obej)
                print(adj,'\n')
    again_(little)

extract(book[350:399])


