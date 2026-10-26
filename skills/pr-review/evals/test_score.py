"""Meaningful scoring checks, independent of generated fixture wording."""
import unittest
from score import score


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.expected = [{'id': 'case', 'verdict': 'REQUEST CHANGES',
                          'required': ['Explain the broken contract.'],
                          'forbidden': ['Dismiss an unchanged caller.']}]
        self.grade = {'id': 'case', 'actual_verdict': 'REQUEST CHANGES',
                      'satisfied_required': [0], 'violated_forbidden': [],
                      'false_positives': [], 'evidence': 'Report explains the changed return type.'}

    def test_empty_suite_is_not_a_pass(self):
        with self.assertRaises(ValueError):
            score([], [])

    def test_correct_review(self):
        self.assertEqual(score(self.expected, [self.grade])['passed'], 1)

    def test_right_verdict_does_not_hide_missed_bug(self):
        self.grade['satisfied_required'] = []
        result = score(self.expected, [self.grade])
        self.assertEqual(result['passed'], 0)
        self.assertEqual(result['missed_required_criteria'], 1)

    def test_false_positive_fails_otherwise_correct_review(self):
        self.grade['false_positives'] = ['Claims a nonexistent SQL injection.']
        self.assertEqual(score(self.expected, [self.grade])['passed'], 0)

    def test_forbidden_behavior_fails(self):
        self.grade['violated_forbidden'] = [0]
        self.assertEqual(score(self.expected, [self.grade])['passed'], 0)

    def test_wrong_verdict_fails(self):
        self.grade['actual_verdict'] = 'APPROVE'
        self.assertEqual(score(self.expected, [self.grade])['verdict_accuracy'], 0)

    def test_omitted_case_cannot_inflate_score(self):
        with self.assertRaises(ValueError):
            score(self.expected, [])

    def test_invalid_criterion_rejected(self):
        self.grade['satisfied_required'] = [8]
        with self.assertRaises(ValueError):
            score(self.expected, [self.grade])

    def test_duplicate_case_rejected(self):
        with self.assertRaises(ValueError):
            score(self.expected, [self.grade, self.grade])


if __name__ == '__main__':
    unittest.main()
