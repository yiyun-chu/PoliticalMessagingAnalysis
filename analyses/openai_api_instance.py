import openai
import json
import pandas as pd
from tqdm import tqdm
import os
import time

API_KEY = 'your_api_key'

def get_subissues_for_issues(email_text, issues_list):
    """
    Process email to get sub-issues for each topic.
    Returns a dictionary with topics and their respective sub-issues.
    """
    issues_str = ", ".join(issues_list) if isinstance(issues_list, list) else issues_list

    prompt = f"""
    Identify and list relevant sub-issues associated with each main issue from the issues_list that are mentioned in the email.
    Return the data in JSON format with each issue as a key and its associated sub-issues as a list.

    Format:
    {{
        "issue1": ["sub_issue1", "sub_issue2"],
        "issue2": ["sub_issue1", "sub_issue2"]
    }}

    Only include issues from issues_list and ensure unique sub-issues for each issue. Make sure to extract sub-issues for each issue in the issues_list.

    Issues List: {issues_str}

    Email:
    {email_text}
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that identifies sub-issues related to issues from an email."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0
        )

        sub_issues = response.choices[0].message.content.strip()

        return sub_issues
            
    except Exception as e:
        print(f"Error processing email: {e}")
        return {}
    
def process_email(body_template_id, email_text, issues_list):
    """
    Process a single email and return the result as a dictionary
    """
    try:
        matched_subissues = get_subissues_for_issues(email_text, issues_list)
        return {body_template_id: matched_subissues}
    except Exception as e:
        return {body_template_id: f"Error: {str(e)}"}

def main(input_file='input_file.csv', output_file='output_file.json', delay=2, batch_size=5):
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            results = json.load(f)
    else:
        results = {}

    full = pd.read_csv(input_file)
    for i in tqdm(range(0, len(full), batch_size), desc="Processing Emails in Batches"):
        batch = full.iloc[i:i + batch_size]

        for _, row in batch.iterrows():
            body_template_id = row['body_template_id']
            email_text = row['cleaned_body']
            issues_list = row['issue_split'].split(', ')
            result = process_email(body_template_id, email_text, issues_list)
            results.update(result)

            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
            time.sleep(delay)
    
if __name__ == "__main__":
    openai.api_key = API_KEY
    main()