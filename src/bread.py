import spacy as sp
from bake import *

nlp = sp.load('en_core_web_sm')

data = output()

package = []

for d, u in enumerate(data):
    script = nlp(u)
    pack = []
    print(u)
    noun = []
    verb = []
    obej = []
    for j in range(len(script)):
        print(script[j].text,"=>",script[j].pos_,"=>",script[j].tag_)
    print("\n")
