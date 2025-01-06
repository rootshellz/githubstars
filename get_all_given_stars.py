#!/usr/bin/env python

import sys
import json
import requests

api_url = "https://api.github.com"
list_stared_url = f"{api_url}/user/starred"

token_file_name = ".token"
out_file_name = "given_stars.json"

with open(token_file_name) as token_file:
    token = token_file.readline().strip()
headers = {
    "Authorization": f"token {token}",  # curl -i -H "Authorization: token $(cat .token)" https://api.github.com/user/starred
    "Accept": "application/vnd.github.star+json",  # curl -i -H "Authorization: token $(cat .token)" -H "Accept: application/vnd.github.star+json" https://api.github.com/user/starred
}


def get_stars_by_page(page_number):
    print(f"Getting page: {page_number}")
    response = requests.get(f"{list_stared_url}?page={page_number}", headers=headers)
    if response.status_code == 200:
        next_page = 0
        if "link" in response.headers and 'rel="next"' in response.headers["link"]:
            # link: <https://api.github.com/user/starred?page=2>; rel="next", <https://api.github.com/user/starred?page=40>; rel="last"
            # link: <https://api.github.com/user/starred?page=1>; rel="prev", <https://api.github.com/user/starred?page=3>; rel="next", <https://api.github.com/user/starred?page=40>; rel="last", <https://api.github.com/user/starred?page=1>; rel="first"
            # link: <https://api.github.com/user/starred?page=39>; rel="prev", <https://api.github.com/user/starred?page=1>; rel="first"
            for link in response.headers["link"].split(","):
                if 'rel="next"' in link:
                    next_page = int(link[link.find("=") + 1 : link.find(">")])
                    print(f"  Next page: {next_page}")
                    break
        return response.json(), next_page
    else:
        print(
            f"  Failed to fetch starred repositories page {page_number}: {response.status_code} - {response.text}"
        )
        sys.exit(1)


def get_all_user_stared_repos():
    print("Getting stared repos")
    stared_repos = list()
    next_page = 1
    while next_page:
        stared_repos_page, next_page = get_stars_by_page(next_page)
        print(f"  Got {len(stared_repos_page)} stared repos")
        stared_repos.extend(stared_repos_page)
    print(f"Got {len(stared_repos)} stared repos")
    return stared_repos


if __name__ == "__main__":
    print("Script starting")
    stared_repos = get_all_user_stared_repos()
    with open(out_file_name, "w") as out_file:
        json.dump(stared_repos, out_file, indent=4)
        print(f"Wrote results to {out_file_name}")
    print("Script done")
