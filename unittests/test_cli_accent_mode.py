#!/usr/bin/env python3
"""
Unit tests for command-line interface accent mode option.

Tests the --accent-mode command-line argument that allows choosing
between text-mode and math-mode accent commands.
"""

import unittest
import sys
import os
import io
import tempfile
import subprocess

# Add parent directory to path to from unicode2latex import u2l
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unicode2latex import u2l

# Get the absolute path to the script for cross-platform compatibility
_test_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.dirname(_test_dir)
maincli = os.path.join(_repo_root, 'unicode2latex', 'u2l.py')

def _run_cli(*cli_args, **kwargs):
    """Run the unicode2latex CLI with consistent UTF-8 pipes across platforms."""
    env = os.environ.copy()
    env.setdefault('PYTHONIOENCODING', 'utf-8')
    env.setdefault('PYTHONUTF8', '1')
    run_kwargs = {
        'capture_output': True,
        'text': True,
        'encoding': 'utf-8',
        'errors': 'replace',
        'cwd': _repo_root,
        'env': env,
    }
    run_kwargs.update(kwargs)
    return subprocess.run([sys.executable, maincli, *cli_args], **run_kwargs)

class TestCLIAccentModeArgument(unittest.TestCase):
    """Test the --accent-mode command-line argument."""

    

    def test_help_shows_accent_mode_option(self):
        """Test that --help shows the --accent-mode option."""
        result = _run_cli('--help')
        # On some systems, help might go to stderr if there's an issue
        output = result.stdout + result.stderr
        # Debug output for CI
        if not output:
            print(f"DEBUG: returncode={result.returncode}, stdout={result.stdout!r}, stderr={result.stderr!r}", file=sys.stderr)
        self.assertIn('--accent-mode', output, f"Help output was empty. returncode={result.returncode}, stderr={result.stderr}")
        self.assertIn('text', output)
        self.assertIn('math', output)
        self.assertIn('auto', output)

    def test_accent_mode_default_text(self):
        """Test that default accent mode is 'text'."""
        result = _run_cli('é')
        self.assertEqual(result.returncode, 0)
        self.assertIn("\\'", result.stdout)
        self.assertNotIn("\\acute", result.stdout)

    def test_accent_mode_text_explicit(self):
        """Test --accent-mode=text explicitly."""
        result = _run_cli('--accent-mode=text', 'é')
        self.assertEqual(result.returncode, 0)
        self.assertIn("\\'", result.stdout)
        self.assertNotIn("\\acute", result.stdout)

    def test_accent_mode_math(self):
        """Test --accent-mode=math."""
        result = _run_cli('--accent-mode=math', 'é')
        self.assertEqual(result.returncode, 0)
        self.assertIn("\\acute", result.stdout)
        self.assertNotIn("\\'", result.stdout)

    def test_accent_mode_auto(self):
        """Test --accent-mode=auto (currently defaults to text)."""
        result = _run_cli('--accent-mode=auto', 'é')
        self.assertEqual(result.returncode, 0)
        # Currently auto defaults to text
        self.assertIn("\\'", result.stdout)

    def test_invalid_accent_mode_rejected(self):
        """Test that invalid accent mode is rejected."""
        result = _run_cli('--accent-mode=invalid', 'é')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('invalid choice', result.stderr.lower())


class TestCLIAccentModeWithMultipleAccents(unittest.TestCase):
    """Test accent mode with multiple accent types."""

    def test_multiple_accents_text_mode(self):
        """Test multiple accents in text mode."""
        result = _run_cli('é è ê ñ ü')
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("\\'", output)
        self.assertIn("\\`", output)
        self.assertIn("\\^", output)
        self.assertIn("\\~", output)
        self.assertIn('\\"', output)
        # Should NOT have math mode accents
        self.assertNotIn("\\acute", output)
        self.assertNotIn("\\grave", output)
        self.assertNotIn("\\hat", output)
        self.assertNotIn("\\tilde", output)
        self.assertNotIn("\\ddot", output)

    def test_multiple_accents_math_mode(self):
        """Test multiple accents in math mode."""
        result = _run_cli('--accent-mode=math', 'é è ê ñ ü')
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("\\acute", output)
        self.assertIn("\\grave", output)
        self.assertIn("\\hat", output)
        self.assertIn("\\tilde", output)
        self.assertIn("\\ddot", output)
        # Should NOT have text mode accents
        self.assertNotIn("\\'", output)
        self.assertNotIn("\\`", output)
        self.assertNotIn("\\^", output)
        self.assertNotIn("\\~", output)
        self.assertNotIn('\\"', output)


class TestCLIAccentModeWithFileInput(unittest.TestCase):
    """Test accent mode with file input."""

    def test_file_input_text_mode(self):
        """Test file input with text mode."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt', delete=False) as f:
            f.write('café résumé')
            temp_file = f.name

        try:
            result = _run_cli('--input', temp_file)
            self.assertEqual(result.returncode, 0)
            self.assertIn("\\'", result.stdout)
            self.assertNotIn("\\acute", result.stdout)
        finally:
            os.unlink(temp_file)

    def test_file_input_math_mode(self):
        """Test file input with math mode."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt', delete=False) as f:
            f.write('café résumé')
            temp_file = f.name

        try:
            result = _run_cli('--accent-mode=math', '--input', temp_file)
            self.assertEqual(result.returncode, 0)
            self.assertIn("\\acute", result.stdout)
            self.assertNotIn("\\'", result.stdout)
        finally:
            os.unlink(temp_file)

    def test_stdin_input_text_mode(self):
        """Test stdin input with text mode."""
        result = _run_cli('--stdin', input='é')
        self.assertEqual(result.returncode, 0)
        self.assertIn("\\'", result.stdout)
        self.assertNotIn("\\acute", result.stdout)

    def test_stdin_input_math_mode(self):
        """Test stdin input with math mode."""
        result = _run_cli('--accent-mode=math', '--stdin', input='é')
        self.assertEqual(result.returncode, 0)
        self.assertIn("\\acute", result.stdout)
        self.assertNotIn("\\'", result.stdout)


class TestCLIAccentModeWithOtherOptions(unittest.TestCase):
    """Test accent mode combined with other CLI options."""

    def test_accent_mode_with_no_accents(self):
        """Test that --no-accents disables accent conversion even with accent-mode."""
        result = _run_cli('--accent-mode=math', '--no-accents', 'é')
        self.assertEqual(result.returncode, 0)
        # Should preserve the unicode character
        self.assertIn('é', result.stdout)

    def test_accent_mode_with_no_fonts(self):
        """Test accent mode with --no-fonts."""
        result = _run_cli('--accent-mode=math', '--no-fonts', 'é ⅅ')
        self.assertEqual(result.returncode, 0)
        # Should have math accent
        self.assertIn("\\acute", result.stdout)
        # Should convert font character to plain letter (no font command)
        self.assertIn('D', result.stdout)
        self.assertNotIn('\\symbbit', result.stdout)

    def test_accent_mode_with_prefer_unicode_math(self):
        """Test accent mode with --prefer-unicode-math."""
        result = _run_cli('--accent-mode=math', '--prefer-unicode-math', 'é')
        self.assertEqual(result.returncode, 0)
        self.assertIn("\\acute", result.stdout)


class TestCLIAccentModeEdgeCases(unittest.TestCase):
    """Test edge cases for accent mode CLI option."""

    def test_empty_input_text_mode(self):
        """Test empty input with text mode."""
        result = _run_cli('')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), '')

    def test_empty_input_math_mode(self):
        """Test empty input with math mode."""
        result = _run_cli('--accent-mode=math', '')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), '')

    def test_no_accents_in_input(self):
        """Test input without accents in math mode."""
        result = _run_cli('--accent-mode=math', 'hello world')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), 'hello world')

    def test_mixed_unicode_text_mode(self):
        """Test mixed unicode (accents + greek) with text mode."""
        result = _run_cli('é α è')
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("\\'", output)
        self.assertIn("\\alpha", output)
        self.assertIn("\\`", output)

    def test_mixed_unicode_math_mode(self):
        """Test mixed unicode (accents + greek) with math mode."""
        result = _run_cli('--accent-mode=math', 'é α è')
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("\\acute", output)
        self.assertIn("\\alpha", output)
        self.assertIn("\\grave", output)


if __name__ == '__main__':
    unittest.main()
