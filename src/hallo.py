import pandas as pd

df = pd.ExcelFile('./testCorpus.xlsx')
df32 = pd.read_excel(df,'32').iloc[:,1:]
df33 = pd.read_excel(df,'33').iloc[:,1:]
df34 = pd.read_excel(df,'34').iloc[:,1:]
df173 = pd.read_excel(df,'173').iloc[:,1:]
df174 = pd.read_excel(df,'174').iloc[:,1:]

df = df32[
         'header'
     ].tolist() + df33[
    'header'].tolist() + df34[
    'header'].tolist() + df173[
    'header'].tolist() + df174['header'].tolist()

def listlist():
    jojo = []
    for i in range(len(df)):
        se = df[i].split('"')[1]
        jojo.append(se)
    return jojo