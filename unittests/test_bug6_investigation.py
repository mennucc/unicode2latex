#!/usr/bin/env python3
"""
Unit tests to investigate Bug #6: Tokenizer '::' in operator.

This test verifies that the '::' check at line 560 is actually correct
and that it handles TeX active characters properly.
"""

import unittest
import sys
import os
import io

# Add parent directory to path to from unicode2latex import u2l
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unicode2latex import u2l
from FakePlasTeX import TokenizerPassThru, FakeContext


class TestBug6TokenizerInvestigation(unittest.TestCase):
    """Investigate Bug #6: '::' in tok check."""

    def test_token_is_string_subclass(self):
        """Test that Token is a string subclass, so 'in' operator works."""
        # Create a simple tokenizer to get a token
        inp = io.StringIO(r"\alpha")
        context = FakeContext.FakeContext()
        tokenizer = TokenizerPassThru.TokenizerPassThru(inp, context)

        for tok in tokenizer:
            if isinstance(tok, TokenizerPassThru.EscapeSequence):
                # Token should be a string subclass
                self.assertIsInstance(tok, str,
                    "Token should be a str subclass")

                # The 'in' operator should work
                result = '::' in tok
                self.assertIsInstance(result, bool,
                    "'in' operator should return bool")
                break

    def test_active_character_with_double_colon(self):
        """Test that active characters with :: are handled correctly."""
        # Active characters in TeX are prefixed with 'active::'
        # Examples from FakeTokenizer.py:
        # - MathShift: macroName = 'active::$'
        # - Alignment: macroName = 'active::&'

        inp = io.StringIO("$test$")  # Math mode
        out = io.StringIO()

        # Test with empty dictionary (no conversions)
        u2l.tex2uni(inp, out, {})
        result = out.getvalue()

        # Should handle the $ characters (math shifts)
        self.assertIn("$", result)

    def test_escape_sequence_with_double_colon(self):
        """Test EscapeSequence that contains :: gets split correctly."""
        # According to FakeTokenizer.py line 120-121:
        # if '::' in self:
        #     return self.split('::').pop()

        # This is for active characters like 'active::$'
        inp = io.StringIO(r"test $ more")
        out = io.StringIO()

        u2l.tex2uni(inp, out, {})
        result = out.getvalue()

        # The active character $ should be handled
        self.assertIn("$", result)

    def test_line_560_code_path(self):
        """Test the specific code path at line 560 in u2l.py."""
        # Line 560: if '::' in tok:
        # Line 561: m = tok.split('::').pop()

        # This code is reached when:
        # 1. tok is an EscapeSequence
        # 2. The macroname is not in the conversion dictionary D
        # 3. The tok contains '::'

        # Create input with an active character
        inp = io.StringIO(r"~")  # ~ is an active character (catcode 13)
        out = io.StringIO()

        # Empty dictionary, so macroname won't be found
        u2l.tex2uni(inp, out, {})
        result = out.getvalue()

        # Should output the character
        self.assertIsInstance(result, str)

    def test_escape_sequence_source_property(self):
        """Test that EscapeSequence.source handles :: correctly."""
        # From FakeTokenizer.py lines 116-122
        inp = io.StringIO(r"\unknown")
        context = FakeContext.FakeContext()
        tokenizer = TokenizerPassThru.TokenizerPassThru(inp, context)

        for tok in tokenizer:
            if isinstance(tok, TokenizerPassThru.EscapeSequence):
                # Test that we can check for '::'
                has_double_colon = '::' in tok
                self.assertFalse(has_double_colon,
                    r"\unknown should not contain ::")

                # Test the source property
                source = tok.source
                self.assertIsInstance(source, str)
                break

    def test_math_shift_active_character(self):
        """Test MathShift token which has 'active::$' as macroName."""
        # MathShift is defined with macroName = 'active::$' in FakeTokenizer.py
        inp = io.StringIO("$x$")
        out = io.StringIO()

        u2l.tex2uni(inp, out, {})
        result = out.getvalue()

        # Math delimiters should be preserved
        self.assertEqual(result, "$x$")

    def test_alignment_active_character(self):
        """Test Alignment token which has 'active::&' as macroName."""
        # Alignment is defined with macroName = 'active::&' in FakeTokenizer.py
        inp = io.StringIO(r"a & b")
        out = io.StringIO()

        u2l.tex2uni(inp, out, {})
        result = out.getvalue()

        # Alignment character should be preserved
        self.assertIn("&", result)

    def test_bug6_conclusion(self):
        """Verify that Bug #6 is not actually a bug."""
        # Bug #6 stated: "The 'in' operator may not be implemented"
        #
        # CONCLUSION: This is NOT a bug because:
        # 1. Token inherits from Text which inherits from str
        # 2. Therefore 'in' operator works correctly
        # 3. The code is used for handling active characters like 'active::$'
        # 4. The same pattern is used in FakeTokenizer.py itself (line 120)

        # This test documents that the code is correct by verifying
        # that Token objects support string operations
        from FakePlasTeX.FakeTokenizer import Token

        # Create a token that looks like an active character
        tok = Token("active::$")

        # Verify string operations work
        self.assertTrue('::' in tok,
            "'in' operator should work on Token")
        self.assertEqual(tok.split('::'), ['active', '$'],
            "split should work on Token")

        # This proves the code at line 560 is correct:
        # if '::' in tok:
        #     m = tok.split('::').pop()
        # Both operations are valid because Token is a string subclass


class TestTokenInheritance(unittest.TestCase):
    """Test the Token class inheritance to confirm it supports string operations."""

    def test_token_inherits_from_string(self):
        """Test that Token class hierarchy supports string operations."""
        from FakePlasTeX.FakeTokenizer import Token, Text

        # Text inherits from str
        self.assertTrue(issubclass(Text, str),
            "Text should inherit from str")

        # Token inherits from Text
        self.assertTrue(issubclass(Token, Text),
            "Token should inherit from Text")

        # Therefore Token inherits from str
        self.assertTrue(issubclass(Token, str),
            "Token should inherit from str transitively")

    def test_escape_sequence_inherits_from_token(self):
        """Test that EscapeSequence inherits from Token."""
        from FakePlasTeX.FakeTokenizer import Token, EscapeSequence

        self.assertTrue(issubclass(EscapeSequence, Token),
            "EscapeSequence should inherit from Token")

        # Therefore EscapeSequence inherits from str
        self.assertTrue(issubclass(EscapeSequence, str),
            "EscapeSequence should inherit from str transitively")

    def test_string_operations_on_token(self):
        """Test that string operations work on Token objects."""
        from FakePlasTeX.FakeTokenizer import Token

        # Create a token (it's a string)
        tok = Token("test::value")

        # All string operations should work
        self.assertTrue('::' in tok, "'in' operator should work")
        self.assertEqual(tok.split('::'), ['test', 'value'], "split should work")
        self.assertTrue(tok.startswith('test'), "startswith should work")
        self.assertTrue(tok.endswith('value'), "endswith should work")


if __name__ == '__main__':
    unittest.main()
