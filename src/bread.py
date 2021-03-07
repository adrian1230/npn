import spacy as sp
from bake import *
from operator import itemgetter

nlp = sp.load('en_core_web_sm')

# get the preprocessed data from the bake file
data = output()

# standard stop words
stops = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
    'you', "you're", "you've", "you'll", "you'd", 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
    'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its',
    'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
    'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
    'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
    'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain',
    'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',
    "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't",
    'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn',
    "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
]

# core stop words
left = [
    "we","he","she","it","I","they","us","them","themselves",
    "yourself","you","yourselves","herself","himself","itself","outselves"
]

test = [
    "The other driver of course has been the optimization of our merchandising activities, and the resulting impact on gross profit margin.",
    "Building on the S2 flow cell, the new S4 flow cell enables a lower price per sample compared to HiSeq X for customers in our highest tiers of utilization and is therefore ideally suited for high-intensity sequencing applications.",
    "So, I guess the verdict on where the cross border trend is, it's definitely stabilized and is improving.",
    "More importantly, we are substantially enhancing our capabilities through four acquisitions, new strategic partnerships and significant renewals of longstanding relationships with several key renewals and new deals to be executed in the fourth quarter.",
    "Is it actually better than it was before?",
    "So far this is a very productive dialogue, and we will keep you updated as our requirements are finalized.",
    "In new B2B payment flows, we're gearing up to launch B2B Connect in the coming weeks, which is our cross border supplier payments platform designed to simplify international B2B transactions through the use of a distributed ledger."
]

charge = "$%"

punct = ",.'!@#$%^&*()_-+=~`?/:;{}[]<>"

def extract(point):
    for d, u in enumerate(point):
        # if the length of the sentence is too short, then it must be meaningless.
        if len(u) >= 5:
            net = nlp(u)
            for n in net:
                print(n,n.pos_,n.tag_,n.dep_)
            splited = u.split(' ')
            # delete the punctuations in the splited sentence
            for r in range(len(splited)):
                for f in punct:
                    splited[r] = splited[r].split(f)
                    splited[r] = ''.join(splited[r])
            script = nlp(u)
            subj, verb, obej, adv, adj = [], [], [], [], []
            # check the nature of pos and dep tags and apply the words into different categories
            for j in range(len(script)):
                if script[j].dep_ == "xcomp" or script[j].dep_ == "ROOT" or script[j].dep_ == "ccomp" or script[j].dep_ == "pcomp" or script[j].dep_ == "aux" or script[j].dep_ == "auxpass" or script[j].dep_ == "neg":
                    verb.append(script[j].text)
                elif script[j].dep_ == "nsubj" or script[j].dep_ == "nsubjpass":
                    subj.append(script[j].text)
                elif script[j].dep_ == "pobj" or script[j].dep_ == "dobj" or script[j].dep_ == "quantmod" or script[j].dep_ == "nummod":
                    obej.append(script[j].text)
                elif script[j].dep_ == "amod" or script[j].dep_ == "acomp":
                    adj.append((script[j].text))
                elif script[j].dep_ == "advmod" or script[j].dep_ == "advcl":
                    adv.append((script[j].text))
                # elif script[j].dep_ == "ROOT":
                #     obej.append(script[j].text)
                elif script[j].dep_ == "conj":
                    if script[j].pos_ == "PRON" or script[j].pos_ == "PROPN" or script[j].pos_ == "NOUN":
                        subj.append(script[j].text)
                    elif script[j].pos_ == "ADJ":
                        adj.append(script[j].text)
                    elif script[j].pos_ == "VERB":
                        verb.append(script[j].text)
                    else:
                        pass
                elif script[j].dep_ == "relcl":
                    if script[j].pos_ == "VERB":
                        verb.append(script[j].text)
                    else:
                        pass
                elif script[j].dep_ == "compound":
                    if script[j].pos_ == "NOUN":
                        subj.append(script[j].text)
                    elif script[j].pos_ == "PROPN":
                        obej.append(script[j].text)
                    elif script[j].pos_ == "NUM":
                        obej.append(script[j].text)
                    else:
                        pass
                else:
                    pass
            # adverbs go with verbs
            for q in range(len(adv)):
                verb.append(adv[q])
            print(obej)
            print(verb)
            # a meaningfull sentence can go without either subject or object
            if len(verb) == 0:
                pass
            if len(verb) != 0:
                if len(obej) > 0:
                    tup = []
                    reconstructed = []
                    # calculate the distance between the target adjectives and other words
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
                    # remove duplicate and rearrange from min to max distance
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
                                    pos_.append(j)
                                    dis_.append(abs(tup[g][2] - tup[j][1]))
                                else:
                                    pos_.append(j)
                                    dis_.append(abs(tup[g][1] - tup[j][2]))
                            min_ = dis_.index(min(dis_))
                            destination = tup[pos_[min_]]
                            # arrange the adjectives to either subject or object
                            if destination[0] in subj:
                                subj.append(tup[g][0])
                            elif destination[0] in obej:
                                obej.append(tup[g][0])
                        g += 1
                    adj = None
                    adv = None
                    subj = list(set(subj))
                    print(u, '\n')
                    # check if the subject, verb, or object contains stop words
                    for h in range(len(splited)):
                        if splited[h] in subj:
                            reconstructed.append(splited[h])
                        elif splited[h] in verb:
                            reconstructed.append(splited[h])
                        elif splited[h] in obej:
                            reconstructed.append(splited[h])
                        else:
                            pass
                    formulated = ' '.join(reconstructed)
                    doc = nlp(formulated)
                    print(formulated,'\n')
                    refined = []
                    for i in doc:
                        if i.pos_ != "AUX": 
                            if i.dep_ != "aux":
                                refined.append(i.text)
                                print(i,'=>',i.pos_,'=>',i.tag_,'=>',i.dep_)
                    print('\n')
                    refined = ' '.join(refined)
                    print(refined,'\n')
            print("################")
# extract(test[:-1])

extract(data[59:80])

