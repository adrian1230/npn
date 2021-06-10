import spacy as sp
from nltk.corpus import stopwords

nlp = sp.load('en_core_web_sm')
stops__ = stopwords.words('english')
conjunction_ = ["and","or","And","By","by","with","With"]

def extract(_sentence):
    svod_pair = ()
    sentence_ = _sentence
    med_p = len(sentence_) / 2
    sent_in_sp = nlp(sentence_)
    ner_tags = [[str(d), str(d.label_)] for d in sent_in_sp.ents]
    for j in ner_tags:
        if ner_tags.count(j) > 1:
            ner_tags.remove(j)
    all_ner_label_from_spacy_box = [
        "PERSON", "ORG", "MONEY", "TIME",
        "GPE", "DATE", "DATED", "NORP",
        "PERCENT", "EVENT", "FAC", "LOC",
        "CARDINAL", "ORDINAL","PRODUCT", "LAW",
        "WORK_OF_ART", "QUANTITY"
    ]
    entity_b, verb_b, dt_b = [], [], []
    for j in sent_in_sp:
        if j.dep_ == "ROOT" or j.pos_ == "VERB" or j.pos_ == "AUX" or j.dep_ == "advmod" or j.dep_ == "advcl":
            verb_b.append(j.text)
        elif j.dep_ == "nsubj" or j.dep_ == "nsubjpass" or j.dep_ == "pobj" or j.dep_ == "compound" or j.dep_ == "dobj" or j.dep_ == "quantmod" or j.dep_ == "nummod" or j.dep_ == "npadvmod":
            entity_b.append(j.text)
    if len(ner_tags) != 0:
        count_ner = 0
        while count_ner != len(ner_tags):
            ner_tag_ = ner_tags[count_ner][1]
            ner_txt_ = ner_tags[count_ner][0]
            if ner_tag_ == "DATE" or ner_tag_ == "TIME":
                dt_b.append(ner_txt_)
            else:
                pos_1 = sentence_.index(ner_txt_)
                pos_2 = pos_1 + len(ner_txt_)
                if pos_1 <= med_p or pos_2 <= med_p or pos_1 >= med_p or pos_2 >= med_p:
                    entity_b.append(ner_txt_)
            count_ner += 1
    if len(entity_b) != 0:
        ner_text_only = [ner_tags[j][0] for j in range(len(ner_tags))]
        def clean(box):
            for j in box:
                if j in stops__:
                    gps = box.index(j)
                    del box[gps]
            box = list(set(box))
        clean(entity_b)
        clean(verb_b)
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
                final_subj, final_verb, final_obj = '', '', ''
                final_dt, _all_combination_of_verb_break_point = [], []
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
                    counter_(entity_b,_if_subj_or_obej_presented_counter)
                    rating_of_all_verb_combination.append(_if_subj_or_obej_presented_counter)
                    counter_of_verb_combination_box += 1
                # v |(p|s)!(m|t) v
                delete_combination = [_all_combination_of_verb_break_point[d] for d in range(len(rating_of_all_verb_combination)) if rating_of_all_verb_combination[d] != 0]
                _all_combination_of_verb_break_point = [f for f in _all_combination_of_verb_break_point if f not in delete_combination or f != '']
                if len(_all_combination_of_verb_break_point) == 0:
                    final_subj = extracted_core_sent_string.split(verb_only[len(verb_only) - 1])[0].strip()
                    final_obj = extracted_core_sent_string.split(verb_only[len(verb_only) - 1])[1].strip()
                    final_verb = verb_only[len(verb_only) - 1].strip()
                if len(_all_combination_of_verb_break_point) != 0:
                    final_subj = extracted_core_sent_string.split(_all_combination_of_verb_break_point[-1])[0].strip()
                    final_obj = extracted_core_sent_string.split(_all_combination_of_verb_break_point[-1])[1].strip()
                    final_verb = _all_combination_of_verb_break_point[-1].strip()
                for g in range(len(dt_b)):
                    chunk = dt_b[g]
                    counter_of_chunk = dt_b.count(dt_b[g])
                    if chunk in final_subj:
                        if counter_of_chunk <= 1:
                            final_subj = ''.join(final_subj.split(chunk))
                            final_dt.append(''.join([dt_b[g],'']))
                        if counter_of_chunk >= 2:
                            all_recurring_box = []
                            f = 0
                            while f != counter_of_chunk:
                                if f == 0:
                                    all_recurring_box.append(final_subj.index(chunk))
                                else:
                                    all_recurring_box.append(final_subj.index(chunk,all_recurring_box[-1]+f))
                                f += 1
                            filtered_part = final_subj[all_recurring_box[0]:all_recurring_box[-1]+len(dt_b[g])]
                            final_subj = ''.join(final_subj.split(filtered_part))
                            final_dt.append(''.join([filtered_part,'']))
                    elif chunk in final_obj:
                        if counter_of_chunk <= 1:
                            final_obj = ''.join(final_obj.split(chunk))
                            final_dt.append(''.join([dt_b[g],'']))
                        if counter_of_chunk >= 2:
                            all_recurring_box = []
                            f = 0
                            while f != counter_of_chunk:
                                if f == 0:
                                    all_recurring_box.append(final_obj.index(chunk))
                                else:
                                    all_recurring_box.append(
                                        final_obj.index(chunk, all_recurring_box[-1] + f))
                                f += 1
                            filtered_part = final_obj[all_recurring_box[0]:all_recurring_box[-1] + len(dt_b[g])]
                            final_obj = ''.join(final_obj.split(filtered_part))
                            final_dt.append(''.join([filtered_part,'']))
                    else:
                        pass
                final_subj_split = final_subj.split()
                if len(final_subj_split) > 1:
                    rate_subj = []
                    def rating_(_pair,ent,c):
                        for e in range(len(_pair)):
                            if _pair[e] in ent or _pair[e] in c:
                                rate_subj.append(1)
                            else:
                                rate_subj.append(0)
                    rating_(final_subj_split,entity_b,conjunction_)
                    chunk_in_subject_for_removal = 0
                    if rate_subj.count(0) != 0:
                        for j in reversed(range(len(rate_subj))):
                            if rate_subj[j] == 0:
                                chunk_in_subject_for_removal = j
                                break
                        if chunk_in_subject_for_removal == (len(rate_subj) - 1):
                            for w in reversed(range(len(rate_subj))):
                                if rate_subj[w] == 1:
                                    e = 1
                                    while (w-e) != 0:
                                        if rate_subj[w-e]==0:
                                            break
                                        e += 1
                                    break
                            chunk_in_subject_for_removal_1 = w
                            final_subj_split = final_subj_split[chunk_in_subject_for_removal_1:chunk_in_subject_for_removal_1+1]
                        if chunk_in_subject_for_removal != (len(rate_subj)-1):
                            final_subj_split = final_subj_split[chunk_in_subject_for_removal+1:]
                svod_pair = (' '.join(final_subj_split).strip(),final_verb,final_obj.strip(),' '.join(final_dt).strip())
    return svod_pair

if __name__ == '__main__':
    print(extract(input("=> ")))