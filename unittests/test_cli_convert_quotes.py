#!/usr/bin/env python3
"""CLI regression tests for --convert-quotes/--convert-dashes."""

import os
import sys
import subprocess
import unittest

_test_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.dirname(_test_dir)
maincli = os.path.join(_repo_root, 'unicode2latex', 'u2l.py')


def _run_cli(*cli_args, **kwargs):
    """Invoke unicode2latex with UTF-8-safe pipes."""
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


class TestCLIConvertQuotes(unittest.TestCase):
    """Verify --convert-quotes toggles curly-quote conversion."""

    def test_help_mentions_convert_quotes(self):
        result = _run_cli('--help')
        output = result.stdout + result.stderr
        self.assertIn('--convert-quotes', output)

    def test_convert_quotes_flag(self):
        result = _run_cli('--convert-quotes', '“quoted”', '‘text’')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("``quoted''", result.stdout)
        self.assertIn("`text'", result.stdout)

    def test_without_flag_preserves_unicode(self):
        result = _run_cli('“quoted”')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('“', result.stdout)
        self.assertIn('”', result.stdout)


class TestCLIDashConversion(unittest.TestCase):
    """Verify --convert-dashes normalizes punctuation."""

    def test_help_mentions_convert_dashes(self):
        result = _run_cli('--help')
        output = result.stdout + result.stderr
        self.assertIn('--convert-dashes', output)

    def test_convert_dashes_flag(self):
        text = "a–b\u00A0c"
        result = _run_cli('--convert-dashes', text)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("a--b~c", result.stdout)

    def test_without_flag_preserves_dash(self):
        result = _run_cli('a–b')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('–', result.stdout)
        self.assertNotIn('--', result.stdout)


if __name__ == '__main__':
    unittest.main()
