from github import Github
from github import Auth
import os

class GitRepos:
    def get_repos(self):
        print("Fetching Git repositories...")
        auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
        github = Github(auth=auth)
        print("Repositories for user:", type(github.get_user().get_repos()))
        print("=" * 40)
        for repo in github.get_user().get_repos():
            pulls = repo.get_pulls(state="open")
            print(f"Open pull requests for repository {repo.name}:")
            for pull in pulls:
                print(f"- {pull.title}")
                print(f"-- {pull.number}")
                print(f"-- URL: {pull.html_url}")