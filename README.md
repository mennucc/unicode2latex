unicode2latex
=============

convert unicode to LaTeX

This script will convert unicode to a suitable LaTeX representation.

- It will convert accents, e.g. è  → \`e 
  or Ç  → \c{C} .
  It will work fine   both the single codepoint Ç that is U+00C7 ;
  and the combining version Ç  that is  U+0043  followed by U+0327

- It will also convert multiple accents ṩ  → \.{\d{s}}

- It will expand ligatures ﬃ → ffi

- It will expand fractions ⅖ → \sfrac{2}{5}
  (this needs package `xfrac`)

- It will convert small characters such as ﹦﹖

- It will convert subscripts rₐ tᵪ → r_{a} t_{\chi}

- And superscripts  0⁺ → 0^{+}

- It will convert math symbols, e.g.  ∩ → \cap

- It will convert greek letters ϑ → \vartheta .

- It will express fonts, e.g.  ⅅ → \symbbit{D} .

The aim is that the output be pure ASCII; but some characters
such as  æ  are currently not converted: in that
case the output should be compatible with standard `LaTeX`
by using `\usepackage[utf8]{inputenc}`

If instead conversions such as  `ⅅ → \symbbit{D}`
are happening, then the resulting LaTeX code
will need `xelatex` or `lualatex` with packages
`fontspec` and `unicode-math`.

Similarly if some particular unicode are used, such
as ⇎ that will be converted to `\nLeftrightarrow`

latex2unicode
=============
convert LaTeX to unicode

TODO

