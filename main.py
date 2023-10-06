import csv
from github import Github

ACCESS_TOKEN = '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'  # Replace with your GitHub Token
ORG_NAME = 'cmpt-276-fall-2023-project'  # Replace with your organization name
CSV_FILE = 'usernames.csv'  # Ensure the CSV file has a 'username' column

g = Github(ACCESS_TOKEN)


def get_user_id(username):
    try:
        # print(g.get_user(login=username).id)
        return g.get_user(login=username).id
    except:
        print(f"***** Failed to get ID for {username} *****")
        return None


def invite_user(org_name, user_id=None, gitUsername=None, email=None, role='direct_member', team_ids=None):
    org = g.get_organization(org_name)

    if user_id:
        invitee_id = {'invitee_id': user_id}
    elif email:
        invitee_id = {'email': email}
    else:
        print("Neither user ID nor email provided. Skipping...")
        return

    try:
        headers = {'accept': 'application/vnd.github.v3+json'}
        data = {**invitee_id, 'role': role}

        if team_ids:
            data['team_ids'] = team_ids

        # Using the internal requester to send the invite, since direct support is not available
        org._requester.requestJsonAndCheck(
            "POST",
            f"/orgs/{org_name}/invitations",
            input=data,
            headers=headers
        )
        print(f"Successfully invited {gitUsername} ({user_id or email})")
    except Exception as e:
        print(f"Failed to invite {gitUsername} ({user_id or email}). Reason: {str(e)}")


def main():
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # print("reader :", reader)
        for row in reader:
            username = row[0]  # Ensure your CSV has a 'username' column as the first column
            user_id = get_user_id(username)
            if user_id:
                invite_user(ORG_NAME, user_id=user_id, gitUsername=username)


if __name__ == '__main__':
    main()
