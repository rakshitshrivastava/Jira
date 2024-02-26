import pandas as pd
import requests
import getpass
import csv

# Jira API endpoint for getting an issue by its key
url_get_issue = "https://Yourjira.atlassian.net/rest/api/3/issue/{}/?fields=labels"

# Authentication details
email = ""
api_token = getpass.getpass(prompt="Enter your Jira API token: ")

def get_issue_labels(issue_key):
    url = f"https://YourZira.atlassian.net/rest/api/3/issue/{issue_key}?fields=labels"
    response = requests.get(url, auth=(email, api_token))
    if response.status_code == 200:
        issue_data = response.json()
        labels = issue_data["fields"]["labels"]
        print("Current Labels:", labels)
        return labels
    else:
        print(f"Failed to get issue details for {issue_key}. Status code:", response.status_code)
        print("Response:", response.text)
        return None

def add_label(issue_key, label):
    labels = get_issue_labels(issue_key)
    if labels is None:
        return
    
    if label not in labels:
        labels.append(label)
        update_data = {"fields": {"labels": labels}}
        url = f"https://YourJira.atlassian.net/rest/api/3/issue/{issue_key}"
        response = requests.put(url, auth=(email, api_token), headers={"Content-Type": "application/json"}, json=update_data)
        if response.status_code == 204:
            print(f"Label '{label}' added successfully.")
        else:
            print("Failed to add label. Status code:", response.status_code)
            print("Response:", response.text)
    else:
        print(f"Label '{label}' already exists.")

def add_comment(issue_key, comment):
    url = f"https://YourJira.atlassian.net/rest/api/3/issue/{issue_key}/comment"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment
                        }
                    ]
                }
            ]
        }
    }
    response = requests.post(url, auth=(email, api_token), headers=headers, json=data)
    if response.status_code == 201:
        print("Comment added successfully.")
    else:
        print("Failed to add comment. Status code:", response.status_code)
        print("Response:", response.text)

# Read CSV file
csv_file_path = "res.csv"
df = pd.read_csv(csv_file_path)

# Iterate over rows
for index, row in df.iterrows():
    issue_key = row["Ticket"]
    if pd.isnull(issue_key):
        print("Empty value found in 'Ticket' column. Stopping.")
        break
    label = "Issue_Fixed"
    add_label(issue_key, label)

    comment = "Write Your Comment  "
    add_comment(issue_key, comment)
