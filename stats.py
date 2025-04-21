import os
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ORG_NAME = "TheUnknownGroup"
HEADERS = { "Authorization": f"Bearer {GITHUB_TOKEN}" }
MAIN = "https://github.com/TheUnknownGroup"

a = """## Welcome! :wave:
This is the README markdown file for the organization `The Unknown Group`!

There are currently four repositories that are able to worked on, or just to add your own code. The repositories are the following:

  - [Unknown Mod](https://github.com/TheUnknownGroup/unknown-mod)!
  - [Custom Splashes](https://github.com/TheUnknownGroup/custom-splashes)!
  - [Our website](https://github.com/TheUnknownGroup/theunknowngroup.github.io)!
  - [Java](https://github.com/TheUnknownGroup/Java)!
  - [Our minecraft launcher - UKMCL](https://github.com/TheUnknownGroup/UKMCL)!
  - [Our minecraft duplicate - Elementa](https://github.com/TheUnknownGroup/Elementa)!
  - [and finally, VSCode-Snippets](https://github.com/TheUnknownGroup/VSCode-Snippets)!

You can click on any of the links above and they will take you to each repository, allowing you to check them out!

💪Heres our stats!\n
"""

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
markdown = """
| Repository | Stars | Forks | Languages | Pull Requests | Issues | Commits |
|------------|-------|-------|-----------|---------------|--------|---------|\n"""

data = response.json()
repos = data["data"]["organization"]["repositories"]["nodes"]

print(a)
for repo in repos:
  name = repo["name"]
  langs = [lang["name"] for lang in repo["languages"]["nodes"]]
  prs = repo["pullRequests"]["totalCount"]
  iss = repo["issues"]["totalCount"]
  commits_img = f"https://img.shields.io/github/commit-activity/t/{ORG_NAME}/{name}?style=for-the-badge&color=green"
  forks_img = f"https://img.shields.io/github/forks/{ORG_NAME}/{name}?style=for-the-badge&color=green"
  stars_img = f"https://img.shields.io/github/stars/{ORG_NAME}/{name}?style=for-the-badge&color=green"
  markdown += f"| {name} | [![{name}]({commits_img})]({MAIN}/) | {', '.join(langs) if langs else 'None'} | {prs} | {iss} | [![{name}]({stars_img})]({MAIN}/{name}) | [![{name}]({forks_img})]({MAIN}/{name})\n"

print(markdown)