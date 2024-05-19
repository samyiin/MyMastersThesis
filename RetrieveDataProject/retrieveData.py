"""
This script is used for retrieving repositories. it depends on githubAPI.py
In order for githubAPI to run, the executing directory must be the same as the githubAPI.py
"""
"""
After a failed attempt, I decided that I will retrieve data in the following way: There are two aspects we need to balance:
number of programmers with different “proficiency”, measured by number of repositories they have
number of repositories with each size: to make sure that number of variables between chinese programmers and american programmers are similar
One thing will be too hard to balance: the number of small/big size repositories written by non-proficient/proficient programmer, for now we will ignore it.
"""
from githubAPI import search_for_user, search_for_repository
import pandas as pd
import time
def find_users_and_repos(location, use_cache=True):
    """
    The function might seem nested, but the general idea is, for each proficiency level (the first for loop),
    we will find about 100 users that have repos of size > 3Mb (the while loop), we won't stop until we find 100.
    :param location: China or USA
    :return:
    """
    list_df_final_users = []
    list_df_final_repos = []
    for proficiency_level in ['<50', '50..100', '>100']:
        dic_user_constraint = {'location': location, 'repos': proficiency_level, "language": 'Python', "type": 'user'}
        page_num = 1
        user_number = 0
        while user_number < 100:
            # first get all the users that satisfies constraints for users
            df_users = search_for_user(dic_constraint=dic_user_constraint, page_num=page_num)
            df_users['userProficiency'] = proficiency_level
            df_users['location'] = location
            list_df_final_users.append(df_users)
            # filter out users who do not have repo size > 3Mb
            list_df_repos = []
            for user_login in df_users['login']:
                dic_repo_constraint = {"user": user_login, 'language': 'Python', 'size': '>3000'}
                df_user_repos = search_for_repository(dic_constraint=dic_repo_constraint)
                if df_user_repos is not None:
                    df_user_repos['author'] = user_login
                    list_df_repos.append(df_user_repos)
            df_repos = pd.concat(list_df_repos, ignore_index=True)
            list_df_final_repos.append(df_repos)
            # see how many users are left
            user_number += df_repos['author'].unique().size
            # if we don't yet have enough users, we will continue this process
            page_num += 1
            if not use_cache:
                # for the rate limit
                time.sleep(20)
            # if we can't find any more users, we will break too
            if df_users.shape[0] < 100:
                print("ran out of users")
                break
    df_final_repos = pd.concat(list_df_final_repos, ignore_index=True)
    df_final_users = pd.concat(list_df_final_users, ignore_index=True)
    # now we take information we want
    df_final_repos = df_final_repos[['name', 'full_name', 'owner', 'git_url', 'clone_url', 'size', 'language', 'author']]
    df_final_users = df_final_users[['login', 'url', 'userProficiency', 'location']]
    # and we just need to keep final repos
    df_final_repos = pd.merge(df_final_repos, df_final_users, how='inner', left_on='author', right_on='login')
    return df_final_repos

"""
First of all, for each proficiency group: we will select 100 american programmers that have at least one repository
bigger than 3Mb. Then we will see the distribution of the size of the repositories
"""
df_repos = find_users_and_repos('USA')
df_repos.to_csv('USA_repos.csv', index=False)

"""
Now let's do the same for chinese
"""
df_repos = find_users_and_repos('China')
df_repos.to_csv('Chinese_repos.csv', index=False)

