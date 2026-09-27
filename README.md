Local Development Setup
Prerequisites
Python 3.11+
# PRLens


PRLens is an AI-powered pull request review tool designed to analyze code changes, identify potential issues, and suggest testing improvements.


The project is being built with a **model-agnostic architecture**, allowing different LLM providers to be used without coupling the review engine to a specific model.


## Goals


PRLens aims to provide:


- Automated pull request analysis
- Structured code review findings
- Detection of correctness, performance, concurrency, security, and error-handling issues
- Suggested testing improvements
- Repository-aware review context
- Support for multiple LLM providers
- GitHub workflow integration
- Model Context Protocol (MCP) integration


## Planned Workflow


```text
GitHub Pull Request
        |
        v
Fetch PR Metadata + Diff
        |
        v
Gather Repository Context
        |
        v
AI Review Engine
        |
        v
Structured Review
        |
        +-- Potential Issues
        +-- Testing Gaps
        +-- Recommendations
```


## Project Status


PRLens is currently under active development.


### Phase 1 — Core PR Reviewer


- [ ] CLI
- [ ] GitHub PR URL parsing
- [ ] GitHub API integration
- [ ] PR diff retrieval
- [ ] Diff parsing
- [ ] Model-agnostic LLM provider interface
- [ ] Initial LLM provider
- [ ] Structured review output
- [ ] Unit tests


### Phase 2 — Repository-Aware Reviews


- [ ] Retrieve related source files
- [ ] Search repository context
- [ ] Identify related tests
- [ ] Provide repository context to the review engine
- [ ] Configurable review rules


### Phase 3 — Agentic & GitHub Integration


- [ ] MCP server
- [ ] Repository tools exposed through MCP
- [ ] GitHub Actions integration
- [ ] Automated PR reviews
- [ ] Inline review comments


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


Verify that the virtual environment is being used.


For Git Bash, macOS, or Linux:


```bash
which python
python --version
python -m pip --version
```


For PowerShell:


```powershell
Get-Command python
python --version
python -m pip --version
```


### Install the Project


Once the virtual environment is active:


```bash
python -m pip install -e .
```


The `-e` flag installs PRLens in **editable mode**, allowing changes under `src/` to be used without reinstalling the package after every modification.


### Deactivate the Virtual Environment


```bash
deactivate
```


When returning to the project later on Windows with Git Bash:


```bash
cd prlens
source .venv/Scripts/activate
```


## Project Structure


```text
prlens/
├── .gitignore
├── README.md
├── pyproject.toml
└── src/
    └── prlens/
        ├── __init__.py
        └── cli.py
```


The project structure will expand as GitHub integration, LLM providers, review models, and repository-aware tooling are implemented.


## Design Principles


### Model Agnostic


The core review engine should not depend directly on a specific LLM provider. Provider-specific integrations will implement a common interface.


### Structured Reviews


LLM responses will be converted into structured findings rather than returned as unrestricted text.


### Evidence-Based Findings


Reviews should focus on issues supported by concrete evidence in the code and avoid speculative findings.


### Extensible


GitHub integration, repository context, LLM providers, and MCP tooling will remain separate components so they can evolve independently.


## License


A license has not yet been selected.
Git
Clone the repository
git clone git@github.com:ssarfare/prlens.git
cd prlens
PRLens
PRLens is an AI-powered pull request review tool designed to analyze code changes, identify potential issues, and suggest testing improvements.
The project is being built with a model-agnostic architecture so that different LLM providers can be used without coupling the review engine to a specific model.
Goals
PRLens aims to provide:
Automated pull request analysis
Structured code review findings
Detection of correctness, performance, concurrency, security, and error-handling issues
Suggested testing improvements
Repository-aware review context
Support for multiple LLM providers
GitHub workflow integration
Model Context Protocol (MCP) integration
Planned Workflow
GitHub Pull Request
        |
        v
Fetch PR Metadata + Diff
        |
        v
Gather Repository Context
        |
        v
AI Review Engine
        |
        v
Structured Review
        |
        +-- Potential Issues
        +-- Testing Gaps
        +-- Recommendations

Project Status
PRLens is currently under active development.
Phase 1 — Core PR Reviewer
CLI
GitHub PR URL parsing
GitHub API integration
PR diff retrieval
Diff parsing
Model-agnostic LLM provider interface
Initial LLM provider
Structured review output
Unit tests
Phase 2 — Repository-Aware Reviews
Retrieve related source files
Search repository context
Identify related tests
Provide repository context to the review engine
Configurable review rules
Phase 3 — Agentic & GitHub Integration
MCP server
Repository tools exposed through MCP
GitHub Actions integration
Automated PR reviews
Inline review comments
Local Development
Prerequisites
Python 3.11+
Git
Clone the Repository
Using SSH:
git clone git@github.com:ssarfare/prlens.git
cd prlens

Create a Virtual Environment
python -m venv .venv

Activate the Virtual Environment
Windows — Git Bash
source .venv/Scripts/activate

Windows — PowerShell
.\.venv\Scripts\Activate.ps1

Windows — Command Prompt
.venv\Scripts\activate.bat

macOS / Linux
source .venv/bin/activate

After activation, the terminal prompt should include:
(.venv)

Verify that the virtual environment is being used:
Git Bash / macOS / Linux
which python
python --version
python -m pip --version

PowerShell
Get-Command python
python --version
python -m pip --version

Install the Project
Once the virtual environment is active:
python -m pip install -e .

The -e flag installs PRLens in editable mode, allowing changes under src/ to be used without reinstalling the package after every modification.
Deactivate the Virtual Environment
deactivate

When returning to the project later on Windows with Git Bash:
cd prlens
source .venv/Scripts/activate

Project Structure
prlens/
├── .gitignore
├── README.md
├── pyproject.toml
└── src/
    └── prlens/
        ├── __init__.py
        └── cli.py

The project structure will expand as GitHub integration, LLM providers, review models, and repository-aware tooling are implemented.
Design Principles
Model Agnostic
The core review engine should not depend directly on a specific LLM provider. Provider-specific integrations will implement a common interface.
Structured Reviews
LLM responses will be converted into structured findings rather than returned as unrestricted text.
Evidence-Based Findings
Reviews should focus on issues supported by concrete evidence in the code and avoid speculative findings.
Extensible
GitHub integration, repository context, LLM providers, and MCP tooling will remain separate components so they can evolve independently.
License
A license has not yet been selected.

Create a virtual environment
python -m venv .venv

Activate the virtual environment
Windows — Git Bash
source .venv/Scripts/activate

Windows — PowerShell
.\.venv\Scripts\Activate.ps1

macOS / Linux
source .venv/bin/activate

After activation, your terminal should show (.venv).
Verify that Python is running from the virtual environment:
which python
python --version
python -m pip --version

Deactivate the virtual environment
When you're finished working on the project:
deactivate

To work on PRLens again later, navigate to the repository and reactivate the environment:
cd prlens
source .venv/Scripts/activate



