import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from pr_agent.business.get_repos import GitRepos
from pr_agent.utils.github_client import get_github_client
from pr_agent.business.get_prs import GitPRs
from pr_agent.agent.agent import PrAgent
from pr_agent.prompts.write_md import PrMdFile
from pr_agent.prompts.get_system_prompt import GetSystemPrompt

def main() -> None:
    github_client = get_github_client()
    git_repos = GitRepos(github_client)
    git_prs = GitPRs(git_repos)

    system_prompt_path = Path(__file__).parent.parent / "prompts" / "system_prompts"

    pr_system_prompt = GetSystemPrompt(system_prompt_path / "pr_review_prompt.md").get_prompt()
    
    pr_agent = PrAgent(os.getenv("MODEL"), pr_system_prompt)
    for pr in git_prs.get_prs():
        md_file = PrMdFile(pr)
        output = pr_agent.ask(md_file.write_md())
        print(output.review)
        print(output.usage)
        print("=========================================================================\n")


    
if __name__ == "__main__":
    main()