import os
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ORG_NAME = "TheUnknownGroup"
HEADERS = { "Authorization": f"Bearer {GITHUB_TOKEN}" }

query = """
{
  organization(login: "{0}") {
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
""".format(ORG_NAME)

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
  languages = repo["languages"]["nodes"]["name"]
  commits
  stars = sum(repo["stargazerCount"])
  forks = sum(repo["forkCount"])

print(f""+
      f"Total Stars: {stars}\n"+
      f"TotalForks: {forks}\n")