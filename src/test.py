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

conn.request("GET", "/extract?url=https://www.quantamagazine.org/plant-cells-of-different-species-can-swap-organelles-20210120/", headers=headers)
res = conn.getresponse()
data = res.read()
data = data.decode("utf-8")
loc = data[data.find("article"):data.find("article")+len('article')]
data = data.split(loc)[1].split('\n')[0][4:].split('.')
print(data)