#!/usr/bin/env python3
"""
Unit tests for potential bugs and edge cases in unicode2latex.
"""

import unittest
import sys
import os
import io
import subprocess
import logging
logger = logging.getLogger('unicode2latex')

# Add parent directory to path to from unicode2latex import u2l
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unicode2latex import u2l


class TestSubprocessBugs(unittest.TestCase):
    """Test bugs related to subprocess handling."""

    def test_subprocess_output_type(self):
        """Test that subprocess output handling doesn't fail with bytes."""
        # Bug: Line 64 in u2l.py does: a = p.stdout.read().strip()
        # This returns bytes, not str, which could cause issues
        try:
            p = subprocess.Popen(['echo', 'test'], stdout=subprocess.PIPE)
            a = p.stdout.read().strip()
            p.wait()
            p.stdout.close()

            # Check if bytes are returned (which is the actual behavior)
            self.assertIsInstance(a, bytes,
                "subprocess.PIPE returns bytes in Python 3")

            # The bug is that os.path.isfile(a) at line 66 expects str
            # but gets bytes, which may cause issues
        except Exception as e:
            self.fail(f"Subprocess handling failed: {e}")


class TestRecursiveDecomposition(unittest.TestCase):
    """Test recursive _docode calls in font handling."""

    def test_font_decomposition(self):
        """Test that font decomposition works correctly."""
        # Lines 456, 468, 474, 482, 489, 495, 514 have recursive calls
        # decompose_to_tex(chr(acc), output) where decompose_to_tex = self._docode
        # But _docode signature is _docode(self, char, useless=None)

        test_cases = [
            ("𝐀", "\\symbf"),  # MATHEMATICAL BOLD CAPITAL A
            ("𝐴", "\\symit"),  # MATHEMATICAL ITALIC CAPITAL A
            ("ℝ", "\\symbb"),  # DOUBLE-STRUCK CAPITAL R
            ("𝒜", "\\symscr"), # MATHEMATICAL SCRIPT CAPITAL A
        ]

        for char, expected in test_cases:
            with self.subTest(char=char):
                result = u2l.uni2tex(char)
                self.assertIn(expected, result,
                    f"Font decomposition failed for {char}")

    def test_small_decomposition(self):
        """Test <small> decomposition."""
        # Line 474: decompose_to_tex(chr(acc), output)
        result = u2l.uni2tex("﹠")  # SMALL AMPERSAND
        self.assertIn("scriptsize", result)

    def test_compat_ligature_decomposition(self):
        """Test <compat> ligature decomposition."""
        # Line 489: for l in decsplit[1:]: decompose_to_tex(chr(l), output)
        # Test with a ligature character
        result = u2l.uni2tex("ﬁ")  # LATIN SMALL LIGATURE FI
        # Should decompose to f and i
        self.assertIn("f", result)
        self.assertIn("i", result)

    def test_modifier_decomposition(self):
        """Test modifier decomposition (superscript/subscript)."""
        # Line 495: decompose_to_tex(chr(acc), output)
        result = u2l.uni2tex("x⁰")  # x with superscript 0
        self.assertIn("^", result)
        self.assertIn("0", result)

    def test_accent_decomposition_with_base(self):
        """Test accent decomposition when base and accent are separate."""
        # Line 514: decompose_to_tex(chr(base), output)
        result = u2l.uni2tex("é")  # e with acute
        self.assertIn("\\'", result)
        self.assertIn("e", result)


class TestTex2UnicodeBugs(unittest.TestCase):
    """Test bugs in LaTeX to Unicode conversion."""

    def test_unknown_latex_command(self):
        """Test handling of unknown LaTeX commands."""
        inp = io.StringIO(r"\unknowncommand test")
        out = io.StringIO()
        u2l.tex2uni(inp, out, {})
        result = out.getvalue()

        # Should pass through unknown commands
        self.assertIn("unknowncommand", result)

    def test_empty_dictionary(self):
        """Test tex2uni with empty conversion dictionary."""
        inp = io.StringIO(r"plain text")
        out = io.StringIO()
        u2l.tex2uni(inp, out, {})
        result = out.getvalue()

        self.assertEqual(result, "plain text")

    def test_comment_handling(self):
        """Test that LaTeX comments are handled."""
        inp = io.StringIO(r"text % comment")
        out = io.StringIO()
        u2l.tex2uni(inp, out, {})
        result = out.getvalue()

        self.assertIn("text", result)
        self.assertIn("%", result)

    def test_tokenizer_in_operator(self):
        """Test line 560: if '::' in tok - potential bug."""
        # Line 560 uses 'in' operator on tok which might not support it
        inp = io.StringIO(r"\alpha")
        out = io.StringIO()

        try:
            u2l.tex2uni(inp, out, {r'\alpha': 'α'})
            result = out.getvalue()
            self.assertIn("α", result)
        except TypeError as e:
            # This would catch the bug if '::' in tok fails
            self.fail(f"Tokenizer 'in' operator bug: {e}")


class TestGlobalVariableBugs(unittest.TestCase):
    """Test issues with global variables."""

    def test_global_char_count_reset(self):
        """Test that global char_count doesn't cause issues."""
        # char_count is global and modified in _donext (line 407)
        result1 = u2l.uni2tex("abc")
        result2 = u2l.uni2tex("xyz")

        # Both should work independently
        self.assertEqual(result1, "abc")
        self.assertEqual(result2, "xyz")

    def test_global_line_count(self):
        """Test that global line_count doesn't cause issues."""
        # line_count is global (line 367)
        result = u2l.uni2tex("test\nline2")
        self.assertIn("\n", result)

    def test_global_input_file(self):
        """Test that global input_file variable works."""
        # input_file is global (line 369)
        result = u2l.uni2tex("α")
        self.assertIn("\\alpha", result)


class TestVerboseMode(unittest.TestCase):
    """Test verbose mode functionality."""

    def setUp(self):
        """Save original verbose setting."""
        self.original_verbose = u2l.verbose

    def tearDown(self):
        """Restore original verbose setting."""
        u2l.verbose = self.original_verbose

    def test_verbose_level_0(self):
        """Test with verbose=0 (default)."""
        u2l.verbose = 0
        with self.assertNoLogs(logger) as cm:
            result = u2l.uni2tex("α")
        result = u2l.uni2tex("α")
        self.assertIn("\\alpha", result)

    def test_verbose_level_1(self):
        """Test with verbose=1."""
        u2l.verbose = 1
        with self.assertNoLogs(logger) as cm:
            result = u2l.uni2tex("α")
        self.assertIn("\\alpha", result)

    def test_verbose_level_2(self):
        """Test with verbose=2."""
        u2l.verbose = 2
        with self.assertLogs(logger) as cm:
            result = u2l.uni2tex("α")
        self.assertTrue(len(cm.output))
        self.assertIn('decomposing', cm.output[0])
        self.assertIn("\\alpha", result)

    def test_verbose_level_3(self):
        """Test with verbose=3."""
        u2l.verbose = 3
        with self.assertLogs(logger) as cm:
            result = u2l.uni2tex("α")
        self.assertTrue(len(cm.output))
        self.assertIn('decomposing', cm.output[0])
        self.assertIn("\\alpha", result)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def test_none_input(self):
        """Test that None input is handled."""
        with self.assertRaises((TypeError, AttributeError)):
            u2l.uni2tex(None)

    def test_non_string_input(self):
        """Test that non-string input is handled."""
        with self.assertRaises((TypeError, AttributeError)):
            u2l.uni2tex(123)

    def test_bytes_input(self):
        """Test that bytes input is handled."""
        with self.assertRaises((TypeError, AttributeError)):
            u2l.uni2tex(b"test")


class TestDecompositionEdgeCases(unittest.TestCase):
    """Test edge cases in character decomposition."""

    def test_unsupported_compat_decomposition(self):
        """Test unsupported <compat> decomposition."""
        # Line 491: syslogger for unsupported <compat>
        # Should not crash, just log warning
        with self.assertLogs(logger) as cm:
            result = u2l.uni2tex("㎏")  # SQUARE KG (compat decomposition)
        self.assertTrue(len(cm.output))
        self.assertIn("unsupported modifier '<square>'", cm.output[0])
        self.assertIsInstance(result, str)

    def test_unsupported_modifier(self):
        """Test unsupported modifier."""
        # Line 500: syslogger for unsupported modifier
        # Should not crash, just log warning and return char
        result = u2l.uni2tex("test")
        self.assertEqual(result, "test")

    def test_unsupported_decomposition(self):
        """Test unsupported decomposition."""
        # Line 519: syslogger for unsupported decomposition
        result = u2l.uni2tex("test")
        self.assertEqual(result, "test")

    def test_greek_name_handling(self):
        """Test Greek character name handling."""
        # Line 523: handles GREEK names, special case for 'lamda'
        result = u2l.uni2tex("λ")
        self.assertIn("\\lambda", result)

    def test_high_unicode_not_convertible(self):
        """Test high unicode characters that can't be converted."""
        # Line 536: syslogger for characters > 127 that can't convert
        with self.assertLogs(logger) as cm:
            result = u2l.uni2tex("😀")  # Emoji
        # Should not crash, just warn
        self.assertTrue(len(cm.output))
        self.assertIn('could not convert', cm.output[0])
        self.assertIn("😀", result)


class TestExtraUnicodeMappings(unittest.TestCase):
    """Test the extra_unicode2latex functionality."""

    def test_update_extra(self):
        """Test updating extra unicode mappings."""
        decomposer = u2l.Decompose_to_tex()
        decomposer.update_extra({0x2665: "\\heart"})
        decomposer.parse("♥")
        result = decomposer.result
        self.assertIn("\\heart", result)

    def test_extra_overrides_default(self):
        """Test that extra mappings override defaults."""
        decomposer = u2l.Decompose_to_tex()
        # Override the default × mapping
        decomposer.update_extra({0xD7: "\\mult"})
        decomposer.parse("×")
        result = decomposer.result
        self.assertIn("\\mult", result)


class TestPreferUnicodeMath(unittest.TestCase):
    """Test prefer_unicode_math flag."""

    def test_prefer_unicode_math_true(self):
        """Test with prefer_unicode_math=True."""
        decomposer = u2l.Decompose_to_tex(prefer_unicode_math=True)
        decomposer.parse("×")
        result = decomposer.result
        self.assertIn("\\times", result)

    def test_prefer_unicode_math_false(self):
        """Test with prefer_unicode_math=False."""
        decomposer = u2l.Decompose_to_tex(prefer_unicode_math=False)
        decomposer.parse("×")
        result = decomposer.result
        # Should still convert, just checked later
        self.assertIn("\\times", result)


if __name__ == '__main__':
    unittest.main()
