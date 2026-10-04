from dataclasses import dataclass

from unidiff import PatchSet


@dataclass
class DiffSection:
    # Starting line in the original file.
    old_start: int

    # Number of lines represented from the original file.
    old_count: int

    # Starting line in the updated file.
    new_start: int

    # Number of lines represented from the updated file.
    new_count: int

    # Added, removed, and context lines in this section.
    content: str


@dataclass
class ChangedFile:
    # Repository-relative path of the changed file.
    path: str

    # Separate changed sections within the file.
    sections: list[DiffSection]


def parse_diff(diff: str) -> list[ChangedFile]:
    """Parse a raw unified Git diff into PRLens domain models."""

    patch = PatchSet(diff)

    changed_files: list[ChangedFile] = []

    for patched_file in patch:
        sections: list[DiffSection] = []

        for section in patched_file:
            content = "".join(str(line) for line in section).rstrip("\n")

            sections.append(
                DiffSection(
                    old_start=section.source_start,
                    old_count=section.source_length,
                    new_start=section.target_start,
                    new_count=section.target_length,
                    content=content,
                )
            )

        changed_files.append(
            ChangedFile(
                path=patched_file.path,
                sections=sections,
            )
        )

    return changed_files
