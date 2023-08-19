from toolbox import *


def fix_result_error(result_fp):
    def get_correct_col(row):
        # if it's english speaker
        if pd.notna(row["Can you watch TV in English without subtitles?"]):
            result = row[3:24]
        # if it's korean speaker
        elif pd.notna(row["자막 없이 영어로 TV를 볼 수 있나요?"]):
            result = row[24:45]
            result[0] = "Korean"
        # if it's russian speaker
        elif pd.notna(row["Можете ли вы смотреть телевизор на английском без субтитров?"]):
            result = row[45:66]
            result[0] = "Russian"
        # if it's chinese user
        elif pd.notna(row["你看英文電影的時候可以不用字幕嗎？"]):
            result = row[66:87]
            result[0] = "Chinese"
        # if it's hebrew speaker
        elif pd.notna(row["?האם את/ה יכול/ה לצפות בטלוויזיה באנגלית ללא כתוביות"]):
            result = row[87:108]
            result[0] = "Hebrew"
        # if it's arabic speaker
        elif pd.notna(row["هل يمكنك مشاهدة عروض تلفازية باللغة الإنجليزية بدون قراءة النص المترجم؟"]):
            result = row[108:129]
            result[0] = "Arabic"
        else:
            result = row[3:24]  # later we will get rid of this row
        good_rows.append(result)

    # read raw source
    raw_result_df = pd.read_csv(result_fp)
    # append the actual answers for each user
    good_rows = []
    raw_result_df.apply(get_correct_col, axis=1)
    # make a dataframe
    values_list = [s.tolist() for s in good_rows]
    good_result = pd.DataFrame(values_list)
    # label the columns?
    # unify results
    good_result = good_result.apply(_unify_results, axis=1)
    good_result = _rename_columns(good_result)
    return good_result

def _rename_columns(df):
    df.columns = [
        'What is your native language?',
        'How would you rate your English proficiency?',
        'How many hours per day do you spend speaking English?',
        'Can you watch TV in English without subtitles?',
        'How often do you use variable names transcribed from your language while coding? ',
        'How would you rate your coding proficiency?',
        'How many years have you worked coding (not including higher education)',
        'Which of the following is a Boolean?',
        'Which website do you use for coding help?',
        '1. How would you name this piece of code?',
        '1. How easy was this code to understand?',
        '2. How would you name this piece of code?',
        '2. How easy was this code to understand?',
        '3. How would you name this piece of code?',
        '3. How easy was this code to understand?',
        '4. How would you name this piece of code?',
        '4. How easy was this code to understand?',
        '5. How would you name this piece of code?',
        '5. How easy was this code to understand?',
        '6. How would you name this piece of code?',
        '6. How easy was this code to understand?']
    return df

def _unify_results(good_results_row):
    year_string = good_results_row[6]
    # reformat year
    good_results_row[6] = _turn_year_to_numerical(year_string)
    return good_results_row


def _turn_year_to_numerical(year_string):
    pattern = r'(\d+(?:-\d+|\+))'
    match = re.search(pattern, year_string)
    if match:
        year = match.group(1)
        return year
    else:
        return "heyheyhey"


result = fix_result_error("responses.csv")
result.to_csv("ungraded_good_result.csv", index=False)
print("Processed")

