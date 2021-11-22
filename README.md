# unicode2latex
convert unicode to LaTeX and vice versa

This script will convert unicode to a suitable LaTeX representation.

It will convert accents, e.g. è  → \`{e} .

It will expand ligatures ﬃ → ffi

It will expand fractions ⅖ → \sfrac{2}{5}
(this needs package `xfrac`)

It will convert math symbols, e.g.  ∩ → \cap

It will convert greek letters ϑ → \vartheta .

It will express fonts, e.g.  ⅅ → \symbbit{D} .

Note that in this latter case the resulting LaTeX code
will need `xelatex` or `lualatex` with packages
`fontspec` and `unicode-math`.
