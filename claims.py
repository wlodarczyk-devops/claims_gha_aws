import requests
import sys
import os
import ast
import argparse

def claims(
        github_token,
        use_default: bool = False,
        claims=["repo","repository_owner","context","actor_id","actor"], 
        organisation="wlodarczyk-devops", 
        repository="shared-modules",
        github_api="https://api.github.com"
        ):

    payload_api = {
        "use_default": False,
        "include_claim_keys": list(claims)
    }

    headers_api = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    url = f"{github_api}/repos/{organisation}/{repository}/actions/oidc/customization/sub"
    request_api = requests.put(url, headers=headers_api, json=payload_api)

    # TO IMPROVE ALONG WITH GHA
    # if use_default == False:
    #     payload_api = {
    #         "use_default": False,
    #         "include_claim_keys": list(claims)
    #     }
    # else:
    #     payload_api = {
    #         "use_default": True
    #     }
    # urls = []
    # for repo in repositories:
    #     url = f"{github_api}/repos/{organisation}/{repo}/actions/oidc/customization/sub"
    #     urls.append(url)
    #     print(url)
    # for url in urls:
    #     request_api = requests.put(url, headers=headers_api, json=payload_api)
    #     request_api.raise_for_status()
    #     return request_api.json()

# repos = ast.literal_eval(sys.argv[1])

req = claims(github_token=os.environ["GITHUB_TOKEN"], organisation=os.environ["ORGANISATION"], repository=os.environ["REPOSITORY"])
