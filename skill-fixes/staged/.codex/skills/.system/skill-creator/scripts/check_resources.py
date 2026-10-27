#!/usr/bin/env python3
"""Check declared resources and prose Markdown links, without executing skill content."""
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def check_resources(skill_path, available_tools=None):
    import yaml
    root = Path(skill_path).resolve()
    content = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.S)
    metadata = (yaml.safe_load(match.group(1)) or {}).get("metadata", {}) if match else {}
    if not isinstance(metadata, dict):
        return ["metadata must be a dictionary"]
    errors = []
    resources = metadata.get("required_resources", [])
    if not isinstance(resources, list) or any(not isinstance(p, str) for p in resources):
        return ["metadata.required_resources must be a list of relative file paths"]
    for resource in resources:
        path = (root / resource).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append(f"Required resource missing or outside skill: {resource}")
    # Fenced examples and indented code do not declare package dependencies.
    marker = None
    length = 0
    prose = []
    for line in content[match.end() if match else 0:].splitlines():
        fence = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker is None:
                marker, length = fence.group(1)[0], len(fence.group(1))
            elif fence.group(1)[0] == marker and len(fence.group(1)) >= length and not fence.group(2).strip():
                marker = None
            continue
        if marker is None and not line.startswith(("    ", "\t")):
            prose.append(line)
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", "\n".join(prose)):
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            continue
        path = Path(unquote(url.path))
        if path.is_absolute():
            continue  # Host locations are not package resources.
        if not (root / path).exists():
            errors.append(f"Linked resource missing: {target}")
    required_tools = metadata.get("required_tools", [])
    if not isinstance(required_tools, list) or any(not isinstance(t, str) for t in required_tools):
        errors.append("metadata.required_tools must be a list of names")
    elif available_tools is not None:
        for name in required_tools:
            if name not in available_tools:
                errors.append(f"Required tool unavailable: {name}")
    return sorted(set(errors))
