#!/usr/bin/env python3
"""Apply this reviewed skill patch with hash guards, backups and atomic file replacement."""
from pathlib import Path
import argparse,hashlib,json,os,stat,tempfile,uuid
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent
ALLOWED=[Path('/home/surajsinh/.agents/skills'),Path('/home/surajsinh/.codex/skills/.system'),Path('/home/surajsinh/.codex/plugins/cache')]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def atomic_bytes(p,data,mode=0o644):
 p.parent.mkdir(parents=True,exist_ok=True)
 fd,name=tempfile.mkstemp(prefix='.'+p.name+'.skill-fix-',dir=p.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.chmod(name,mode);os.replace(name,p)
 finally:
  if os.path.exists(name):os.unlink(name)
def save_json(p,data):atomic_bytes(p,(json.dumps(data,indent=2)+'\n').encode())
def entries():
 result=[]
 for x in json.loads((ROOT/'manifest.json').read_text()):
  if not x.get('changed'):continue
  target=Path(x['target']);staged=Path(x['staged'])
  if not any(target.resolve().is_relative_to(r.resolve()) for r in ALLOWED):raise RuntimeError(f'Target outside skill roots: {target}')
  if target.is_symlink():raise RuntimeError(f'Refusing to replace symlink: {target}')
  if not staged.resolve().is_relative_to((ROOT/'staged').resolve()):raise RuntimeError(f'Invalid staged path: {staged}')
  if digest(staged)!=x['after_sha256']:raise RuntimeError(f'Staged file changed: {staged}')
  result.append(x)
 return result

def verify(xs):
 failures=[x['target'] for x in xs if digest(Path(x['target']))!=x['after_sha256']]
 if failures:raise RuntimeError('Installed hash mismatch: '+', '.join(failures))
 print(f'Verified {len(xs)} installed files.')

def rollback(state):
 conflicts=[]
 for x in reversed(state['files']):
  p=Path(x['target']);now=digest(p)
  if now==x['before_sha256']:continue
  if now!=x['after_sha256']:
   conflicts.append(str(p));continue
  if x['existed']:atomic_bytes(p,Path(x['backup']).read_bytes(),x['mode'])
  else:p.unlink()
 state['status']='rollback-conflict' if conflicts else 'rolled-back';state['rollback_conflicts']=conflicts
 save_json(Path(state['state_path']),state)
 if conflicts:raise RuntimeError('Rollback preserved concurrently changed files: '+', '.join(conflicts))

def apply(xs):
 conflicts=[];pending=[]
 for x in xs:
  current=digest(Path(x['target']))
  if current==x['after_sha256']:continue
  if current!=x['before_sha256']:conflicts.append(x['target'])
  else:pending.append(x)
 if conflicts:raise RuntimeError('Concurrent changes detected; no files written: '+', '.join(conflicts))
 if not pending:verify(xs);return
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
 backup_root=ROOT/'backups'/stamp
 backup_root.mkdir(parents=True)
 state={'status':'prepared','state_path':str(backup_root/'state.json'),'files':[]}
 for x in pending:
  p=Path(x['target']);exists=p.exists();mode=stat.S_IMODE(p.stat().st_mode) if exists else 0o644
  backup=backup_root/'files'/p.relative_to('/home/surajsinh')
  if exists:atomic_bytes(backup,p.read_bytes(),mode)
  if digest(p)!=x['before_sha256']:raise RuntimeError(f'Target changed while backing up: {p}')
  state['files'].append({**x,'existed':exists,'backup':str(backup),'mode':mode})
 save_json(Path(state['state_path']),state)
 try:
  for x in state['files']:
   p=Path(x['target'])
   if digest(p)!=x['before_sha256']:raise RuntimeError(f'Target changed before replacement: {p}')
   atomic_bytes(p,Path(x['staged']).read_bytes(),x['mode'])
  verify(xs)
 except BaseException:
  rollback(state)
  raise
 state['status']='applied';save_json(Path(state['state_path']),state)
 save_json(ROOT/'installation.json',{'status':'applied','backup_state':state['state_path'],'changed_files':len(pending),'verified_files':len(xs),'time_utc':datetime.now(timezone.utc).isoformat()})
 print(f'Applied {len(pending)} files. Backup: {backup_root}')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--apply',action='store_true');g.add_argument('--verify',action='store_true');g.add_argument('--check',action='store_true');g.add_argument('--rollback',type=Path);args=p.parse_args()
 if args.rollback:
  rollback(json.loads(args.rollback.read_text()));print('Rollback completed.')
 else:
  xs=entries()
  if args.apply:apply(xs)
  elif args.verify:verify(xs)
  else:
   conflicts=[x['target'] for x in xs if digest(Path(x['target'])) not in {x['before_sha256'],x['after_sha256']}]
   if conflicts:raise RuntimeError('Concurrent changes: '+', '.join(conflicts))
   print(f'Ready: {len(xs)} validated changes; no target conflicts.')
