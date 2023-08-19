"""
This script works only for the specific result we get from typeform, doesn't have much extendability because of all the
function names.
"""
from toolbox import *


# =====================================================================================================================
# =========================================delete unwanted rows========================================================
# =====================================================================================================================
def clean_up_df(graded_result_df):
    graded_result_df = graded_result_df.apply(_english_speaker_default, axis=1)
    # graded_result_df = graded_result_df.dropna()
    return graded_result_df


def _english_speaker_default(row):
    if row["What is your native language?"] == "English":
        row["How would you rate your English proficiency?"] = 5
        row["How many hours per day do you spend speaking English?"] = 10
        row["Can you watch TV in English without subtitles?"] = 1.0
        row["How often do you use variable names transcribed from your language while coding?"] = 1
    return row


def globally_normalize_scores(graded_result_df, col_name):
    # high = graded_result_df[col_name].max()
    # low = graded_result_df[col_name].min()
    # graded_result_df[col_name] = (graded_result_df[col_name] - low) / (high - low)
    return graded_result_df


# =====================================================================================================================
# =========================================default coding proficiency scoring==========================================
# =====================================================================================================================
def add_code_proficiency_score(graded_result_df):
    for question_type in [Q_TYPE_ALL, Q_TYPE_FULL, Q_TYPE_ABRIV, Q_TYPE_NONE]:
        graded_result_df = default_scoring_standard(graded_result_df, question_type)
    return graded_result_df


def default_scoring_standard(graded_result_df, question_type):
    # normalize score: special normalize: for not confident users
    graded_result_df = graded_result_df.apply(_normalize_grades, axis=1)

    # type 1: self-subjective-assess: locally normalize to [0,1]
    self_subjective_assess_score = graded_result_df["How would you rate your coding proficiency?"] / 5
    # type 2: self-objective-assess: locally normalize to [0, 1]
    graded_result_df = graded_result_df.apply(_default_coding_background_scoring_standard, axis=1)
    self_objective_assess_score = graded_result_df["coding_background_score"]
    # type 3: objective-assess: locally normalize to [0, 1]
    graded_result_df = graded_result_df.apply(_default_code_scoring_standard, question_type=question_type, axis=1)
    objective_assess_score = graded_result_df[f"code_score({question_type})"]
    # we can't know if background score is more important or code test is more important, so use unweighted average
    graded_result_df[f"coding_proficiency({question_type})"] = (
                                                                           objective_assess_score + self_objective_assess_score + self_subjective_assess_score) / 3
    # globally normalize the score, in case everyone get low/high grade
    graded_result_df = globally_normalize_scores(graded_result_df, f"coding_proficiency({question_type})")
    return graded_result_df


def _default_code_scoring_standard(row, question_type=Q_TYPE_ALL):
    """
        This is a callback func for pandas apply
        The naive grading standard:
        for each of the six questions: if correct 1, else 0.
        for each of the six self-examination: it's from 1 to 5
        then the score of a person is determined by
        for each question:
            sum(binary_correct * self_examination_score)
        """
    # checking if he has basic knowledge - 1
    check_basics_1 = 1 if row["Which of the following is a Boolean?"] == "TRUE" else 0
    # checking if he has basic knowledge - 2
    check_basics_2 = 1 if row["Which website do you use for coding help?"] == "StackOverflow" else 0
    total_grade = check_basics_1 + check_basics_2
    # check coding questions
    if question_type == Q_TYPE_FULL:
        iter_range = [1, 4]
    elif question_type == Q_TYPE_ABRIV:
        iter_range = [2, 5]
    elif question_type == Q_TYPE_NONE:
        iter_range = [3, 6]
    else:
        iter_range = range(1, 7)
    for i in iter_range:
        code_grade = row[f"q{i} graded"]
        # since 1 is easiest 5 is hardest, and we think those who says it's easy will be better, so we will use 6 - i
        self_assess = (6 - row[f"{i}. How easy was this code to understand?"]) / 5
        # normalize: one question is one point - locally normalize: don't know importance
        total_grade += (code_grade * self_assess)
    # normalize: locally: because this is one category of assessment, and we don't know the importance of each category
    row[f"code_score({question_type})"] = total_grade / 8
    return row


def _normalize_grades(row):
    """
    This is a callback func for pandas apply
    :param row: a row of the graded_result_df
    :return:
    """
    all_score = [row[f"{i}. How easy was this code to understand?"] for i in range(1, 7)]
    lowest = min(all_score)
    highest = max(all_score)
    if highest == lowest:
        normalized_score = [3 for i in range(6)]
    else:
        normalized_score = [int(((i - lowest) / (highest - lowest)) * 4 + 1) for i in all_score]
    for i in range(1, 7):
        row[f"{i}. How easy was this code to understand?"] = normalized_score[i - 1]
    return row


def _default_coding_background_scoring_standard(row):
    # assessing years
    user_answer = row["How many years have you worked coding (not including higher education)"]
    map_answer_to_score = {"0-1": 1 / 4, "2-5": 2 / 4, "5-10": 3 / 4, "10+": 1}
    working_years = map_answer_to_score[user_answer] if user_answer in map_answer_to_score else 0

    # we can't know which attribute is the most important, so use unweighted average
    row["coding_background_score"] = working_years
    return row


# =====================================================================================================================
# =========================================default english proficiency scoring=========================================
# =====================================================================================================================
def add_english_proficiency_score(graded_result_df):
    graded_result_df = graded_result_df.apply(_default_english_proficiency_grading, axis=1)
    # globally normalize
    graded_result_df = globally_normalize_scores(graded_result_df, "English_proficiency")
    return graded_result_df


def _default_english_proficiency_grading(row):
    # type 1: self - subjective assess: locally normalize to [0, 1]
    self_assess = row["How would you rate your English proficiency?"] / 5
    watch_english_subtitle = row["Can you watch TV in English without subtitles?"]
    transcribed_names = (6 - row["How often do you use variable names transcribed from your language while coding?"]) / 5
    self_subjective_assess_score = (self_assess + watch_english_subtitle + transcribed_names) / 3

    # type 2: self-objective assess: locally normalized to [0,1]
    watch_english_hours = row["How many hours per day do you spend speaking English?"] / 10
    # grade native bonus: native = 1
    native_score = 1 if row["What is your native language?"] == "English" else 0
    self_objective_assess_score = (native_score + watch_english_hours) / 2

    # so use unweighted average, however we can know which attribute are subjective and which are objective
    english_proficiency_score = (self_subjective_assess_score + self_objective_assess_score) / 2
    row["English_proficiency"] = english_proficiency_score
    return row


# =====================================================================================================================
# =========================================test =======================================================================
# =====================================================================================================================
graded_result_df = pd.read_csv("manually_graded.csv")
graded_result_df = clean_up_df(graded_result_df)
graded_result_df = add_code_proficiency_score(graded_result_df)
graded_result_df = add_english_proficiency_score(graded_result_df)
graded_result_df.to_csv("auto_graded.csv", index=False)
print("Processed")
