from jira_client import fetch_issues
import pandas as pd

def compute_metrics():

    issues = fetch_issues("project = DEV")

    sprint_data = {}

    # =========================================
    # PROCESS EACH ISSUE
    # =========================================

    for issue in issues:

        f = issue["fields"]

        # =========================================
        # DEBUG SECTION
        # =========================================

        print("\n====================")
        print("ISSUE KEY:", issue["key"])
        print("ISSUE TYPE:", f["issuetype"]["name"])

        # =========================================
        # SPRINT FIELD
        # =========================================

        sprint_field = f.get("customfield_10020")

        # Skip issues without sprint
        if not sprint_field:
            continue

        sprint_name = sprint_field[0]["name"]

        # =========================================
        # INITIALIZE SPRINT
        # =========================================

        if sprint_name not in sprint_data:

            sprint_data[sprint_name] = {
                "total_stories": 0,
                "done_stories": 0,
                "critical_bugs": 0,
                "must_have_total": 0,
                "must_have_done": 0,
                "demo_feedback_scores": []
            }

        issue_type = f["issuetype"]["name"]
        status = f["status"]["name"]
        priority = f.get("priority", {}).get("name", "")
        labels = f.get("labels", [])

        sprint = sprint_data[sprint_name]

        # =========================================
        # STORY / TASK COMPLETION
        # =========================================

        if issue_type in ["Story", "Task"]:

            sprint["total_stories"] += 1

            if status == "Done":
                sprint["done_stories"] += 1

        # =========================================
        # OPEN CRITICAL BUGS
        # =========================================

        label_list = [l.lower() for l in labels]

        print("LABELS:", label_list)
        print("PRIORITY:", priority)

        if (
            issue_type == "Bug"
            and status != "Done"
            and (
                priority in ["Critical", "Highest"]
                or "Critical" in labels
            )
        ):
            sprint["critical_bugs"] += 1

            print("CRITICAL BUG COUNTED")
        # =========================================
        # MUST HAVE COMPLETION
        # =========================================

        if "must-have" in [l.lower() for l in labels]:

            sprint["must_have_total"] += 1

            if status == "Done":
                sprint["must_have_done"] += 1

        # =========================================
        # DEMO FEEDBACK
        # =========================================

        feedback = f.get("customfield_10071")

        print("\n-------------------")
        print("ISSUE:", issue["key"])
        print("SPRINT:", sprint_name)
        print("RAW FEEDBACK:", feedback)

        if feedback:

            # Handle dict/string formats
            if isinstance(feedback, dict):
                value = feedback.get("value", "")
            else:
                value = str(feedback)

            print("FEEDBACK VALUE:", value)

            value_lower = value.lower()

            if "expected" in value_lower:
                score = 5

            elif "enhancement" in value_lower:
                score = 3

            elif "poor" in value_lower:
                score = 1

            else:
                score = 3

            print("SCORE ADDED:", score)

            sprint["demo_feedback_scores"].append(score)

    # =========================================
    # FINAL SPRINT METRICS
    # =========================================

    data = []

    for sprint_name, s in sprint_data.items():

        # =========================================
        # DEMO FEEDBACK AVERAGE
        # =========================================

        if len(s["demo_feedback_scores"]) > 0:

            demo_score = (
                sum(s["demo_feedback_scores"])
                / len(s["demo_feedback_scores"])
            )

        else:
            demo_score = 3

        print("\n======================")
        print("SPRINT:", sprint_name)
        print("ALL FEEDBACK SCORES:", s["demo_feedback_scores"])
        print("AVERAGE FEEDBACK:", demo_score)

        # =========================================
        # TEST COVERAGE FROM ZEPHYR
        # =========================================

        coverage_map = {
            "DEV Sprint 1": 0.67,
            "DEV Sprint 2": 1.00,
            "DEV Sprint 3": 0.25
        }

        test_coverage = coverage_map.get(sprint_name, 0)

        # =========================================
        # SIMULATED BUILD SUCCESS RATE
        # =========================================

        build_map = {
            "DEV Sprint 1": 0.85,
            "DEV Sprint 2": 0.95,
            "DEV Sprint 3": 0.60
        }

        build_success_rate = build_map.get(sprint_name, 0.90)

        # =========================================
        # FINAL METRICS ROW
        # =========================================

        data.append({

            "Sprint": sprint_name,

            "StoryCompletionRate":
                s["done_stories"] / s["total_stories"]
                if s["total_stories"] else 0,

            "TestCoverage": test_coverage,

            "OpenCriticalBugs": s["critical_bugs"],

            "BuildSuccessRate": build_success_rate,

            "DemoFeedback": round(demo_score, 2),

            "MustHaveCompletion":
                s["must_have_done"] / s["must_have_total"]
                if s["must_have_total"] else 0
        })

    print("\nJIRA DATA FETCHED SUCCESSFULLY")
    print("TOTAL ISSUES:", len(issues))

    return pd.DataFrame(data)