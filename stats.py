import os
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ORG_NAME = "TheUnknownGroup"
HEADERS = { "Authorization": f"Bearer {GITHUB_TOKEN}" }
MAIN = "https://github.com/TheUnknownGroup/"

query = f"""
{{
  organization(login: "{ORG_NAME}") {{
    name
    repositories(first: 100) {{
      nodes {{
      name
        stargazerCount
        forkCount
        languages(first: 100) {{
          nodes {{
            name
          }}
        }}
        defaultBranchRef {{
          target {{
            ... on Commit {{
              history {{
                totalCount
              }}
            }}
          }}
        }}
        pullRequests {{
          totalCount
        }}
        issues {{
          totalCount
        }}
      }}
    }}
  }}
}}
"""

response = requests.post(
  "https://api.github.com/graphql",
  json={"query": query},
  headers=HEADERS
)

data = response.json()
repos = data["data"]["organization"]["repositories"]["nodes"]

print(f"\n\n💪 Heres out stats!\n\n")
for repo in repos:
  name = repo["name"]
  langs = [lang["name"] for lang in repo["languages"]["nodes"]]
  prs = repo["pullRequests"]["totalCount"]
  iss = repo["issues"]["totalCount"]
  stars = repo["stargazerCount"]
  forks = repo["forkCount"]
  commits_img = f"https://img.shields.io/github/commit-activity/t/{ORG_NAME}/{name}"
  print(f"\nRepo: {name}" +
        f"[![Name: {name}]({commits_img})]({MAIN})\n"+
        f"\nLanguages: {', '.join(langs) if langs else 'None'}\n"+
        f"\nPull Requests: {prs}\n"+
        f"\nIssues: {iss}\n"+
        f"\nTotal Stars: {stars}\n"+
        f"\nTotal Forks: {forks}\n")