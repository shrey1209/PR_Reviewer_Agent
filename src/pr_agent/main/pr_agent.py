import os
from dotenv import load_dotenv
load_dotenv()

from pr_agent.business.get_repos import GitRepos

def main() -> None:
    print("Hello from pr-agent!")
    git_repos = GitRepos()
    git_repos.get_repos()
    
if __name__ == "__main__":
    main()