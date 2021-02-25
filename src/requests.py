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

data = data.split(loc)[1].split('\n')[0][4:]

e, q = [], []

for i in range(len(data)):
    if data[i] == "!":
        e.append(i)
    elif data[i] == "?":
        q.append(i)
    else:
        pass

print(e)
print(q)

# I love chicken wings! But I was too fat. How can I stop eating them?
# ,..!,? => 4