#!/usr/bin/env python3
"""
Unit tests for font modifier handling in unicode2latex.
"""

import unittest
import sys
import os

# Add parent directory to path to import u2l
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import u2l


class TestBoldFont(unittest.TestCase):
    """Test bold font conversions."""

    def test_bold_capital_a(self):
        """Test bold capital A: 𝐀 → \\symbf{A}."""
        result = u2l.uni2tex("𝐀")
        self.assertIn("\\symbf", result)
        self.assertIn("A", result)

    def test_bold_capital_z(self):
        """Test bold capital Z: 𝐙 → \\symbf{Z}."""
        result = u2l.uni2tex("𝐙")
        self.assertIn("\\symbf", result)
        self.assertIn("Z", result)

    def test_bold_lowercase_a(self):
        """Test bold lowercase a: 𝐚 → \\symbf{a}."""
        result = u2l.uni2tex("𝐚")
        self.assertIn("\\symbf", result)
        self.assertIn("a", result)

    def test_bold_lowercase_z(self):
        """Test bold lowercase z: 𝐳 → \\symbf{z}."""
        result = u2l.uni2tex("𝐳")
        self.assertIn("\\symbf", result)
        self.assertIn("z", result)


class TestItalicFont(unittest.TestCase):
    """Test italic font conversions."""

    def test_italic_capital_a(self):
        """Test italic capital A: 𝐴 → \\symit{A}."""
        result = u2l.uni2tex("𝐴")
        self.assertIn("\\symit", result)
        self.assertIn("A", result)

    def test_italic_lowercase_a(self):
        """Test italic lowercase a: 𝑎 → \\symit{a}."""
        result = u2l.uni2tex("𝑎")
        self.assertIn("\\symit", result)
        self.assertIn("a", result)


class TestBoldItalicFont(unittest.TestCase):
    """Test bold italic font conversions."""

    def test_bold_italic_capital_a(self):
        """Test bold italic capital A: 𝑨 → \\symbfit{A}."""
        result = u2l.uni2tex("𝑨")
        self.assertIn("\\symbfit", result)
        self.assertIn("A", result)

    def test_bold_italic_lowercase_a(self):
        """Test bold italic lowercase a: 𝒂 → \\symbfit{a}."""
        result = u2l.uni2tex("𝒂")
        self.assertIn("\\symbfit", result)
        self.assertIn("a", result)


class TestDoubleStruckFont(unittest.TestCase):
    """Test double-struck (blackboard bold) font conversions."""

    def test_double_struck_r(self):
        """Test double-struck R: ℝ → \\symbb{R}."""
        result = u2l.uni2tex("ℝ")
        self.assertIn("\\symbb", result)
        self.assertIn("R", result)

    def test_double_struck_c(self):
        """Test double-struck C: ℂ → \\symbb{C}."""
        result = u2l.uni2tex("ℂ")
        self.assertIn("\\symbb", result)
        self.assertIn("C", result)

    def test_double_struck_n(self):
        """Test double-struck N: ℕ → \\symbb{N}."""
        result = u2l.uni2tex("ℕ")
        self.assertIn("\\symbb", result)
        self.assertIn("N", result)

    def test_double_struck_q(self):
        """Test double-struck Q: ℚ → \\symbb{Q}."""
        result = u2l.uni2tex("ℚ")
        self.assertIn("\\symbb", result)
        self.assertIn("Q", result)

    def test_double_struck_z(self):
        """Test double-struck Z: ℤ → \\symbb{Z}."""
        result = u2l.uni2tex("ℤ")
        self.assertIn("\\symbb", result)
        self.assertIn("Z", result)

    def test_double_struck_one(self):
        """Test double-struck digit 1: 𝟙 → \\symbb{1}."""
        result = u2l.uni2tex("𝟙")
        self.assertIn("\\symbb", result)
        self.assertIn("1", result)


class TestScriptFont(unittest.TestCase):
    """Test script font conversions."""

    def test_script_capital_a(self):
        """Test script capital A: 𝒜 → \\symscr{A}."""
        result = u2l.uni2tex("𝒜")
        self.assertIn("\\symscr", result)
        self.assertIn("A", result)

    def test_script_capital_f(self):
        """Test script capital F: ℱ → \\symscr{F}."""
        result = u2l.uni2tex("ℱ")
        self.assertIn("\\symscr", result)
        self.assertIn("F", result)

    def test_script_lowercase_a(self):
        """Test script lowercase a: 𝒶 → \\symscr{a}."""
        result = u2l.uni2tex("𝒶")
        self.assertIn("\\symscr", result)
        self.assertIn("a", result)


class TestBoldScriptFont(unittest.TestCase):
    """Test bold script font conversions."""

    def test_bold_script_capital_a(self):
        """Test bold script capital A: 𝓐 → \\symbfscr{A}."""
        result = u2l.uni2tex("𝓐")
        self.assertIn("\\symbfscr", result)
        self.assertIn("A", result)

    def test_bold_script_lowercase_a(self):
        """Test bold script lowercase a: 𝓪 → \\symbfscr{a}."""
        result = u2l.uni2tex("𝓪")
        self.assertIn("\\symbfscr", result)
        self.assertIn("a", result)


class TestFrakturFont(unittest.TestCase):
    """Test Fraktur (Gothic) font conversions."""

    def test_fraktur_capital_a(self):
        """Test Fraktur capital A: 𝔄 → \\symfrak{A}."""
        result = u2l.uni2tex("𝔄")
        self.assertIn("\\symfrak", result)
        self.assertIn("A", result)

    def test_fraktur_lowercase_a(self):
        """Test Fraktur lowercase a: 𝔞 → \\symfrak{a}."""
        result = u2l.uni2tex("𝔞")
        self.assertIn("\\symfrak", result)
        self.assertIn("a", result)


class TestSansSerifFont(unittest.TestCase):
    """Test sans-serif font conversions."""

    def test_sans_serif_capital_a(self):
        """Test sans-serif capital A: 𝖠 → \\symsf{A}."""
        result = u2l.uni2tex("𝖠")
        self.assertIn("\\symsf", result)
        self.assertIn("A", result)

    def test_sans_serif_lowercase_a(self):
        """Test sans-serif lowercase a: 𝖺 → \\symsf{a}."""
        result = u2l.uni2tex("𝖺")
        self.assertIn("\\symsf", result)
        self.assertIn("a", result)


class TestSansSerifBoldFont(unittest.TestCase):
    """Test sans-serif bold font conversions."""

    def test_sans_serif_bold_capital_a(self):
        """Test sans-serif bold capital A: 𝗔 → \\symbfit{A}."""
        result = u2l.uni2tex("𝗔")
        # Should contain symbfit or similar
        self.assertTrue("\\symbf" in result or "\\symsf" in result)
        self.assertIn("A", result)

    def test_sans_serif_bold_lowercase_a(self):
        """Test sans-serif bold lowercase a: 𝗮 → \\symbfit{a}."""
        result = u2l.uni2tex("𝗮")
        self.assertTrue("\\symbf" in result or "\\symsf" in result)
        self.assertIn("a", result)


class TestSansSerifItalicFont(unittest.TestCase):
    """Test sans-serif italic font conversions."""

    def test_sans_serif_italic_capital_a(self):
        """Test sans-serif italic capital A: 𝘈 → \\symsfit{A}."""
        result = u2l.uni2tex("𝘈")
        self.assertIn("\\symsfit", result)
        self.assertIn("A", result)

    def test_sans_serif_italic_lowercase_a(self):
        """Test sans-serif italic lowercase a: 𝘢 → \\symsfit{a}."""
        result = u2l.uni2tex("𝘢")
        self.assertIn("\\symsfit", result)
        self.assertIn("a", result)


class TestSansSerifBoldItalicFont(unittest.TestCase):
    """Test sans-serif bold italic font conversions."""

    def test_sans_serif_bold_italic_capital_a(self):
        """Test sans-serif bold italic capital A: 𝘼 → \\symbfsfit{A}."""
        result = u2l.uni2tex("𝘼")
        self.assertIn("\\symbfsfit", result)
        self.assertIn("A", result)

    def test_sans_serif_bold_italic_lowercase_a(self):
        """Test sans-serif bold italic lowercase a: 𝙖 → \\symbfsfit{a}."""
        result = u2l.uni2tex("𝙖")
        self.assertIn("\\symbfsfit", result)
        self.assertIn("a", result)


class TestMonospaceFont(unittest.TestCase):
    """Test monospace (typewriter) font conversions."""

    def test_monospace_capital_a(self):
        """Test monospace capital A: 𝙰 → \\symtt{A}."""
        result = u2l.uni2tex("𝙰")
        self.assertIn("\\symtt", result)
        self.assertIn("A", result)

    def test_monospace_lowercase_a(self):
        """Test monospace lowercase a: 𝚊 → \\symtt{a}."""
        result = u2l.uni2tex("𝚊")
        self.assertIn("\\symtt", result)
        self.assertIn("a", result)


class TestDoubleStruckItalicFont(unittest.TestCase):
    """Test double-struck italic font conversions."""

    def test_double_struck_italic_d(self):
        """Test double-struck italic D: ⅅ → \\symbbit{D}."""
        result = u2l.uni2tex("ⅅ")
        self.assertIn("\\symbbit", result)
        self.assertIn("D", result)

    def test_double_struck_italic_i(self):
        """Test double-struck italic i: ⅈ → \\symbbit{i}."""
        result = u2l.uni2tex("ⅈ")
        self.assertIn("\\symbbit", result)
        self.assertIn("i", result)

    def test_double_struck_italic_j(self):
        """Test double-struck italic j: ⅉ → \\symbbit{j}."""
        result = u2l.uni2tex("ⅉ")
        self.assertIn("\\symbbit", result)
        self.assertIn("j", result)


class TestFontConversionDisabled(unittest.TestCase):
    """Test behavior when font conversion is disabled."""

    def test_bold_with_fonts_disabled(self):
        """Test bold font with font modifiers disabled."""
        result = u2l.uni2tex("𝐀", add_font_modifiers=False)
        # Should convert to base letter without font modifier
        self.assertIn("A", result)
        self.assertNotIn("\\symbf", result)

    def test_italic_with_fonts_disabled(self):
        """Test italic font with font modifiers disabled."""
        result = u2l.uni2tex("𝐴", add_font_modifiers=False)
        self.assertIn("A", result)
        self.assertNotIn("\\symit", result)

    def test_double_struck_with_fonts_disabled(self):
        """Test double-struck with font modifiers disabled."""
        result = u2l.uni2tex("ℝ", add_font_modifiers=False)
        self.assertIn("R", result)
        self.assertNotIn("\\symbb", result)

    def test_mixed_with_fonts_disabled(self):
        """Test mixed text with font modifiers disabled."""
        result = u2l.uni2tex("𝐀 α ℝ", add_font_modifiers=False)
        # Greek should still convert
        self.assertIn("\\alpha", result)
        # But fonts should not
        self.assertNotIn("\\symbf", result)
        self.assertNotIn("\\symbb", result)


class TestFontTables(unittest.TestCase):
    """Test the font tables structure."""

    def test_fonts_tuple_structure(self):
        """Test that fonts tuple is properly structured."""
        self.assertIsInstance(u2l.fonts, tuple)
        for item in u2l.fonts:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            font_name, latex_cmd = item
            self.assertIsInstance(font_name, str)
            self.assertIsInstance(latex_cmd, str)
            self.assertTrue(latex_cmd.startswith("\\sym"))

    def test_font_names(self):
        """Test that expected font names are in the table."""
        font_names = [item[0] for item in u2l.fonts]
        self.assertIn("BOLD", font_names)
        self.assertIn("ITALIC", font_names)
        self.assertIn("DOUBLE-STRUCK", font_names)
        self.assertIn("SCRIPT", font_names)
        self.assertIn("FRAKTUR", font_names)
        self.assertIn("SANS-SERIF", font_names)
        self.assertIn("MONOSPACE", font_names)


class TestMixedFontsAndAccents(unittest.TestCase):
    """Test interaction between fonts and accents."""

    def test_font_with_regular_text(self):
        """Test font symbols mixed with regular text."""
        result = u2l.uni2tex("text 𝐀 more text")
        self.assertIn("text", result)
        self.assertIn("\\symbf", result)
        self.assertIn("more text", result)

    def test_multiple_fonts_in_sequence(self):
        """Test multiple different font styles in sequence."""
        result = u2l.uni2tex("𝐀 𝐴 ℝ")
        self.assertIn("\\symbf", result)
        self.assertIn("\\symit", result)
        self.assertIn("\\symbb", result)


class TestGreekWithFonts(unittest.TestCase):
    """Test Greek letters in different fonts."""

    def test_bold_greek_theta(self):
        """Test bold Greek theta: 𝚯 → should handle font."""
        result = u2l.uni2tex("𝚯")
        # Should contain either symbf or Theta
        self.assertTrue("\\symbf" in result or "\\Theta" in result)

    def test_bold_italic_greek_theta(self):
        """Test bold italic Greek theta: 𝜣."""
        result = u2l.uni2tex("𝜣")
        # Should handle the font variant
        self.assertTrue("\\symbf" in result or "\\Theta" in result)


class TestComplexFontExpressions(unittest.TestCase):
    """Test complex expressions with fonts."""

    def test_mathematical_expression(self):
        """Test expression: x ∈ ℝ with italic x."""
        result = u2l.uni2tex("𝑥 ∈ ℝ")
        self.assertIn("\\symit", result)
        self.assertIn("x", result)
        self.assertIn("\\in", result)
        self.assertIn("\\symbb", result)
        self.assertIn("R", result)

    def test_script_and_regular(self):
        """Test script mixed with regular symbols."""
        result = u2l.uni2tex("𝒜 ⊂ 𝒲")
        self.assertIn("\\symscr", result)
        self.assertIn("\\subset", result)


if __name__ == '__main__':
    unittest.main()
