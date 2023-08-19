from toolbox import *
import statsmodels.api as sm

results = pd.read_csv("auto_graded.csv")

# task 1: calculate p-value
from scipy.stats import pearsonr
from scipy.stats import spearmanr


def calculate_p_value(x_col_name, y_col_name):
    correlation_coefficient, p_value = pearsonr(results[x_col_name], results[y_col_name])

    print(f"Pearson Correlation Coefficient: {correlation_coefficient}")
    print(f"P-value: {p_value}")

    if p_value < 0.05:  # You can adjust the significance level as needed
        print("The variables are significantly correlated.")
    else:
        print("Pearson: There is no significant correlation between the variables.")

def calculate_Spearman(x_col_name, y_col_name):
    # Assuming your DataFrame is named df
    correlation_coefficient, p_value = spearmanr(results[x_col_name], results[y_col_name])

    print(f"Spearman Rank Correlation Coefficient: {correlation_coefficient}")
    print(f"Spearman Rank: {p_value}")

    if p_value < 0.05:  # You can adjust the significance level as needed
        print("The variables are significantly correlated.")
    else:
        print("Spearman Rank: There is no significant correlation between the variables.")
for question_type in [Q_TYPE_ALL, Q_TYPE_FULL, Q_TYPE_ABRIV, Q_TYPE_NONE]:
    x_col_name = "English_proficiency"
    y_col_name = f"coding_proficiency({question_type})"
    calculate_p_value(x_col_name, y_col_name)
    calculate_Spearman(x_col_name, y_col_name)
    print("========================================")


