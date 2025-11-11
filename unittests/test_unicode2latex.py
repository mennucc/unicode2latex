#!/usr/bin/env python3
"""
Unit tests for unicode2latex conversion functionality.
"""

import unittest
import sys
import os

# Add parent directory to path to from unicode2latex import u2l
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unicode2latex import u2l


class TestBasicUnicode2Latex(unittest.TestCase):
    """Test basic unicode to latex conversions."""

    def test_simple_ascii(self):
        """Test that ASCII text passes through unchanged."""
        result = u2l.uni2tex("hello world")
        self.assertEqual(result, "hello world")

    def test_simple_ascii_numbers(self):
        """Test ASCII numbers and punctuation."""
        result = u2l.uni2tex("123 + 456 = 579")
        self.assertEqual(result, "123 + 456 = 579")


class TestMathSymbols(unittest.TestCase):
    """Test mathematical symbol conversions."""

    def test_times_symbol(self):
        """Test multiplication symbol × → \\times."""
        result = u2l.uni2tex("a × b")
        self.assertIn("\\times", result)

    def test_infinity_symbol(self):
        """Test infinity symbol ∞ → \\infty."""
        result = u2l.uni2tex("∞")
        self.assertIn("\\infty", result)

    def test_subset_symbol(self):
        """Test subset symbol ⊂ → \\subset."""
        result = u2l.uni2tex("A ⊂ B")
        self.assertIn("\\subset", result)

    def test_element_symbol(self):
        """Test element symbol ∈ → \\in."""
        result = u2l.uni2tex("x ∈ ℝ")
        self.assertIn("\\in", result)

    def test_cap_symbol(self):
        """Test intersection symbol ∩ → \\cap."""
        result = u2l.uni2tex("A ∩ B")
        self.assertIn("\\cap", result)

    def test_integral_symbol(self):
        """Test integral symbol ∫ → \\int."""
        result = u2l.uni2tex("∫")
        self.assertIn("\\int", result)

    def test_em_dash(self):
        """Test em dash — → ---."""
        result = u2l.uni2tex("text — more text")
        self.assertIn("---", result)

    def test_circ_operator(self):
        """Test circ operator ∘ → \\circ."""
        result = u2l.uni2tex("f ∘ g")
        self.assertIn("\\circ", result)


class TestGreekLetters(unittest.TestCase):
    """Test Greek letter conversions."""

    def test_lowercase_alpha(self):
        """Test lowercase Greek alpha α → \\alpha."""
        result = u2l.uni2tex("α")
        self.assertIn("\\alpha", result)

    def test_lowercase_beta(self):
        """Test lowercase Greek beta β → \\beta."""
        result = u2l.uni2tex("β")
        self.assertIn("\\beta", result)

    def test_lowercase_gamma(self):
        """Test lowercase Greek gamma γ → \\gamma."""
        result = u2l.uni2tex("γ")
        self.assertIn("\\gamma", result)

    def test_lowercase_delta(self):
        """Test lowercase Greek delta δ → \\delta."""
        result = u2l.uni2tex("δ")
        self.assertIn("\\delta", result)

    def test_uppercase_gamma(self):
        """Test uppercase Greek Gamma Γ → \\Gamma."""
        result = u2l.uni2tex("Γ")
        self.assertIn("\\Gamma", result)

    def test_uppercase_delta(self):
        """Test uppercase Greek Delta Δ → \\Delta."""
        result = u2l.uni2tex("Δ")
        self.assertIn("\\Delta", result)

    def test_uppercase_omega(self):
        """Test uppercase Greek Omega Ω → \\Omega."""
        result = u2l.uni2tex("Ω")
        self.assertIn("\\Omega", result)


class TestAccents(unittest.TestCase):
    """Test accent conversions."""

    def test_grave_accent(self):
        """Test grave accent è → \\`{e}."""
        result = u2l.uni2tex("è")
        self.assertIn("\\`", result)
        self.assertIn("e", result)

    def test_acute_accent(self):
        """Test acute accent é → \\'{e}."""
        result = u2l.uni2tex("é")
        self.assertIn("\\'", result)
        self.assertIn("e", result)

    def test_circumflex_accent(self):
        """Test circumflex ê → \\^{e}."""
        result = u2l.uni2tex("ê")
        self.assertIn("\\^", result)
        self.assertIn("e", result)

    def test_tilde_accent(self):
        """Test tilde ñ → \\~{n}."""
        result = u2l.uni2tex("ñ")
        self.assertIn("\\~", result)
        self.assertIn("n", result)

    def test_umlaut_accent(self):
        """Test umlaut ü → \\"{u}."""
        result = u2l.uni2tex("ü")
        self.assertIn('\\"', result)
        self.assertIn("u", result)

    def test_no_accents_mode(self):
        """Test with accent conversion disabled."""
        result = u2l.uni2tex("è", convert_accents=False)
        self.assertEqual(result, "è")


class TestSuperscriptSubscript(unittest.TestCase):
    """Test superscript and subscript conversions."""

    def test_superscript(self):
        """Test superscript characters."""
        result = u2l.uni2tex("x⁰")
        self.assertIn("^", result)
        self.assertIn("0", result)

    def test_subscript(self):
        """Test subscript characters."""
        result = u2l.uni2tex("x₀")
        self.assertIn("_", result)
        self.assertIn("0", result)


class TestFractions(unittest.TestCase):
    """Test fraction conversions."""

    def test_one_quarter(self):
        """Test ¼ → \\sfrac{1}{4}."""
        result = u2l.uni2tex("¼")
        self.assertIn("sfrac", result)
        self.assertIn("1", result)
        self.assertIn("4", result)

    def test_one_half(self):
        """Test ½ → \\sfrac{1}{2}."""
        result = u2l.uni2tex("½")
        self.assertIn("sfrac", result)
        self.assertIn("1", result)
        self.assertIn("2", result)

    def test_three_quarters(self):
        """Test ¾ → \\sfrac{3}{4}."""
        result = u2l.uni2tex("¾")
        self.assertIn("sfrac", result)
        self.assertIn("3", result)
        self.assertIn("4", result)


class TestFontModifiers(unittest.TestCase):
    """Test font modifier conversions."""

    def test_bold_letter(self):
        """Test bold letter conversion."""
        result = u2l.uni2tex("𝐀")  # MATHEMATICAL BOLD CAPITAL A
        self.assertIn("\\symbf", result)
        self.assertIn("A", result)

    def test_italic_letter(self):
        """Test italic letter conversion."""
        result = u2l.uni2tex("𝐴")  # MATHEMATICAL ITALIC CAPITAL A
        self.assertIn("\\symit", result)
        self.assertIn("A", result)

    def test_double_struck(self):
        """Test double-struck (blackboard bold) conversion."""
        result = u2l.uni2tex("ℝ")  # DOUBLE-STRUCK CAPITAL R
        self.assertIn("\\symbb", result)
        self.assertIn("R", result)

    def test_script_letter(self):
        """Test script letter conversion."""
        result = u2l.uni2tex("𝒜")  # MATHEMATICAL SCRIPT CAPITAL A
        self.assertIn("\\symscr", result)
        self.assertIn("A", result)

    def test_fraktur_letter(self):
        """Test fraktur letter conversion."""
        result = u2l.uni2tex("𝔄")  # MATHEMATICAL FRAKTUR CAPITAL A
        self.assertIn("\\symfrak", result)
        self.assertIn("A", result)

    def test_no_fonts_mode(self):
        """Test with font conversion disabled."""
        result = u2l.uni2tex("𝐀", add_font_modifiers=False)
        # Should just convert to base letter
        self.assertIn("A", result)
        self.assertNotIn("\\symbf", result)


class TestSmartQuotes(unittest.TestCase):
    """Test conversion of Unicode smart quotes to TeX-friendly ASCII."""

    def test_single_curly_quotes(self):
        result = u2l.uni2tex("‘quoted’ text", convert_quotes=True)
        self.assertEqual(result, "`quoted' text")

    def test_double_curly_quotes(self):
        result = u2l.uni2tex("“quoted” text", convert_quotes=True)
        self.assertEqual(result, "``quoted'' text")


class TestDashConversion(unittest.TestCase):
    """Test conversion of dashes and thin spaces to ASCII equivalents."""

    def test_basic_unicode_dashes(self):
        self.assertEqual(u2l.uni2tex("‐", convert_dashes=True), "-")
        self.assertEqual(u2l.uni2tex("–", convert_dashes=True), "--")
        self.assertEqual(u2l.uni2tex("—", convert_dashes=True), "---")

    def test_nbsp_to_tilde(self):
        self.assertEqual(u2l.uni2tex("A\u00A0B", convert_dashes=True), "A~B")

    def test_space_like_characters(self):
        text = "\u2002\u2003\u2009\u202F"
        result = u2l.uni2tex(text, convert_dashes=True)
        self.assertEqual(result, "    ")  # four regular spaces


class TestDecomposeToTexClass(unittest.TestCase):
    """Test the Decompose_to_tex class directly."""

    def test_char_method(self):
        """Test the char method."""
        decomposer = u2l.Decompose_to_tex()
        decomposer.char("α")
        result = decomposer.result
        self.assertIn("\\alpha", result)

    def test_parse_method(self):
        """Test the parse method."""
        decomposer = u2l.Decompose_to_tex()
        decomposer.parse("α β γ")
        result = decomposer.result
        self.assertIn("\\alpha", result)
        self.assertIn("\\beta", result)
        self.assertIn("\\gamma", result)

    def test_extra_unicode2latex(self):
        """Test updating extra unicode mappings."""
        decomposer = u2l.Decompose_to_tex()
        # Add a custom mapping
        decomposer.update_extra({0x263A: "\\smiley"})
        decomposer.parse("☺")
        result = decomposer.result
        self.assertIn("\\smiley", result)

    def test_prefer_unicode_math(self):
        """Test prefer_unicode_math flag."""
        decomposer = u2l.Decompose_to_tex(prefer_unicode_math=True)
        decomposer.parse("×")
        result = decomposer.result
        self.assertIn("\\times", result)


class TestComplexExpressions(unittest.TestCase):
    """Test complex mathematical expressions."""

    def test_expression_with_greek_and_math(self):
        """Test expression with Greek letters and math symbols."""
        result = u2l.uni2tex("α ∈ ℝ")
        self.assertIn("\\alpha", result)
        self.assertIn("\\in", result)
        self.assertIn("\\symbb", result)

    def test_expression_with_accents_and_greek(self):
        """Test expression mixing accents and Greek."""
        result = u2l.uni2tex("café α")
        self.assertIn("caf", result)
        self.assertIn("\\alpha", result)

    def test_mixed_super_sub_script(self):
        """Test mixed superscripts and subscripts."""
        result = u2l.uni2tex("x₁²")
        self.assertIn("_", result)
        self.assertIn("^", result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_empty_string(self):
        """Test empty string input."""
        result = u2l.uni2tex("")
        self.assertEqual(result, "")

    def test_whitespace_only(self):
        """Test whitespace-only input."""
        result = u2l.uni2tex("   ")
        self.assertEqual(result, "   ")

    def test_newlines(self):
        """Test newlines are preserved."""
        result = u2l.uni2tex("line1\nline2")
        self.assertIn("\n", result)

    def test_tabs(self):
        """Test tabs are preserved."""
        result = u2l.uni2tex("a\tb")
        self.assertIn("\t", result)


if __name__ == '__main__':
    unittest.main()
