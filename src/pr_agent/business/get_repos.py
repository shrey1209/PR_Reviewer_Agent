from github.Repository import Repository
from github import Github
from github.PaginatedList import PaginatedList

class GitRepos:
    def __init__(self, github_client: Github):
        self.github_client = github_client

    def get_repos(self) -> PaginatedList[Repository]:
        return self.github_client.get_user().get_repos()
