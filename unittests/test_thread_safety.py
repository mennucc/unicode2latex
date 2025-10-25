#!/usr/bin/env python3
"""
Unit tests for thread safety in unicode2latex.
"""

import unittest
import sys
import os
import threading

# Add parent directory to path to from unicode2latex import u2l
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unicode2latex import u2l


class TestThreadSafety(unittest.TestCase):
    """Test thread safety of u2l module."""

    def test_concurrent_conversions(self):
        """Test that concurrent conversions don't interfere with each other."""
        results = []
        errors = []

        def convert_text(text, expected):
            try:
                result = u2l.uni2tex(text)
                results.append((text, result, expected))
                # Check if the expected substring is in result
                if expected not in result:
                    errors.append(f"Expected '{expected}' in result for '{text}', got: {result}")
            except Exception as e:
                errors.append(f"Exception for '{text}': {e}")

        # Create multiple threads doing different conversions
        threads = []
        test_cases = [
            ('α β γ', '\\alpha'),
            ('∞ ∫ ∈', '\\infty'),
            ('é è ê', '\\^'),
            ('𝐀 𝐴 ℝ', '\\symbf'),
            ('× ∩ ⊂', '\\times'),
        ]

        # Run each test case 10 times in parallel
        for _ in range(10):
            for text, expected in test_cases:
                t = threading.Thread(target=convert_text, args=(text, expected))
                threads.append(t)
                t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Check for errors
        if errors:
            self.fail(f"Thread safety issues found:\n" + "\n".join(errors))

        self.assertEqual(len(results), len(threads), "Not all threads completed")

    def test_global_variable_corruption(self):
        """Test that global variables (line_count, char_count) don't cause issues."""
        # The module uses global variables line_count and char_count
        # which could cause issues in multi-threaded contexts

        def convert_long_text():
            text = "α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω"
            result = u2l.uni2tex(text)
            return result

        threads = []
        results = []

        for _ in range(5):
            t = threading.Thread(target=lambda: results.append(convert_long_text()))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # All results should be the same
        self.assertEqual(len(results), 5)
        # Check that all results contain expected content
        for result in results:
            self.assertIn('\\alpha', result)
            self.assertIn('\\omega', result)

    def test_decompose_to_tex_instance_isolation(self):
        """Test that Decompose_to_tex instances don't interfere with each other."""
        def convert_with_instance(text, expected):
            decomposer = u2l.Decompose_to_tex()
            decomposer.parse(text)
            result = decomposer.result
            return (result, expected in result)

        threads = []
        results = []

        test_cases = [
            ('α', '\\alpha'),
            ('β', '\\beta'),
            ('γ', '\\gamma'),
            ('δ', '\\delta'),
            ('ε', '\\epsilon'),
        ]

        for _ in range(10):
            for text, expected in test_cases:
                t = threading.Thread(target=lambda t=text, e=expected: results.append(convert_with_instance(t, e)))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()

        # Check all conversions succeeded
        for result, success in results:
            self.assertTrue(success, f"Conversion failed: {result}")


if __name__ == '__main__':
    unittest.main()
