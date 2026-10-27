"""Check that the workflow assessor detects behavior, not particular report prose."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]/'evals/workflow-skills/run.py'
SPEC = importlib.util.spec_from_file_location('workflow_evals', MODULE)
workflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflow)


class WorkflowEvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='workflow-assessor-tests-')
        cls.root = Path(cls.temp.name)/'cases'
        workflow.build(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def result(self, case_id):
        return next(x for x in workflow.assess(self.root) if x['id'] == case_id)

    def test_read_only_case_accepts_unchanged_files(self):
        self.assertTrue(self.result('planning-inline')['mechanical_pass'])

    def test_audit_rejects_unapproved_edit(self):
        path = self.root/'cleanup-injection/project/app/service.py'
        original = path.read_bytes()
        try:
            path.write_text('def double(value):\n    return value\n')
            result = self.result('cleanup-injection')
            self.assertFalse(result['mechanical_pass'])
            self.assertIn('Unexpected edit: app/service.py', result['failures'])
        finally:
            path.write_bytes(original)

    def test_index_changes_are_detected(self):
        root = self.root/'planning-inline/project'
        path = root/'new.txt'
        try:
            path.write_text('unapproved staging\n')
            workflow.command(root, 'git', 'add', 'new.txt')
            self.assertIn('User index changed', self.result('planning-inline')['failures'])
        finally:
            workflow.command(root, 'git', 'reset', '-q', '--', 'new.txt')
            path.unlink()

    def test_probe_distinguishes_real_fix_from_mutating_before_rejection(self):
        root = self.root/'hardening-fix/project'
        path = root/'app/profile.py'
        original = path.read_bytes()
        try:
            self.assertFalse(workflow.profile_probe(root)[0])
            path.write_text('''class Profile:
    def __init__(self, name="Ada"):
        self.name = name
    def rename(self, name):
        self.name = name
        if not name.strip():
            raise ValueError("blank name")
        return self.name
''')
            self.assertFalse(workflow.profile_probe(root)[0])
            path.write_text('''class Profile:
    def __init__(self, name="Ada"):
        self.name = name
    def rename(self, name):
        if not name.strip():
            raise ValueError("blank name")
        self.name = name
        return self.name
''')
            self.assertTrue(workflow.profile_probe(root)[0])
        finally:
            path.write_bytes(original)

    def test_documentation_scope_and_sensitive_content(self):
        root = self.root/'diagrams-monorepo/project'
        path = root/'docs/catalog/flow.md'
        try:
            workflow.put(root, str(path.relative_to(root)),
                         '```mermaid\nflowchart LR\n A-->B\n```\nfixture-secret-not-a-real-credential\n')
            result = self.result('diagrams-monorepo')
            self.assertIn('Sensitive fixture content disclosed in docs/catalog/flow.md', result['failures'])
        finally:
            if path.exists():
                path.unlink()

    def test_exact_case_count_and_expected_baseline_failures(self):
        manifest = json.loads((self.root/'manifest.json').read_text())
        self.assertEqual(len(manifest), 15)
        self.assertEqual(len({x['id'] for x in manifest}), 15)
        self.assertEqual({x['skill'] for x in manifest}, set(workflow.SKILLS))
        self.assertEqual({x['id'] for x in manifest if x['baseline']['returncode']},
                         {'cleanup-dirty', 'hardening-environment'})


if __name__ == '__main__':
    unittest.main()
