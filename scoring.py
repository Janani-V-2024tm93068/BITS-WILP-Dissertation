import pandas as pd

def calculate_readiness(df):

    weights = {
        "StoryCompletionRate": 0.25,
        "TestCoverage": 0.20,
        "OpenCriticalBugs": 0.15,
        "BuildSuccessRate": 0.15,
        "DemoFeedback": 0.10,
        "MustHaveCompletion": 0.15
    }

    results = []

    for index, row in df.iterrows():

        score = 0

        # Weighted scoring
        score += row["StoryCompletionRate"] * weights["StoryCompletionRate"]

        score += row["TestCoverage"] * weights["TestCoverage"]

        score += (1 - row["OpenCriticalBugs"] / 10) * weights["OpenCriticalBugs"]

        score += row["BuildSuccessRate"] * weights["BuildSuccessRate"]

        score += (row["DemoFeedback"] / 5) * weights["DemoFeedback"]

        score += row["MustHaveCompletion"] * weights["MustHaveCompletion"]


        # Readiness Classification
        if score >= 0.8:
            status = "READY"

        elif score >= 0.6:
            status = "CONDITIONAL"

        else:
            status = "NOT READY"


        # Business Rule for Must-Have Stories
        if row["MustHaveCompletion"] < 0.70 and status == "READY":
            status = "CONDITIONAL"


        results.append({
            "Sprint": row["Sprint"],
            "StoryCompletionRate": row["StoryCompletionRate"],
            "TestCoverage": row["TestCoverage"],
            "OpenCriticalBugs": row["OpenCriticalBugs"],
            "BuildSuccessRate": row["BuildSuccessRate"],
            "DemoFeedback": row["DemoFeedback"],
            "MustHaveCompletion": row["MustHaveCompletion"],
            "ReadinessScore": round(score, 2),
            "Status": status
        })

    result_df = pd.DataFrame(results)

    column_order = [
        "Sprint",
        "StoryCompletionRate",
        "TestCoverage",
        "BuildSuccessRate",
        "OpenCriticalBugs",
        "DemoFeedback",
        "MustHaveCompletion",
        "ReadinessScore",
        "Status"
    ]

    result_df = result_df[column_order]

    return result_df