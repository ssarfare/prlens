import pytest

from prlens.diff_parser import ChangedFile, DiffSection
from prlens.prompt_builder import build_review_prompt, load_skill


def test_load_general_review_skill():
    skill = load_skill()

    assert "correctness" in skill
    assert "Do not speculate" in skill
    assert "Return only valid JSON" in skill
    assert "overall_status" in skill


def test_unknown_skill():
    with pytest.raises(ValueError, match="Unknown review skill"):
        load_skill("does_not_exist")


def test_build_review_prompt():
    changed_files = [
        ChangedFile(
            path="example.py",
            sections=[
                DiffSection(
                    old_start=1,
                    old_count=1,
                    new_start=1,
                    new_count=1,
                    content="-old\n+new",
                )
            ],
        )
    ]

    prompt = build_review_prompt(changed_files)

    assert "example.py" in prompt
    assert "-old" in prompt
    assert "+new" in prompt
    assert "correctness" in prompt
