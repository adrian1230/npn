import spacy as sp
from bye import *
from operator import itemgetter
import numpy as np
import math as ma

# load the spacy module
# nlp = sp.load('../model/spacy_finance')
nlp = sp.load('en_core_web_sm')
# call the data stored in another file
book = dry()

book = list(set(book))

def extract(point):
    little = []
    for d, u in enumerate(point):
        # no contextual sentences will be made
        if len(u) >= 5:
            little.append(u)
    # return little
    # the final array is for the original sentence and the pos pair(s)
    final = []

    for d in range(len(little)):
        # the original sentence
        sent_ = little[d]
        # the extracted sentence
        words = sent_
        total_width = len(words)
        median = total_width / 2
        last = nlp(words)
        ner = []
        # get ner to capture the core parts of the extracted sentence
        for d in last.ents:
            ner.append([str(d), str(d.label_)])
        for j in range(len(ner)):
            ner[j] = list(set(ner[j]))
        left = ''
        # if ner tag is none, then we ignore the sentence
        if len(ner) != 0:
            labels_ = [
                "PERSON", "ORG", "MONEY", "TIME",
                "GPE", "DATE", "DATED", "NORP",
                "PERCENT", "EVENT", "FAC", "LOC",
                "CARDINAL", "ORDINAL","PRODUCT", "LAW",
                "WORK_OF_ART"
            ]
            # remove the ner words from the extracted sentence
            e = 0
            while e != len(ner):
                for d in range(len(ner[e])):
                    if e == 0:
                        if ner[e][d].isupper() != True:
                            left = ''.join(words.split(ner[e][d]))
                        else:
                            if ner[e][d] in labels_:
                                pass
                            else:
                                left = ''.join(words.split(ner[e][d]))
                    else:
                        if ner[e][d].isupper() != True:
                            left = ''.join(left.split(ner[e][d]))
                        else:
                            if ner[e][d] in labels_:
                                pass
                            else:
                                left = ''.join(left.split(ner[e][d]))
                e += 1
            remained = nlp(left)
            # main_entity == subject
            # action == verb
            # target_entity == object
            # way == adverb
            # description = adjective
            main_entity, action, target_entity, way, description = [], [], [], [], []
            date = []
            def allocation(sentence_):
                for j in range(len(sentence_)):
                    if sentence_[j].dep_ == "ROOT":
                        if sentence_[j].pos_ == "VERB":
                            action.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "NUM":
                            target_entity.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "AUX":
                            action.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "xcomp" or sentence_[j].dep_ == "advcl" or sentence_[j].dep_ == "ccomp" or sentence_[j].dep_ == "pcomp" or sentence_[j].dep_ == "aux" or sentence_[j].dep_ == "auxpass" or sentence_[j].dep_ == "neg" or sentence_[j].dep_ == "attr" or sentence_[j].dep_ == "nmod":
                        action.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "nsubj" or sentence_[j].dep_ == "nsubjpass":
                        main_entity.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "pobj" or sentence_[j].dep_ == "dobj" or sentence_[j].dep_ == "quantmod" or sentence_[j].dep_ == "nummod" or sentence_[j].dep_ == "npadvmod":
                        target_entity.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "amod" or sentence_[j].dep_ == "acomp":
                        description.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "advmod" or sentence_[j].dep_ == "advcl":
                        way.append(sentence_[j].text)
                    elif sentence_[j].dep_ == "conj":
                        if sentence_[j].pos_ == "PRON" or sentence_[j].pos_ == "PROPN" or sentence_[j].pos_ == "NOUN":
                            main_entity.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "ADJ":
                            description.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "VERB":
                            action.append(sentence_[j].text)
                        else:
                            pass
                    elif sentence_[j].dep_ == "relcl":
                        if sentence_[j].pos_ == "VERB":
                            action.append(sentence_[j].text)
                        else:
                            pass
                    elif sentence_[j].dep_ == "compound":
                        if sentence_[j].pos_ == "NOUN":
                            main_entity.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "PROPN":
                            target_entity.append(sentence_[j].text)
                        elif sentence_[j].pos_ == "NUM":
                            target_entity.append(sentence_[j].text)
                        else:
                            pass
                    else:
                        pass
            allocation(remained)
            # put the adverbs into the verb list
            for q in range(len(way)):
                action.append(way[q])
            location = []
            # get the dependency of the extracted sentence without ner words
            for w in remained:
                location.append([w.text,w.dep_])
            # put adjective(s) into either subject or object list
            for h in range(len(location)):
                if location[h][0] in description:
                    if location[h-1][1] != "nsubj":
                        main_entity.append(location[h][0])
                    else:
                        target_entity.append(location[h][0])
            # put ner words into either subject or object list
            # by its distance from the median
            j = 0
            while j != len(ner):
                for v in range(len(ner[j])):
                    if ner[j][v] == "DATE":
                        if v == 0:
                            date.append(ner[j][1])
                            if ner[j][1] in main_entity:
                                index = main_entity.index(ner[j][1])
                                del main_entity[index]
                            elif ner[j][1] in target_entity:
                                index = target_entity.index(ner[j][1])
                                del target_entity[index]
                            else:
                                pass
                        else:
                            date.append(ner[j][0])
                            if ner[j][0] in main_entity:
                                index = main_entity.index(ner[j][0])
                                del main_entity[index]
                            elif ner[j][0] in target_entity:
                                index = target_entity.index(ner[j][0])
                                del target_entity[index]
                            else:
                                pass
                    elif ner[j][v] == "TIME":
                        if v == 0:
                            date.append(ner[j][1])
                            if ner[j][1] in main_entity:
                                index = main_entity.index(ner[j][1])
                                del main_entity[index]
                            elif ner[j][1] in target_entity:
                                index = target_entity.index(ner[j][1])
                                del target_entity[index]
                            else:
                                pass
                        else:
                            date.append(ner[j][0])
                            if ner[j][0] in main_entity:
                                index = main_entity.index(ner[j][0])
                                del main_entity[index]
                            elif ner[j][0] in target_entity:
                                index = target_entity.index(ner[j][0])
                                del target_entity[index]
                            else:
                                pass
                    else:
                        if ner[j][v].isupper() != True:
                            position_1, position_2 = words.index(ner[j][v]), words.index(ner[j][v]) + len(ner[j][v]) - 1
                            if position_1 <= median or position_2 <= median:
                                main_entity.append(ner[j][v])
                            elif position_1 >= median or position_2 >= median:
                                target_entity.append(ner[j][v])
                        else:
                            if ner[j][v] in labels_:
                                pass
                            else:
                                position_1, position_2 = words.index(ner[j][v]), words.index(ner[j][v]) + len(ner[j][v]) - 1
                                if position_1 <= median or position_2 <= median:
                                    main_entity.append(ner[j][v])
                                elif position_1 >= median or position_2 >= median:
                                    target_entity.append(ner[j][v])
                j += 1
            for f in range(len(date)):
                if date[f] in main_entity:
                    index_ = main_entity.index(date[f])
                    del main_entity[index_]
                elif date[f] in target_entity:
                    index_ = target_entity.index(date[f])
                    del target_entity[index_]
            if len(main_entity) == len(target_entity):
                if len(main_entity) == 0:
                    pass
            else:
                c = 0
                p = 0
                while p != len(ner):
                    for y in range(len(ner[p])):
                        if ner[p][y] in labels_:
                            if ner[p][y] != "DATE" and ner[p][y] != "TIME":
                                c += 1
                    p += 1
                if c != 0:
                    ner_text = []
                    n = 0
                    while n != len(ner):
                        for d in range(len(ner[n])):
                            if ner[n][d] not in labels_:
                                ner_text.append(ner[n][d])
                        n += 1
                    kucken = nlp(words)
                    for j in kucken:
                        if j.is_stop == True:
                            if j.text in main_entity:
                                gps = main_entity.index(j.text)
                                del main_entity[gps]
                            elif j.text in target_entity:
                                gps = target_entity.index(j.text)
                                del target_entity[gps]
                            elif j.text in action:
                                gps = action.index(j.text)
                                del action[gps]
                            else:
                                pass
                    main_entity = list(set(main_entity))
                    action = list(set(action))
                    target_entity = list(set(target_entity))
                    stop_ = []
                    for k in kucken:
                        if k.is_stop == True:
                            stop_.append(k.text)
                    for f in kucken.ents:
                        if f.text in stop_:
                            stop_.remove(f.text)
                    stop_ = list(set(stop_))
                    coin = left.split(' ')
                    for j in range(len(coin)):
                        if ',' in coin[j]:
                            coin[j] = coin[j].split(',')[0]
                        elif '.' in coin[j]:
                            coin[j] = coin[j].split('.')[0]
                        elif '?' in coin[j]:
                            coin[j] = coin[j].split('?')[0]
                        elif '!' in coin[j]:
                            coin[j] = coin[j].split('!')[0]
                        else:
                            pass
                    g = 0
                    impure = []
                    while g != len(coin):
                        if coin[g] in stop_:
                            impure.append(coin[g])
                        g += 1
                    coin = ' '.join([j for j in coin if j not in set(impure)]).strip()
                    ########################
                    cow = sent_.split(',')
                    for k in range(len(cow)):
                        cow[k] = cow[k].strip()
                    jo = cow[0].split()
                    m = 0
                    b = 0
                    length_ner = len(ner_text)
                    for n in range(len(jo)):
                        if jo[n] in stop_:
                           m += 1
                    for n in range(len(jo)):
                        if jo[n] in ner_text:
                           length_ner -= 1
                    for n in range(len(jo)):
                        if jo[n] in main_entity:
                            b += 1
                        elif jo[n] in target_entity:
                            b += 1
                        elif jo[n] in action:
                            b += 1
                        else:
                            pass
                    med = int(ma.floor(len(jo)/2))
                    if m <= med or b <= med:
                        if length_ner == 0:
                            del cow[0]
                    w = 0
                    selection = []
                    d = 0
                    while w != (len(cow)-d):
                        h = 0
                        r = 0
                        out = []
                        beef = cow[w]
                        for q in range(len(ner_text)):
                            if ner_text[q] in beef:
                                out.append(ner_text[q])
                                beef = ' '.join(cow[w].split(ner_text[q]))
                        merch = beef.split()
                        for s in out:
                            merch.append(s)
                        print(merch)
                        height = len(merch)
                        if height != 2:
                            wer = 1
                        if height == 2:
                            wer = 0
                        ian = int(ma.floor(height/2)+wer)
                        for s in range(len(merch)):
                            if merch[s] in stop_:
                                print("stop",merch[s])
                                h += 1
                        for s in range(len(merch)):
                            if merch[s] in ner_text:
                                if merch[s] in main_entity:
                                    print("ner","subj", merch[s])
                                    r += 4
                                elif merch[s] in target_entity:
                                    print("ner", "obej", merch[s])
                                    r += 3
                                else:
                                    pass
                            else:
                                if merch[s] in main_entity:
                                    print("subj", merch[s])
                                    r += 2
                                elif merch[s] in target_entity:
                                    print("obej", merch[s])
                                    r += 1
                                elif merch[s] in action:
                                    print("verb", merch[s])
                                    r += 1
                                else:
                                    pass
                        print(h, r, ian, '\n##############')
                        if (h + 1) >= ian and (r - 1) <= ian:
                            selection.append(cow[w])
                        w += 1
                    selection = set(selection)
                    cows = [j for j in cow if j not in selection]
                    if length_ner != 0:
                        print(cows)
                        # dos = nlp(sent_)
                        never = [
                                (
                                    sent_,
                                    {
                                        "combination": [
                                            main_entity,
                                            action,
                                            target_entity,
                                            date,
                                        ]
                                    }
                                )
                            ]
                        # print(never,'\n')
                        final.append(
                            never
                        )
    return final

bit = [
    "In the domestic business, against a backdrop where the NDP-reported consume electronic categories, which represents approximately 65% of our revenue were down 5.3%, our comparable sales in contracts, excluding the impact of installment billing, declined only 0.7% as we continued to take advantage of strong product cycles in large screen television and iconic mobile phones and confined growth in the appliance category.",
    "The FDA's approval of KYMRIAH as the first immune cell therapy is, of course, a very exciting development for the field of oncology, opening a whole new world of possibility for gene and cell therapies.",
    # "At Illumina, we strongly believe that sequencing offers the promise to transform lives and are encouraged to see sequencing continue its progress into clinical application.",
    # "The other driver of course has been the optimization of our merchandising activities, and the resulting impact on gross profit margin."
]

wer = extract(bit)

# go = np.random.randint(420)
#
# wer = extract(book[go:go+25])

