from pathlib import Path
import json,hashlib,difflib
r=Path(__file__).resolve().parent;m=json.loads((r/'manifest.json').read_text());by={Path(x['target']).parent.name:x for x in m if Path(x['target']).name=='SKILL.md'}
def mutate(n,func):
 p=Path(by[n]['staged']);p.write_text(func(p.read_text()))
mutate('openai-docs',lambda s:s.replace('**First substantive action:** Search', '**For public documentation questions, first substantive source action:** Search').replace('before reading a reference, inspecting local or repository files, running a Codex manual or model resolver, drafting a plan, or answering from memory.', 'before answering public product facts from memory or running a model resolver. Local inspection and host-required progress updates may precede documentation lookup.').replace('**Only exception:**','**Broad documentation exception:**'))
mutate('codebase-knowledge',lambda s:s.replace('For each stale file, regenerate it per `references/knowledge-spec.md`, bump `version`, and set `timestamp` to now (ISO 8601).','For each stale file, first apply the human-edit protection in the next step. Regenerate only eligible or explicitly authorized files per `references/knowledge-spec.md`, bump `version`, and set `timestamp` to now (ISO 8601).'))
# A pinned commit may not be reachable in a shallow clone of the default branch.
p=Path('/home/surajsinh/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py')
s=p.read_text();old='    _run_git(["git", "-C", repo_dir, "checkout", ref])'
assert old in s
s=s.replace(old,'    _run_git(["git", "-C", repo_dir, "fetch", "--depth", "1", "origin", ref])\n    _run_git(["git", "-C", repo_dir, "checkout", "--detach", "FETCH_HEAD"])')
st=r/'staged'/p.relative_to('/home/surajsinh');st.parent.mkdir(parents=True,exist_ok=True);st.write_text(s)
m.append({'target':str(p),'staged':str(st),'before_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
# Preserve the exact baseline of every existing target for review and rollback planning.
diffs=[];changed=[]
for x in m:
 p=Path(x['target']);st=Path(x['staged']);old=p.read_bytes() if p.exists() else None;new=st.read_bytes()
 if old is not None and hashlib.sha256(old).hexdigest()!=x['before_sha256']:
  raise RuntimeError(f'Target changed during preparation: {p}')
 x['after_sha256']=hashlib.sha256(new).hexdigest();x['changed']=old!=new
 if x['changed']:
  changed.append(x['target'])
  diffs.extend(difflib.unified_diff((old or b'').decode().splitlines(True),new.decode().splitlines(True),fromfile=str(p),tofile=str(p)))
(r/'changes.diff').write_text(''.join(diffs))
(r/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print('Final package:',len(changed),'changed/new files')
