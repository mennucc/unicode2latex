#!/usr/bin/env python3
"""
Unit tests for accent handling in unicode2latex.
"""

import unittest
import sys
import os

# Add parent directory to path to from unicode2latex import u2l
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unicode2latex import u2l


class TestBasicAccents(unittest.TestCase):
    """Test basic accent conversions."""

    def test_grave_on_a(self):
        """Test à → \\`{a}."""
        result = u2l.uni2tex("à")
        self.assertIn("\\`", result)
        self.assertIn("a", result)

    def test_grave_on_e(self):
        """Test è → \\`{e}."""
        result = u2l.uni2tex("è")
        self.assertIn("\\`", result)
        self.assertIn("e", result)

    def test_grave_on_i(self):
        """Test ì → \\`{i}."""
        result = u2l.uni2tex("ì")
        self.assertIn("\\`", result)
        self.assertIn("i", result)

    def test_grave_on_o(self):
        """Test ò → \\`{o}."""
        result = u2l.uni2tex("ò")
        self.assertIn("\\`", result)
        self.assertIn("o", result)

    def test_grave_on_u(self):
        """Test ù → \\`{u}."""
        result = u2l.uni2tex("ù")
        self.assertIn("\\`", result)
        self.assertIn("u", result)

    def test_acute_on_a(self):
        """Test á → \\'{a}."""
        result = u2l.uni2tex("á")
        self.assertIn("\\'", result)
        self.assertIn("a", result)

    def test_acute_on_e(self):
        """Test é → \\'{e}."""
        result = u2l.uni2tex("é")
        self.assertIn("\\'", result)
        self.assertIn("e", result)

    def test_acute_on_i(self):
        """Test í → \\'{i}."""
        result = u2l.uni2tex("í")
        self.assertIn("\\'", result)
        self.assertIn("i", result)

    def test_acute_on_o(self):
        """Test ó → \\'{o}."""
        result = u2l.uni2tex("ó")
        self.assertIn("\\'", result)
        self.assertIn("o", result)

    def test_acute_on_u(self):
        """Test ú → \\'{u}."""
        result = u2l.uni2tex("ú")
        self.assertIn("\\'", result)
        self.assertIn("u", result)

    def test_circumflex_on_a(self):
        """Test â → \\^{a}."""
        result = u2l.uni2tex("â")
        self.assertIn("\\^", result)
        self.assertIn("a", result)

    def test_circumflex_on_e(self):
        """Test ê → \\^{e}."""
        result = u2l.uni2tex("ê")
        self.assertIn("\\^", result)
        self.assertIn("e", result)

    def test_circumflex_on_i(self):
        """Test î → \\^{i}."""
        result = u2l.uni2tex("î")
        self.assertIn("\\^", result)
        self.assertIn("i", result)

    def test_circumflex_on_o(self):
        """Test ô → \\^{o}."""
        result = u2l.uni2tex("ô")
        self.assertIn("\\^", result)
        self.assertIn("o", result)

    def test_circumflex_on_u(self):
        """Test û → \\^{u}."""
        result = u2l.uni2tex("û")
        self.assertIn("\\^", result)
        self.assertIn("u", result)


class TestTildeAccent(unittest.TestCase):
    """Test tilde accent conversions."""

    def test_tilde_on_a(self):
        """Test ã → \\~{a}."""
        result = u2l.uni2tex("ã")
        self.assertIn("\\~", result)
        self.assertIn("a", result)

    def test_tilde_on_n(self):
        """Test ñ → \\~{n}."""
        result = u2l.uni2tex("ñ")
        self.assertIn("\\~", result)
        self.assertIn("n", result)

    def test_tilde_on_o(self):
        """Test õ → \\~{o}."""
        result = u2l.uni2tex("õ")
        self.assertIn("\\~", result)
        self.assertIn("o", result)

    def test_tilde_on_u(self):
        """Test ũ → \\~{u}."""
        result = u2l.uni2tex("ũ")
        self.assertIn("\\~", result)
        self.assertIn("u", result)


class TestUmlautAccent(unittest.TestCase):
    """Test umlaut (diaeresis) accent conversions."""

    def test_umlaut_on_a(self):
        """Test ä → \\"{a}."""
        result = u2l.uni2tex("ä")
        self.assertIn('\\"', result)
        self.assertIn("a", result)

    def test_umlaut_on_e(self):
        """Test ë → \\"{e}."""
        result = u2l.uni2tex("ë")
        self.assertIn('\\"', result)
        self.assertIn("e", result)

    def test_umlaut_on_i(self):
        """Test ï → \\"{i}."""
        result = u2l.uni2tex("ï")
        self.assertIn('\\"', result)
        self.assertIn("i", result)

    def test_umlaut_on_o(self):
        """Test ö → \\"{o}."""
        result = u2l.uni2tex("ö")
        self.assertIn('\\"', result)
        self.assertIn("o", result)

    def test_umlaut_on_u(self):
        """Test ü → \\"{u}."""
        result = u2l.uni2tex("ü")
        self.assertIn('\\"', result)
        self.assertIn("u", result)

    def test_umlaut_on_y(self):
        """Test ÿ → \\"{y}."""
        result = u2l.uni2tex("ÿ")
        self.assertIn('\\"', result)
        self.assertIn("y", result)


class TestOtherAccents(unittest.TestCase):
    """Test other accent types."""

    def test_ring_above(self):
        """Test ring above å → \\r{a}."""
        result = u2l.uni2tex("å")
        self.assertIn("\\r", result)
        self.assertIn("a", result)

    def test_cedilla(self):
        """Test cedilla ç → \\c{c}."""
        result = u2l.uni2tex("ç")
        self.assertIn("\\c", result)
        self.assertIn("c", result)

    def test_macron(self):
        """Test macron ā → \\={a}."""
        result = u2l.uni2tex("ā")
        self.assertIn("\\=", result)
        self.assertIn("a", result)

    def test_breve(self):
        """Test breve ă → \\u{a}."""
        result = u2l.uni2tex("ă")
        self.assertIn("\\u", result)
        self.assertIn("a", result)

    def test_dot_above(self):
        """Test dot above ȧ → \\.{a}."""
        result = u2l.uni2tex("ȧ")
        self.assertIn("\\.", result)
        self.assertIn("a", result)

    def test_caron(self):
        """Test caron č → \\v{c}."""
        result = u2l.uni2tex("č")
        self.assertIn("\\v", result)
        self.assertIn("c", result)


class TestMultipleAccents(unittest.TestCase):
    """Test words with multiple accented characters."""

    def test_french_word(self):
        """Test French word 'café'."""
        result = u2l.uni2tex("café")
        self.assertIn("caf", result)
        self.assertIn("\\'", result)
        self.assertIn("e", result)

    def test_spanish_word(self):
        """Test Spanish word 'señor'."""
        result = u2l.uni2tex("señor")
        self.assertIn("se", result)
        self.assertIn("\\~", result)
        self.assertIn("n", result)
        self.assertIn("or", result)

    def test_portuguese_word(self):
        """Test Portuguese word 'português'."""
        result = u2l.uni2tex("português")
        self.assertIn("portugu", result)
        # Should have circumflex on e
        self.assertIn("\\^", result)
        self.assertIn("e", result)

    def test_german_word(self):
        """Test German word 'Müller'."""
        result = u2l.uni2tex("Müller")
        self.assertIn("M", result)
        self.assertIn('\\"', result)
        self.assertIn("u", result)
        self.assertIn("ller", result)


class TestAccentDisabled(unittest.TestCase):
    """Test behavior when accent conversion is disabled."""

    def test_accents_disabled(self):
        """Test that accents are preserved when conversion is disabled."""
        original = "àèìòù"
        result = u2l.uni2tex(original, convert_accents=False)
        self.assertEqual(result, original)

    def test_mixed_with_accents_disabled(self):
        """Test mixed text with accents disabled."""
        # Greek should still convert, but accents should not
        result = u2l.uni2tex("é α è", convert_accents=False)
        self.assertIn("\\alpha", result)
        self.assertIn("é", result)
        self.assertIn("è", result)


class TestCapitalAccents(unittest.TestCase):
    """Test accents on capital letters."""

    def test_capital_a_grave(self):
        """Test À → \\`{A}."""
        result = u2l.uni2tex("À")
        self.assertIn("\\`", result)
        self.assertIn("A", result)

    def test_capital_e_acute(self):
        """Test É → \\'{E}."""
        result = u2l.uni2tex("É")
        self.assertIn("\\'", result)
        self.assertIn("E", result)

    def test_capital_n_tilde(self):
        """Test Ñ → \\~{N}."""
        result = u2l.uni2tex("Ñ")
        self.assertIn("\\~", result)
        self.assertIn("N", result)

    def test_capital_u_umlaut(self):
        """Test Ü → \\"{U}."""
        result = u2l.uni2tex("Ü")
        self.assertIn('\\"', result)
        self.assertIn("U", result)


class TestAccentDictionaries(unittest.TestCase):
    """Test the accent dictionary structures."""

    def test_accents_unicode2latex_completeness(self):
        """Test that accent dictionary contains expected entries."""
        self.assertIn(0x0300, u2l.accents_unicode2latex)  # COMBINING GRAVE ACCENT
        self.assertEqual(u2l.accents_unicode2latex[0x0300], "`")

        self.assertIn(0x0301, u2l.accents_unicode2latex)  # COMBINING ACUTE ACCENT
        self.assertEqual(u2l.accents_unicode2latex[0x0301], "'")

        self.assertIn(0x0302, u2l.accents_unicode2latex)  # COMBINING CIRCUMFLEX
        self.assertEqual(u2l.accents_unicode2latex[0x0302], "^")

        self.assertIn(0x0303, u2l.accents_unicode2latex)  # COMBINING TILDE
        self.assertEqual(u2l.accents_unicode2latex[0x0303], "~")

        self.assertIn(0x0308, u2l.accents_unicode2latex)  # COMBINING DIAERESIS
        self.assertEqual(u2l.accents_unicode2latex[0x0308], '"')

    def test_accents_latex2unicode_is_reverse(self):
        """Test that latex2unicode is the reverse of unicode2latex."""
        for unicode_code, latex_accent in u2l.accents_unicode2latex.items():
            self.assertIn(latex_accent, u2l.accents_latex2unicode)
            self.assertEqual(u2l.accents_latex2unicode[latex_accent], unicode_code)


class TestAccentEdgeCases(unittest.TestCase):
    """Test edge cases for accent handling."""

    def test_combining_accent_alone(self):
        """Test combining accent without base character."""
        # This should not crash, but may produce a warning
        combining_grave = "\u0300"
        result = u2l.uni2tex(combining_grave)
        # Should handle gracefully (may add space as base)
        self.assertIsInstance(result, str)

    def test_double_accents(self):
        """Test character with multiple combining accents."""
        # e with circumflex and acute (if representable)
        # Most double accents are pre-composed in Unicode
        # This tests the decomposition handling
        result = u2l.uni2tex("ế")  # Vietnamese e with circumflex and acute
        self.assertIsInstance(result, str)
        # Should contain accent markers
        self.assertTrue("\\^" in result or "\\'" in result)


if __name__ == '__main__':
    unittest.main()
