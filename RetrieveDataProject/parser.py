import ast
import os

import pandas as pd
import ast_scope
import sqlite3


def extract_variables_and_functions_naive(file_path, author_type):
    try:
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read(), filename=file_path)
    except:
        # If a syntax error occurs, print the error message
        print(f"Syntax error in file '{file_path}'")
        raise
    scope_info = ast_scope.annotate(tree)
    names = []
    # todo: need nested scope number: recursion on tree/push stack on
    # todo: function parameter, classDef, other?
    # todo: detect author
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            nameScope = "GlobalScope" if isinstance(scope_info[node], ast_scope.scope.GlobalScope) else "FunctionScope"
            name = {"name": node.name, "nameType": "function", "nameScope": nameScope,
                    "author": author_type}
            names.append(name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    nameScope = "GlobalScope" if isinstance(scope_info[target],
                                                            ast_scope.scope.GlobalScope) else "FunctionScope"
                    name = {"name": target.id, "nameType": "variable", "nameScope": nameScope,
                            "author": author_type}
                    names.append(name)
        elif isinstance(node, ast.ClassDef):
            nameScope = "GlobalScope" if isinstance(scope_info[node], ast_scope.scope.GlobalScope) else "FunctionScope"
            name = {"name": node.name, "nameType": "class", "nameScope": nameScope,
                    "author": author_type}
            names.append(name)
    # Now write the result to pandas dataframe
    names_df = pd.DataFrame.from_records(names)
    return names_df


conn = sqlite3.connect('data.db')
# I remember Open is relative path to the running directory, so need to call this script at this dir.
chinese_py_file_dir = 'PyFiles/ChineseProjectPyFile/'
files = os.listdir(chinese_py_file_dir)
for filename in files:
    # Construct the full file path
    file_path = os.path.join(chinese_py_file_dir, filename)
    try:
        names_df = extract_variables_and_functions_naive(file_path, author_type='Chinese')
        names_df.to_sql('ChineseVariableTable', conn, if_exists='append', index=False)
    except:
        continue

chinese_py_file_dir = 'PyFiles/EnglishProjectPyFile/'
files = os.listdir(chinese_py_file_dir)
for filename in files:
    # Construct the full file path
    file_path = os.path.join(chinese_py_file_dir, filename)
    try:
        names_df = extract_variables_and_functions_naive(file_path, author_type='English')
        names_df.to_sql('EnglishVariableTable', conn, if_exists='append', index=False)
    except:
        continue

