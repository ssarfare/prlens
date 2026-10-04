from prlens.diff_parser import parse_diff


def test_parse_single_file_diff():
    diff = """diff --git a/example.py b/example.py
index 1234567..7654321 100644
--- a/example.py
+++ b/example.py
@@ -1 +1 @@
-print("old")
+print("new")
"""

    files = parse_diff(diff)

    assert len(files) == 1
    assert files[0].path == "example.py"

    assert len(files[0].sections) == 1

    section = files[0].sections[0]

    assert section.old_start == 1
    assert section.old_count == 1
    assert section.new_start == 1
    assert section.new_count == 1
    assert section.content == '-print("old")\n+print("new")'


def test_parse_multiple_files():
    diff = """diff --git a/foo.py b/foo.py
--- a/foo.py
+++ b/foo.py
@@ -1 +1 @@
-old
+new
diff --git a/bar.py b/bar.py
--- a/bar.py
+++ b/bar.py
@@ -1 +1 @@
-before
+after
"""

    files = parse_diff(diff)

    assert len(files) == 2

    assert files[0].path == "foo.py"
    assert len(files[0].sections) == 1
    assert files[0].sections[0].content == "-old\n+new"

    assert files[1].path == "bar.py"
    assert len(files[1].sections) == 1
    assert files[1].sections[0].content == "-before\n+after"


def test_parse_multiple_sections_in_same_file():
    diff = """diff --git a/example.py b/example.py
--- a/example.py
+++ b/example.py
@@ -1 +1 @@
-old_one
+new_one
@@ -10 +10 @@
-old_two
+new_two
"""

    files = parse_diff(diff)

    assert len(files) == 1
    assert files[0].path == "example.py"
    assert len(files[0].sections) == 2

    first_section = files[0].sections[0]
    second_section = files[0].sections[1]

    assert first_section.old_start == 1
    assert first_section.old_count == 1
    assert first_section.new_start == 1
    assert first_section.new_count == 1
    assert first_section.content == "-old_one\n+new_one"

    assert second_section.old_start == 10
    assert second_section.old_count == 1
    assert second_section.new_start == 10
    assert second_section.new_count == 1
    assert second_section.content == "-old_two\n+new_two"
