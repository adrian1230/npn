import spacy as sp
from bye import *
import math as ma

# load the spacy module
# nlp = sp.load('../model/spacy_finance')
nlp = sp.load('en_core_web_sm')
# call the data stored in another file
book = dry()

# create a pronoun list for better s v o differentiation
pronouns_ = [
    "we","We","they","They","you","You","He","he","she","She","It","it", "i", "I",
    "Our","our","Their","their","his","Her","her","His","my","My","your","Your"
]

book = list(set(book))

def extract(point):
    little = []
    for d, u in enumerate(point):
        # no contextual sentences will be made
        if len(u) >= 15:
            if u.endswith('?') != True:
                little.append(u)
    # for the original sentence and the pos pair(s)
    final = []

    for d in range(len(little)):
        sent_ = little[d]
        # set another variable for change
        # and keep the first one unchanged
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
            remained_sentence = nlp(left)
            # main_entity == subject
            # action == verb
            # target_entity == object
            # adv_2 == adverb
            # description = adjective
            main_entity, action, target_entity, adv_2, description = [], [], [], [], []
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
                        adv_2.append(sentence_[j].text)
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
                    elif sentence_[j].dep_ == "parataxis":
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
            allocation(remained_sentence)
            # put the adverbs into the verb list
            for q in range(len(adv_2)):
                action.append(adv_2[q])
            location = []
            # get the dependency of the extracted sentence without ner words
            for w in remained_sentence:
                location.append([w.text,w.dep_])
            # put adjective(s) into either subject or object list
            for h in range(len(location)):
                if location[h][0] in description:
                    if h != (len(location) - 1):
                        if location[h+1][1] == "nsubj":
                            main_entity.append(location[h][0])
                        else:
                            target_entity.append(location[h][0])
            # put ner words into either subject or object list
            # by its distance from the median
            j = 0
            while j != len(ner):
                for v in range(len(ner[j])):
                    # if the ner label is either date of time,
                    # put into date all together
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
            # delete date or time text from subj and obej
            for f in range(len(date)):
                if date[f] in main_entity:
                    index_ = main_entity.index(date[f])
                    del main_entity[index_]
                elif date[f] in target_entity:
                    index_ = target_entity.index(date[f])
                    del target_entity[index_]
            # if subj and obej both null, then skip
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
                # if c != 0 means
                # we have ner words with labels other than time and date
                if c != 0:
                    ner_text = []
                    n = 0
                    while n != len(ner):
                        for d in range(len(ner[n])):
                            if ner[n][d] not in labels_:
                                ner_text.append(ner[n][d])
                        n += 1
                    ner_original_sent = nlp(words)
                    for j in ner_original_sent:
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
                    stop_words_array = []
                    # get stop words from the original text
                    for k in ner_original_sent:
                        if k.is_stop == True:
                            stop_words_array.append(k.text)
                    # remove ner words from stop word array,
                    # like first and second need to be removed from stop_words_array
                    for f in ner_original_sent.ents:
                        if f.text in stop_words_array:
                            stop_words_array.remove(f.text)
                    stop_words_array = list(set(stop_words_array))
                    splitted_original_sent = sent_.split(',')
                    for k in range(len(splitted_original_sent)):
                        splitted_original_sent[k] = splitted_original_sent[k].strip()
                    first_sent_in_ori_splitted = splitted_original_sent[0].split()
                    m = 0
                    b = 0
                    c = 0
                    for n in range(len(first_sent_in_ori_splitted)):
                        if first_sent_in_ori_splitted[n] in stop_words_array:
                           m += 1
                    for n in range(len(ner_text)):
                        if ner_text[n] in splitted_original_sent[0]:
                            c += 1
                    for n in range(len(first_sent_in_ori_splitted)):
                        if first_sent_in_ori_splitted[n] in main_entity:
                            b += 1
                        elif first_sent_in_ori_splitted[n] in target_entity:
                            b += 1
                        elif first_sent_in_ori_splitted[n] in action:
                            b += 1
                        else:
                            pass
                    median_position = int(ma.floor(len(first_sent_in_ori_splitted)/2))
                    if c == 0:
                        if m >= median_position or b <= median_position:
                            del splitted_original_sent[0]
                    w = 0
                    selection_4removal = []
                    d = 0
                    # check if there is more naunce than info in a sub-sentence
                    while w != (len(splitted_original_sent)-d):
                        # rating for stop words
                        h = 0
                        # rating for non-stop words
                        r = 0
                        # counter for stop words
                        st = 0
                        # counter for non-stop words
                        pos = 0
                        extracted_ner_words = []
                        sub_sent_copy = splitted_original_sent[w]
                        # split the text without spliting ner words
                        # to avoid deconstrcuting the ner words' structures
                        for q in range(len(ner_text)):
                            if ner_text[q] in sub_sent_copy:
                                extracted_ner_words.append(ner_text[q])
                                sub_sent_copy = ' '.join(splitted_original_sent[w].split(ner_text[q]))
                        sub_sent_copy_splitted = sub_sent_copy.split()
                        for s in extracted_ner_words:
                            sub_sent_copy_splitted.append(s)
                        height = len(sub_sent_copy_splitted)
                        # median_sub_sent = int(ma.floor(height/2)+1)
                        for s in range(len(sub_sent_copy_splitted)):
                            if sub_sent_copy_splitted[s] in stop_words_array:
                                st += 1
                                h += 2
                        for s in range(len(sub_sent_copy_splitted)):
                            if sub_sent_copy_splitted[s] in ner_text:
                                if sub_sent_copy_splitted[s] in main_entity:
                                    pos += 1
                                    r -= 1
                                elif sub_sent_copy_splitted[s] in target_entity:
                                    r -= 1
                                    pos += 1
                                else:
                                    pass
                            else:
                                if sub_sent_copy_splitted[s] in main_entity:
                                    r += 2
                                    pos += 1
                                elif sub_sent_copy_splitted[s] in target_entity:
                                    r += 2
                                    pos += 1
                                elif sub_sent_copy_splitted[s] in action:
                                    r += 2
                                    pos += 1
                                else:
                                    pass
                        # if stop word counter is greater or equal to non-stop word counter
                        # put the sub sentence into selection
                        # remove it later
                        if st > pos or pos == st:
                            selection_4removal.append(splitted_original_sent[w])
                        else:
                            pass
                        w += 1
                    selection_4removal = set(selection_4removal)
                    extracted_core = [j for j in splitted_original_sent if j not in selection_4removal]
                    v = 0
                    while v != len(extracted_core):
                        marked_box = []
                        # counter of the amount of ner words in
                        # each sub sent of the extracted_core
                        bs = 0
                        for s in range(len(ner_text)):
                            if ner_text[s] in extracted_core[v]:
                                bs += 1
                                pos_1 = extracted_core[v].index(ner_text[s])
                                pos_2 = pos_1 + len(ner_text[s])
                                marked_box.append(pos_2)
                        # if counter had been increased, use the last updated value
                        # to locate and separate the sentence
                        if bs != 0:
                            # a = the sub sent from the beginning of it to the last ner word
                            a = extracted_core[v][:marked_box[bs-1]]
                            # b = the rest
                            # b = extracted_core[v][marked_box[bs-1]+1:]
                            extracted_core[v] = a
                        else:
                            pass
                        v += 1
                    extracted_core_sent_string = ' '.join(extracted_core)
                    if len(extracted_core) != 0:
                        # if the length of the extracted sentence is less than 40 characters
                        # then mostly it is useless and definitely be meaningless
                        if len(extracted_core_sent_string) > 30:
                            # if the string is a question; useless too
                            if extracted_core_sent_string.endswith('?') != True:
                                verb_only = []
                                def only_verb(sentence_):
                                    for j in range(len(sentence_)):
                                        if sentence_[j].dep_ == "ROOT" or sentence_[j].dep_ == "xcomp" or sentence_[j].dep_ == "ccomp" or sentence_[
                                            j].dep_ == "pcomp" or sentence_[j].dep_ == "aux" or sentence_[
                                            j].dep_ == "auxpass" or sentence_[
                                            j].dep_ == "neg" or sentence_[j].dep_ == "attr" or sentence_[
                                            j].dep_ == "nmod" or sentence_[j].dep_ == "dobj" or sentence_[
                                            j].dep_ == "pobj" or sentence_[j].dep_ == "parataxis":
                                            if sentence_[j].pos_ == "VERB" or sentence_[j].pos_ == "AUX":
                                                verb_only.append(sentence_[j].text)
                                only_verb(nlp(extracted_core_sent_string))
                                removal = []
                                for f in range(len(verb_only)):
                                    if verb_only[f] == 'to':
                                        removal.append(verb_only[f])
                                verb_only = [g for g in verb_only if g not in removal]
                                if len(verb_only) != 0:
                                    final_subject_for_pos_pair = ''
                                    final_verb_for_pos_pair = ''
                                    final_object_for_pos_pair = ''
                                    combination = []
                                    for h in range(len(verb_only)):
                                        if h == (len(verb_only) - 1):
                                            combination.append(verb_only[h])
                                    while len(combination) != len(verb_only):
                                        diff = len(verb_only) - len(combination)
                                        start = extracted_core_sent_string.index(verb_only[diff-1])
                                        end = extracted_core_sent_string.index(verb_only[-1])+len(verb_only[-1])
                                        verb_ = extracted_core_sent_string[start:end]
                                        combination.append(verb_)
                                    e = 0
                                    rating = []
                                    while e != len(combination):
                                        _if_subj_or_obej_presented_counter = 0
                                        for g in main_entity:
                                            if g in combination[e]:
                                                _if_subj_or_obej_presented_counter += 1
                                        for g in target_entity:
                                            if g in combination[e]:
                                                _if_subj_or_obej_presented_counter += 1
                                        rating.append(_if_subj_or_obej_presented_counter)
                                        e += 1
                                    # v |(p|s)!(m|t) v
                                    delete_combination = []
                                    for d in range(len(rating)):
                                        if rating[d] != 0:
                                            delete_combination.append(combination[d])
                                    for j in combination:
                                        if j == '':
                                            delete_combination.append(j)
                                    combination = [f for f in combination if f not in delete_combination]
                                    if len(combination) == 0:
                                        final_subject_for_pos_pair = extracted_core_sent_string.split(verb_only[len(verb_only) - 1])[
                                            0].strip()
                                        final_object_for_pos_pair = extracted_core_sent_string.split(verb_only[len(verb_only) - 1])[
                                            1].strip()
                                        final_verb_for_pos_pair = verb_only[len(verb_only) - 1].strip()
                                    if len(combination) != 0:
                                        final_subject_for_pos_pair = extracted_core_sent_string.split(combination[-1])[
                                            0].strip()
                                        final_object_for_pos_pair = extracted_core_sent_string.split(combination[-1])[
                                            1].strip()
                                        final_verb_for_pos_pair = combination[-1].strip()
                                    never = (
                                                final_subject_for_pos_pair,
                                                final_verb_for_pos_pair,
                                                final_object_for_pos_pair
                                    )
                                    # print(never[0][0],'\n')
                                    # print(never[0][1],'\n#####################')
                                    final.append(
                                        never
                                    )
    return final

wer = extract(book)

print(wer)

