from toolbox import *

auto_graded_results = pd.read_csv("auto_graded.csv")

for question_type in [Q_TYPE_ALL, Q_TYPE_FULL, Q_TYPE_ABRIV, Q_TYPE_NONE]:
    fig = px.scatter(auto_graded_results, x="English_proficiency", y=f"coding_proficiency({question_type})",
                     title=f'correlation ({question_type})', trendline="ols")
    fig.show()
print("Processed")