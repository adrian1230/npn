import http.client

conn = http.client.HTTPSConnection("aylien-text.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "8810a1c805msh80237adbb2df873p1b6680jsnfdd7df955b97",
    'x-rapidapi-host': "aylien-text.p.rapidapi.com"
    }

conn.request("GET", "/extract?url=https://medium.com/sexposblog/good-vibes-130e2eba4cd2", headers=headers)

res = conn.getresponse()
data = res.read()

data = data.decode("utf-8")

loc = data[data.find("article"):data.find("article")+len('article')]

data = data.split(loc)[1].split('\n')[0][4:].split('.')

others = []

main = []

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

print(note)

for p in range(len(data)):
    for q in data[p]:
        if q == "!" or q == "?":
            others.append(data[p])
        else:
            main.append(data[p])

modified = []

for w in range(len(others)):
    if '!' in others[w]:
        sentences = others[w].split('!')
        modified += sentences
    elif '?' in others[w]:
        sentences = others[w].split('?')
        modified += sentences
    else:
        modified += others[w]

entire = modified + main

# print(main)
# for e in range(len(main)):
#     entire.append(main[e])

# for r in range(len(modified)):
#     entire.append(modified[r])

