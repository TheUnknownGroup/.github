import os
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ORG_NAME = "TheUnknownGroup"
HEADERS = { "Authorization": f"Bearer {GITHUB_TOKEN}" }
MAIN = "https://github.com/TheUnknownGroup"

query = f"""
{{
  organization(login: "{ORG_NAME}") {{
    name
    repositories(first: 100) {{
      nodes {{
      name
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
  commits_img = f"https://img.shields.io/github/commit-activity/t/{ORG_NAME}/{name}"
  forks_img = f"https://img.shields.io/github/forks/{ORG_NAME}/{name}"
  stars_img = f"https://img.shields.io/github/stars/{ORG_NAME}/{name}"
  print(f"\nRepo: {name}" +
        f"\nCommits: [![{name}]({commits_img})]({MAIN}/)\n"+
        f"\nLanguages: {', '.join(langs) if langs else 'None'}\n"+
        f"\nPull Requests: {prs}\n"+
        f"\nIssues: {iss}\n"+
        f"\nStars: [![{name}]({stars_img})]({MAIN}/{name})\n"
        f"\nForks: [![{name}]({forks_img})]({MAIN}/{name})\n")