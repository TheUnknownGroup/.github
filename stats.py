import os
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ORG_NAME = "TheUnknownGroup"
HEADERS = { "Authorization": f"Bearer {GITHUB_TOKEN}" }

query = """
{
  organization(login: "%s") {
    name
    repositories(first: 100) {
      nodes {
        name
        stargazerCount
        forkCount
        languages(first: 10) {
          nodes {
            name
          }
        }
        defaultBranchRef {
          target {
            ... on Commit {
              history {
                totalCount
              }
            }
          }
        }
        pullRequests {
          totalCount
        }
        issues {
          totalCount
        }
      }
    }
  }
}
""" % (ORG_NAME)

response = requests.post(
  "https://api.github.com/graphql",
  json={"query": query},
  headers=HEADERS
)

data = response.json()
repos = data["data"]["organization"]["repositories"]["nodes"]

print(f"💪 Heres our stats!\n")
for repo in repos:
  name = repo["name"]
  languages = repo["languages"]["nodes"]
  commits = repo["defaultBranchRef"]["target"]["history"]["totalCount"] if repo["defaultBranchRef"] else 0
  prs = repo["pullRequests"]["totalCount"]
  issues = repo["issues"]["totalCount"]
  stars = repo["stargazerCount"]
  forks = repo["forkCount"]

commits_img = requests.get(
  f"https://img.shields.io/github/commit-activity/t/{ORG_NAME}/{name}"
)

print(f"[![Name: {name}]()\n"+
      f"Languages: {languages}\n"+
      f"Commits: {commits}\n"+
      f"Pull Requests"
      f"Total Stars: {stars}\n"+
      f"TotalForks: {forks}\n")