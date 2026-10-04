from pathlib import Path

from prlens.diff_parser import ChangedFile

SKILLS_DIR = Path(__file__).parent / "skills"


def load_skill(skill_name: str = "general_review") -> str:
    skill_path = SKILLS_DIR / f"{skill_name}.md"

    if not skill_path.exists():
        raise ValueError(f"Unknown review skill: {skill_name}")

    return skill_path.read_text(encoding="utf-8")


def format_line_range(start: int, count: int) -> str:
    if count == 0:
        return "none"

    if count == 1:
        return str(start)

    return f"{start}-{start + count - 1}"


def build_review_prompt(
    changed_files: list[ChangedFile],
    skill_name: str = "general_review",
) -> str:
    instructions = load_skill(skill_name)

    diff_sections: list[str] = []

    for changed_file in changed_files:
        diff_sections.append(f"File: {changed_file.path}")

        for section in changed_file.sections:
            old_lines = format_line_range(
                section.old_start,
                section.old_count,
            )

            new_lines = format_line_range(
                section.new_start,
                section.new_count,
            )

            diff_sections.append(
                f"""
Old lines: {old_lines}
New lines: {new_lines}

{section.content}
""".strip()
            )

    diff_content = "\n\n".join(diff_sections)

    return f"""
{instructions}

## Pull Request Changes

{diff_content}
""".strip()
