#!/usr/bin/env python3
"""
Unit tests for latex2unicode conversion functionality.
"""

import unittest
import sys
import os
import io

# Add parent directory to path to import u2l
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import u2l


class TestLatex2UnicodeMath(unittest.TestCase):
    """Test LaTeX to Unicode math conversions."""

    def setUp(self):
        """Set up test fixtures."""
        self.maxDiff = None

    def _convert(self, latex_str):
        """Helper to convert LaTeX to Unicode."""
        inp = io.StringIO(latex_str)
        out = io.StringIO()
        D = {k: chr(v[0]) for k, v in u2l.math_latex2unicode.items()}
        u2l.tex2uni(inp, out, D)
        return out.getvalue()

    def test_times_latex(self):
        """Test \\times → ×."""
        result = self._convert(r"\times")
        self.assertIn("×", result)

    def test_infty_latex(self):
        """Test \\infty → ∞."""
        result = self._convert(r"\infty")
        self.assertIn("∞", result)

    def test_cap_latex(self):
        """Test \\cap → ∩."""
        result = self._convert(r"\cap")
        self.assertIn("∩", result)

    def test_cup_latex(self):
        """Test \\cup → ∪."""
        result = self._convert(r"\cup")
        self.assertIn("∪", result)

    def test_int_latex(self):
        """Test \\int → ∫."""
        result = self._convert(r"\int")
        self.assertIn("∫", result)

    def test_subset_latex(self):
        """Test \\subset → ⊂."""
        result = self._convert(r"\subset")
        self.assertIn("⊂", result)

    def test_in_latex(self):
        """Test \\in → ∈."""
        result = self._convert(r"\in")
        self.assertIn("∈", result)

    def test_pm_latex(self):
        """Test \\pm → ±."""
        result = self._convert(r"\pm")
        self.assertIn("±", result)

    def test_neq_latex(self):
        """Test \\neq → ≠."""
        result = self._convert(r"\neq")
        self.assertIn("≠", result)

    def test_leq_latex(self):
        """Test \\leq → ≤."""
        result = self._convert(r"\leq")
        self.assertIn("≤", result)

    def test_geq_latex(self):
        """Test \\geq → ≥."""
        result = self._convert(r"\geq")
        self.assertIn("≥", result)

    def test_iff_latex(self):
        """Test \\iff → ⇔."""
        result = self._convert(r"\iff")
        self.assertIn("⇔", result)

    def test_circ_latex(self):
        """Test \\circ → ∘."""
        result = self._convert(r"\circ")
        self.assertIn("∘", result)


class TestLatex2UnicodeGreek(unittest.TestCase):
    """Test LaTeX to Unicode Greek letter conversions."""

    def _convert(self, latex_str):
        """Helper to convert LaTeX Greek to Unicode."""
        inp = io.StringIO(latex_str)
        out = io.StringIO()
        D = {k: chr(v) for k, v in u2l.greek_latex2unicode.items()}
        u2l.tex2uni(inp, out, D)
        return out.getvalue()

    def test_alpha_latex(self):
        """Test \\alpha → α."""
        result = self._convert(r"\alpha")
        self.assertIn("𝛼", result)  # Mathematical alpha

    def test_beta_latex(self):
        """Test \\beta → β."""
        result = self._convert(r"\beta")
        self.assertIn("𝛽", result)

    def test_gamma_latex(self):
        """Test \\gamma → γ."""
        result = self._convert(r"\gamma")
        self.assertIn("𝛾", result)

    def test_delta_latex(self):
        """Test \\delta → δ."""
        result = self._convert(r"\delta")
        self.assertIn("𝛿", result)

    def test_Gamma_latex(self):
        """Test \\Gamma → Γ."""
        result = self._convert(r"\Gamma")
        self.assertIn("Γ", result)

    def test_Delta_latex(self):
        """Test \\Delta → Δ."""
        result = self._convert(r"\Delta")
        # Delta can be either Δ or ∆
        self.assertTrue("Δ" in result or "∆" in result)

    def test_Omega_latex(self):
        """Test \\Omega → Ω."""
        result = self._convert(r"\Omega")
        self.assertIn("Ω", result)

    def test_theta_latex(self):
        """Test \\theta → θ."""
        result = self._convert(r"\theta")
        self.assertIn("𝜃", result)

    def test_lambda_latex(self):
        """Test \\lambda → λ."""
        result = self._convert(r"\lambda")
        self.assertIn("𝜆", result)

    def test_pi_latex(self):
        """Test \\pi → π."""
        result = self._convert(r"\pi")
        self.assertIn("𝜋", result)


class TestLatex2UnicodeMixed(unittest.TestCase):
    """Test mixed LaTeX to Unicode conversions."""

    def _convert_all(self, latex_str):
        """Helper to convert LaTeX to Unicode with both math and greek."""
        inp = io.StringIO(latex_str)
        out = io.StringIO()
        D = {}
        D.update({k: chr(v[0]) for k, v in u2l.math_latex2unicode.items()})
        D.update({k: chr(v) for k, v in u2l.greek_latex2unicode.items()})
        u2l.tex2uni(inp, out, D)
        return out.getvalue()

    def test_mixed_greek_and_math(self):
        """Test mixed Greek and math symbols."""
        result = self._convert_all(r"\alpha \in \mathbb{R}")
        self.assertIn("𝛼", result)
        self.assertIn("∈", result)

    def test_expression_with_multiple_symbols(self):
        """Test expression with multiple symbols."""
        result = self._convert_all(r"\alpha \times \beta")
        self.assertIn("𝛼", result)
        self.assertIn("×", result)
        self.assertIn("𝛽", result)


class TestLatex2UnicodePassthrough(unittest.TestCase):
    """Test that regular text passes through."""

    def _convert_empty(self, latex_str):
        """Helper to convert with empty dictionary."""
        inp = io.StringIO(latex_str)
        out = io.StringIO()
        u2l.tex2uni(inp, out, {})
        return out.getvalue()

    def test_plain_text(self):
        """Test plain text passes through unchanged."""
        result = self._convert_empty("hello world")
        self.assertEqual(result, "hello world")

    def test_numbers(self):
        """Test numbers pass through unchanged."""
        result = self._convert_empty("123 456")
        self.assertEqual(result, "123 456")

    def test_unknown_command(self):
        """Test unknown LaTeX commands pass through."""
        result = self._convert_empty(r"\unknown")
        self.assertIn("unknown", result)


class TestMathAccents(unittest.TestCase):
    """Test mathematical accents conversions."""

    def test_mathaccents_exist(self):
        """Test that mathaccents dictionaries are populated if possible."""
        # This will be populated if unicode_math_table_file exists
        # Just test that the dictionaries exist
        self.assertIsInstance(u2l.mathaccents_unicode2latex, dict)
        self.assertIsInstance(u2l.mathaccents_latex2unicode, dict)


class TestReplacementsTable(unittest.TestCase):
    """Test the replacements table."""

    def test_replacements_table_exists(self):
        """Test that math_replacements dictionary exists."""
        self.assertIsInstance(u2l.math_replacements, dict)

    def test_replacements_consistency(self):
        """Test that replacements are consistent with round-trip conversions."""
        for latex1, latex2 in u2l.math_replacements.items():
            # latex1 -> unicode -> latex2
            if latex1 in u2l.math_latex2unicode:
                unicode_code = u2l.math_latex2unicode[latex1][0]
                if unicode_code in u2l.math_unicode2latex:
                    back_latex = u2l.math_unicode2latex[unicode_code][0]
                    # The back conversion should match latex2
                    self.assertEqual(back_latex, latex2,
                                     f"Replacement {latex1} -> {latex2} inconsistent")


class TestDictionaryStructures(unittest.TestCase):
    """Test the internal dictionary structures."""

    def test_math_unicode2latex_structure(self):
        """Test math_unicode2latex dictionary structure."""
        self.assertIsInstance(u2l.math_unicode2latex, dict)
        for key, value in u2l.math_unicode2latex.items():
            self.assertIsInstance(key, int, "Keys should be integers (unicode codes)")
            self.assertIsInstance(value, list, "Values should be lists")
            if value:
                self.assertIsInstance(value[0], str, "List items should be strings")

    def test_math_latex2unicode_structure(self):
        """Test math_latex2unicode dictionary structure."""
        self.assertIsInstance(u2l.math_latex2unicode, dict)
        for key, value in u2l.math_latex2unicode.items():
            self.assertIsInstance(key, str, "Keys should be strings (LaTeX commands)")
            self.assertIsInstance(value, list, "Values should be lists")
            if value:
                self.assertIsInstance(value[0], int, "List items should be integers")

    def test_greek_latex2unicode_structure(self):
        """Test greek_latex2unicode dictionary structure."""
        self.assertIsInstance(u2l.greek_latex2unicode, dict)
        for key, value in u2l.greek_latex2unicode.items():
            self.assertIsInstance(key, str, "Keys should be strings")
            self.assertIsInstance(value, int, "Values should be integers")

    def test_greek_unicode2latex_structure(self):
        """Test greek_unicode2latex dictionary structure."""
        self.assertIsInstance(u2l.greek_unicode2latex, dict)
        for key, value in u2l.greek_unicode2latex.items():
            self.assertIsInstance(key, int, "Keys should be integers")
            self.assertIsInstance(value, str, "Values should be strings")

    def test_accents_unicode2latex_structure(self):
        """Test accents_unicode2latex dictionary structure."""
        self.assertIsInstance(u2l.accents_unicode2latex, dict)
        for key, value in u2l.accents_unicode2latex.items():
            self.assertIsInstance(key, int, "Keys should be integers")
            self.assertIsInstance(value, str, "Values should be strings")

    def test_accents_latex2unicode_structure(self):
        """Test accents_latex2unicode dictionary structure."""
        self.assertIsInstance(u2l.accents_latex2unicode, dict)
        for key, value in u2l.accents_latex2unicode.items():
            self.assertIsInstance(key, str, "Keys should be strings")
            self.assertIsInstance(value, int, "Values should be integers")


if __name__ == '__main__':
    unittest.main()
