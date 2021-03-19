import spacy as sp
from bye import *
import math as ma

nlp = sp.load('en_core_web_sm')
# call the data stored in another file
book = dry()

# create a pronoun list for better (s v o) differentiation
pronouns_ = [
    "we","We","they","They","you","You","He","he","she","She","It","it", "i", "I",
    "Our","our","Their","their","his","Her","her","His","my","My","your","Your"
]

conjunction_ = [
    "from","and","or","From",
    "nor","By","by","with","With"
]

def filter(original_sentence):
    # no contextual sentences will be made
    if len(original_sentence) >= 10:
        return original_sentence
    else:
        return ''

def extract(passed_sentence):
    svod_pair = ()
    if passed_sentence != '':
        sentence_ = passed_sentence
        sentence_copy = sentence_
        median_point_of_original_sentence_by_char = len(sentence_copy) / 2
        sentence_in_spacy_for_ner_recognition = nlp(sentence_copy)
        ner_tags_from_sentence_box = []
        # get ner_tags_from_sentence_box to capture the core parts of the extracted sentence
        for d in sentence_in_spacy_for_ner_recognition.ents:
            ner_tags_from_sentence_box.append([str(d), str(d.label_)])
        for j in range(len(ner_tags_from_sentence_box)):
            ner_tags_from_sentence_box[j] = list(set(ner_tags_from_sentence_box[j]))
        sentence_without_ner_words = ''
        # if ner_tags_from_sentence_box tag is none, then we ignore the sentence
        all_ner_label_from_spacy_box = [
            "PERSON", "ORG", "MONEY", "TIME",
            "GPE", "DATE", "DATED", "NORP",
            "PERCENT", "EVENT", "FAC", "LOC",
            "CARDINAL", "ORDINAL","PRODUCT", "LAW",
            "WORK_OF_ART", "QUANTITY"
        ]
        remained_sentence = ''
        if len(ner_tags_from_sentence_box) != 0:
            # remove the ner_tags_from_sentence_box sentence_copy from the extracted sentence
            _for_ner_removal_from_sentence_counter = 0
            while _for_ner_removal_from_sentence_counter != len(ner_tags_from_sentence_box):
                for d in range(len(ner_tags_from_sentence_box[_for_ner_removal_from_sentence_counter])):
                    if _for_ner_removal_from_sentence_counter == 0:
                        if ner_tags_from_sentence_box[_for_ner_removal_from_sentence_counter][d].isupper() != True:
                            sentence_without_ner_words = ''.join(sentence_copy.split(ner_tags_from_sentence_box[_for_ner_removal_from_sentence_counter][d]))
                        else:
                            if ner_tags_from_sentence_box[_for_ner_removal_from_sentence_counter][d] in all_ner_label_from_spacy_box:
                                pass
                            else:
                                sentence_without_ner_words = ''.join(sentence_copy.split(ner_tags_from_sentence_box[_for_ner_removal_from_sentence_counter][d]))
                    else:
                        if ner_tags_from_sentence_box[_for_ner_removal_from_sentence_counter][d].isupper() != True:
                            sentence_without_ner_words = ''.join(sentence_without_ner_words.split(ner_tags_from_sentence_box[_for_ner_removal_from_sentence_counter][d]))
                        else:
                            if ner_tags_from_sentence_box[_for_ner_removal_from_sentence_counter][d] in all_ner_label_from_spacy_box:
                                pass
                            else:
                                sentence_without_ner_words = ''.join(sentence_without_ner_words.split(ner_tags_from_sentence_box[_for_ner_removal_from_sentence_counter][d]))
                _for_ner_removal_from_sentence_counter += 1
            remained_sentence = nlp(sentence_without_ner_words)
        if len(ner_tags_from_sentence_box) == 0:
            remained_sentence = nlp(sentence_copy)
        # all_subject_box == subject
        # all_verb_box == verb
        # all_object_box == object
        # all_adverb_box == adverb
        # all_adjective_box = adjective
        all_subject_box, all_verb_box, all_object_box, all_adverb_box, all_adjective_box = [], [], [], [], []
        all_date_time_box = []
        def allocation_of_subject_object_verb_adjecvtive_adverb(sentence_):
            for j in range(len(sentence_)):
                if sentence_[j].dep_ == "ROOT":
                    if sentence_[j].pos_ == "VERB":
                        all_verb_box.append(sentence_[j].text)
                    elif sentence_[j].pos_ == "NUM":
                        all_object_box.append(sentence_[j].text)
                    elif sentence_[j].pos_ == "AUX":
                        all_verb_box.append(sentence_[j].text)
                elif sentence_[j].dep_ == "xcomp" or sentence_[j].dep_ == "advcl" or sentence_[j].dep_ == "ccomp" or sentence_[j].dep_ == "pcomp" or sentence_[j].dep_ == "aux" or sentence_[j].dep_ == "auxpass" or sentence_[j].dep_ == "neg" or sentence_[j].dep_ == "attr" or sentence_[j].dep_ == "nmod":
                    all_verb_box.append(sentence_[j].text)
                elif sentence_[j].dep_ == "nsubj" or sentence_[j].dep_ == "nsubjpass":
                    all_subject_box.append(sentence_[j].text)
                elif sentence_[j].dep_ == "pobj" or sentence_[j].dep_ == "dobj" or sentence_[j].dep_ == "quantmod" or sentence_[j].dep_ == "nummod" or sentence_[j].dep_ == "npadvmod":
                    all_object_box.append(sentence_[j].text)
                elif sentence_[j].dep_ == "amod" or sentence_[j].dep_ == "acomp":
                    all_adjective_box.append(sentence_[j].text)
                elif sentence_[j].dep_ == "advmod" or sentence_[j].dep_ == "advcl":
                    all_adverb_box.append(sentence_[j].text)
                elif sentence_[j].dep_ == "conj":
                    if sentence_[j].pos_ == "PRON" or sentence_[j].pos_ == "PROPN" or sentence_[j].pos_ == "NOUN":
                        all_subject_box.append(sentence_[j].text)
                    elif sentence_[j].pos_ == "ADJ":
                        all_adjective_box.append(sentence_[j].text)
                    elif sentence_[j].pos_ == "VERB":
                        all_verb_box.append(sentence_[j].text)
                    else:
                        pass
                elif sentence_[j].dep_ == "relcl":
                    if sentence_[j].pos_ == "VERB":
                        all_verb_box.append(sentence_[j].text)
                    else:
                        pass
                elif sentence_[j].dep_ == "parataxis":
                    if sentence_[j].pos_ == "VERB":
                        all_verb_box.append(sentence_[j].text)
                    else:
                        pass
                elif sentence_[j].dep_ == "compound":
                    if sentence_[j].pos_ == "NOUN":
                        all_subject_box.append(sentence_[j].text)
                    elif sentence_[j].pos_ == "PROPN":
                        all_object_box.append(sentence_[j].text)
                    elif sentence_[j].pos_ == "NUM":
                        all_object_box.append(sentence_[j].text)
                    else:
                        pass
                else:
                    pass
        allocation_of_subject_object_verb_adjecvtive_adverb(remained_sentence)
        # put the adverbs into the verb list
        for q in range(len(all_adverb_box)):
            all_verb_box.append(all_adverb_box[q])
        location = []
        # get the dependency of the extracted sentence without ner_tags_from_sentence_box sentence_copy
        for w in remained_sentence:
            location.append([w.text,w.dep_])
        # put adjective(s) into either subject or object list
        for h in range(len(location)):
            if location[h][0] in all_adjective_box:
                if h != (len(location) - 1):
                    if location[h+1][1] == "nsubj" or location[h+1][1] == "dobj" or location[h+1][1] == "pobj" or location[h+1][1] == "compound" or location[h+1][1] == "nsubjpass" or location[h+1][1] =="attr" or location[h+1][1] == "conj" or location[h+1][1] == "pcomp":
                        all_subject_box.append(location[h][0])
                    else:
                        all_object_box.append(location[h][0])
        # put ner_tags_from_sentence_box sentence_copy into either subject or object list
        # by its distance from the median_point_of_original_sentence_by_char
        if len(ner_tags_from_sentence_box) != 0:
            counter_for_ner_box = 0
            while counter_for_ner_box != len(ner_tags_from_sentence_box):
                # print(ner_tags_from_sentence_box[counter_for_ner_box])
                for v in range(len(ner_tags_from_sentence_box[counter_for_ner_box])):
                    # if the ner_tags_from_sentence_box label is either all_date_time_box of time,
                    # put into all_date_time_box all together
                    if ner_tags_from_sentence_box[counter_for_ner_box][v] == "DATE":
                        if v == 0:
                            all_date_time_box.append(ner_tags_from_sentence_box[counter_for_ner_box][1])
                        else:
                            all_date_time_box.append(ner_tags_from_sentence_box[counter_for_ner_box][0])
                    elif ner_tags_from_sentence_box[counter_for_ner_box][v] == "TIME":
                        if v == 0:
                            all_date_time_box.append(ner_tags_from_sentence_box[counter_for_ner_box][1])
                        else:
                            all_date_time_box.append(ner_tags_from_sentence_box[counter_for_ner_box][0])
                    else:
                        if ner_tags_from_sentence_box[counter_for_ner_box][v].isupper() != True:
                            position_1, position_2 = sentence_copy.index(ner_tags_from_sentence_box[counter_for_ner_box][v]), sentence_copy.index(ner_tags_from_sentence_box[counter_for_ner_box][v]) + len(ner_tags_from_sentence_box[counter_for_ner_box][v]) - 1
                            if position_1 <= median_point_of_original_sentence_by_char or position_2 <= median_point_of_original_sentence_by_char:
                                all_subject_box.append(ner_tags_from_sentence_box[counter_for_ner_box][v])
                            elif position_1 >= median_point_of_original_sentence_by_char or position_2 >= median_point_of_original_sentence_by_char:
                                all_object_box.append(ner_tags_from_sentence_box[counter_for_ner_box][v])
                        else:
                            if ner_tags_from_sentence_box[counter_for_ner_box][v] in all_ner_label_from_spacy_box:
                                pass
                            else:
                                position_1 = sentence_copy.index(ner_tags_from_sentence_box[counter_for_ner_box][v])
                                position_2 = position_1 + len(ner_tags_from_sentence_box[counter_for_ner_box][v]) - 1
                                if position_1 <= median_point_of_original_sentence_by_char or position_2 <= median_point_of_original_sentence_by_char:
                                    all_subject_box.append(ner_tags_from_sentence_box[counter_for_ner_box][v])
                                elif position_1 >= median_point_of_original_sentence_by_char or position_2 >= median_point_of_original_sentence_by_char:
                                    all_object_box.append(ner_tags_from_sentence_box[counter_for_ner_box][v])
                counter_for_ner_box += 1
            # delete all_date_time_box or time text from subj and obej
            for f in range(len(all_date_time_box)):
                if all_date_time_box[f] in all_subject_box:
                    index_ = all_subject_box.index(all_date_time_box[f])
                    del all_subject_box[index_]
                elif all_date_time_box[f] in all_object_box:
                    index_ = all_object_box.index(all_date_time_box[f])
                    del all_object_box[index_]
        # if subj and obej both null, then skip
        if len(all_subject_box) != 0 and len(all_object_box) != 0:
            ner_text_only = []
            if len(ner_tags_from_sentence_box) != 0:
                counter_for_ner_tag_box_3 = 0
                while counter_for_ner_tag_box_3 != len(ner_tags_from_sentence_box):
                    for d in range(len(ner_tags_from_sentence_box[counter_for_ner_tag_box_3])):
                        if ner_tags_from_sentence_box[counter_for_ner_tag_box_3][d] not in all_ner_label_from_spacy_box:
                            ner_text_only.append(ner_tags_from_sentence_box[counter_for_ner_tag_box_3][d])
                    counter_for_ner_tag_box_3 += 1
            # remove stop words from subject, verb, object boxes
            for j in sentence_in_spacy_for_ner_recognition:
                if j.is_stop == True:
                    if j.text in all_subject_box:
                        gps = all_subject_box.index(j.text)
                        del all_subject_box[gps]
                    elif j.text in all_object_box:
                        gps = all_object_box.index(j.text)
                        del all_object_box[gps]
                    elif j.text in all_verb_box:
                        gps = all_verb_box.index(j.text)
                        del all_verb_box[gps]
                    else:
                        pass
            all_subject_box = list(set(all_subject_box))
            all_verb_box = list(set(all_verb_box))
            all_object_box = list(set(all_object_box))
            stop_words_array = []
            # get stop sentence_copy from the original text
            for k in sentence_in_spacy_for_ner_recognition:
                if k.is_stop == True:
                    stop_words_array.append(k.text)
            # remove ner_tags_from_sentence_box sentence_copy from stop word array,
            # like first and second need to be removed from stop_words_array
            if len(ner_tags_from_sentence_box) != 0:
                for f in sentence_in_spacy_for_ner_recognition.ents:
                    if f.text in stop_words_array:
                        stop_words_array.remove(f.text)
            stop_words_array = list(set(stop_words_array))
            splitted_original_sentence = sentence_.split(',')
            for k in range(len(splitted_original_sentence)):
                splitted_original_sentence[k] = splitted_original_sentence[k].strip()
            counter_for_splitted_original_sent_box = 0
            selection_4removal = []
            # check if there is more naunce than info in a sub-sentence
            while counter_for_splitted_original_sent_box != (len(splitted_original_sentence)):
                # counter for stop sentence_copy
                stop_word_counter = 0
                # counter for non-stop sentence_copy
                svo_counter = 0
                extracted_ner_words = []
                sub_sent_copy = splitted_original_sentence[counter_for_splitted_original_sent_box]
                sub_sent_copy_splitted = sub_sent_copy.split()
                # split the text without spliting ner_tags_from_sentence_box sentence_copy
                # to avoid deconstrcuting the ner_tags_from_sentence_box sentence_copy' structures
                if len(ner_tags_from_sentence_box) != 0:
                    for q in range(len(ner_text_only)):
                        if ner_text_only[q] in sub_sent_copy:
                            extracted_ner_words.append(ner_text_only[q])
                            sub_sent_copy = ' '.join(splitted_original_sentence[counter_for_splitted_original_sent_box].split(ner_text_only[q]))
                    sub_sent_copy_splitted = sub_sent_copy.split()
                    for s in extracted_ner_words:
                        sub_sent_copy_splitted.append(s)
                for s in range(len(sub_sent_copy_splitted)):
                    if sub_sent_copy_splitted[s] in stop_words_array:
                        stop_word_counter += 1
                for s in range(len(sub_sent_copy_splitted)):
                    if sub_sent_copy_splitted[s] in all_subject_box:
                        svo_counter += 1
                    elif sub_sent_copy_splitted[s] in all_object_box:
                        svo_counter += 1
                    elif sub_sent_copy_splitted[s] in all_verb_box:
                        svo_counter += 1
                    else:
                        pass
                # if stop word counter is greater or equal to non-stop word counter
                # put the sub sentence into selection
                # remove it later
                if stop_word_counter > (svo_counter + 5) or (svo_counter + 5) == stop_word_counter:
                    selection_4removal.append(splitted_original_sentence[counter_for_splitted_original_sent_box])
                counter_for_splitted_original_sent_box += 1
            selection_4removal = set(selection_4removal)
            extracted_core = [j for j in splitted_original_sentence if j not in selection_4removal]
            counter_cor_extracted_core_parts = 0
            while counter_cor_extracted_core_parts != len(extracted_core):
                marked_box = []
                # counter of the amount of ner_tags_from_sentence_box sentence_copy in
                # each sub sent of the extracted_core
                counter_ner_in_this_extracted_part = 0
                for s in range(len(ner_text_only)):
                    if ner_text_only[s] in extracted_core[counter_cor_extracted_core_parts]:
                        counter_ner_in_this_extracted_part += 1
                        pos_start = extracted_core[counter_cor_extracted_core_parts].index(ner_text_only[s])
                        try:
                            pos_start = extracted_core[counter_cor_extracted_core_parts].index(ner_text_only[s],pos_start+1)
                            pos_end = pos_start + len(ner_text_only[s])
                        except:
                            pos_end = pos_start + len(ner_text_only[s])
                        marked_box.append(pos_end)
                # if counter had been increased, use the sentence_in_spacy_for_ner_recognition updated value
                # to locate and separate the sentence
                if counter_ner_in_this_extracted_part != 0:
                    # a = the sub sent from the beginning of it to the sentence_in_spacy_for_ner_recognition ner_tags_from_sentence_box word
                    a = extracted_core[counter_cor_extracted_core_parts][:marked_box[counter_ner_in_this_extracted_part-1]]
                    extracted_core[counter_cor_extracted_core_parts] = a
                else:
                    pass
                counter_cor_extracted_core_parts += 1
            extracted_core_sent_string = ' '.join(extracted_core)
            if len(extracted_core) != 0:
                verb_only = []
                def only_verb(sentence_):
                    for j in range(len(sentence_)):
                        if sentence_[j].dep_ == "ROOT" or sentence_[j].dep_ == "xcomp" or sentence_[j].dep_ == "ccomp" or sentence_[j].dep_ == "pcomp" or sentence_[j].dep_ == "aux" or sentence_[j].dep_ == "auxpass" or sentence_[j].dep_ == "neg" or sentence_[j].dep_ == "attr" or sentence_[j].dep_ == "nmod" or sentence_[j].dep_ == "dobj" or sentence_[j].dep_ == "pobj" or sentence_[j].dep_ == "parataxis":
                            if sentence_[j].pos_ == "VERB" or sentence_[j].pos_ == "AUX":
                                verb_only.append(sentence_[j].text)
                only_verb(nlp(extracted_core_sent_string))
                word_from_verb_only_4removal = []
                for f in range(len(verb_only)):
                    if verb_only[f] == 'to':
                        word_from_verb_only_4removal.append(verb_only[f])
                verb_only = [g for g in verb_only if g not in word_from_verb_only_4removal]
                if len(verb_only) != 0:
                    final_subject_for_svod_pair = ''
                    final_verb_for_svod_pair = ''
                    final_object_for_svod_pair = ''
                    final_date_time_for_svod_pair = []
                    _all_combination_of_verb_break_point = []
                    # if we have A B C D 4 verbs, by order, in a sentence
                    # we only need to get D, CD, BCD, ABCD these 4 combinations
                    for h in range(len(verb_only)):
                        if h == (len(verb_only) - 1):
                            _all_combination_of_verb_break_point.append(verb_only[h])
                    while len(_all_combination_of_verb_break_point) != len(verb_only):
                        diff = len(verb_only) - len(_all_combination_of_verb_break_point)
                        start_position_of_verb = extracted_core_sent_string.index(''.join([verb_only[diff-1],' ']))
                        end_position_of_verb = extracted_core_sent_string.index(verb_only[-1])+len(verb_only[-1])
                        verb_string = extracted_core_sent_string[start_position_of_verb:end_position_of_verb]
                        _all_combination_of_verb_break_point.append(verb_string)
                    counter_of_verb_combination_box = 0
                    rating_of_all_verb_combination = []
                    while counter_of_verb_combination_box != len(_all_combination_of_verb_break_point):
                        _if_subj_or_obej_presented_counter = 0
                        for g in all_subject_box:
                            g = ''.join([g,' '])
                            if g in _all_combination_of_verb_break_point[counter_of_verb_combination_box]:
                                _if_subj_or_obej_presented_counter += 1
                        for g in all_object_box:
                            g = ''.join([g, ' '])
                            if g in _all_combination_of_verb_break_point[counter_of_verb_combination_box]:
                                _if_subj_or_obej_presented_counter += 1
                        for g in pronouns_:
                            g = ''.join([g, ' '])
                            if g in _all_combination_of_verb_break_point[counter_of_verb_combination_box]:
                                _if_subj_or_obej_presented_counter += 1
                        rating_of_all_verb_combination.append(_if_subj_or_obej_presented_counter)
                        counter_of_verb_combination_box += 1
                    # v |(p|s)!(m|t) v
                    delete_combination = []
                    for d in range(len(rating_of_all_verb_combination)):
                        if rating_of_all_verb_combination[d] != 0:
                            delete_combination.append(_all_combination_of_verb_break_point[d])
                    for j in _all_combination_of_verb_break_point:
                        if j == '':
                            delete_combination.append(j)
                    _all_combination_of_verb_break_point = [f for f in _all_combination_of_verb_break_point if f not in delete_combination]
                    if len(_all_combination_of_verb_break_point) == 0:
                        final_subject_for_svod_pair = extracted_core_sent_string.split(verb_only[len(verb_only) - 1])[0].strip()
                        final_object_for_svod_pair = extracted_core_sent_string.split(verb_only[len(verb_only) - 1])[1].strip()
                        final_verb_for_svod_pair = verb_only[len(verb_only) - 1].strip()
                    if len(_all_combination_of_verb_break_point) != 0:
                        final_subject_for_svod_pair = extracted_core_sent_string.split(_all_combination_of_verb_break_point[-1])[0].strip()
                        final_object_for_svod_pair = extracted_core_sent_string.split(_all_combination_of_verb_break_point[-1])[1].strip()
                        final_verb_for_svod_pair = _all_combination_of_verb_break_point[-1].strip()
                    for g in range(len(all_date_time_box)):
                        chunk = all_date_time_box[g]
                        counter_of_chunk = all_date_time_box.count(all_date_time_box[g])
                        if chunk in final_subject_for_svod_pair:
                            if counter_of_chunk <= 1:
                                final_subject_for_svod_pair = ''.join(final_subject_for_svod_pair.split(chunk))
                                final_date_time_for_svod_pair.append(''.join([all_date_time_box[g],'']))
                            if counter_of_chunk >= 2:
                                all_recurring_box = []
                                f = 0
                                while f != counter_of_chunk:
                                    if f == 0:
                                        all_recurring_box.append(final_subject_for_svod_pair.index(chunk))
                                    else:
                                        all_recurring_box.append(final_subject_for_svod_pair.index(chunk,all_recurring_box[-1]+f))
                                    f += 1
                                filtered_part = final_subject_for_svod_pair[all_recurring_box[0]:all_recurring_box[-1]+len(all_date_time_box[g])]
                                final_subject_for_svod_pair = ''.join(
                                    final_subject_for_svod_pair.split(
                                        filtered_part
                                    )
                                )
                                final_date_time_for_svod_pair.append(''.join([filtered_part,'']))
                        elif chunk in final_object_for_svod_pair:
                            if counter_of_chunk <= 1:
                                final_object_for_svod_pair = ''.join(final_object_for_svod_pair.split(chunk))
                                final_date_time_for_svod_pair.append(''.join([all_date_time_box[g],'']))
                            if counter_of_chunk >= 2:
                                all_recurring_box = []
                                f = 0
                                while f != counter_of_chunk:
                                    if f == 0:
                                        all_recurring_box.append(final_object_for_svod_pair.index(chunk))
                                    else:
                                        all_recurring_box.append(
                                            final_object_for_svod_pair.index(chunk, all_recurring_box[-1] + f))
                                    f += 1
                                filtered_part = final_object_for_svod_pair[
                                                all_recurring_box[0]:all_recurring_box[-1] + len(all_date_time_box[g])]
                                final_object_for_svod_pair = ''.join(
                                    final_object_for_svod_pair.split(
                                        filtered_part
                                    )
                                )
                                final_date_time_for_svod_pair.append(''.join([filtered_part,'']))
                        else:
                            pass
                    splitted_final_subject_for_svod_pair = final_subject_for_svod_pair.split()
                    if len(splitted_final_subject_for_svod_pair) > 1:
                        rating_for_subject_part = []
                        for h in range(len(splitted_final_subject_for_svod_pair)):
                            if splitted_final_subject_for_svod_pair[h] in all_subject_box:
                                rating_for_subject_part.append(1)
                            elif splitted_final_subject_for_svod_pair[h] in all_object_box:
                                rating_for_subject_part.append(1)
                            elif splitted_final_subject_for_svod_pair[h] in pronouns_:
                                rating_for_subject_part.append(1)
                            elif splitted_final_subject_for_svod_pair[h] in conjunction_:
                                if splitted_final_subject_for_svod_pair[h] == "to":
                                    if "from" in splitted_final_subject_for_svod_pair:
                                        rating_for_subject_part.append(1)
                                    else:
                                        rating_for_subject_part.append(0)
                                else:
                                    rating_for_subject_part.append(1)
                            else:
                                rating_for_subject_part.append(0)
                        chunk_in_subject_for_removal = 0
                        if rating_for_subject_part.count(0) != 0:
                            for j in reversed(range(len(rating_for_subject_part))):
                                if rating_for_subject_part[j] == 0:
                                    chunk_in_subject_for_removal = j
                                    break
                            if chunk_in_subject_for_removal == (len(rating_for_subject_part) - 1):
                                for j in reversed(range(len(rating_for_subject_part))):
                                    if rating_for_subject_part[j] == 1:
                                        e = 1
                                        while (j-e) != 0:
                                            if rating_for_subject_part[j-e]==0:
                                                break
                                            e += 1
                                        break
                                chunk_in_subject_for_removal_1 = j
                                splitted_final_subject_for_svod_pair = splitted_final_subject_for_svod_pair[
                                                                       chunk_in_subject_for_removal_1:chunk_in_subject_for_removal_1+1
                                                                       ]
                            if chunk_in_subject_for_removal != (len(rating_for_subject_part)-1):
                                splitted_final_subject_for_svod_pair = splitted_final_subject_for_svod_pair[chunk_in_subject_for_removal+1:]
                        final_subject_for_svod_pair = ' '.join(splitted_final_subject_for_svod_pair)
                    final_subject_for_svod_pair = final_subject_for_svod_pair.strip()
                    final_date_time_for_svod_pair = ' '.join(final_date_time_for_svod_pair).strip()
                    final_object_for_svod_pair = final_object_for_svod_pair.strip()
                    svod_pair = (
                                final_subject_for_svod_pair,
                                final_verb_for_svod_pair,
                                final_object_for_svod_pair,
                                final_date_time_for_svod_pair
                    )
    return svod_pair

def run_single_sentence(sent):
    return extract(filter(sent))

if __name__ == '__main__':
    print(run_single_sentence(input("=> ")))

