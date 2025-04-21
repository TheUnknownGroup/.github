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
      }
    }
  }
}
""" % ORG_NAME

response = requests.post(
  "https://api.github.com/graphql",
  json={"query": query},
  headers=HEADERS
)

data = response.json()
repos = data["data"]["organization"]["repositories"]["nodes"]

total_stars = sum(repo["stargazerCount"] for repo in repos)
total_forks = sum(repo["forkCount"] for repo in repos)

print(f"Total Stars: {total_stars}")
print(f"Total Forks: {total_forks}")