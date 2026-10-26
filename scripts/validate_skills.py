#!/usr/bin/env python3
"""Official metadata validation plus collection-specific packaging checks."""
from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

from skills_ref import read_properties, validate

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', '.agents', '.claude', '.codex', '.cursor', '.aws', '.venv',
             'node_modules', '__pycache__', '.pytest_cache'}
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
INLINE_LINK = re.compile(r'!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\s*\)')
REFERENCE_LINK = re.compile(r'^ {0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)', re.M)
SECRET_PATTERNS = [
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
    re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    re.compile(r'\bgh[pousr]_[A-Za-z0-9]{36,}\b'),
    re.compile(r'\bgithub_pat_[A-Za-z0-9_]{60,}\b'),
    re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b'),
    re.compile(r'''(?i)\b(?:api[_-]?key|client[_-]?secret|password|access[_-]?token)\b["']?\s*[:=]\s*["']([A-Za-z0-9+/=_-]{20,})["']'''),
]
PERSONAL_PATH = re.compile(r'/(?:home|Users)/[A-Za-z0-9_.-]+/|[A-Za-z]:\\Users\\[^\\]+\\')


def files_under(root: Path):
    """Walk distribution content, without entering installations or following symlinks."""
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in dirs + sorted(files):
            path = Path(parent) / name
            if path.is_symlink() or path.is_file():
                yield path


def read_text(path: Path):
    try:
        data = path.read_bytes()
        return None if b'\0' in data else data.decode('utf-8')
    except (UnicodeDecodeError, OSError):
        return None


def unfenced(text: str) -> str:
    """Remove fenced examples for rendered Markdown link and heading checks."""
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            lines.append('')
        else:
            lines.append(line if fence is None else '')
    return '\n'.join(lines)


def anchors(text: str) -> set[str]:
    found = set(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)', text, re.I))
    counts = {}
    for line in unfenced(text).splitlines():
        match = re.match(r'^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?$', line)
        if not match:
            continue
        title = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', match[1]).strip().lower()
        slug = ''.join(c for c in title if c in ' -_' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        found.add(slug if count == 0 else f'{slug}-{count}')
    return found


def local_links(path: Path, text: str, boundary: Path) -> list[str]:
    errors = []
    visible = unfenced(text)
    for match in list(INLINE_LINK.finditer(visible)) + list(REFERENCE_LINK.finditer(visible)):
        destination = match[1].strip('<>')
        parsed = urlsplit(destination)
        if parsed.scheme or parsed.netloc:
            continue
        relative = unquote(parsed.path)
        target = (path.parent / relative).resolve() if relative else path.resolve()
        line = visible.count('\n', 0, match.start()) + 1
        prefix = f'{path}:{line}'
        if not target.is_relative_to(boundary.resolve()):
            errors.append(f'{prefix}: local reference escapes its distribution boundary: {destination}')
        elif not target.exists():
            errors.append(f'{prefix}: missing local reference: {destination}')
        elif parsed.fragment and target.suffix.lower() == '.md':
            content = read_text(target)
            if content is not None and unquote(parsed.fragment) not in anchors(content):
                errors.append(f'{prefix}: missing Markdown anchor: {destination}')
    return errors


def scan_text(path: Path, text: str) -> list[str]:
    errors = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if any(pattern.search(line) for pattern in SECRET_PATTERNS):
            errors.append(f'{path}:{line_number}: suspected credential/private key; value redacted')
        if PERSONAL_PATH.search(line):
            errors.append(f'{path}:{line_number}: hardcoded personal filesystem path')
    return errors


def discover(root: Path) -> list[Path]:
    directory = root / 'skills'
    return sorted(p for p in directory.iterdir() if p.is_dir() and not p.name.startswith('.')) if directory.is_dir() else []


def check_repository(root: Path) -> tuple[list[str], int]:
    root = root.resolve()
    errors = []
    skills = discover(root)
    if not skills:
        errors.append('No skills discovered under skills/<name>/')
    if (root / 'SKILL.md').exists():
        errors.append('Root SKILL.md shadows collection discovery; place skills under skills/<name>/')
    names = {}
    for skill in skills:
        entry = skill / 'SKILL.md'
        if skill.is_symlink():
            errors.append(f'{skill}: skill directories must not be symlinks')
            continue
        if not entry.is_file():
            errors.append(f'{skill}: missing SKILL.md')
            continue
        if not NAME.fullmatch(skill.name) or len(skill.name) > 64:
            errors.append(f'{skill}: use lowercase ASCII kebab-case, at most 64 characters')
        try:
            metadata = read_properties(skill)
            if metadata.metadata is not None and not isinstance(metadata.metadata, dict):
                errors.append(f'{entry}: metadata must be a string-to-string mapping')
            key = metadata.name.casefold()
            if key in names:
                errors.append(f'{entry}: duplicate skill name (also {names[key]})')
            names[key] = entry
            errors.extend(f'{entry}: {error}' for error in validate(skill))
        except Exception as exc:
            # YAML error messages can echo sensitive input; report type and location only.
            errors.append(f'{entry}: invalid frontmatter ({type(exc).__name__}); inspect locally')
        nested = [p for p in skill.rglob('SKILL.md') if p != entry and not any(part in SKIP_DIRS for part in p.relative_to(skill).parts)]
        if nested:
            errors.append(f'{skill}: nested SKILL.md creates ambiguous discovery')
    for path in files_under(root):
        boundary = next((s for s in skills if path.is_relative_to(s)), root)
        if path.is_symlink():
            if not path.resolve().is_relative_to(boundary) or not path.exists():
                errors.append(f'{path}: broken or escaping symlink')
            continue
        text = read_text(path)
        if text is None:
            continue
        errors.extend(scan_text(path, text))
        if path.suffix.lower() == '.md':
            errors.extend(local_links(path, text, boundary))
    return errors, len(skills)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    errors, count = check_repository(args.root)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Validated {count} skill(s): official metadata, packaging, local links/anchors, and basic secret/path scan.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
