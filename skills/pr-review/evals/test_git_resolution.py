"""Verify Git edge cases used by the target-resolution guidance, not agent decisions."""
from pathlib import Path
import subprocess
import tempfile
import unittest

from run import Repo


class GitResolutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='review-resolution-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = Repo(self.root / 'repo')
        self.repo.write('file.txt', 'base\n')
        self.base = self.repo.commit('base')

    def test_branch_tag_short_name_can_be_ambiguous(self):
        self.repo.git('tag', 'release')
        self.repo.write('file.txt', 'next\n')
        head = self.repo.commit('next')
        self.repo.git('branch', 'release')
        self.assertNotEqual(self.repo.git('rev-parse', 'refs/tags/release^{commit}'),
                            self.repo.git('rev-parse', 'refs/heads/release^{commit}'))
        self.assertEqual(self.repo.git('rev-parse', '--verify', '--end-of-options',
                                       'refs/heads/release^{commit}'), head)

    def test_same_sha_remote_aliases_are_identical_comparisons(self):
        self.repo.git('update-ref', 'refs/remotes/upstream/main', self.base)
        self.repo.git('update-ref', 'refs/remotes/mirror/main', self.base)
        inventory = self.repo.git('for-each-ref', '--format=%(refname) %(objectname)',
                                  'refs/heads', 'refs/remotes')
        self.assertEqual(len(inventory.splitlines()), 3)
        self.assertEqual({line.split()[1] for line in inventory.splitlines()}, {self.base})

    def test_already_contained_head_has_empty_proposed_diff(self):
        self.repo.write('file.txt', 'newer base\n')
        newer = self.repo.commit('base advances')
        self.assertEqual(self.repo.git('merge-base', '--all', newer, self.base), self.base)
        self.assertEqual(self.repo.git('diff', newer + '...' + self.base), '')

    def test_unrelated_history_has_no_merge_base(self):
        tree = self.repo.git('rev-parse', 'HEAD^{tree}')
        unrelated = self.repo.git('commit-tree', tree, '-m', 'independent root')
        result = subprocess.run(['git', 'merge-base', '--all', self.base, unrelated],
                                cwd=self.repo.path, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '')
        self.assertEqual(self.repo.git('rev-parse', '--is-shallow-repository'), 'false')

    def test_criss_cross_graph_has_multiple_merge_bases(self):
        tree = self.repo.git('rev-parse', 'HEAD^{tree}')
        left = self.repo.git('commit-tree', tree, '-p', self.base, '-m', 'left')
        right = self.repo.git('commit-tree', tree, '-p', self.base, '-m', 'right')
        a = self.repo.git('commit-tree', tree, '-p', left, '-p', right, '-m', 'merge a')
        b = self.repo.git('commit-tree', tree, '-p', right, '-p', left, '-m', 'merge b')
        self.assertEqual(set(self.repo.git('merge-base', '--all', a, b).splitlines()),
                         {left, right})

    def test_shallow_clone_does_not_prove_unrelated_history(self):
        self.repo.write('file.txt', 'next\n')
        self.repo.commit('next')
        clone = self.root / 'shallow'
        subprocess.run(['git', 'clone', '-q', '--depth=1', self.repo.path.as_uri(), str(clone)],
                       check=True, capture_output=True)
        result = subprocess.check_output(['git', 'rev-parse', '--is-shallow-repository'],
                                         cwd=clone, text=True).strip()
        self.assertEqual(result, 'true')
        result = subprocess.run(['git', 'cat-file', '-e', self.base], cwd=clone,
                                capture_output=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
