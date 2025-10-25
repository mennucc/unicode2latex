#!/usr/bin/env python3
"""
Unit tests to verify Bug #5 fix: Thread safety with instance variables.
"""

import unittest
import sys
import os
import threading
import time

# Add parent directory to path to from unicode2latex import u2l
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unicode2latex import u2l


class TestBug5ThreadSafetyFix(unittest.TestCase):
    """Test that Bug #5 fix makes the code thread-safe."""

    def test_no_global_variables(self):
        """Test that global variables are removed."""
        # Check that the old global variables don't exist
        self.assertFalse(hasattr(u2l, 'line_count'),
                        "Global line_count should be removed")
        self.assertFalse(hasattr(u2l, 'char_count'),
                        "Global char_count should be removed")
        self.assertFalse(hasattr(u2l, 'input_file'),
                        "Global input_file should be removed")

    def test_instance_variables_exist(self):
        """Test that instance variables are added."""
        decomposer = u2l.Decompose_to_tex()
        self.assertTrue(hasattr(decomposer, 'line_count'),
                       "Instance should have line_count")
        self.assertTrue(hasattr(decomposer, 'char_count'),
                       "Instance should have char_count")
        self.assertTrue(hasattr(decomposer, 'input_file'),
                       "Instance should have input_file")

    def test_instance_variables_initialized(self):
        """Test that instance variables are properly initialized."""
        decomposer = u2l.Decompose_to_tex()
        self.assertEqual(decomposer.line_count, 1)
        self.assertEqual(decomposer.char_count, 0)
        self.assertEqual(decomposer.input_file, 'cmdline')

    def test_custom_input_file_name(self):
        """Test that custom input_file can be set."""
        decomposer = u2l.Decompose_to_tex(input_file='test.txt')
        self.assertEqual(decomposer.input_file, 'test.txt')

    def test_char_count_increments_per_instance(self):
        """Test that char_count increments per instance."""
        decomposer1 = u2l.Decompose_to_tex()
        decomposer2 = u2l.Decompose_to_tex()

        decomposer1.parse("abc")
        decomposer2.parse("xy")

        # Each instance should track its own count
        self.assertEqual(decomposer1.char_count, 3)
        self.assertEqual(decomposer2.char_count, 2)

    def test_concurrent_instances_isolated(self):
        """Test that concurrent instances don't interfere."""
        results = []
        errors = []

        def convert_and_check(text, expected_chars):
            try:
                decomposer = u2l.Decompose_to_tex()
                decomposer.parse(text)
                result = decomposer.result

                # Check that char_count matches the text length
                if decomposer.char_count != expected_chars:
                    errors.append(
                        f"Expected char_count={expected_chars}, got {decomposer.char_count}"
                    )
                results.append((text, result, decomposer.char_count))
            except Exception as e:
                errors.append(f"Exception: {e}")

        threads = []
        test_cases = [
            ('α', 1),
            ('α β', 3),
            ('α β γ', 5),
            ('α β γ δ', 7),
            ('α β γ δ ε', 9),
        ]

        # Run multiple threads with different text lengths
        for _ in range(10):
            for text, expected in test_cases:
                t = threading.Thread(target=convert_and_check, args=(text, expected))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()

        # Check for errors
        if errors:
            self.fail(f"Thread isolation failures:\n" + "\n".join(errors))

        self.assertEqual(len(results), 50, "All threads should complete")

    def test_concurrent_line_count_isolated(self):
        """Test that line_count is isolated per instance."""
        results = []

        def parse_multiline(lines):
            decomposer = u2l.Decompose_to_tex()
            for line in lines:
                decomposer.parse(line)
                decomposer.line_count += 1
            results.append(decomposer.line_count)

        threads = []
        # Thread 1: 3 lines, Thread 2: 5 lines, Thread 3: 2 lines
        test_cases = [
            ['α\n', 'β\n', 'γ\n'],      # Should end with line_count=4
            ['a\n', 'b\n', 'c\n', 'd\n', 'e\n'],  # Should end with line_count=6
            ['x\n', 'y\n'],              # Should end with line_count=3
        ]

        for lines in test_cases:
            t = threading.Thread(target=parse_multiline, args=(lines,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Each thread should have its own line_count
        self.assertEqual(sorted(results), [3, 4, 6],
                        "Line counts should be isolated per instance")

    def test_input_file_isolated_per_instance(self):
        """Test that input_file is isolated per instance."""
        results = []

        def convert_with_filename(filename, text):
            decomposer = u2l.Decompose_to_tex(input_file=filename)
            decomposer.parse(text)
            results.append((filename, decomposer.input_file))

        threads = []
        filenames = ['file1.txt', 'file2.txt', 'file3.txt', 'stdin', 'cmdline']

        for filename in filenames:
            for _ in range(5):  # Create 5 threads for each filename
                t = threading.Thread(target=convert_with_filename,
                                   args=(filename, 'α'))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()

        # Check that each instance maintained its own filename
        for original_name, instance_name in results:
            self.assertEqual(original_name, instance_name,
                           "input_file should be isolated per instance")

    def test_uni2tex_creates_new_instance(self):
        """Test that uni2tex() creates a new instance each time."""
        # This ensures backward compatibility
        result1 = u2l.uni2tex("abc")
        result2 = u2l.uni2tex("xyz")

        self.assertEqual(result1, "abc")
        self.assertEqual(result2, "xyz")

    def test_stress_test_many_threads(self):
        """Stress test with many concurrent threads."""
        import random

        errors = []
        completed = []

        def random_conversion():
            try:
                texts = ['α', 'β', 'γ', '×', '∞', 'é', 'ñ', 'ℝ']
                text = random.choice(texts)
                result = u2l.uni2tex(text)
                completed.append(True)
            except Exception as e:
                errors.append(str(e))

        threads = []
        for _ in range(100):  # 100 concurrent threads
            t = threading.Thread(target=random_conversion)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
        self.assertEqual(len(completed), 100, "All threads should complete")


class TestBug5BackwardCompatibility(unittest.TestCase):
    """Test that the fix maintains backward compatibility."""

    def test_uni2tex_still_works(self):
        """Test that uni2tex() function still works as before."""
        result = u2l.uni2tex("α β γ")
        self.assertIn("\\alpha", result)
        self.assertIn("\\beta", result)
        self.assertIn("\\gamma", result)

    def test_decompose_to_tex_still_works(self):
        """Test that Decompose_to_tex class still works."""
        decomposer = u2l.Decompose_to_tex()
        decomposer.parse("α")
        result = decomposer.result
        self.assertIn("\\alpha", result)

    def test_all_constructor_params_still_work(self):
        """Test that all constructor parameters still work."""
        decomposer = u2l.Decompose_to_tex(
            add_font_modifiers=False,
            convert_accents=False,
            prefer_unicode_math=True
        )
        self.assertFalse(decomposer.add_font_modifiers)
        self.assertFalse(decomposer.convert_accents)
        self.assertTrue(decomposer.prefer_unicode_math)

    def test_new_input_file_param_optional(self):
        """Test that new input_file parameter is optional."""
        # Should work without input_file parameter
        decomposer = u2l.Decompose_to_tex()
        self.assertEqual(decomposer.input_file, 'cmdline')

        # Should work with input_file parameter
        decomposer = u2l.Decompose_to_tex(input_file='test.txt')
        self.assertEqual(decomposer.input_file, 'test.txt')


if __name__ == '__main__':
    unittest.main()
