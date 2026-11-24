class PrMdFile:
    def __init__(self, pr):
        self.pr = pr

    def write_md(self) -> str:
        md = f"# PR: {self.pr.title}\n\n"
        md += f"**Repository:** {self.pr.repo}\n\n"
        md += f"**URL:** {self.pr.url}\n\n"
        if self.pr.description:
            md += f"**Description:**\n{self.pr.description}\n\n"
        md += "## Files Changed\n\n"
        for file in self.pr.files:
            md += f"- **{file.file_name}** ({file.status}, {file.total_changes} changes)\n"
            md += f"  - Additions: {file.additions}, Deletions: {file.deletions}\n"
            if file.diff:
                md += f"  - Diff:\n```\n{file.diff}\n```\n"
            else:
                if file.total_changes != 0:
                    md += f"  - Diff:File changed but diff not available\n"
        return md