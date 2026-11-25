from pathlib import Path

from pr_agent.model import SavePrResult

def read_review_file(file: Path) -> str:
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

def get_review_json() -> list[SavePrResult]:
    review_dir = Path(__file__).parent.parent.parent.parent.parent / "reviews"
    files = sorted(review_dir.glob("*.json"))
    prs = []
    for file in files:
        result = SavePrResult.model_validate_json(read_review_file(file))
        prs.append(result)
    return prs