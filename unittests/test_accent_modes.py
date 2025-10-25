#!/usr/bin/env python3
"""
Unit tests for accent mode feature (Bug #7 fix).

Tests the accent_mode parameter that allows choosing between text-mode
and math-mode accent commands.
"""

import unittest
import sys
import os

# Add parent directory to path to from unicode2latex import u2l
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unicode2latex import u2l


class TestAccentModeParameter(unittest.TestCase):
    """Test the accent_mode parameter."""

    def test_default_accent_mode_is_text(self):
        """Test that default accent_mode is 'text'."""
        decomposer = u2l.Decompose_to_tex()
        self.assertEqual(decomposer.accent_mode, 'text')

    def test_accent_mode_text_explicit(self):
        """Test explicit accent_mode='text'."""
        decomposer = u2l.Decompose_to_tex(accent_mode='text')
        self.assertEqual(decomposer.accent_mode, 'text')

    def test_accent_mode_math(self):
        """Test accent_mode='math'."""
        decomposer = u2l.Decompose_to_tex(accent_mode='math')
        self.assertEqual(decomposer.accent_mode, 'math')

    def test_accent_mode_auto(self):
        """Test accent_mode='auto'."""
        decomposer = u2l.Decompose_to_tex(accent_mode='auto')
        self.assertEqual(decomposer.accent_mode, 'auto')

    def test_invalid_accent_mode_raises_error(self):
        """Test that invalid accent_mode raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            u2l.Decompose_to_tex(accent_mode='invalid')

        self.assertIn("accent_mode must be", str(cm.exception))


class TestTextModeAccents(unittest.TestCase):
    """Test text-mode accent output (default behavior)."""

    def test_acute_accent_text_mode(self):
        """Test é → \\'{e} in text mode."""
        result = u2l.uni2tex("é", accent_mode='text')
        self.assertIn("\\'", result)
        self.assertIn("{e}", result)
        self.assertNotIn("\\acute", result)

    def test_grave_accent_text_mode(self):
        """Test è → \\`{e} in text mode."""
        result = u2l.uni2tex("è", accent_mode='text')
        self.assertIn("\\`", result)
        self.assertIn("{e}", result)
        self.assertNotIn("\\grave", result)

    def test_circumflex_text_mode(self):
        """Test ê → \\^{e} in text mode."""
        result = u2l.uni2tex("ê", accent_mode='text')
        self.assertIn("\\^", result)
        self.assertIn("{e}", result)
        self.assertNotIn("\\hat", result)

    def test_tilde_text_mode(self):
        """Test ñ → \\~{n} in text mode."""
        result = u2l.uni2tex("ñ", accent_mode='text')
        self.assertIn("\\~", result)
        self.assertIn("{n}", result)
        self.assertNotIn("\\tilde", result)

    def test_umlaut_text_mode(self):
        """Test ü → \\"{u} in text mode."""
        result = u2l.uni2tex("ü", accent_mode='text')
        self.assertIn('\\"', result)
        self.assertIn("{u}", result)
        self.assertNotIn("\\ddot", result)


class TestMathModeAccents(unittest.TestCase):
    """Test math-mode accent output."""

    def test_acute_accent_math_mode(self):
        """Test é → \\acute{e} in math mode."""
        result = u2l.uni2tex("é", accent_mode='math')
        self.assertIn("\\acute{e}", result)
        self.assertNotIn("\\'", result)

    def test_grave_accent_math_mode(self):
        """Test è → \\grave{e} in math mode."""
        result = u2l.uni2tex("è", accent_mode='math')
        self.assertIn("\\grave{e}", result)
        self.assertNotIn("\\`", result)

    def test_circumflex_math_mode(self):
        """Test ê → \\hat{e} in math mode."""
        result = u2l.uni2tex("ê", accent_mode='math')
        self.assertIn("\\hat{e}", result)
        self.assertNotIn("\\^", result)

    def test_tilde_math_mode(self):
        """Test ñ → \\tilde{n} in math mode."""
        result = u2l.uni2tex("ñ", accent_mode='math')
        self.assertIn("\\tilde{n}", result)
        self.assertNotIn("\\~", result)

    def test_umlaut_math_mode(self):
        """Test ü → \\ddot{u} in math mode."""
        result = u2l.uni2tex("ü", accent_mode='math')
        self.assertIn("\\ddot{u}", result)
        self.assertNotIn('\\"', result)

    def test_macron_math_mode(self):
        """Test ā → \\bar{a} in math mode."""
        result = u2l.uni2tex("ā", accent_mode='math')
        self.assertIn("\\bar{a}", result)
        self.assertNotIn("\\=", result)

    def test_dot_above_math_mode(self):
        """Test ȧ → \\dot{a} in math mode."""
        result = u2l.uni2tex("ȧ", accent_mode='math')
        self.assertIn("\\dot{a}", result)
        self.assertNotIn("\\.", result)

    def test_breve_math_mode(self):
        """Test ă → \\breve{a} in math mode."""
        result = u2l.uni2tex("ă", accent_mode='math')
        self.assertIn("\\breve{a}", result)
        self.assertNotIn("\\u", result)

    def test_caron_math_mode(self):
        """Test č → \\check{c} in math mode."""
        result = u2l.uni2tex("č", accent_mode='math')
        self.assertIn("\\check{c}", result)
        self.assertNotIn("\\v", result)


class TestAccentsWithoutMathEquivalent(unittest.TestCase):
    """Test accents that don't have math-mode equivalents."""

    def test_cedilla_falls_back_to_text(self):
        """Test ç → \\c{c} even in math mode (no math equivalent)."""
        result = u2l.uni2tex("ç", accent_mode='math')
        # Should fallback to text mode
        self.assertIn("\\c{c}", result)

    def test_ring_above_falls_back_to_text(self):
        """Test å → \\r{a} even in math mode (no math equivalent)."""
        result = u2l.uni2tex("å", accent_mode='math')
        # Should fallback to text mode
        self.assertIn("\\r{a}", result)


class TestAutoMode(unittest.TestCase):
    """Test auto mode (currently defaults to text mode)."""

    def test_auto_mode_defaults_to_text(self):
        """Test that 'auto' mode currently defaults to text mode."""
        result = u2l.uni2tex("é", accent_mode='auto')
        # Currently auto mode defaults to text
        self.assertIn("\\'", result)
        self.assertIn("{e}", result)

    def test_auto_mode_todo_comment(self):
        """Verify TODO comment exists for auto mode implementation."""
        # Check that the TODO is documented
        import inspect
        source = inspect.getsource(u2l.Decompose_to_tex._docode)
        self.assertIn("TODO", source)
        self.assertIn("auto", source.lower())


class TestMixedText(unittest.TestCase):
    """Test mixed text with accents."""

    def test_multiple_accents_text_mode(self):
        """Test multiple accents in text mode."""
        result = u2l.uni2tex("café", accent_mode='text')
        self.assertIn("caf", result)
        self.assertIn("\\'", result)
        self.assertIn("e", result)

    def test_multiple_accents_math_mode(self):
        """Test multiple accents in math mode."""
        result = u2l.uni2tex("café", accent_mode='math')
        self.assertIn("caf", result)
        self.assertIn("\\acute", result)
        self.assertIn("e", result)

    def test_mixed_content_text_mode(self):
        """Test mixed content (accents + Greek) in text mode."""
        result = u2l.uni2tex("é α è", accent_mode='text')
        self.assertIn("\\'", result)
        self.assertIn("\\alpha", result)
        self.assertIn("\\`", result)

    def test_mixed_content_math_mode(self):
        """Test mixed content (accents + Greek) in math mode."""
        result = u2l.uni2tex("é α è", accent_mode='math')
        self.assertIn("\\acute", result)
        self.assertIn("\\alpha", result)
        self.assertIn("\\grave", result)


class TestAccentModeWithUni2tex(unittest.TestCase):
    """Test that uni2tex() passes accent_mode correctly."""

    def test_uni2tex_with_text_mode(self):
        """Test uni2tex() with accent_mode='text'."""
        result = u2l.uni2tex("é", accent_mode='text')
        self.assertIn("\\'", result)

    def test_uni2tex_with_math_mode(self):
        """Test uni2tex() with accent_mode='math'."""
        result = u2l.uni2tex("é", accent_mode='math')
        self.assertIn("\\acute", result)

    def test_uni2tex_default_is_text(self):
        """Test that uni2tex() defaults to text mode."""
        result = u2l.uni2tex("é")
        self.assertIn("\\'", result)
        self.assertNotIn("\\acute", result)


class TestDecomposedAccents(unittest.TestCase):
    """Test that decomposed (precomposed) characters also use accent_mode."""

    def test_decomposed_acute_text_mode(self):
        """Test decomposed é in text mode."""
        # é can be represented as e + combining acute (U+0301)
        decomposer = u2l.Decompose_to_tex(accent_mode='text')
        decomposer.parse("e\u0301")  # e + combining acute
        result = decomposer.result
        self.assertIn("\\'", result)

    def test_decomposed_acute_math_mode(self):
        """Test decomposed é in math mode."""
        decomposer = u2l.Decompose_to_tex(accent_mode='math')
        decomposer.parse("e\u0301")  # e + combining acute
        result = decomposer.result
        self.assertIn("\\acute", result)


class TestAccentModeMapping(unittest.TestCase):
    """Test the accent mapping dictionary."""

    def test_textmode_to_mathmode_dict_exists(self):
        """Test that the mapping dictionary exists."""
        self.assertIsInstance(u2l.accents_textmode_to_mathmode, dict)

    def test_common_accents_have_math_equivalents(self):
        """Test that common accents have math equivalents."""
        common_accents = ['`', "'", '^', '~', '"', '=', '.']
        for accent in common_accents:
            self.assertIn(accent, u2l.accents_textmode_to_mathmode,
                f"Accent {accent!r} should have math equivalent")

    def test_math_accent_names_are_correct(self):
        """Test that math accent names are correct."""
        expected_mappings = {
            '`': 'grave',
            "'": 'acute',
            '^': 'hat',
            '~': 'tilde',
            '"': 'ddot',
            '=': 'bar',
            '.': 'dot',
            'u': 'breve',
            'v': 'check',
        }
        for text_accent, math_accent in expected_mappings.items():
            self.assertEqual(
                u2l.accents_textmode_to_mathmode.get(text_accent),
                math_accent,
                f"Accent {text_accent!r} should map to {math_accent!r}"
            )


if __name__ == '__main__':
    unittest.main()
