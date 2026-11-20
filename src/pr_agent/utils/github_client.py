from github import Github
from github import Auth
import os

def get_github_client() -> Github:
    token = os.getenv("GITHUB_TOKEN")
    if not token or not token.strip():
        raise ValueError("GITHUB_TOKEN is missing or empty in the environment variables")
    auth = Auth.Token(token)
    return Github(auth=auth)