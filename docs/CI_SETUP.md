# CI Setup for Agentic Projects

This document outlines the continuous integration (CI) setup for the core Agentic projects: `agentic-core`, `agentic-issues`, and `agentic-notes`. Each project should implement these CI workflows to ensure code quality and reliability.

## GitHub Actions Workflow Files

For each project, create a `.github/workflows` directory and add the following workflow files:

### 1. Python Tests Workflow (`python-tests.yml`)

This workflow runs linting and tests on every push and pull request.

```yaml
name: Python Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install uv
        uv venv .venv
        source .venv/bin/activate
        uv pip install -e .
        uv pip install pytest pytest-cov flake8
    - name: Lint with flake8
      run: |
        source .venv/bin/activate
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test with pytest
      run: |
        source .venv/bin/activate
        pytest tests/ --cov=src/ --cov-report=xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
```

### 2. Package Publishing Workflow (`publish-package.yml`)

This workflow publishes the package to PyPI when a new release is created.

```yaml
name: Publish Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build and publish
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python -m build
        twine upload dist/*
```

### 3. Security Scanning Workflow (`security-scan.yml`)

This workflow runs security scans on the codebase.

```yaml
name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Run weekly on Sundays

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install bandit safety
    - name: Run bandit
      run: |
        bandit -r src/ -f json -o bandit-results.json
    - name: Run safety
      run: |
        safety check
```

## Implementation Steps

For each project (`agentic-core`, `agentic-issues`, `agentic-notes`):

1. Create the `.github/workflows` directory:
   ```bash
   mkdir -p .github/workflows
   ```

2. Create each workflow file:
   ```bash
   cp /path/to/python-tests.yml .github/workflows/
   cp /path/to/publish-package.yml .github/workflows/
   cp /path/to/security-scan.yml .github/workflows/
   ```

3. Customize the workflow files as needed for each project's specific requirements.

4. Add the necessary GitHub secrets:
   - `PYPI_USERNAME`: Your PyPI username
   - `PYPI_PASSWORD`: Your PyPI API token

## Additional Configuration

### Code Coverage with Codecov

1. Sign up for [Codecov](https://codecov.io/) and connect your GitHub repository.
2. Add a `.codecov.yml` file to the root of your project:
   ```yaml
   coverage:
     precision: 2
     round: down
     range: "70...100"
   
   parsers:
     gcov:
       branch_detection:
         conditional: yes
         loop: yes
         method: no
         macro: no
   
   comment:
     layout: "reach,diff,flags,files,footer"
     behavior: default
     require_changes: no
   ```

### Dependency Management

1. Ensure your `pyproject.toml` file includes development and test dependencies:
   ```toml
   [project.optional-dependencies]
   dev = [
     "black",
     "flake8",
     "isort",
   ]
   test = [
     "pytest",
     "pytest-cov",
     "pytest-mock",
   ]
   ```

## Best Practices

1. **Run Tests Locally**: Before pushing changes, run tests locally to catch issues early.
2. **Keep Dependencies Updated**: Regularly update dependencies to address security vulnerabilities.
3. **Monitor CI Results**: Regularly check CI results and address failures promptly.
4. **Add Badges**: Add CI status badges to your README.md file to show build status.

## Example README Badges

Add these badges to your README.md file:

```markdown
[![Python Tests](https://github.com/agentic-framework/agentic-core/actions/workflows/python-tests.yml/badge.svg)](https://github.com/agentic-framework/agentic-core/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/agentic-framework/agentic-core/branch/main/graph/badge.svg)](https://codecov.io/gh/agentic-framework/agentic-core)
[![PyPI version](https://badge.fury.io/py/agentic-core.svg)](https://badge.fury.io/py/agentic-core)
```

Adjust the repository names for each project.
