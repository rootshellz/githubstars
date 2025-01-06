#!/usr/bin/env python

import requests

api_url = "https://api.github.com"
stared_url = f"{api_url}/user/starred"

token_file_name = ".token"
remove_file_name = "remove_stars.txt"

with open(token_file_name) as token_file:
    token = token_file.readline().strip()
headers = {
    "Authorization": f"token {token}",  # curl -i -X DELETE -H "Authorization: token $(cat .token)" https://api.github.com/user/starred/{owner}/{repo}
}

with open(remove_file_name) as remove_file:
    repos_to_unstar = [line.strip() for line in remove_file.readlines()]


def remove_star_from_repo(repo):
    print(f"Removing star from repo: {repo}")
    response = requests.delete(f"{stared_url}/{repo}", headers=headers)
    if response.status_code == 204:
        print(f"  - Successfully removed star from repo: {repo}")
    else:
        print(f"  ! Failed to remove star from repo: {repo}")


if __name__ == "__main__":
    print("Script starting")
    for repo in repos_to_unstar:
        remove_star_from_repo(repo)
    print("Script done")
