from __future__ import annotations

import configparser
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
    "lakehouse-data-platform",
    "feature-store-inference",
    "mlops-lifecycle-platform",
    "data-observability-lineage",
    "rag-evaluation-pipeline",
    "streaming-fraud-anomaly",
    "elt-connector-framework",
]
GUIDES = [
    "docs/portfolio-mentor-review.md",
    "docs/recruiter-guide.md",
    "docs/shared-engineering-standard.md",
    "docs/interview-guide.md",
    "docs/cv-bullets.md",
    "docs/roadmap.md",
]
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    return [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]


def local_link_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>")
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith("#"):
        return None
    return (source.parent / unquote(parsed.path)).resolve()


def check_local_links() -> list[str]:
    errors: list[str] = []
    for source in markdown_files():
        for match in LINK_PATTERN.finditer(source.read_text(encoding="utf-8")):
            target = local_link_target(source, match.group(1))
            if target is not None and not target.exists():
                errors.append(f"{source.relative_to(ROOT)}: missing {match.group(1)}")
    return errors


def check_index_contract() -> list[str]:
    errors: list[str] = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for project in PROJECTS:
        url = f"https://github.com/kevinmeix1/{project}"
        if url not in readme:
            errors.append(f"README.md: missing project link {url}")
    for guide in GUIDES:
        if not (ROOT / guide).exists():
            errors.append(f"missing required guide {guide}")
        if guide not in readme:
            errors.append(f"README.md: missing guide link {guide}")
    return errors


def check_submodules() -> list[str]:
    parser = configparser.ConfigParser()
    parser.read(ROOT / ".gitmodules", encoding="utf-8")
    configured = {
        parser[section]["url"].removesuffix(".git").rsplit("/", 1)[-1]
        for section in parser.sections()
    }
    expected = set(PROJECTS)
    if configured == expected:
        return []
    missing = sorted(expected - configured)
    unexpected = sorted(configured - expected)
    return [f".gitmodules mismatch: missing={missing}, unexpected={unexpected}"]


def main() -> int:
    errors = [*check_local_links(), *check_index_contract(), *check_submodules()]
    if errors:
        print("Portfolio documentation contract failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Portfolio documentation contract passed ({len(PROJECTS)} projects, {len(GUIDES)} guides).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
