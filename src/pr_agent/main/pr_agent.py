from dotenv import load_dotenv
load_dotenv()

from pr_agent.business.get_repos import GitRepos
from pr_agent.utils.github_client import get_github_client
from pr_agent.business.get_prs import GitPRs

def main() -> None:
    github_client = get_github_client()
    git_repos = GitRepos(github_client)
    git_prs = GitPRs(git_repos)
    for pr in git_prs.get_prs():
        print(pr.model_dump_json(indent=2))        
    
if __name__ == "__main__":
    main()