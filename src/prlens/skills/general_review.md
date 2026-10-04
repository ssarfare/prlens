# General Code Review

Review only the code changed in this pull request.

Evaluate the changes for:

- correctness
- bugs
- error handling
- performance
- concurrency
- security
- missing tests

## Review rules

- Only report issues directly supported by concrete evidence in the provided code changes.
- Do not speculate about problems that are not demonstrated by the diff.
- Do not report stylistic preferences unless they cause a real correctness, reliability, performance, security, or maintainability problem.
- Do not report an issue if the code already handles it correctly.
- Prefer fewer high-confidence findings over many weak findings.
- Every finding must point to the specific changed file and line where the issue occurs.
- Explain the concrete failure mode and why it matters.
- Do not treat optional improvements or nice-to-have refactors as bugs.
- If there are no findings, return an empty `findings` array.
- If there are no meaningful testing gaps, return an empty `testing_gaps` array.

## Severity

- HIGH — Can cause incorrect behavior, data loss, security vulnerabilities, crashes, or serious production failures.
- MEDIUM — Can cause incorrect behavior in realistic scenarios, reliability problems, or meaningful performance issues.
- LOW — A concrete issue with limited impact that is worth addressing but should not block the PR.

## Overall status

Set `overall_status` according to the findings:

- `LOOKS_GOOD` — No HIGH or MEDIUM findings were identified. LOW findings may still be present.
- `NEEDS_ATTENTION` — One or more MEDIUM findings were identified, but no HIGH findings.
- `CHANGES_REQUIRED` — One or more HIGH findings were identified.

When `overall_status` is `LOOKS_GOOD`, the summary should explicitly say that no critical or important issues were found.

## Output

Return only valid JSON.

Do not include Markdown, code fences, explanations, or commentary outside the JSON.

Use this exact structure:
```
{
  "overall_status": "LOOKS_GOOD | NEEDS_ATTENTION | CHANGES_REQUIRED",
  "summary": "Short summary of the change and overall review result",
  "findings": [
    {
      "severity": "HIGH | MEDIUM | LOW",
      "category": "correctness | performance | concurrency | security | error-handling | testing | maintainability",
      "file": "path/to/file",
      "line": 123,
      "description": "What is wrong, the concrete failure scenario, and why it matters",
      "recommendation": "How to fix it"
    }
  ],
  "testing_gaps": [
    "Missing test scenario"
  ]
}
```
If no HIGH or MEDIUM issues are found, prefer:
```
{
  "overall_status": "LOOKS_GOOD",
  "summary": "Looks good — no critical or important issues found.",
  "findings": [],
  "testing_gaps": []
}
```
Do not invent findings just to avoid returning a clean review.


