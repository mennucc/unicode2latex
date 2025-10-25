# Testing Guide

This document explains how to run tests for the unicode2latex package.

## Quick Start

```bash
# Run all tests with current Python version
python3 -m unittest discover unittests -v

# Run tests with tox (multiple Python versions)
tox
```

## Testing with Tox

### Installation

```bash
pip install tox
# or
pip install -r requirements-test.txt
```

### Available Tox Environments

#### Test across all Python versions (3.8-3.13)
```bash
tox
```

This will run the full test suite on Python 3.8, 3.9, 3.10, 3.11, 3.12, and 3.13 (if installed).

#### Test specific Python version
```bash
tox -e py38    # Python 3.8
tox -e py39    # Python 3.9
tox -e py310   # Python 3.10
tox -e py311   # Python 3.11
tox -e py312   # Python 3.12
tox -e py313   # Python 3.13
```

#### Run linting only
```bash
tox -e lint
```

#### Test CLI commands
```bash
tox -e cli
```

#### Run with coverage report
```bash
tox -e coverage
```

This generates:
- Terminal coverage report
- HTML coverage report in `htmlcov/`

#### Run everything (tests + CLI + linting)
```bash
tox -e all
```

### Parallel Testing

Speed up testing by running environments in parallel:

```bash
# Run all environments in parallel
tox -p auto

# Run specific environments in parallel
tox -p auto -e py310,py311,py312,py313
```

### List Available Environments

```bash
tox -l
```

## Testing Without Tox

### Run all unit tests
```bash
python3 -m unittest discover unittests -v
```

### Run specific test file
```bash
python3 -m unittest unittests/test_unicode2latex.py -v
```

### Run specific test class
```bash
python3 -m unittest unittests.test_accents.TestAccentConversion -v
```

### Run specific test method
```bash
python3 -m unittest unittests.test_accents.TestAccentConversion.test_acute_accent -v
```

## Test Coverage

The project includes 285 comprehensive tests:

- **Unicode → LaTeX**: 88 tests
- **LaTeX → Unicode**: 38 tests
- **Accent handling**: 75 tests (40 basic + 35 accent modes)
- **Font modifiers**: 47 tests
- **Bug regression**: 29 tests
- **Thread safety**: 17 tests
- **CLI integration**: 20 tests
- **Investigation**: 11 tests

## Continuous Integration

Tests run automatically on GitHub Actions for every push and pull request:

- **Platform**: Ubuntu 24.04
- **Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **Total test runs per push**: 1,710 (285 tests × 6 versions)

View test results: https://github.com/mennucc/unicode2latex/actions

## Test Requirements

### System Dependencies

Some tests require TeX Live:

```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-base texlive-latex-extra

# Fedora
sudo dnf install texlive-scheme-basic texlive-latex-extra

# macOS
brew install texlive
```

### Python Dependencies

All Python test dependencies are in `requirements-test.txt`:

```bash
pip install -r requirements-test.txt
```

## Writing Tests

Tests are located in the `unittests/` directory. To add new tests:

1. Create a new file: `unittests/test_feature.py`
2. Import unittest and the module:
   ```python
   import unittest
   import sys
   import os
   sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   from unicode2latex import u2l
   ```
3. Create test classes inheriting from `unittest.TestCase`
4. Write test methods starting with `test_`
5. Run with `python3 -m unittest unittests/test_feature.py`

## Pre-commit Hooks

To run tests before every commit:

```bash
git config --local core.hooksPath .githooks/
```

The pre-commit hook will:
- Run flake8 linting
- Run the full test suite
- Block the commit if tests fail

## Troubleshooting

### Tox can't find Python version

If tox reports "InterpreterNotFound":

```bash
# Install missing Python versions or skip them
tox --skip-missing-interpreters
```

### Tests fail with "kpsewhich not found"

Install TeX Live (see System Dependencies above).

### Import errors

Make sure the package is installed:

```bash
pip install -e .
```

## Performance

Typical test execution times:

- Single Python version: ~2-3 seconds
- All 6 versions (sequential): ~15-20 seconds
- All 6 versions (parallel): ~5-8 seconds
- With coverage: ~3-4 seconds

## Validation Scripts

The project includes validation scripts in `local/`:

```bash
# Validate YAML syntax
local/test-yaml .github/workflows/test.yaml

# Validate tox.ini syntax
local/test-tox-ini tox.ini
```
