
# coding: utf-8

# In[12]:

import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from difflib import SequenceMatcher


# In[117]:

train=pd.read_csv('train.csv')
test=pd.read_csv('test.csv')
attributes=pd.read_csv('attributes.csv')


# In[118]:

attributes=attributes.dropna(how='all')
attributes.reset_index(inplace=True)


# In[119]:

Trans_Attr=pd.DataFrame(None,index=attributes.product_uid.unique(),columns=attributes.groupby('name').count().index)


# In[120]:

for i in range(len(attributes)):
    Trans_Attr[attributes.name[i]].loc[attributes.product_uid[i]]=attributes.value[i]



# In[250]:

All=pd.merge(Trans_Attr,train,left_index=True,right_on='product_uid')


# In[248]:

def match(a,b):
    if isinstance(a,basestring)==False:
        return 0
    else:
        return SequenceMatcher(None,a,b).ratio()


# In[275]:

All2=pd.DataFrame(None,columns=All.columns)


# In[293]:

for i in range(1,21):
    All2=All2.append(All.iloc[i].apply(lambda x: match(x,All.search_term.iloc[i])))

print All2.iloc[:,:20]




