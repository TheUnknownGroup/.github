import os
import requests
from collections import Counter

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ORG_NAME = "TheUnknownGroup"
HEADERS = { "Authorization": f"Bearer {GITHUB_TOKEN}" }

query = f"""
{{
  organization(login: "{ORG_NAME}") {{
    name
    repositories(first: 100) {{
      nodes {{
      name
        stargazerCount
        forkCount
        languages(first: 10) {{
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

lang_count = Counter()

print(f"💪 Heres our stats!\n")
for repo in repos:
  name = repo["name"]
  for names in name:
      names = name
  langs = [lang["name"] for lang in repo["languages"]["nodes"]]
  commits = repo["defaultBranchRef"]["target"]["history"]["totalCount"] if repo["defaultBranchRef"] else 0
  prs = repo["pullRequests"]["totalCount"]
  iss = repo["issues"]["totalCount"]
  stars = repo["stargazerCount"]
  forks = repo["forkCount"]

for repos2 in names:
  commits_img = requests.get(
    f"https://img.shields.io/github/commit-activity/t/{ORG_NAME}/{names}"
  )

for names in name:
   print(f"[![Name: {names}]()]()\n\n")
print(f"Languages: {', '.join(langs) if langs else 'None' }\n\n"+
      f"Commits: {commits}\n\n"+
      f"Pull Requests: {prs}\n\n"+
      f"Issues: {iss}\n\n"+
      f"Total Stars: {stars}\n\n"+
      f"Total Forks: {forks}\n\n")