"""
One basic analysis is the length of the name. Length by letter, length by word, length of each word,
Then also: cleaned: get rid of some things?
Naturally grouped by author, And then group by Scope, Type
"""
import pickle
import re

import pandas as pd
import sqlite3

name_table = "NameTable"
col_name = "name"
col_type = "nameType"
col_scope = "nameScope"
col_author = "author"
# sqlite connect is also relative path relative to the folder running the script.
conn = sqlite3.connect('../RetrieveDataProject/data.db')

query = f"SELECT * FROM {name_table}"
df = pd.read_sql_query(query, conn)

# calculate the length of each variable: length as in number of letters.

length_by_letter = df[col_name].apply(lambda x: len(x.replace('_', '')))
length_by_letter = pd.concat([length_by_letter, df['id']], axis=1)
length_by_letter = length_by_letter.rename(columns={col_name: 'LengthByLetter'})
length_by_letter.to_sql('LengthByLetter', conn, if_exists='replace', index=False)


# identify the naming convention of each variable
def detect_timeframe_convention(name):
    # no need to check .isidentifier() because we extracted them from syntax error free script
    if '_' in name:
        return 'snake_case'
    elif re.search(r'[A-Z][a-z]*', name):
        if name[0].islower():
            return 'camelCase'
        else:
            return 'Pascal'
    else:
        return 'unknown'


naming_convention = df[col_name].apply(lambda x: detect_timeframe_convention(x))
naming_convention = pd.concat([naming_convention, df['id']], axis=1)
naming_convention = naming_convention.rename(columns={col_name: 'NamingConvention'})
# todo: if we add in ton more field: the file name, and then we can see other variables in the same file to determine
#  the type. Also this classification is too simple, what if we have something like "filename", need more scrutiny in
#  this in next iteration. mix.
naming_convention.to_sql('NamingConvention', conn, if_exists='replace', index=False)

# extract the words from the name
query = f"SELECT * FROM {name_table} JOIN NamingConvention ON {name_table}.id = NamingConvention.id;"
df_with_naming_convention = pd.read_sql_query(query, conn)


def extract_names_and_serialize(row):
    if row['NamingConvention'] == 'snake_case' or row['NamingConvention'] == 'unknown':
        words = [word for word in row[col_name].split('_') if word]  # Filtering out empty strings
        number_of_words = len(words)
        pickled_words = pickle.dumps(words)
        return pickled_words, number_of_words
    else:
        # todo: camel or Pascal, for now... maybe later there will be more types
        # todo: this regex doesn't work so well for things like Word2Vec, which is clearly a camel case.
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', row[col_name])
        words = [m.group(0) for m in matches]
        number_of_words = len(words)
        pickled_words = pickle.dumps(words)
        return pickled_words, number_of_words


df_words_count = df_with_naming_convention.apply(extract_names_and_serialize, axis=1)
df_words_count = pd.DataFrame(df_words_count.tolist(), columns=['wordList', 'NumberOfWords'])
df_words_count = pd.concat([df_words_count, df['id']], axis=1)
df_words_count.to_sql('WordCount', conn, if_exists='replace', index=False)

conn.close()
