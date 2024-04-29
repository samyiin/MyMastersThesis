import pandas as pd
import sqlite3

name_table = "NameTable"
col_name = "name"
col_type = "nameType"
col_scope = "nameScope"
col_author = "author"

length_by_letter_table = 'LengthByLetter'
col_length_by_letter = 'LengthByLetter'

length_by_word_table = 'WordCount'
col_word_list = 'wordList'
col_number_of_words = 'NumberOfWords'

naming_convention_table = 'NamingConvention'
col_naming_convention = 'NamingConvention'



conn = sqlite3.connect('../RetrieveDataProject/data.db')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to get the mean of a column
cursor.execute(f"""
SELECT AVG({col_length_by_letter}), AVG({col_number_of_words}) FROM (
SELECT *
FROM {name_table}
JOIN {length_by_letter_table} ON {name_table}.id = {length_by_letter_table}.id
JOIN {length_by_word_table} ON {name_table}.id = {length_by_word_table}.id)
where {col_author} == 'Chinese'
""")

# Fetch the result
mean = cursor.fetchone()
print(mean)

# Execute a query to get the mean of a column
cursor.execute(f"""
SELECT AVG({col_length_by_letter}), AVG({col_number_of_words}) FROM (
SELECT *
FROM {name_table}
JOIN {length_by_letter_table} ON {name_table}.id = {length_by_letter_table}.id
JOIN {length_by_word_table} ON {name_table}.id = {length_by_word_table}.id)
where {col_author} == 'English'
""")

# Fetch the result
mean = cursor.fetchone()
print(mean)


# Close the connection
conn.close()

