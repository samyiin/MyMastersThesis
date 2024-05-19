"""
Github have api, so this saves us time to write a web crawler
Github API allows search by repository (size, stars, language, ...)
Github API also allows search by user (location, language, ....)
Beside from search, there are other endpoints, need to read the documentation, or just ask ChatGPT
Regarding the access token: You can use the classic github access token, but then you need to authenticate it before
use. Else you can use a "fine grained" token.

We will cache the function call
"""

import requests
import pandas as pd
import joblib

# cache function calls
memory = joblib.Memory(location='cacheGithubCall', verbose=1)


def make_github_request(url):
    """
    request through github's rest API, here are the website
    https://docs.github.com/en/rest?apiVersion=2022-11-28
    :param url:
    :return:
    """
    YOUR_ACCESS_TOKEN = read_access_token()
    # Replace 'YOUR_ACCESS_TOKEN' with your actual GitHub personal access token
    headers = {'Authorization': f'Bearer {YOUR_ACCESS_TOKEN}',
               "X-GitHub-Api-Version": "2022-11-28"}
    # Make a GET request to the rate limit endpoint
    response = requests.get(url, headers=headers)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the remaining rate limit details
        res = response.json()
        return res
    else:
        # If the request was not successful, print the error status code
        print(f"Error: {response.status_code}")
        return None


def read_access_token(file_path="githubAPIToken"):
    """
    Put your access token in an empty file named: githubAPIToken under the same directory of this file (Assume running
    this script from the same directory where it located
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as file:
        access_token = file.read().strip()
    return access_token


def construct_search_query(dic_search_query):
    """
    The dictionary should consist of type of constraint and the constraint, both in string format
    :param dic_search_query:
    :return:
    """
    constraints = []
    for k, v in dic_search_query.items():
        if v is None:
            continue
        constraints.append(k.strip() + ":" + v.strip())
    query = "+".join(constraints)
    return query


def check_rate_limit():
    """
    This function will check the rate limit left for me
    :return:
    """
    url = 'https://api.github.com/rate_limit'
    res = make_github_request(url)
    if res is not None:
        df = pd.DataFrame.from_dict(res['resources'], orient='index')
        print(df)


@memory.cache
def search_for_user(dic_constraint, page_num, per_page=100):
    """
    This will be a wrapped api for github api search users: the options are here:
    https://docs.github.com/en/search-github/searching-on-github/searching-users
    The above link also specifies what are the options for constraints, an example would be:
    dic_constraint = {"type": user_type, "repos": repos, "location": location, "language": language}
    (even when they are number)
    :param per_page: number of result per search (each time returns a "page")
    :param page_num: the page number we want
    :param dic_constraint: the constraints for searching for user
    :param num: number of result we want

    :return: the search results
    """
    # construct query
    query = construct_search_query(dic_constraint)
    res = make_github_request(f'https://api.github.com/search/users?q={query}&per_page=100&page={page_num}')
    if res is None:
        return None
    # return the result in pandas format
    df_users = pd.DataFrame(res["items"])
    return df_users


@memory.cache
def search_for_repository(dic_constraint):
    """
    This is wrapped up api for searching repository in github
    https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories
    :param dic_constraint: again, dic_constraint is as described above
    :return: the result of request in dataframe
    """
    # construct query
    query = construct_search_query(dic_constraint)

    # we assume that there is no more than 100 repositories, this will not include fork repositories
    url = f'https://api.github.com/search/repositories?q={query}'
    res = make_github_request(url)
    # if there is no such repository, we will ignore the case
    if res is None:
        return None
    df_repos = pd.DataFrame(res["items"])
    return df_repos

# check_rate_limit()
# make_github_request('https://api.github.com/users/tan-xu/repos')
