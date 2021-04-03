import spacy as sp
import pickle as pk

nlp=sp.load('en_core_web_sm')

training = [
]

default_ner = []
new_ner = []
ner = []

for k in range(len(training)):
    doc = nlp(training[k])
    line = []
    print(doc)
    for j in doc.ents:
        print(" ")
        word = j.text
        start = training[k].find(word)
        end = start + len(word)
        label = j.label_
        print(word,label)
        ans = input("Do you agree with the label for {}: Y/y => ".format(word))
        if ans.lower() == 'y':
            group = (start,end,label)
            line.append(group)
    default_ner.append(line)
    print("---------------------------------------")

new_label = []

while True:
    a = input("=> ")
    if a.lower() == "stop":
        break
    new_label.append(a)

for g in range(len(training)):
    split = training[g].split()
    ran = [(training[g].find(kl),training[g].find(kl)+len(kl)) for kl in split]
    mark = []
    for f in range(len(default_ner)):
        if f == g:
            for k in range(len(default_ner[f])):
                for h in range(len(ran)):
                    if default_ner[f][k][0] == ran[h][0]:
                        if default_ner[f][k][1] == ran[h][1]:
                            mark.append(h)
    split = [split[y] for y in range(len(split)) if y not in mark]
    ran = [ran[c] for c in range(len(ran)) if c not in mark]
    print(training[g])
    print(split)
    print(ran)
    print(" ")
    more = []
    while True:
        ranger = input("range of position: like this 3,10 which starts from 3 and ends at 9. => ")
        if ranger == "0,0":
            break
        ranger = ranger.split(',')
        print("what tag do you want for {} from the new label?\n".format(training[g][int(ranger[0]):int(ranger[1])]))
        print("input the index as integer below")
        for w, t in enumerate(new_label):
            print(w, "=>",t)
        ind = int(input("index here: "))
        if ind > w:
            raise ValueError("No this option")
        pack = (int(ranger[0]),int(ranger[1]),new_label[ind])
        more.append(pack)
    new_ner.append(more)
    print("-------------------------------------")

out = []
for z in range(len(default_ner)):
    for s in range(len(new_ner)):
        if z == s:
            if len(default_ner[z]) == 0:
                if len(default_ner[z]) == len(new_ner[s]):
                    out.append(z)

default_ner = [default_ner[v] for v in range(len(default_ner)) if v not in out]
new_ner = [new_ner[g] for g in range(len(new_ner)) if g not in out]
training = [training[d] for d in range(len(training)) if d not in out]

c = 0
while len(ner) != len(default_ner):
    squad = []
    for n in range(len(default_ner[c])):
        squad.append(default_ner[c][n])
    for m in range(len(new_ner[c])):
        squad.append(new_ner[c][m])
    c += 1
    ner.append(squad)

stack = []
u = 0
while len(stack) != len(new_ner):
    txt = training[u]
    dic = {"entities":ner[u]}
    tup = (txt,dic)
    u += 1
    stack.append(tup)

open_file = open('./annotated.pickle', "wb")
pk.dump(stack, open_file)
open_file.close()

open_file = open('./annotated.pickle', "rb")
loaded_list = pk.load(open_file)
open_file.close()

print(loaded_list)
