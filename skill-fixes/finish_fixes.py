from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'manifest.json').read_text());by={Path(x['target']).parent.name:x for x in m if Path(x['target']).name=='SKILL.md'}
def stage(n):return Path(by[n]['staged'])
def add(target,s):
 target=Path(target);p=ROOT/'staged'/target.relative_to('/home/surajsinh');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
 if not any(x['target']==str(target) for x in m):m.append({'target':str(target),'staged':str(p),'before_sha256':hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None})
 return p
# Restore special URL schemes changed by moving references.
p=stage('template-creator').parent/'references/create-workflow.md';s=p.read_text().replace('](../plugin://','](plugin://').replace('directory containing this `SKILL.md`','directory containing the parent `SKILL.md` (one directory above this reference)');p.write_text(s)
# The shared document now delegates a surface-specific citation contract.
p=stage('spreadsheets').parent/'references/workbook-quality.md';s=p.read_text().replace('[Citation Requirements](#citation-requirements)','the Citation Requirements section of the active skill entrypoint');p.write_text(s)
# Moved references should explicitly state the resource base for inline paths too.
for n,rel in [('documents','references/equations.md'),('template-creator','references/create-workflow.md'),('visualize','references/specialized-layouts.md')]:
 p=stage(n).parent/rel;s=p.read_text();p.write_text('Resource paths in this reference are relative to the parent skill directory unless a link specifies otherwise.\n\n'+s)
# The shared formula guidance must not leave an old blanket prohibition in finance guides.
base=Path(by['spreadsheets']['target']).parent.parent
for n in ['spreadsheets','excel-live-control']:
 for p in (base/n).rglob('*.md'):
  if p.name=='SKILL.md':continue
  s=p.read_text()
  old='do not introduce `LET`, array/spill formulas, `MAP`, `REDUCE` or `LAMBDA`'
  if old in s:
   s=s.replace(old,'use `LET`, array/spill formulas, `MAP`, `REDUCE` or `LAMBDA` only when supported by the intended calculation engine and clearer for the requested task; validate recalculation and export compatibility')
   add(p,s)
# Optional package completeness checker: real links outside examples plus explicit metadata.
resource_checker='''#!/usr/bin/env python3
"""Check declared resources and prose Markdown links, without executing skill content."""
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def check_resources(skill_path, available_tools=None):
    import yaml
    root = Path(skill_path).resolve()
    content = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\\n(.*?)\\n---(?:\\n|$)", content, re.S)
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
        fence = re.match(r"^\\s*(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker is None:
                marker, length = fence.group(1)[0], len(fence.group(1))
            elif fence.group(1)[0] == marker and len(fence.group(1)) >= length and not fence.group(2).strip():
                marker = None
            continue
        if marker is None and not line.startswith(("    ", "\\t")):
            prose.append(line)
    for target in re.findall(r"\\[[^\\]]+\\]\\(([^)]+)\\)", "\\n".join(prose)):
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
'''
creator=Path(by['skill-creator']['target']).parent
add(creator/'scripts/check_resources.py',resource_checker)
p=creator/'scripts/quick_validate.py';s=p.read_text();s=s.replace('    if name:\n', '    if not name:\n        return False, "Name must not be empty"\n    if name:\n',1).replace('    if description.startswith("[TODO:"):', '    if not description:\n        return False, "Description must not be empty"\n    if description.startswith("[TODO:"):')
a=s.index('if __name__ == "__main__":')
s=s[:a]+'''if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory")
    parser.add_argument("--check-resources", action="store_true")
    parser.add_argument("--available-tool", action="append", default=None)
    args = parser.parse_args()
    valid, message = validate_skill(args.skill_directory)
    print(message)
    if valid and args.check_resources:
        from check_resources import check_resources
        errors = check_resources(args.skill_directory, args.available_tool)
        for error in errors:
            print(error)
        valid = not errors
    sys.exit(0 if valid else 1)
'''
add(p,s)
p=stage('skill-creator');s=p.read_text().replace('scripts/quick_validate.py <path/to/skill-folder>','scripts/quick_validate.py <path/to/skill-folder> --check-resources');s+='''\n## Package completeness\n\nThe optional `--check-resources` validator checks real Markdown links outside fenced examples and `metadata.required_resources` file paths. Declare essential scripts and schemas in that metadata when they are otherwise mentioned only as inline code. Use a list of skill-relative paths; do not declare illustrative examples. `metadata.required_tools` can list actual tool names, checked only when the caller supplies `--available-tool` entries from the current inventory. Resource validation does not execute scripts or prove behavioral correctness.\n''';p.write_text(s)
p=stage('codebase-knowledge');s=p.read_text().replace('license: MIT','license: MIT\nmetadata:\n  required_resources:\n    - references/knowledge-spec.md\n    - scripts/quick_validate.py\n    - scripts/visualize.py');p.write_text(s)
# Restored renderer must safely handle arbitrary documentation text, including closing-script strings.
p=stage('codebase-knowledge').parent/'scripts/visualize.py';s=p.read_text().replace('            node_type = fm.get("type") or "Untyped"\n            title = fm.get("title") or rel', '            if not isinstance(fm, dict):\n                fm = {}\n            node_type = str(fm.get("type") or "Untyped")\n            title = str(fm.get("title") or rel)')
s=s.replace("  row.innerHTML = '<span class=\"swatch\" style=\"background:' + colorOf[t] + '\"></span>' + t;", "  const swatch = document.createElement('span');\n  swatch.className = 'swatch';\n  swatch.style.background = colorOf[t];\n  row.append(swatch, document.createTextNode(t));")
s=s.replace("  tip.innerHTML = '<b>' + n.title + '</b><br>' + n.type + '<br><span style=\"color:#999\">' + n.id + '</span>';", "  tip.textContent = n.title + ' — ' + n.type + ' — ' + n.id;")
s=s.replace('    data = json.dumps({"nodes": nodes, "edges": edges})', '    data = json.dumps({"nodes": nodes, "edges": edges}).replace("<", "\\\\u003c").replace(">", "\\\\u003e").replace("&", "\\\\u0026")')
p.write_text(s)
(ROOT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print('Finalized',len(m),'staged file records')
