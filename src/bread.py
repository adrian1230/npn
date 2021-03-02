import spacy as sp
from bake import *

nlp = sp.load('en_core_web_sm')

data = output()

package = []

for d, u in enumerate(data):
    script = nlp(u)
    pack = []
    print(u)
    noun = []
    verb = []
    obej = []
    adv = []
    adj = []
    splited = u.split(' ')
    for j in range(len(script)):
        print(script[j].text,"=>",script[j].pos_,"=>",script[j].tag_, "=>", script[j].dep_)
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
            verify = script[j].text
            ing = nlp(verify)
            for f in ing:
                if f.pos_ == "PRON" or f.pos_ == "PROPN" or f.pos_ == "NOUN":
                    noun.append(script[j].text)
                elif f.pos_ == "ADJ":
                    adj.append(script[j].text)
        elif script[j].dep_ == "relcl":
            verify = script[j].text
            ing = nlp(verify)
            for f in ing:
                if f.pos_ == "VERB":
                    verb.append(script[j].text)
        else:
            pass
    # noun = list(set(noun))
    # verb = list(set(verb))
    # obej = list(set(obej))
    # adj = list(set(adj))
    # adv = list(set(adv))
    print("subject")
    print(noun)
    print("verb")
    print(verb)
    print("object")
    print(obej)
    print("adjective")
    print(adj)
    print("adverb")
    print(adv)
    print("\n")
    if len(verb) == 0:
        pass
    if len(verb) != 0:
        if len(obej) > 0:
            # for d in range(len(adj)):
            #     adj_loca_start, adj_loca_end = u.find(adj[d]),u.find(adj[d])+len(adj[d])
            #     print(adj_loca_start,adj_loca_end)
            #     print(u[adj_loca_start:adj_loca_end])
            # w = 0
            print(len(u),u,len(adj))
            # while w != len(adj):
            #     length = len(adj[w])
            #     print(w,length,adj[w])
            #     for r in range(len(u)):
            #         print(r,u[r])
            #         if u[r] == adj[w][0]:
            #             sets_ = [
            #                 u
            #                 [r+s] for s in range(length)]
            #             print(sets_)
            #             print("#############")
            #             if ''.join(sets_) == adj[w]:
            #                 print(r,r+length-1)
            #                 print(u[r:r+length])
            #     w += 1
            for w in range(len(adj)):
                print(adj[w])
                length = len(adj[w])
                for h in range(len(u)):
                    print(h)
                    if u[h] == adj[w][0]:
                        if (h + length - 1) > len(u):
                            pass
                        else:
                            sets_ = [u[h+s] for s in range(length)]
                            if ''.join(sets_) == adj[w]:
                                print(h,h+length-1)
                                print(u[h:h+length])
            # print(splited)
            c = 0
            while c != len(splited):
                word = splited[c]
                c += 1

