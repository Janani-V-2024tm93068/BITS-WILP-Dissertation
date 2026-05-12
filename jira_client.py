import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

EMAIL = os.getenv("JIRA_EMAIL")
TOKEN = os.getenv("JIRA_API_TOKEN")
DOMAIN = os.getenv("JIRA_DOMAIN")


def fetch_issues(jql):

    url = f"{DOMAIN}/rest/api/3/search/jql"

    auth = HTTPBasicAuth(EMAIL, TOKEN)

    params = {
        "jql": jql,
        "maxResults": 50,
        "startAt": 0,
        "fields": "*all"
        # IMPORTANT fields we need
     #   "fields": "summary,issuetype,status,priority,labels,customfield_10020,customfield_100071"
    }

    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params, auth=auth)

    print("STATUS:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        raise Exception(response.text)

    return response.json().get("issues", [])