# PRLens

PRLens is an AI-powered pull request review tool that analyzes code changes, identifies potential issues, and highlights missing test coverage before code is merged.

PRLens is built with a **model-agnostic architecture** using LiteLLM, allowing reviews to run against different LLM providers without coupling the application to a specific model.

## Features

- Fetch pull requests directly from GitHub
- Parse changed files and diff sections
- Review code using configurable LLM providers
- Estimate token usage before sending code to a model
- Require confirmation before running an interactive review
- Produce structured, schema-validated review results
- Categorize findings by severity and type
- Identify potential testing gaps
- Provide consistent review output across different models
- Validate changes through automated CI, linting, formatting, and tests

## How It Works

```text
GitHub Pull Request
        |
        v
Fetch PR Metadata + Diff
        |
        v
Parse Changed Files
        |
        v
Load Review Skill
        |
        v
Build Review Prompt
        |
        v
Estimate Token Usage
        |
        v
Confirm Review
        |
        v
LiteLLM
        |
        +-------------------------+
        |            |            |
        v            v            v
     Gemini        Claude        GPT
        |
        v
Structured Review
        |
        +-- Overall Status
        +-- Findings
        +-- Testing Gaps
        +-- Recommendations
```

## Review Output

PRLens produces structured findings rather than relying on arbitrary model-generated formatting.

Each review contains:

- Overall review status
- Summary of the changes
- Findings with severity and category
- File and line information
- Description of the concrete issue
- Recommended fix
- Missing test scenarios

Example:

```text
⚠️ NEEDS ATTENTION

Summary
-------
Adds explicit API key support but lacks validation coverage.

Findings
--------

🟠 MEDIUM | testing | openai/api_resources/moderation.py:25

The new api_key path is not covered by tests.

💡 Add a unit test verifying explicit API key propagation.

🧪 Testing Gaps
---------------
- Explicit API key propagation
```

## Review Philosophy

PRLens is designed to prioritize high-confidence findings over review volume.

Reviews follow these principles:

- Only report issues supported by concrete evidence in the changed code
- Avoid speculative findings
- Avoid stylistic preferences unless they create a real engineering problem
- Do not report issues already handled correctly
- Prefer fewer high-confidence findings over many weak findings
- Identify the specific changed file and line for each finding
- Explain the concrete failure scenario
- Do not invent findings when a pull request looks correct

## Project Status

PRLens is under active development.

### Phase 1 — Core PR Reviewer

- [x] CLI
- [x] GitHub PR URL parsing
- [x] GitHub API integration
- [x] PR metadata retrieval
- [x] PR diff retrieval
- [x] Structured diff parsing
- [x] Model-agnostic LLM integration
- [x] Review skill support
- [x] Token estimation before review
- [x] Structured review models
- [x] Schema validation of model responses
- [x] Consistent CLI review rendering
- [x] Unit tests
- [x] CI linting, formatting, and testing
- [ ] Graceful provider error handling

### Phase 2 — Repository-Aware Reviews

- [ ] Retrieve related source files
- [ ] Search repository context
- [ ] Identify related tests
- [ ] Analyze code outside the PR diff when additional context is required
- [ ] Configurable review rules
- [ ] Multiple review skills

### Phase 3 — Automated & Agentic Reviews

- [ ] GitHub Actions review integration
- [ ] Automated reviews when pull requests are opened or updated
- [ ] Inline GitHub review comments
- [ ] Token and cost budgets for automated reviews
- [ ] MCP server
- [ ] Repository tools exposed through MCP
- [ ] Agent-driven repository exploration

## Local Development

### Prerequisites

- Python 3.11+
- Git

### Clone the Repository

Using SSH:

```bash
git clone git@github.com:ssarfare/prlens.git
cd prlens
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

#### Windows — Git Bash

```bash
source .venv/Scripts/activate
```

#### Windows — PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

#### Windows — Command Prompt

```cmd
.venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

After activation, the terminal prompt should include:

```text
(.venv)
```

Verify that the virtual environment is being used:

#### Git Bash / macOS / Linux

```bash
which python
python --version
python -m pip --version
```

#### PowerShell

```powershell
Get-Command python
python --version
python -m pip --version
```

### Install PRLens

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

The `-e` flag installs PRLens in editable mode, allowing changes under `src/` to be used without reinstalling the package after every modification.

### Deactivate the Virtual Environment

```bash
deactivate
```

When returning to the project later on Windows using Git Bash:

```bash
cd prlens
source .venv/Scripts/activate
```

## Model Providers

PRLens uses [LiteLLM](https://github.com/BerriAI/litellm) to provide a model-agnostic interface to different LLM providers.

The model is selected at runtime using the `--model` option rather than being hardcoded into PRLens.

Examples:

```bash
prlens review <PR_URL> --model gemini/<model>
```

```bash
prlens review <PR_URL> --model anthropic/<model>
```

```bash
prlens review <PR_URL> --model openai/<model>
```

Provider availability, model names, authentication requirements, and pricing depend on the selected provider.

## API Keys

Set the environment variable required by the model provider before running a review.

For example, when using Gemini:

```bash
export GEMINI_API_KEY="your-api-key"
```

For Anthropic:

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

API keys should never be committed to the repository.

## Usage

Run PRLens with a GitHub pull request URL and the model you want to use:

```bash
prlens review https://github.com/owner/repository/pull/123 \
  --model gemini/<model>
```

PRLens will:

1. Parse the GitHub pull request URL
2. Fetch pull request metadata
3. Retrieve the raw Git diff
4. Parse changed files and diff sections
5. Load the configured review skill
6. Build the review prompt
7. Estimate input token usage
8. Display the selected model and token estimate
9. Ask for confirmation
10. Send the review to the selected model
11. Validate the response against the PRLens review schema
12. Render the structured review

Example:

```text
Title: Fix cache fallback handling
Author: developer
State: open
Changed files: 3

Changed files parsed: 3
- src/cache.py (2 diff section(s))
- src/service.py (1 diff section(s))
- tests/test_cache.py (2 diff section(s))

Model: gemini/<model>
Estimated input tokens: 2,840

Continue with review? [y/N]: y
```

## Review Skills

Review behavior is defined through skill files rather than being hardcoded into the LLM client.

The default review skill is:

```text
src/prlens/skills/general_review.md
```

The general review evaluates changed code for:

- Correctness
- Bugs
- Error handling
- Performance
- Concurrency
- Security
- Missing tests

This separation allows additional review modes to be introduced later without changing the model integration.

Planned examples include:

```text
general_review.md
security_review.md
performance_review.md
testing_review.md
```

## Token Estimation

Before sending code to an LLM, PRLens estimates the number of input tokens required for the review.

Example:

```text
Model: gemini/<model>
Estimated input tokens: 8,421
Continue with review? [y/N]:
```

This allows users to understand the approximate request size before making an API call.

Future automated reviews will use the same mechanism to enforce configurable token and cost budgets.

## Development

### Formatting

Format the project using Ruff:

```bash
ruff format .
```

Check formatting without modifying files:

```bash
ruff format --check .
```

### Linting

Run Ruff:

```bash
ruff check .
```

Automatically apply safe fixes:

```bash
ruff check . --fix
```

### Testing

Run the complete test suite:

```bash
pytest
```

Before pushing changes, run:

```bash
ruff format .
ruff check .
pytest
```

## Continuous Integration

GitHub Actions automatically validates changes by running:

```text
Formatting
    |
    v
Linting
    |
    v
Unit Tests
```

The CI workflow runs on pull requests and changes to `main`.

## Project Structure

```text
prlens/
├── .github/
│   └── workflows/
│       └── test.yml
├── src/
│   └── prlens/
│       ├── __init__.py
│       ├── cli.py
│       ├── diff_parser.py
│       ├── github_client.py
│       ├── llm_client.py
│       ├── prompt_builder.py
│       ├── review_models.py
│       ├── token_estimator.py
│       └── skills/
│           └── general_review.md
├── tests/
├── .gitignore
├── README.md
└── pyproject.toml
```

## Design Principles

### Model Agnostic

PRLens does not directly depend on a specific LLM provider. LiteLLM provides the model abstraction while PRLens owns the review workflow and domain models.

### Structured Reviews

Model responses are validated against PRLens-owned schemas using Pydantic instead of relying on arbitrary free-form text.

### Evidence-Based Findings

Reviews prioritize concrete issues demonstrated by the code changes and avoid speculative or low-confidence findings.

### Cost Awareness

Token usage is estimated before interactive model calls and will eventually be used to enforce budgets for automated reviews.

### Separation of Review Policy and Model Integration

Review instructions live in skill files, while model communication remains separate. This allows review behavior to evolve independently from model providers.

### Extensible

GitHub integration, diff parsing, review skills, model access, repository context, and future MCP tooling remain separate components so they can evolve independently.

## Roadmap

Near-term development will focus on:

1. Graceful handling of provider failures and rate limits
2. Repository-aware code review
3. Additional review skills
4. Automated GitHub pull request reviews
5. Inline review comments
6. Review token and cost budgets
7. MCP-based repository tooling
8. Agent-driven repository exploration

## License

A license has not yet been selected.




