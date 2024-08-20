# Description
My master thesis aims to answer one question: would Chinese programmer give different variable names and function names than American speakers? I am planning to tackle the problem from two main directions:
1. I will gather code from github, that is written by Chinese programmers and American programmers, and perform analysis on them.
2. I will try to come up with question that can show that under certain circumstances Chinese programmers will give different names.
And then after all that I will perform causal inference on the result, to show that there is a causal relation between being a Chinese programmer and giving variable names. Because there have been many other factors that might affect the way programmers gives variable names. 

# Github Code Analysis

## RetrieveDataProject
In this project, I filtered and pulled a lot of github reositories from both Chinese and English speakers. Regarding how do I decide which repos are written by Americans and which are by Chinese, please see the description in the directory. I also tried to make sure that the data I pulled are balanced, in terms of the popularity of repo and the size of repo, I anallyzed the conposition of the repositories in the end to show that the data are balanced. (Should I randomlly pull repos instead?)

## ZipfLawAnalysis
In the project, I parsed all the codes to get all the variable/function/class names, and then I tried to verify if ZipfLaw appear in programming languages. I checked the following cases: 
1. Original variable names 
2. Take the variable names and split them into terms (Actual English words or Abbreviations)
3. Transform all the abbreviations back to actual English words
4. Tokenize all the Englsih words, get rid of plural and tenses
[Progress: I am struggling on interpreting abbreviations. So far the most promising ways are LLMs, but there are still some problems I need to solve in order to increase the accuracy.]
[todo: re-order the files according to this logic.]

## SemanticAnalysis
There are some fundamental differences between Chinese (natural) language and English language. The point of this project is trying to check if such differences exist in programming languages. In order to achieve such goal, we need to first understand what are the differences between Chinese and Englsih. In order to do that, we need to understand some linguistics. I am planning to consult some linguists regarding this. There are some differences I already spot: 
1. The MPM (modifier preceeds modified) structure. (Head finality) [todo: delete the MPM.py]
2. The lack of plural in nouns and lack of tenses in verbs.
But I still need some time to read more about it and consult my linguist friends.
[Progress: I have analyzed the distributional difference from the MPM, the single/plural, and tense aspect. I need to explore more aspects until a certain point when I feel like it's comprehensive. Also solving the abbreviation problem will increase the reliabililty of the results in this analysis.]

# Suvey
## WarmupProject
In this project, me and Dalia formulated some programming questions, and hand out the surveys to Chinese and American speakers repectively. Then we analyze the results and found that there is no significant difference between coding proficiency and language groups. The detail of how we formulated the questions and how we evaluate the coding proficiency are written under the directory. 

## Actual Survey
I am going to wait until I see the results from Github Code Review. Then I can decide which angle I am going to "attack". 

# Causal Inferences
I am waiting until I finish GithubAnalysis, and then I will schedule a meeting with amir to discuss about the design of surveys and performing causal inferences on existing data. 
