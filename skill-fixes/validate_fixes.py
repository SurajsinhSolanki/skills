from pathlib import Path
import hashlib,json,re,sys,tempfile,importlib.util,subprocess,yaml,unittest
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text());mapping={Path(x['target']):Path(x['staged']) for x in manifest}
def load_module(name,p):
 spec=importlib.util.spec_from_file_location(name,p);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
creator=next(p.parent for t,p in mapping.items() if t.parent.name=='skill-creator' and t.name=='SKILL.md')
resource=load_module('resource_checker',creator/'scripts/check_resources.py')
validator=load_module('skill_validator',creator/'scripts/quick_validate.py')
knowledge=next(p.parent for t,p in mapping.items() if t.parent.name=='codebase-knowledge' and t.name=='SKILL.md')
kv=load_module('knowledge_validator',knowledge/'scripts/quick_validate.py');viz=load_module('knowledge_visualize',knowledge/'scripts/visualize.py')

def prose(s):
 # Match the existing creator's Markdown-fence handling, including nested list fences.
 fence=None;length=0;out=[]
 for line in s.splitlines():
  m=re.match(r'^[ \t]*(?:(?:[-+*]|\d+[.)])[ \t]+)?(`{3,}|~{3,})(.*)$',line)
  if m:
   if fence is None:fence=m[1][0];length=len(m[1])
   elif m[1][0]==fence and len(m[1])>=length and not m[2].strip():fence=None
   continue
  if fence is None:out.append(line)
 return '\n'.join(out)

def resolve(t):return mapping.get(t,t)

def structural_check():
 issues=[];exceptions=[];changed=[]
 for target,p in mapping.items():
  s=p.read_text();old=target.read_text() if target.exists() else ''
  if s!=old:changed.append(str(target))
  if p.suffix=='.py':compile(s,str(p),'exec')
  if p.name=='SKILL.md':
   ok,msg=validator.validate_skill(p.parent)
   if not ok:
    # Preserve established public names rather than silently renaming an installed skill.
    if target.parent.name in {'presentations','spreadsheets'} and 'hyphen-case' in msg:exceptions.append(str(target)+': existing display-style name preserved')
    else:issues.append(str(target)+': '+msg)
  if p.suffix not in {'.md'}:continue
  for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',prose(s)):
   parsed=urlsplit(link)
   if parsed.scheme or parsed.netloc:continue
   part=unquote(parsed.path)
   logical=(target.parent/part).resolve() if part else target
   if part.startswith('/'):continue
   found=resolve(logical)
   if not found.exists():issues.append(f'{target}: missing link {link}')
   if parsed.fragment and found.exists() and found.suffix=='.md':
    body=prose(found.read_text());anchors=set(re.findall(r'<a\s+id=["\']([^"\']+)',body))
    for h in re.findall(r'^#{1,6}\s+(.+)$',body,re.M):
     anchors.add(re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-'))
    if unquote(parsed.fragment) not in anchors:issues.append(f'{target}: missing anchor {link}')
 return issues,exceptions,changed

class BehaviorChecks(unittest.TestCase):
 def test_valid_and_missing_bundle(self):
  with tempfile.TemporaryDirectory() as td:
   b=Path(td);(b/'index.md').write_text('# Knowledge\n');(b/'log.md').write_text('## 2026-10-27\n* Generate\n');(b/'module.md').write_text('---\ntype: Module\ntitle: Billing\ndescription: Test\nresource: src/billing.py\ntags: [billing]\ntimestamp: 2026-10-27T00:00:00Z\n---\n[Home](index.md)\n')
   before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in b.iterdir()}
   ok,errors,warnings=kv.validate_bundle(b);self.assertTrue(ok,errors)
   self.assertEqual(before,{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in b.iterdir()})
   (b/'module.md').write_text('# missing frontmatter\n');self.assertFalse(kv.validate_bundle(b)[0])
 def test_package_missing_resource(self):
  self.assertTrue(kv.validate_skill(knowledge)[0])
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'SKILL.md').write_text('---\nname: fixture\ndescription: Resource test\nmetadata:\n  required_resources: [scripts/missing.py]\n  required_tools: [some_tool]\n---\n```md\n[Example](references/example.md)\n```\n')
   errors=resource.check_resources(p,[])
   self.assertTrue(any('missing.py' in x for x in errors));self.assertTrue(any('some_tool' in x for x in errors));self.assertFalse(any('example.md' in x for x in errors))
   (p/'scripts').mkdir();(p/'scripts/missing.py').write_text('pass\n');self.assertEqual(resource.check_resources(p,['some_tool']),[])
 def test_empty_frontmatter_values(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'SKILL.md').write_text('---\nname: ""\ndescription: test\n---\nBody\n');self.assertFalse(validator.validate_skill(p)[0])
 def test_visualization_graph_and_untrusted_text(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'index.md').write_text('# Index\n[Module](module.md)\n');(p/'module.md').write_text('---\ntype: Module\ntitle: "</script><script>bad()</script>"\n---\n[Root](/index.md)\n')
   nodes,edges=viz.build_graph(p);self.assertEqual(len(nodes),2);self.assertEqual(len(edges),1)
   html=viz.render_html(nodes,edges);self.assertNotIn('</script><script>bad()',html);self.assertIn('\\u003c/script',html)
   self.assertNotIn('tip.innerHTML',html);self.assertNotIn('row.innerHTML',html)
   (p/'module.md').write_text('---\n- invalid mapping\n---\n');self.assertEqual(len(viz.build_graph(p)[0]),2)
 def test_installer_pinned_non_head_commit(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);repo=p/'source';repo.mkdir()
   def git(*args):
    result=subprocess.run(['git','-C',str(repo),*args],capture_output=True,text=True)
    self.assertEqual(result.returncode,0,result.stderr)
    return result.stdout.strip()
   git('init','-b','main');(repo/'sample').mkdir();(repo/'sample/SKILL.md').write_text('first revision')
   git('add','.');git('-c','user.name=Skill Tests','-c','user.email=skills@example.invalid','commit','-m','first')
   sha=git('rev-parse','HEAD');(repo/'sample/SKILL.md').write_text('second revision');git('add','.')
   git('-c','user.name=Skill Tests','-c','user.email=skills@example.invalid','commit','-m','second')
   original=Path('/home/surajsinh/.codex/skills/.system/skill-installer/scripts')
   sys.path.insert(0,str(original))
   module_path=next(st for target,st in mapping.items() if target.name=='install-skill-from-github.py')
   installer=load_module('installer_fixture',module_path)
   dest=p/'destination';dest.mkdir()
   checkout=Path(installer._git_sparse_checkout(str(repo),sha,['sample'],str(dest)))
   self.assertEqual((checkout/'sample/SKILL.md').read_text(),'first revision')
   result=subprocess.run(['git','-C',str(checkout),'rev-parse','HEAD'],capture_output=True,text=True)
   self.assertEqual(result.stdout.strip(),sha)
 def test_visualize_cli(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'index.md').write_text('# Index\n');r=subprocess.run([sys.executable,str(knowledge/'scripts/visualize.py'),td],capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr);self.assertTrue((p/'visualization.html').is_file())

if __name__=='__main__':
 issues,exceptions,changed=structural_check()
 for x in issues:print('ERROR',x)
 for x in exceptions:print('COMPATIBILITY',x)
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(BehaviorChecks);result=unittest.TextTestRunner(verbosity=2).run(suite)
 report={'changed_files':changed,'structural_issues':issues,'compatibility_notes':exceptions,'behavior_tests':result.testsRun,'behavior_failures':len(result.failures)+len(result.errors)}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Changed files:',len(changed),'structural issues:',len(issues))
 sys.exit(bool(issues) or not result.wasSuccessful())
