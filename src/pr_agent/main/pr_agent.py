import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from pr_agent.utils.write_to_file import FileWriter
from pr_agent.model import SavePrResult

from datetime import datetime
from pr_agent.business.get_repos import GitRepos
from pr_agent.utils.github_client import get_github_client
from pr_agent.business.get_prs import GitPRs
from pr_agent.agent.agent import PrAgent
from pr_agent.prompts.write_md import PrMdFile
from pr_agent.prompts.get_system_prompt import GetSystemPrompt
from rich.console import Console

def main() -> None:
    github_client = get_github_client()
    git_repos = GitRepos(github_client)
    git_prs = GitPRs(git_repos)

    system_prompt_path = Path(__file__).parent.parent / "prompts" / "system_prompts"

    pr_system_prompt = GetSystemPrompt(system_prompt_path / "pr_review_prompt.md").get_prompt()

    console = Console()
    current_datetime = datetime.now()
    review_dir = Path(__file__).parent.parent.parent.parent / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    pr_agent = PrAgent(os.getenv("MODEL"), pr_system_prompt)
    for pr in git_prs.get_prs():
        md_file = PrMdFile(pr)
        with console.status(f"Reviewing {pr.repo} #{pr.number}: {pr.title}..."):
            output = pr_agent.ask(md_file.write_md())
        save_pr_result = SavePrResult(
            repository=pr.repo,
            title=pr.title,
            pr_number=pr.number,
            agent_output=output
        )
        review_file_path = review_dir / f"{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}_{pr.repo.replace('/', '_')}_{pr.number}_review.json"
        
        file_write = FileWriter(review_file_path)
        file_write.write(save_pr_result.model_dump_json(indent=2))
        console.print(f"[green]✓[/green] {pr.repo} #{pr.number} saved to {review_file_path.name}")


    
if __name__ == "__main__":
    main()