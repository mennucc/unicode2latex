unicode2latex
=============

convert unicode to LaTeX

This script will convert unicode to a suitable LaTeX representation.

- It will convert accents, e.g. è  → \\`e
  or ũ → \\~{u}
  or Ç  → \\c{C} .
  It will work fine   both for the single codepoint Ç that is U+00C7 ;
  and for the combining version Ç  that is  U+0043  followed by U+0327

- It will also convert multiple accents ṩ  → \\.{\\d{s}}

- It will expand ligatures ﬃ → ffi

- It will expand fractions ⅖ → \\sfrac{2}{5}
  (this needs package `xfrac`)

- It will convert small characters such as ﹦﹖

- It will convert subscripts rₐ tᵪ → r_{a} t_{\\chi}

- And superscripts  0⁺ → 0^{+}

- It will convert math symbols, e.g.  ∩ → \\cap

- It will convert greek letters ϑ → \\vartheta .

- It will express fonts, e.g.  ⅅ → \\symbbit{D} .

The aim is that the output be pure ASCII; but some characters
such as  æ  are currently not converted: in that
case the output should be compatible with standard `LaTeX`
by using `\usepackage[utf8]{inputenc}`

If instead conversions such as  `ⅅ → \\symbbit{D}`
are happening, then the resulting LaTeX code
will need `xelatex` or `lualatex` with packages
`fontspec` and `unicode-math`.

Similarly if some particular unicode are used, such
as ⇎ that will be converted to `\\nLeftrightarrow`

latex2unicode
=============
This script will convert  LaTeX to unicode.

With the --greek arguments,
  it will convert greek letters, \\alpha → 𝛼

With the --math arguments,
  it will convert math symbols, e.g.  \\cap → ∩ .

Issues
------

Currently accents are always converted using the non-math representation,
for example Ù becomes `\~u` but in math-mode it should be  `\tilde u`


Similarly the conversion of greek letters should be differentiated
 inside and outside mathematical environments.

Developing
==========

If you wish to help in developing, please

    pip -r requirements-test.txt
    git config --local core.hooksPath .githooks/

so that each commit is pre tested.

Acknowledgements
================

The principal author has used the Python code editor
[`wing8` by Wingware](http://wingware.com/)
to develop this project, with a license kindly donated
by WingWare.

[Claude Code](https://claude.ai/claude-code) by [Anthropic](https://www.anthropic.com/)
was used to debug and enhance this package.
