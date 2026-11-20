from pr_agent.business.get_repos import GitRepos
from pr_agent.model import PullRequest, FileChange
from typing import Iterator

class GitPRs:
    def __init__(self, git_repos: GitRepos):
        self.git_repos = git_repos

    def get_prs(self) -> Iterator[PullRequest]:
        for repo in self.git_repos.get_repos():
            pulls = repo.get_pulls(state="open")
            for pull in pulls:
                pr = PullRequest(
                    number=pull.number,
                    repo=repo.full_name,
                    title=pull.title,
                    url=pull.html_url,
                    files=[
                        FileChange(
                            file_name=file.filename,
                            changes=file.changes,
                            status=file.status,
                            additions=file.additions,
                            deletions=file.deletions,
                            diff=file.patch
                        )
                        for file in pull.get_files()
                    ]
                )
                yield pr