# unicode2latex

Convert Unicode text to LaTeX and vice versa.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-285%20passing-brightgreen.svg)](unittests/)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](LICENSE.txt)

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [unicode2latex](#unicode2latex-usage)
  - [Quick Start](#quick-start)
  - [Features](#features)
  - [Command-Line Options](#command-line-options)
  - [Accent Mode](#accent-mode)
  - [Examples](#examples)
- [latex2unicode](#latex2unicode-usage)
- [LaTeX Package Requirements](#latex-package-requirements)
- [Known Limitations](#known-limitations)
- [Development](#development)
- [Testing](#testing)
- [Authors](#authors)
- [License](#license)
- [Continuous Integration](#continuous-integration)
- [Acknowledgements](#acknowledgements)
- [Contributing](#contributing)
- [Support](#support)

## Overview

`unicode2latex` converts Unicode characters to their LaTeX equivalents,
making it easy to prepare text with special characters for LaTeX documents.
The package also includes `latex2unicode` for reverse conversion.

**Key features:**
- Converts accented characters (é → `\'{e}` or `\acute{e}`)
- Handles Greek letters (α → `\alpha`)
- Converts math symbols (∫ → `\int`, ∞ → `\infty`)
- Expands ligatures (ﬃ → ffi)
- Converts fractions (⅖ → `\sfrac{2}{5}`)
- Handles subscripts and superscripts (x₁ → `x_{1}`, x² → `x^{2}`)
- Supports font modifiers (𝔸 → `\mathbb{A}`)
- Thread-safe for concurrent use

## Installation

### From PyPI (recommended)

```bash
pip install unicode2latex
```

### From source

```bash
git clone https://github.com/yourusername/unicode2latex.git
cd unicode2latex
pip install .
```

## unicode2latex Usage

### Quick Start

```bash
# Convert text directly
unicode2latex "café résumé"
# Output: caf\'{e} r\'{e}sum\'{e}

# Process a file
unicode2latex --input myfile.txt

# Read from stdin
cat myfile.txt | unicode2latex --stdin

# Use math-mode accents
unicode2latex --accent-mode=math "é"
# Output: \acute{e}
```

### Features

#### Accents

Converts both precomposed and combining accents:

| Unicode | Codepoint | LaTeX (text) | LaTeX (math) |
|---------|-----------|--------------|--------------|
| è | U+00E8 | `\`{e}` | `\grave{e}` |
| é | U+00E9 | `\'{e}` | `\acute{e}` |
| ê | U+00EA | `\^{e}` | `\hat{e}` |
| ñ | U+00F1 | `\~{n}` | `\tilde{n}` |
| ü | U+00FC | `\"{u}` | `\ddot{u}` |
| ā | U+0101 | `\={a}` | `\bar{a}` |
| Ç | U+00C7 | `\c{C}` | `\c{C}` |

Works with both single codepoints (U+00C7) and combining characters (U+0043 + U+0327).

**Multiple accents:**
```
ṩ → \.{\d{s}}
```

#### Greek Letters

| Unicode | LaTeX |
|---------|-------|
| α | `\alpha` |
| β | `\beta` |
| γ | `\gamma` |
| Δ | `\Delta` |
| θ | `\theta` |
| ϑ | `\vartheta` |
| π | `\pi` |
| Σ | `\Sigma` |

and so on...

#### Math Symbols

| Unicode | LaTeX |
|---------|-------|
| ∫ | `\int` |
| ∞ | `\infty` |
| ∩ | `\cap` |
| ∪ | `\cup` |
| ⊂ | `\subset` |
| ∈ | `\in` |
| × | `\times` |
| ÷ | `\div` |
| ≤ | `\leq` |
| ≥ | `\geq` |
| ≠ | `\neq` |
| ⇎ | `\nLeftrightarrow` |

and so on...

#### Ligatures

| Unicode | LaTeX |
|---------|-------|
| ﬁ | fi |
| ﬂ | fl |
| ﬃ | ffi |
| ﬄ | ffl |

#### Fractions

```
⅓ → \sfrac{1}{3}
⅖ → \sfrac{2}{5}
¾ → \sfrac{3}{4}
```

#### Subscripts and Superscripts

```
rₐ tᵪ → r_{a} t_{\chi}
x² y³ → x^{2} y^{3}
0⁺ → 0^{+}
```

#### Font Modifiers

| Unicode | LaTeX | Font |
|---------|-------|------|
| 𝔸 | `\mathbb{A}` | Blackboard bold |
| ⅅ | `\symbbit{D}` | Double-struck italic |
| 𝒜 | `\mathcal{A}` | Calligraphic |
| 𝔄 | `\mathfrak{A}` | Fraktur |
| 𝐀 | `\mathbf{A}` | Bold |
| 𝐴 | `\mathit{A}` | Italic |

### Command-Line Options

```
unicode2latex [OPTIONS] [text ...]
```

**Input options:**
- `text` - Text to convert (positional arguments)
- `--input FILE`, `-i FILE` - Read from file
- `--stdin`, `-s` - Read from stdin

**Output options:**
- `--output FILE`, `-o FILE` - Write to file (default: stdout)

**Conversion options:**
- `--accent-mode {text,math,auto}` - Accent output mode (default: text)
- `--no-accents` - Do not convert accents
- `--no-fonts` - Do not add font modifiers
- `--prefer-unicode-math`, `-P` - Use unicode-math commands when possible

**Other options:**
- `--verbose`, `-v` - Verbose output
- `--help`, `-h` - Show help message

### Accent Mode

The `--accent-mode` option controls how accented characters are converted:

#### Text Mode (default)

Uses standard LaTeX text-mode accent commands:

```bash
unicode2latex "café"
# Output: caf\'{e}

unicode2latex --accent-mode=text "é è ê ñ ü"
# Output: \'{e} \`{e} \^{e} \~{n} \"{u}
```

**Best for:** Regular text, paragraphs, titles

#### Math Mode

Uses LaTeX math-mode accent commands:

```bash
unicode2latex --accent-mode=math "café"
# Output: caf\acute{e}

unicode2latex --accent-mode=math "é è ê ñ ü"
# Output: \acute{e} \grave{e} \hat{e} \tilde{n} \ddot{u}
```

**Best for:** Mathematical expressions, equations

**Math mode accent mapping:**

| Text mode | Math mode |
|-----------|-----------|
| `\'` | `\acute` |
| `` \` `` | `\grave` |
| `\^` | `\hat` |
| `\~` | `\tilde` |
| `\"` | `\ddot` |
| `\=` | `\bar` |
| `\.` | `\dot` |
| `\u` | `\breve` |
| `\v` | `\check` |

#### Auto Mode (planned)

Auto-detection of context (currently defaults to text mode):

```bash
unicode2latex --accent-mode=auto "é"
# Output: \'{e} (currently defaults to text)
```

Future implementation will detect mathematical vs. text context automatically.

### Examples

#### Basic conversion

```bash
# Simple text
unicode2latex "Hello, café!"
# Output: Hello, caf\'{e}!

# Greek letters
unicode2latex "The angle θ = π/2"
# Output: The angle \theta{} = \pi{}/2

# Math symbols
unicode2latex "∫₀^∞ e^{-x} dx"
# Output: \int{}_{0}^{\infty{}} e^{-x} dx
```

#### File processing

```bash
# Convert a file
unicode2latex --input document.txt --output document.tex

# Process stdin
cat notes.txt | unicode2latex --stdin > notes.tex

# Chain with other tools
grep "café" data.txt | unicode2latex --stdin
```

#### Advanced options

```bash
# Math mode accents for equations
unicode2latex --accent-mode=math "Let á be the acceleration"
# Output: Let \acute{a} be the acceleration

# Disable accent conversion (preserve Unicode)
unicode2latex --no-accents "café"
# Output: café

# Disable font modifiers
unicode2latex --no-fonts "The set ℝ"
# Output: The set ℝ

# Prefer unicode-math package commands
unicode2latex --prefer-unicode-math "α + β"
# Output: \alpha + \beta
```

#### Combining options

```bash
# Math mode with file input
unicode2latex --accent-mode=math --input equations.txt --output equations.tex

# Process multiple files
for file in *.txt; do
    unicode2latex --input "$file" --output "${file%.txt}.tex"
done

# Verbose output for debugging
unicode2latex --verbose --input problematic.txt
```

## latex2unicode Usage

Converts LaTeX commands back to Unicode:

```bash
# Convert Greek letters
latex2unicode --greek "\\alpha \\beta \\gamma"
# Output: α β γ

# Convert math symbols
latex2unicode --math "\\int \\infty \\cap"
# Output: ∫ ∞ ∩

# Combine both
latex2unicode --greek --math "\\alpha \\cap \\beta"
# Output: α ∩ β
```

**Options:**
- `--greek`, `-G` - Convert Greek letters to Unicode
- `--math`, `-M` - Convert math symbols to Unicode
- `--input FILE`, `-i FILE` - Read from file
- `--stdin`, `-s` - Read from stdin
- `--output FILE`, `-o FILE` - Write to file

## LaTeX Package Requirements

### ASCII Output

If your output is pure ASCII, standard LaTeX is sufficient:

```latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\begin{document}
caf\'{e}
\end{document}
```

### Unicode-Math Output

For conversions using unicode-math commands (like `\symbbit{D}`), use XeLaTeX or LuaLaTeX:

```latex
\documentclass{article}
\usepackage{fontspec}
\usepackage{unicode-math}
\begin{document}
\symbbit{D}
\end{document}
```

Compile with:
```bash
xelatex document.tex
# or
lualatex document.tex
```

### Fractions

For `\sfrac` fractions, include the `xfrac` package:

```latex
\documentclass{article}
\usepackage{xfrac}
\begin{document}
\sfrac{2}{5}
\end{document}
```

### Special Symbols

Some symbols may require additional packages:

```latex
\documentclass{article}
\usepackage{amssymb}    % For \nLeftrightarrow, etc.
\usepackage{amsmath}    % For extended math support
\begin{document}
\nLeftrightarrow
\end{document}
```

## Known Limitations

### Greek Letter Context

The conversion of Greek letters is not currently differentiated inside and outside mathematical environments. All Greek letters are converted to their LaTeX command form (e.g., `\alpha`) without distinguishing between text and math mode.

### Emoji and High Unicode

Characters beyond the Basic Multilingual Plane (> U+FFFF), including emoji, are not converted and will be passed through with a warning.

### Multiple Accents

While basic multiple accents are supported (e.g., ṩ), complex combinations of multiple accents per character may not be handled optimally.

### Auto-Detection

The `--accent-mode=auto` option is planned but not yet implemented. It currently defaults to text mode.

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/unicode2latex.git
cd unicode2latex

# Install development dependencies
pip install -r requirements-test.txt

# Set up git hooks for pre-commit testing
git config --local core.hooksPath .githooks/

# Install the developed code, to check installation process
pip install -e .
```

### Project Structure

```
unicode2latex/
├── u2l.py                      # Main module
├── FakePlasTeX/                # Tokenizer for LaTeX parsing
├── unittests/                  # Test suite (285 tests)
│   ├── test_unicode2latex.py   # Unicode → LaTeX tests
│   ├── test_latex2unicode.py   # LaTeX → Unicode tests
│   ├── test_accents.py         # Accent handling tests
│   ├── test_fonts.py           # Font modifier tests
│   ├── test_bugs.py            # Bug regression tests
│   ├── test_accent_modes.py    # Accent mode feature tests
│   ├── test_cli_accent_mode.py # CLI integration tests
│   ├── test_thread_safety.py   # Concurrency tests
│   ├── test_bug5_fix.py        # Thread safety fix tests
│   └── test_bug6_investigation.py
├── BUGS.md                     # Known bugs and fixes
├── README.md                   # This file
├── pyproject.toml              # Package configuration
└── setup.cfg                   # Setup configuration
```

## Testing

The project includes a comprehensive test suite with 285 tests:

```bash
# Run all tests
python3 -m unittest discover unittests

# Run specific test file
python3 -m unittest unittests/test_unicode2latex.py

# Run with verbose output
python3 -m unittest discover unittests -v

# Run specific test
python3 -m unittest unittests.test_accents.TestAccentConversion.test_acute_accent
```

**Test coverage by category:**
- Unicode → LaTeX: 88 tests
- LaTeX → Unicode: 38 tests
- Accent handling: 40 tests (+ 35 accent mode tests)
- Font modifiers: 47 tests
- Bug regression: 29 tests
- Thread safety: 17 tests
- CLI integration: 20 tests
- Investigation: 11 tests

**All 285 tests passing** ✅

## Authors

This software is Copyright © 2023-2025
[Andrea C. G. Mennucci](https://www.sns.it/it/persona/andrea-carlo-giuseppe-mennucci)

## License

See file `LICENSE.txt` in the code distribution.

## Continuous Integration

The code is tested [using *GitHub Actions*](https://github.com/mennucc/unicode2latex/actions/workflows/test.yaml) inside an Ubuntu environment, for Python 3.8 up to 3.13 (but not yet with 3.14).

![Test results](https://github.com/mennucc/unicode2latex/actions/workflows/test.yaml/badge.svg)

## Acknowledgements

The principal author has used the Python code editor [`Wing IDE` by Wingware](http://wingware.com/) to develop this project, with a license kindly donated by WingWare.

[Claude Code](https://claude.ai/claude-code) by [Anthropic](https://www.anthropic.com/) was used to debug and enhance this package, including implementing thread safety, adding the accent mode feature, and creating comprehensive test coverage.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite (`python3 -m unittest discover unittests`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please ensure all tests pass and add new tests for new features.

## Support

For bugs and feature requests, please open an issue on the GitHub repository.

---

**Made with ❤️ for the LaTeX community**
