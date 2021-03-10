import spacy as sp
from bye import *
from operator import itemgetter

# load the spacy english-sm module
# nlp = sp.load('../model/spacy_finance')
nlp = sp.load('en_core_web_sm')
# call the data stored in another file
book = dry()

def extract(point):
    # the array for storing the original and extracted sentences
    little = []
    for d, u in enumerate(point):
        # if the length of a string is less than 5, including
        # punctuations, no contextual sentences will be made
        if len(u) >= 5:
            # split the sentence with ' ' can avoid losing important punctuations like $ and %
            splited = u.split(' ')
            script = nlp(u)
            subj, verb, obej, adv, adj = [], [], [], [], []
            def allocation(sentence_):
                # allocate different words to different arrays by spacy dependencies and pos tags
                # this way works aroung roughly 86% unless spacy goes wrong
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
            # adverbs stay with verbs
            for q in range(len(adv)):
                verb.append(adv[q])
            if len(verb) == 0:
                pass
            # if there is no verb or object in a sentence, then it is meaningless
            if len(verb) != 0:
                if len(obej) > 0:
                    # this array is for storing words and start and end positions
                    tup = []
                    # reconstruct sentence after rearranging adjectives
                    reconstructed = []
                    pack = [subj,verb,obej,adj]
                    # find the location of the same word in a sentence
                    for d in range(len(pack)):
                        for i in range(len(pack[d])):
                            word = pack[d][i]
                            length = len(word)
                            count = pack[d].count(word)
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
                    # remove duplicate from the for loop
                    tup = sorted(list(set(tup)), key=itemgetter(1))
                    g = 0
                    # find the closet word and
                    # if it is subject, put the adjective into subject
                    # vice versa for object
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
                    # rebuild sentences here
                    for h in range(len(splited)):
                        # create variance of words along with different punctuations
                        # so that it resembles with the splited sentence
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
                    # exclude stop, aux, and non-alpha words from the sentences
                    for i in doc:
                        if i.pos_ != "AUX":
                            if i.dep_ != "aux":
                                if i.is_stop == False:
                                    if i.is_alpha == True:
                                        refined.append(i.text)
                    refined = ' '.join(refined)
                    # append the original and extracted sentences into the little array
                    little.append([u,refined])

    # the final array is for the original sentence and the pos tag of the extracted sentence
    final = []

    def again_(rose):
        for d in range(len(rose)):
            # the original sentence
            sent_ = rose[d][0]
            # the extracted sentence
            words = rose[d][1]
            # find the length of the extracted sentence
            total_width = len(words)
            # find the median of the length
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
                    "PERSON", "ORG", "MONEY",
                    "GPE", "DATE", "DATED", "NORP",
                    "PERCENT", "EVENT", "FAC", "LOC",
                    "CARINAL", "ORDINAL"
                ]
                # remove the ner words from the extracted sentence for the next processing
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
                # rerun the allocation of pos tag function again
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
                        elif sentence_[j].dep_ == "xcomp" or sentence_[j].dep_ == "ccomp" or sentence_[j].dep_ == "pcomp" or sentence_[j].dep_ == "aux" or sentence_[j].dep_ == "auxpass" or sentence_[j].dep_ == "neg" or sentence_[j].dep_ == "attr" or sentence_[j].dep_ == "nmod":
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
                    if h == (len(location)-1):
                        if location[h][0] in description:
                            if location[h-1][1] != "nsubj":
                                main_entity.append(location[h][0])
                            else:
                                target_entity.append(location[h][0])
                    else:
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
                if len(main_entity) == len(target_entity):
                    if len(main_entity) == 0:
                        pass
                else:
                    never = [
                            (
                                sent_,
                                {
                                    "combination": [
                                        main_entity,
                                        action,
                                        target_entity,
                                        date
                                    ]
                                }
                            )
                        ]
                    print(never,'\n')
                    final.append(
                        never
                    )
    again_(little)
    return final

wer = extract(book[90:108])

for i in range(len(wer)):
    print(wer[i][0][0],'\n')
    print(wer[i][0][1], '\n')
    print("######################")
