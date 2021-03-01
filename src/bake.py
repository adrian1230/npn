import pickle as pk

open_ = open('./ohy.pickle','rb')
load_ = pk.load(open_)
open_.close()

def get(text):
    txt = text
    if type(txt) == str:
        if '!' in txt:
            txt = txt.split('!')
    if type(txt) == str:
        if '?' in txt:
            txt = txt.split('?')
    if type(txt) == str:
        if '.' in txt:
            txt = txt.split('.')
    if type(txt) == str:
        return [txt]
    if len(txt) > 1:
        punc = "?!."
        logger = []
        c = 0
        marked = []
        while c != len(txt):
            sentence = txt[c]
            chunk = []
            for g in range(len(sentence)):
                if sentence[g] in punc:
                    chunk.append(g)
            marked.append(chunk)
            c += 1
        c = 0
        while c != len(marked):
            if len(marked[c]) == 0:
                logger.append(txt[c].strip())
            if len(marked[c]) > 0:
                for f in range(len(marked[c])):
                    if f == 0:
                        logger.append(txt[c][:marked[c][f]+1].strip())
                    elif f == (len(marked[c])-1):
                        logger.append(txt[c][marked[c][f-1]+1:marked[c][f]+1].strip())
            c += 1
        return logger

stack = []

for t in range(len(load_)):
    doc = load_[t][0]
    inp = get(doc)
    for g in range(len(inp)):
        stack.append(inp[g])

def output():
    return stack