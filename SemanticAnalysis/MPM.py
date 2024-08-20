#!/usr/bin/env python
# coding: utf-8

# # Description
# In this Notebook, we will try to parse each names into dependency trees, and try to identify who ismodifier and who is modified. Then we will conclude that the percentage of use of MPM structure. 

# # Read data
# In order to save time, we will only load some part of the data. 

# In[43]:


import pandas as pd
import sqlite3
name_table = "NameTable"
conn = sqlite3.connect('../ZipfLawAnalysis/data.db')
query = f"""SELECT *
FROM (
    SELECT *
    FROM {name_table}
    WHERE authorLocation = 'China'
    ORDER BY RANDOM()
    LIMIT 100000
) AS Chinese_sample
UNION ALL
SELECT *
FROM (
    SELECT *
    FROM {name_table}
    WHERE authorLocation = 'USA'
    ORDER BY RANDOM()
    LIMIT 100000
) AS USA_sample;"""
# takes 10 second to run 100k
df = pd.read_sql_query(query, conn)
import json
df['terms'] = df.terms.apply(json.loads)
df


# For now convert abbreviation on the fly. There is a lot of problem regarding abbreviations, and I am just putting it off for now. Assume that the abbreviation map will map names to the correct names. 

# In[44]:


abbrev_table = "AbbreviationMap"
query = f"SELECT * FROM {abbrev_table}"
df_abbrev_map = pd.read_sql_query(query, conn)

# I will use a better dictionary: ENABLE (Enhanced North American Benchmark Lexicon)
with open('../ZipfLawAnalysis/SavedFiles/atebits.txt', 'r') as file:
    words = file.read().splitlines()
english_dictionary =  set(words)

# the dictionary that maps abbreviation back to original words
abbrev_map = dict(zip(df_abbrev_map['term'], df_abbrev_map['abbrev_meaning']))
# because the confidence of preicting single letter is too low, I would give up all the single letters
# also there are ones that ChatGPT cannot recognize, generally too wierd ones, so I will get rid of those too. (277 of them)
# also there are about 20k duplicates due to capitalization, here we will combine them together first. ???
filtered_abbrev_map = {k: v for k, v in abbrev_map.items() if v != '-1'}

# function that checks if it's a real word
def lookup_terms(term):
    return term.lower() in english_dictionary

def map_terms_to_actual_terms(terms):
    # if it's dictionary word, it will not be in the dictionary, or it might be something that GPT cannot guess. 
    # either way, the original terms will be in the list. Else, the translated terms will be in the list.
    return [filtered_abbrev_map.get(term, term) for term in terms]

df['actual_terms'] = df['terms'].apply(map_terms_to_actual_terms)   

temp = df['terms'].apply('_'.join).str.lower()
df['standarized_name'] = temp

temp = df['actual_terms'].apply('_'.join).str.lower().str.replace(" ", "_")
df['atual_standarized_name'] = temp

# we use atual_standarized_name to define actual_terms so that we can get rid of the space
# sometimes pd will return view of df not the actual df, depends on the RAM
df = df.copy()
df['actual_terms'] = df['atual_standarized_name'].apply(lambda x: x.split('_'))


# In[45]:


df


# # Dependency Parsing
# ## Example

# In[46]:


# !pip install spacy
# !python -m spacy download en
import spacy

# Load the English NLP model
nlp = spacy.load('en_core_web_sm')


# In[54]:


# Example: Process a sentence
doc = nlp("list comp message")

# Print the dependency parsing results
for token in doc:
    print(f'{token.text:{10}}{token.i:{10}} {token.dep_:{10}} {token.head.text:{10}} {token.head.i:{10}}')


# In[49]:


from spacy import displacy
displacy.render(doc, style="dep", page="true")


# ## perform on names

# In[50]:


df_phrase = df[df["actual_terms"].str.len() > 2].copy()
df_phrase["phrase"] = df_phrase["actual_terms"].apply(" ".join)
df_phrase


# In[51]:


modifiers = {'AMOD', 'ADVCL', 'ACL', 'ADVMOD', 'APPOS', 'COMPOUND', 'META', 'NEG', 'NPMOD', 'POSS', 'PREP', 'RELCL', 'POBJ'}
def count_MPM(phrase):
    '''
    This function will count number of MPM in the phrase, and number of non MPM. Used for df.apply()
    Why do we count it? 
    1. Some phrases doesn't have a MPM structure: evaluate_data
    2. Some phrases have some MPM and some not: starting_time_of_frame
    '''
    num_mpm, num_not_mpm = 0, 0
    doc = nlp(phrase)
    for token in doc:
        if token.dep_.upper() in modifiers:
            if token.i < token.head.i:
                num_mpm += 1
            else:
                num_not_mpm += 1
    return num_mpm, num_not_mpm

temp = df_phrase["phrase"].apply(count_MPM)


# In[52]:


df_phrase[["num_MPM", "num_not_MPM"]] = pd.DataFrame(temp.to_list(), columns=["num_MPM", "num_not_MPM"])
df_phrase


# In[ ]:




