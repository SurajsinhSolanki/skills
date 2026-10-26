"""Execute self-contained guide examples without network or dependency installation."""
import importlib.util
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def code_blocks(path, language):
    text = (ROOT / path).read_text()
    return re.findall(r'^```' + re.escape(language) + r'\n(.*?)^```\s*$', text, re.M | re.S)


class OfflineExamples(unittest.TestCase):
    def test_python_function_defaults(self):
        namespace = {}
        exec(code_blocks('frameworks/python.md', 'python')[0], namespace)
        bad, good = namespace['add_bad'], namespace['add_good']
        self.assertEqual(bad(1), [1])
        self.assertEqual(bad(2), [1, 2])
        self.assertEqual(good(1), [1])
        self.assertEqual(good(2), [2])

    def test_python_style_default_example(self):
        namespace = {}
        exec(code_blocks('styleguides/google-python.md', 'python')[0], namespace)
        self.assertEqual(namespace['collect_bad'](1), [1])
        self.assertEqual(namespace['collect_bad'](2), [1, 2])
        self.assertEqual(namespace['collect_good'](1), [1])
        self.assertEqual(namespace['collect_good'](2), [2])

    def test_sql_null_exclusion_example(self):
        statements = code_blocks('frameworks/sql.md', 'sql')[0].split(';')
        with sqlite3.connect(':memory:') as connection:
            connection.executescript('CREATE TABLE users(id INTEGER); INSERT INTO users VALUES(1),(2); '
                                     'CREATE TABLE blocked(user_id INTEGER); INSERT INTO blocked VALUES(1),(NULL);')
            results = [connection.execute(sql).fetchall() for sql in statements if sql.strip()]
        self.assertEqual(results, [[], [(2,)]])

    @unittest.skipUnless(shutil.which('node'), 'Node is unavailable; JS source was manually verified')
    def test_javascript_return_newline_example(self):
        code = code_blocks('styleguides/google-javascript.md', 'js')[0]
        result = subprocess.run(['node', '-e', code + '\nconst a = require("node:assert/strict"); '
                                 'a.equal(bad(), undefined); a.deepEqual(good(), {ok:true});'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(shutil.which('bash') and shutil.which('cp'), 'Bash/cp unavailable')
    def test_quoted_shell_copy_preserves_path_arguments(self):
        code = code_blocks('styleguides/google-shell.md', 'bash')[0]
        safe = next(line for line in code.splitlines() if line.startswith('cp --'))
        with tempfile.TemporaryDirectory(prefix='offline-shell-') as folder:
            src = Path(folder) / 'source with spaces'
            dst = Path(folder) / 'destination with spaces'
            src.write_text('fixture')
            result = subprocess.run(['bash', '-c', safe],
                                    env={**os.environ, 'source': str(src), 'destination': str(dst)},
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(dst.read_text(), 'fixture')

    @unittest.skipUnless(shutil.which('rustc'), 'rustc unavailable; example source-reviewed')
    def test_rust_checked_index_example(self):
        code = code_blocks('frameworks/rust.md', 'rust')[0]
        checked = next(line for line in code.splitlines() if 'items.get(index)' in line)
        with tempfile.TemporaryDirectory(prefix='offline-rust-') as folder:
            file = Path(folder) / 'main.rs'
            binary = Path(folder) / 'main'
            file.write_text('fn checked(items: &[i32], index: usize) -> Result<&i32, &\'static str> {\n' +
                            checked + '\nOk(item)\n}\nfn main() { '
                            'assert_eq!(checked(&[9], 0), Ok(&9)); assert!(checked(&[9], 2).is_err()); }')
            result = subprocess.run(['rustc', '--edition=2021', str(file), '-o', str(binary)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = subprocess.run([str(binary)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(importlib.util.find_spec('pydantic'), 'Pydantic unavailable; v2 semantics source-verified only')
    def test_pydantic_v2_defaults_if_already_installed(self):
        import pydantic
        if int(pydantic.__version__.split('.')[0]) != 2:
            self.skipTest('Installed Pydantic is not v2')
        class Batch(pydantic.BaseModel):
            items: list[int] = []
        a, b = Batch(), Batch()
        a.items.append(1)
        self.assertEqual(a.items, [1])
        self.assertEqual(b.items, [])


if __name__ == '__main__':
    unittest.main()
