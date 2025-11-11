#!/usr/bin/env python3
"""Command-line tests for --input-encoding handling."""

import os
import sys
import tempfile
import subprocess
import unittest
import shutil
import threading
import time
import codecs

# Make unicode2latex importable if the module gets imported inside tests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_test_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.dirname(_test_dir)
maincli = os.path.join(_repo_root, 'unicode2latex', 'u2l.py')


def _run_cli(*cli_args, **kwargs):
    """Run unicode2latex CLI with UTF-8 pipes for deterministic output."""
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


class TestCLIInputEncodingOption(unittest.TestCase):
    """Regression tests for the --input-encoding/--input-enc option."""

    def test_help_mentions_input_encoding(self):
        result = _run_cli('--help')
        output = result.stdout + result.stderr
        self.assertIn('--input-encoding', output)
        self.assertIn('--input-enc', output)

    def test_custom_legacy_encoding(self):
        """Explicit encoding should allow reading cp1252 files."""
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as fh:
            fh.write('café résumé'.encode('cp1252'))
            input_file = fh.name
        try:
            result = _run_cli('--input', input_file, '--input-encoding', 'cp1252')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("\\'", result.stdout)
        finally:
            os.unlink(input_file)

    def test_auto_detects_utf16_bom(self):
        """AUTO should detect UTF-16 files via BOM and process them."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-16', suffix='.txt', delete=False) as fh:
            fh.write('élève')
            input_file = fh.name
        try:
            result = _run_cli('--input', input_file, '--input-encoding', 'AUTO')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("\\'", result.stdout)
        finally:
            os.unlink(input_file)

    def test_auto_detection_failure_requests_manual_encoding(self):
        """If chardet cannot decide, CLI should politely error out."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt', delete=False) as fh:
            fh.write('plain ascii text')
            input_file = fh.name

        stub_dir = tempfile.mkdtemp()
        try:
            stub_path = os.path.join(stub_dir, 'chardet.py')
            with open(stub_path, 'w', encoding='utf-8') as stub:
                stub.write("def detect(data):\n    return {'encoding': None, 'confidence': 0.0}\n")
            env = os.environ.copy()
            env.setdefault('PYTHONIOENCODING', 'utf-8')
            env.setdefault('PYTHONUTF8', '1')
            existing = env.get('PYTHONPATH', '')
            env['PYTHONPATH'] = stub_dir if not existing else f"{stub_dir}{os.pathsep}{existing}"
            result = _run_cli('--input', input_file, '--input-encoding', 'AUTO', env=env)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('auto-detect', (result.stderr or '').lower())
        finally:
            os.unlink(input_file)
            shutil.rmtree(stub_dir, ignore_errors=True)

    def test_invalid_encoding_rejected(self):
        """Unknown codec names should be rejected by argparse validation."""
        result = _run_cli('--input-encoding', 'definitely-not-an-encoding', 'é')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unknown encoding', (result.stderr or '').lower())

    def test_stdin_auto_encoding_streaming(self):
        """AUTO stdin detection must not drop data arriving after the initial chunk."""
        proc = subprocess.Popen(
            [sys.executable, maincli, '--stdin', '--input-encoding', 'AUTO'],
            cwd=_repo_root,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        first_chunk = codecs.BOM_UTF8 + "café ".encode('utf-8')
        second_chunk = "résumé\n".encode('utf-8')

        writer_error = []

        def _writer():
            try:
                proc.stdin.write(first_chunk)
                proc.stdin.flush()
                time.sleep(0.2)
                proc.stdin.write(second_chunk)
            finally:
                try:
                    proc.stdin.close()
                except BrokenPipeError as exc:
                    writer_error.append(exc)

        t = threading.Thread(target=_writer, daemon=True)
        t.start()
        t.join()
        proc.stdin = None
        stdout, stderr = proc.communicate(timeout=5)
        if writer_error:
            self.fail(f"writer thread errored: {writer_error[0]}")
        self.assertEqual(proc.returncode, 0, stderr.decode('utf-8', errors='replace'))
        text = stdout.decode('utf-8', errors='replace')
        self.assertIn("caf\\'{e}", text)
        self.assertIn("r\\'{e}sum\\'{e}", text)


if __name__ == '__main__':
    unittest.main()
