import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("ZEPHYR_TOKEN")

BASE_URL = "https://prod-api.zephyr4jiracloud.com/connect/public/rest/api/1.0"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

def fetch_test_executions(issue_id: str):
    """
    Fetch all test executions linked to a Jira issue (by numeric issueId).
    """
    url = f"{BASE_URL}/execution?issueId={issue_id}"
    response = requests.get(url, headers=headers)
    print("Execution API status:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        return []

    return response.json().get("executions", [])


def get_test_coverage(issue_id: str) -> float:
    """
    Compute test coverage for a given Jira issueId.
    Coverage = PASS / TOTAL executions.
    """
    executions = fetch_test_executions(issue_id)
    total = len(executions)
    passed = sum(1 for e in executions if e.get("status", "").upper() == "PASS")

    coverage = passed / total if total > 0 else 0.0
    return coverage


if __name__ == "__main__":
    # Example: replace with a real Jira issueId (numeric, not DEV-11)
    issue_id = "10001"  # You must fetch this from Jira REST API
    executions = fetch_test_executions(issue_id)
    print("Executions:", executions)

    coverage_value = get_test_coverage(issue_id)
    print(f"Coverage for issue {issue_id}:", coverage_value)
