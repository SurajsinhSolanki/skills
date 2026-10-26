"""Regression tests for collection failures, not skill prose."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from update_catalog import END, START, update
from validate_skills import check_repository, scan_text


class RepositoryChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skills-validator-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / 'skills' / 'real-task'
        self.skill.mkdir(parents=True)
        self.entry = self.skill / 'SKILL.md'
        self.entry.write_text('---\nname: real-task\ndescription: Perform a concrete task when requested.\n---\n\n# Task\n')

    def errors(self):
        return check_repository(self.root)[0]

    def test_valid_self_contained_skill(self):
        (self.skill / 'guide.md').write_text('# Repeated\n\n# Repeated\n')
        self.entry.write_text(self.entry.read_text() + '\n[Local](guide.md#repeated-1)\n')
        self.assertEqual([], self.errors())

    def test_missing_entry_is_not_silently_skipped(self):
        self.entry.unlink()
        self.assertTrue(any('missing SKILL.md' in error for error in self.errors()))

    def test_invalid_yaml_reports_location_without_echoing_input(self):
        self.entry.write_text('---\nname: [invalid\n---\n')
        errors = self.errors()
        self.assertTrue(any('invalid frontmatter' in error for error in errors))
        self.assertNotIn('[invalid', '\n'.join(errors))

    def test_duplicate_and_mismatched_name(self):
        other = self.root / 'skills' / 'another-task'
        other.mkdir()
        (other / 'SKILL.md').write_text(self.entry.read_text())
        self.assertTrue(any('duplicate skill name' in error for error in self.errors()))
        self.assertTrue(any('must match' in error for error in self.errors()))

    def test_missing_description_uses_official_parser(self):
        self.entry.write_text('---\nname: real-task\n---\n')
        self.assertTrue(any('frontmatter' in error for error in self.errors()))

    def test_metadata_requires_mapping(self):
        self.entry.write_text(self.entry.read_text().replace("description:", "metadata:\n  - invalid\ndescription:"))
        self.assertTrue(any("metadata must be" in error for error in self.errors()))

    def test_invalid_directory_name(self):
        self.skill.rename(self.skill.with_name('Bad_Name'))
        self.assertTrue(any('kebab-case' in error for error in self.errors()))

    def test_missing_file_and_anchor(self):
        self.entry.write_text(self.entry.read_text() + '\n[Absent](missing.md)\n[Anchor](#absent)\n')
        errors = self.errors()
        self.assertTrue(any('missing local reference' in error for error in errors))
        self.assertTrue(any('missing Markdown anchor' in error for error in errors))

    def test_skill_cannot_depend_on_collection_file(self):
        (self.root / 'README.md').write_text('# Collection\n')
        self.entry.write_text(self.entry.read_text() + '\n[Outside](../../README.md)\n')
        self.assertTrue(any('distribution boundary' in error for error in self.errors()))

    def test_fenced_example_is_not_a_live_reference(self):
        self.entry.write_text(self.entry.read_text() + '\n```md\n[Example](missing.md)\n```\n')
        self.assertEqual([], self.errors())

    def test_nested_and_root_entries_shadow_discovery(self):
        (self.root / 'SKILL.md').write_text(self.entry.read_text())
        nested = self.skill / 'nested'
        nested.mkdir()
        (nested / 'SKILL.md').write_text(self.entry.read_text())
        errors = self.errors()
        self.assertTrue(any('Root SKILL.md' in error for error in errors))
        self.assertTrue(any('nested SKILL.md' in error for error in errors))

    def test_escaping_symlink_is_rejected(self):
        (self.skill / 'escape').symlink_to(self.root / 'private')
        self.assertTrue(any('escaping symlink' in error for error in self.errors()))

    def test_credentials_are_detected_without_exposing_values(self):
        synthetic = 'gh' + 'p_' + 'a' * 36
        errors = scan_text(Path('fixture.txt'), synthetic)
        self.assertEqual(1, len(errors))
        self.assertNotIn(synthetic, '\n'.join(errors))
        literal = 'password = "' + 'b' * 24 + '"'
        self.assertTrue(scan_text(Path('fixture.txt'), literal))

    def test_catalog_rejects_staleness_and_updates_from_metadata(self):
        (self.root / 'repository.json').write_text(json.dumps({'github': None}))
        readme = self.root / 'README.md'
        readme.write_text('# Collection\n\n' + START + '\n' + END + '\n')
        original = readme.read_text()
        self.assertFalse(update(self.root, check=True))
        self.assertEqual(original, readme.read_text())
        update(self.root, check=False)
        self.assertTrue(update(self.root, check=True))
        self.assertIn('--skill real-task', readme.read_text())
        (self.root / 'repository.json').write_text(json.dumps({'github': 'example/collection'}))
        self.assertFalse(update(self.root, check=True))
        update(self.root, check=False)
        self.assertIn('example/collection', readme.read_text())


if __name__ == '__main__':
    unittest.main()
