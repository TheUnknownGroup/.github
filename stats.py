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

for repo in repos:
  print([repo["name"]])

# print(f"\n💪 Heres our stats!\n")
# for repo in repos:
#   name = [repo["name"]]
#   langs = [lang["name"] for lang in repo["languages"]["nodes"]]
#   commits = repo["defaultBranchRef"]["target"]["history"]["totalCount"] if repo["defaultBranchRef"] else 0
#   prs = repo["pullRequests"]["totalCount"]
#   iss = repo["issues"]["totalCount"]
#   stars = repo["stargazerCount"]
#   forks = repo["forkCount"]

#   lang_count.update(langs)

# commits_img = requests.get(
#   f"https://img.shields.io/github/commit-activity/t/{ORG_NAME}/{name}"
# )

# print(f"\n[![Name: {', '.join(name)}]({commits_img})](https://github.com/{ORG_NAME}/)\n "+
#       f"\nLanguages: {', '.join(langs) if langs else 'None' }\n "+
#       f"\nCommits: {commits}\n "+
#       f"\nPull Requests: {prs}\n "+
#       f"\nIssues: {iss}\n "+
#       f"\nTotal Stars: {stars}\n "+
#       f"\nTotal Forks: {forks}\n ")