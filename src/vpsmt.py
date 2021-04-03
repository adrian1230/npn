import spacy as sp

nlp = sp.load('en_core_web_sm')

pronouns_ = ["we","We","they","They","you","You","He","he","she","She","It","it", "i", "I","Our","our","Their","their","his","Her","her","His","my","My","your","Your"]

conjunction_ = ["from","and","or","Or","And","From","Nor","nor","By","by","with","With"]

def extract(_sentence):
    svod_pair = ()
    sentence_ = _sentence
    median_sent = len(sentence_) / 2
    sent_in_sp = nlp(sentence_)
    ner_tags_from_sentence_box = []
    for d in sent_in_sp.ents:
        ner_tags_from_sentence_box.append([str(d), str(d.label_)])
    for j in ner_tags_from_sentence_box:
        if ner_tags_from_sentence_box.count(j) > 1:
            ner_tags_from_sentence_box.remove(j)
    sentence_without_ner_words = ''
    all_ner_label_from_spacy_box = [
        "PERSON", "ORG", "MONEY", "TIME",
        "GPE", "DATE", "DATED", "NORP",
        "PERCENT", "EVENT", "FAC", "LOC",
        "CARDINAL", "ORDINAL","PRODUCT", "LAW",
        "WORK_OF_ART", "QUANTITY"
    ]
    nlp_sent = nlp(sentence_)
    all_subject_box, all_verb_box, all_object_box, all_adjective_box, all_date_time_box = [], [], [], [], []
    def allocation_of_words(sentence_):
        for j in range(len(sentence_)):
            if sentence_[j].dep_ == "ROOT" or sentence_[j].pos_ == "VERB" or sentence_[j].pos_ == "AUX" or sentence_[j].dep_ == "advmod" or sentence_[j].dep_ == "advcl":
                all_verb_box.append(sentence_[j].text)
            elif sentence_[j].dep_ == "nsubj" or sentence_[j].dep_ == "nsubjpass":
                all_subject_box.append(sentence_[j].text)
            elif sentence_[j].dep_ == "pobj" or sentence_[j].dep_ == "compound" or sentence_[j].dep_ == "dobj" or sentence_[j].dep_ == "quantmod" or sentence_[j].dep_ == "nummod" or sentence_[j].dep_ == "npadvmod":
                all_object_box.append(sentence_[j].text)
            elif sentence_[j].dep_ == "amod" or sentence_[j].dep_ == "acomp" or sentence_[j].pos_ == "ADJ":
                all_adjective_box.append(sentence_[j].text)
    allocation_of_words(nlp_sent)
    if len(ner_tags_from_sentence_box) != 0:
        counter_for_ner_box = 0
        while counter_for_ner_box != len(ner_tags_from_sentence_box):
            ner_tag_ = ner_tags_from_sentence_box[counter_for_ner_box][1]
            ner_txt_ = ner_tags_from_sentence_box[counter_for_ner_box][0]
            if ner_tag_ == "DATE":
                all_date_time_box.append(ner_txt_)
            elif ner_tag_ == "TIME":
                all_date_time_box.append(ner_txt_)
            else:
                pos_1 = sentence_.index(ner_txt_)
                pos_2 = pos_1 + len(ner_txt_)
                if pos_1 <= median_sent or pos_2 <= median_sent:
                    all_subject_box.append(ner_txt_)
                elif pos_1 >= median_sent or pos_2 >= median_sent:
                    all_object_box.append(ner_txt_)
            counter_for_ner_box += 1
    if len(all_subject_box) != 0 and len(all_object_box) != 0:
        ner_text_only = [ner_tags_from_sentence_box[j][0] for j in range(len(ner_tags_from_sentence_box))]
        def clean(box):
            from nltk.corpus import stopwords
            stops_ = stopwords.words('english')
            for j in box:
                if j in stops_:
                    gps = box.index(j)
                    del box[gps]
            box = list(set(box))
        clean(all_subject_box)
        clean(all_verb_box)
        clean(all_object_box)
        extracted_core = sentence_.split(',')
        extracted_core = [j.strip() for j in extracted_core]
        counter_cor_extracted_core_parts = 0
        while counter_cor_extracted_core_parts != len(extracted_core):
            marked_box = []
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
            if counter_ner_in_this_extracted_part != 0:
                extracted_core[counter_cor_extracted_core_parts] = extracted_core[
                    counter_cor_extracted_core_parts
                    ][:marked_box[counter_ner_in_this_extracted_part-1]
                    ]
            counter_cor_extracted_core_parts += 1
        extracted_core_sent_string = ' '.join(extracted_core)
        if len(extracted_core) != 0:
            verb_only, sent__ = [], nlp(extracted_core_sent_string)
            for j in range(len(sent__)):
                if sent__[j].dep_ == "ROOT" or sent__[j].pos_ == "VERB" or sent__[j].pos_ == "AUX" or sent__[j].dep_ == "advmod" or sent__[j].dep_ == "advcl":
                    verb_only.append(sent__[j].text)
            if len(verb_only) != 0:
                final_subject_for_svod_pair, final_verb_for_svod_pair, final_object_for_svod_pair = '', '', ''
                final_date_time_for_svod_pair, _all_combination_of_verb_break_point = [], []
                # A B C D 4 verbs => (D, CD, BCD, ABCD) only
                _all_combination_of_verb_break_point.append(verb_only[-1])
                while len(_all_combination_of_verb_break_point) != len(verb_only):
                    diff = len(verb_only) - len(_all_combination_of_verb_break_point)
                    start_position_of_verb = extracted_core_sent_string.index(''.join([verb_only[diff-1],'']))
                    end_position_of_verb = extracted_core_sent_string.index(verb_only[-1])+len(verb_only[-1])
                    verb_string = extracted_core_sent_string[start_position_of_verb:end_position_of_verb]
                    _all_combination_of_verb_break_point.append(verb_string)
                counter_of_verb_combination_box = 0
                rating_of_all_verb_combination = []
                def counter_(box,_counter):
                        for h in box:
                            if ''.join([h,' ']) in _all_combination_of_verb_break_point[counter_of_verb_combination_box]:
                                _counter += 1
                while counter_of_verb_combination_box != len(_all_combination_of_verb_break_point):
                    _if_subj_or_obej_presented_counter = 0
                    counter_(all_subject_box,_if_subj_or_obej_presented_counter)
                    counter_(all_object_box,_if_subj_or_obej_presented_counter)
                    counter_(pronouns_,_if_subj_or_obej_presented_counter)
                    rating_of_all_verb_combination.append(_if_subj_or_obej_presented_counter)
                    counter_of_verb_combination_box += 1
                # v |(p|s)!(m|t) v
                delete_combination = [_all_combination_of_verb_break_point[d] for d in range(len(rating_of_all_verb_combination)) if rating_of_all_verb_combination[d] != 0]
                _all_combination_of_verb_break_point = [f for f in _all_combination_of_verb_break_point if f not in delete_combination or f != '']
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
                            final_subject_for_svod_pair = ''.join(final_subject_for_svod_pair.split(filtered_part))
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
                            filtered_part = final_object_for_svod_pair[all_recurring_box[0]:all_recurring_box[-1] + len(all_date_time_box[g])]
                            final_object_for_svod_pair = ''.join(final_object_for_svod_pair.split(filtered_part))
                            final_date_time_for_svod_pair.append(''.join([filtered_part,'']))
                    else:
                        pass
                splitted_final_subject_for_svod_pair = final_subject_for_svod_pair.split()
                if len(splitted_final_subject_for_svod_pair) > 1:
                    rating_for_subject_part = []
                    def rating_(_pair,s,o,p,c):
                        for e in range(len(_pair)):
                            if _pair[e] in s or _pair[e] in o or _pair[e] in p or _pair[e] in c:
                                rating_for_subject_part.append(1)
                            else:
                                rating_for_subject_part.append(0)
                    rating_(splitted_final_subject_for_svod_pair,all_subject_box,all_object_box,pronouns_,conjunction_)
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
                            splitted_final_subject_for_svod_pair = splitted_final_subject_for_svod_pair[chunk_in_subject_for_removal_1:chunk_in_subject_for_removal_1+1]
                        if chunk_in_subject_for_removal != (len(rating_for_subject_part)-1):
                            splitted_final_subject_for_svod_pair = splitted_final_subject_for_svod_pair[chunk_in_subject_for_removal+1:]
                svod_pair = (' '.join(splitted_final_subject_for_svod_pair).strip(),final_verb_for_svod_pair,final_object_for_svod_pair.strip(),' '.join(final_date_time_for_svod_pair).strip())
    return svod_pair

if __name__ == '__main__':
    print(extract(input("=> ")))