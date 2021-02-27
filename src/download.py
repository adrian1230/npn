import os
from dotenv import load_dotenv
import http.client
import re
import spacy as sp

load_dotenv()

nlp = sp.load('en_core_web_sm')

id = os.getenv('appId')

conn = http.client.HTTPSConnection("aylien-text.p.rapidapi.com")

headers = {
    'x-rapidapi-key': id,
    'x-rapidapi-host': "aylien-text.p.rapidapi.com"
}

stack = []

def get(link):
    conn.request("GET", "/extract?url={}".format(link), headers=headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    loc = data[data.find("article"):data.find("article")+len('article')]
    data = data.split(loc)[1].split('\n')[0][4:].split('.')
    note = []
    for t in range(len(data)):
        e, q = [], []
        for y in range(len(data[t])):
            if data[t][y] == '!':
                e.append(y)
            elif data[t][y] == '?':
                q.append(y)
            else:
                pass
        note.append([e,q])

    entire = []

    for c in range(len(note)):
        if len(note[c][0]) == 0 and len(note[c][1]) == 0:
            entire.append(data[c])
        if len(note[c][0]) != 0:
            for f in range(len(note[c][0])):
                line = data[c].split(data[c][note[c][0][f]])
                for b in range(len(line)):
                    entire.append(line[b])
        elif len(note[c][1]) != 0:
            for f in range(len(note[c][1])):
                line = data[c].split(data[c][note[c][1][f]])
                for b in range(len(line)):
                    entire.append(line[b])
        elif len(note[c][0]) != 0 and len(note[c][1]) != 0:
            for f in range(len(note[c][0])):
                line = data[c].split(data[c][note[c][0][f]])
                for b in range(len(line)):
                    entire.append(line[b])
            for f in range(len(note[c][1])):
                line = data[c].split(data[c][note[c][1][f]])
                for b in range(len(line)):
                    entire.append(line[b])
        else:
            pass

    return entire

# 'https://www.quantamagazine.org/plant-cells-of-different-species-can-swap-organelles-20210120/',
# 'https://medium.com/sexposblog/good-vibes-130e2eba4cd2'

links = []

print("input link(s) if input.lower() == 'stop': break\n")

while True:
    intake = input("link => ")
    if intake.lower() == "stop":
        break
    links.append(intake)

def sep(sources):
    c = 0
    while c != len(sources):
        pack = get(sources[c])
        for x in range(len(pack)):
            stack.append(pack[x])
        c += 1
    return stack
        
out = sep(links)
