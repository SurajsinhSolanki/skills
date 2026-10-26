#!/usr/bin/env python3
"""Generate the README catalog from installed-format skill metadata."""
import argparse
import json
import re
from pathlib import Path

from skills_ref import read_properties
from validate_skills import ROOT, discover

START = '<!-- SKILLS:START -->'
END = '<!-- SKILLS:END -->'


def render(root: Path) -> str:
    source = json.loads((root / 'repository.json').read_text())['github']
    if source is not None and not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', source):
        raise ValueError('repository.json github must be null or owner/repo')
    source = source or 'OWNER/REPO'
    lines = ['| Skill | Description | Installation |', '|---|---|---|']
    for skill in discover(root):
        props = read_properties(skill)
        description = ' '.join(props.description.split()).replace('|', '&#124;')
        lines.append(f'| [{props.name}](skills/{skill.name}/SKILL.md) | {description} | `npx skills add {source} --skill {props.name}` |')
    return '\n'.join(lines)


def update(root: Path, check: bool) -> bool:
    path = root / 'README.md'
    original = path.read_text()
    if original.count(START) != 1 or original.count(END) != 1:
        raise ValueError('README must contain one catalog marker pair')
    before, remaining = original.split(START)
    _, after = remaining.split(END)
    expected = before + START + '\n' + render(root) + '\n' + END + after
    if expected == original:
        return True
    if not check:
        path.write_text(expected)
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail instead of rewriting a stale catalog')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    current = update(args.root, args.check)
    if args.check and not current:
        parser.exit(1, 'Catalog is stale: run python scripts/update_catalog.py\n')
    print('Catalog is current.' if current else 'Catalog updated.')


if __name__ == '__main__':
    main()
