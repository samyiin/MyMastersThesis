import shutil
import ast
import os
import pandas as pd
import ast_scope
import fnmatch
# need to install gitpython
import git
import sqlite3

index_counter = 0


def parse_single_file(file_path, dic_add_info):
    """
    This following function will open the python file under parameter "file_path", and parse the file to get variable names and their scope: FunctionScope or GlobalScope.

    :param file_path:
    :param dic_add_info:
    :return:
    """
    global index_counter
    try:
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read(), filename=file_path)
    except:
        # If a syntax error occurs, print the error message
        print(f"Syntax error in file '{file_path}'")
        raise
    scope_info = ast_scope.annotate(tree)
    names = []
    # todo: function parameter, other?
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            nameScope = "GlobalScope" if isinstance(scope_info[node], ast_scope.scope.GlobalScope) else "FunctionScope"
            name = {"id": index_counter, "name": node.name, "nameType": "function", "nameScope": nameScope}
            # add information for the variable
            name.update(dic_add_info)
            names.append(name)
            index_counter += 1
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    nameScope = "GlobalScope" if isinstance(scope_info[target],
                                                            ast_scope.scope.GlobalScope) else "FunctionScope"
                    name = {"id": index_counter, "name": target.id, "nameType": "variable", "nameScope": nameScope}
                    # add information for the variable
                    name.update(dic_add_info)
                    names.append(name)
                    index_counter += 1
        elif isinstance(node, ast.ClassDef):
            nameScope = "GlobalScope" if isinstance(scope_info[node], ast_scope.scope.GlobalScope) else "FunctionScope"
            name = {"id": index_counter, "name": node.name, "nameType": "class", "nameScope": nameScope}
            # add information for the variable
            name.update(dic_add_info)
            names.append(name)
            index_counter += 1
    # Now write the result to pandas dataframe
    names_df = pd.DataFrame.from_records(names)
    return names_df


def parse_single_project(project_path, dic_add_info, db_conn, db_table):
    """
    The following function will walk through a project directory, and open any python files, and parse them.

    :param dic_add_info:
    :param project_path:

    :param db_conn:
    :param db_table:
    :return:
    """
    for foldername, subfolders, filenames in os.walk(project_path):
        for filename in filenames:
            if fnmatch.fnmatch(filename, '*.py'):
                filepath = os.path.join(foldername, filename)
                try:
                    names_df = parse_single_file(filepath, dic_add_info)
                    names_df.to_sql(db_table, db_conn, if_exists='append', index=False)
                except:
                    continue


def pd_apply_parse_project(row):
    """
    Iterating through pandas rows, each row should be a project, and we will parse every python file in the project
    :param row:
    :return:
    """
    repo_url = row['clone_url']
    dic_add_info = {'projectSize': row['size'], 'authorName': row['author'],
                    'authorProficiency': row['userProficiency'], 'authorLocation': row['location']}
    # create the directory for project to clone to
    target_dir = 'TempDownload/'
    os.mkdir(target_dir)
    # download the project
    git.Repo.clone_from(repo_url, target_dir)
    # project path is always the same because we clone to the same directory
    parse_single_project(project_path=target_dir, dic_add_info=dic_add_info, db_conn=conn, db_table=table)
    # delete everything under the directory
    shutil.rmtree(target_dir)
    # print progress
    global progress_counter
    print(f"progress: {progress_counter} out of {total_steps}")
    progress_counter += 1
    return row


conn = sqlite3.connect('data.db')
table = 'NameTable'
# Create a cursor object
cursor = conn.cursor()

# SQL statement to drop the table
sql_statement = f"DROP TABLE IF EXISTS {table}"
cursor.execute(sql_statement)
conn.commit()
# if the tempDownload directory exist, then we delete it
if os.path.exists('TempDownload/'):
    shutil.rmtree('TempDownload/')

df_chinese_repos = pd.read_csv("../RetrieveDataProject/Chinese_trim_repos.csv")
df_american_repos = pd.read_csv('../RetrieveDataProject/USA_trim_repos.csv')

# recorde progress
progress_counter = 1
total_steps = df_chinese_repos.shape[0] + df_american_repos.shape[0]

df_chinese_repos.apply(pd_apply_parse_project, axis=1)
df_american_repos.apply(pd_apply_parse_project, axis=1)

# 2025.05.18: final run time: about 2.5 hours
