#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
#read file paper.csv
paper=pd.read_csv('paper.csv')
p_paper = pd.DataFrame(columns=['title','authors','publication_date','description','cite_by'])
rows = 0
#normalize to 1NF 
for index, row in paper.iterrows():
    for token in str(row['authors']).split(','):
        p_paper.loc[rows]=[row['title'],token,row['publication_date'],row['description'],row['cite_by']]
        rows +=1
#save file as csv
p_paper.to_csv('paper_1NF.csv')

