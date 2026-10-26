#!/usr/bin/env python3
"""Summarize human-graded reviews; this does not infer correctness from prose."""
import argparse
import json
from pathlib import Path

VERDICTS = {'APPROVE', 'APPROVE WITH COMMENTS', 'REQUEST CHANGES', 'INCOMPLETE'}


def score(expected, grades):
    if not expected:
        raise ValueError('Expected suite must contain at least one case')
    expected_by_id = {item['id']: item for item in expected}
    if len(expected_by_id) != len(expected):
        raise ValueError('Duplicate expected case IDs')
    if len({item['id'] for item in grades}) != len(grades):
        raise ValueError('Duplicate graded case IDs')
    if {item['id'] for item in grades} != set(expected_by_id):
        raise ValueError('Grade every case exactly once; missing/extra cases are not allowed')
    results = []
    for grade in grades:
        oracle = expected_by_id[grade['id']]
        if grade['actual_verdict'] not in VERDICTS:
            raise ValueError('Invalid actual_verdict')
        for field, source in [('satisfied_required', 'required'), ('violated_forbidden', 'forbidden')]:
            values = grade[field]
            if not isinstance(values, list) or any(type(i) is not int or not 0 <= i < len(oracle[source]) for i in values):
                raise ValueError(f'Invalid criterion indices: {grade["id"]}.{field}')
            if len(set(values)) != len(values):
                raise ValueError(f'Duplicate criterion indices: {grade["id"]}.{field}')
        if not isinstance(grade['false_positives'], list) or any(not isinstance(s, str) or not s.strip() for s in grade['false_positives']):
            raise ValueError('false_positives must be a list of nonempty finding descriptions')
        if not isinstance(grade['evidence'], str) or not grade['evidence'].strip():
            raise ValueError('Each grade needs report evidence or citations')
        missed = sorted(set(range(len(oracle['required']))) - set(grade['satisfied_required']))
        verdict_ok = grade['actual_verdict'] == oracle['verdict']
        results.append({'id': grade['id'], 'verdict_correct': verdict_ok,
                        'missed_required': missed,
                        'forbidden_violations': grade['violated_forbidden'],
                        'false_positive_count': len(grade['false_positives']),
                        'passed': verdict_ok and not missed and not grade['violated_forbidden'] and not grade['false_positives']})
    return {'cases': len(results), 'passed': sum(r['passed'] for r in results),
            'verdict_accuracy': sum(r['verdict_correct'] for r in results) / len(results) if results else None,
            'missed_required_criteria': sum(len(r['missed_required']) for r in results),
            'false_positives': sum(r['false_positive_count'] for r in results),
            'results': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('expected', type=Path)
    parser.add_argument('grades', type=Path)
    args = parser.parse_args()
    try:
        result = score(json.loads(args.expected.read_text()), json.loads(args.grades.read_text()))
    except (ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] == result['cases'] else 1)


if __name__ == '__main__':
    main()
