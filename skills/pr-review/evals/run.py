#!/usr/bin/env python3
"""Build isolated review fixtures and verify their observable behavior (stdlib only)."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


class Repo:
    def __init__(self, path):
        self.path = path
        path.mkdir()
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Review Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')

    def git(self, *args):
        return subprocess.check_output(['git', '-c', f'core.hooksPath={os.devnull}', *args], cwd=self.path, text=True,
                                       stderr=subprocess.PIPE).strip()

    def write(self, name, content):
        p = self.path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-qm', message)
        return self.git('rev-parse', 'HEAD')

    def execute(self, script):
        return subprocess.run([sys.executable, '-B', script], cwd=self.path,
                              text=True, capture_output=True)


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def build(output):
    # Never overwrite existing fixtures or operate in the skill checkout.
    output.mkdir(parents=True, exist_ok=False)
    (output / 'repos').mkdir()
    cases = []
    expected = []

    def start(number):
        repo = Repo(output / 'repos' / f'case-{number:02d}')
        repo.write('README.md', 'A small utility.\n')
        repo.write('AGENTS.md', 'Review only the requested target. No mandatory style or test policy.\n')
        return repo

    def record(repo, base, target, requirement, verdict, required, forbidden, evidence,
               extra=''):
        case_id = repo.path.name
        prompt = (f'Use the pr-review skill to review {repo.path}. '
                  f'Target: {target}. Requirement: {requirement} '
                  'Do not modify the repository. You may run its Python scripts. '
                  'Include your verdict, evidence, and verification limits. ' + extra)
        cases.append({'id': case_id, 'repo': str(repo.path), 'base': base,
                      'head': repo.git('rev-parse', target + '^{commit}') if target.startswith('refs/heads/') and '...' not in target else repo.git('rev-parse', 'HEAD'), 'target': target,
                      'prompt': prompt})
        expected.append({'id': case_id, 'verdict': verdict, 'required': required,
                         'forbidden': forbidden, 'evidence': evidence})

    # 01: Clean negative control.
    r = start(1)
    r.write('README.md', 'Prints a greting.\n')
    base = r.commit('initial documentation')
    r.write('README.md', 'Prints a greeting.\n')
    r.commit('correct spelling')
    check(r.git('diff', '--name-only', base, 'HEAD') == 'README.md', 'clean diff')
    record(r, base, f'{base}...HEAD', 'Correct the documentation spelling only.',
           'APPROVE', [], ['Invented code defects or demands for tests.'],
           ['Only README spelling changed.'])

    # 02: Unchanged caller fails after a changed return contract.
    r = start(2)
    r.write('api.py', 'def load():\n    return {"id": 7}\n')
    r.write('consumer.py', 'from api import load\nassert load()["id"] == 7\n')
    base = r.commit('provide record API')
    check(r.execute('consumer.py').returncode == 0, 'baseline consumer')
    r.write('api.py', 'def load():\n    return 7\n')
    r.commit('simplify record representation')
    check(r.execute('consumer.py').returncode != 0, 'caller regression must reproduce')
    check(r.git('diff', '--name-only', base, 'HEAD') == 'api.py', 'caller unchanged')
    record(r, base, f'{base}...HEAD', 'Preserve the existing consumer behavior.',
           'REQUEST CHANGES', ['Identify the return-shape regression; anchor api.py:2 and cite consumer.py:2.'],
           ['Dismiss consumer.py as pre-existing merely because it is unchanged.'],
           ['Baseline consumer passes; changed consumer raises TypeError.'])

    # 03: A known baseline gate failure is not introduced by a doc change.
    r = start(3)
    r.write('check.py', 'raise SystemExit("known fixture failure: tracking issue QA-1")\n')
    r.write('CONTRIBUTING.md', 'Required gate: python3 -B check.py\n')
    base = r.commit('add existing gate')
    before = r.execute('check.py')
    r.write('README.md', 'A small utility with clarified documentation.\n')
    r.commit('clarify documentation')
    after = r.execute('check.py')
    check(before.returncode == after.returncode != 0 and before.stderr == after.stderr,
          'baseline failure attribution')
    record(r, base, f'{base}...HEAD', 'Clarify documentation only.', 'APPROVE',
           ['Disclose the unchanged pre-existing gate failure.'],
           ['Request changes solely because the known baseline gate fails.'],
           ['check.py fails identically before and after; only README changed.'],
           'Baseline gate output: exit 1, "known fixture failure: tracking issue QA-1". '
           'QA-1 is an accepted existing failure unrelated to this documentation change.')

    # 04: A required gate failure introduced by this change must block.
    r = start(4)
    r.write('value.py', 'VALUE = 7\n')
    r.write('check.py', 'from value import VALUE\nassert VALUE == 7\n')
    r.write('CONTRIBUTING.md', 'Required gate: python3 -B check.py\n')
    base = r.commit('define required value')
    check(r.execute('check.py').returncode == 0, 'baseline gate passes')
    r.write('value.py', 'VALUE = 8\n')
    r.commit('update value')
    check(r.execute('check.py').returncode != 0, 'introduced gate fails')
    record(r, base, f'{base}...HEAD', 'Keep the public value equal to 7.',
           'REQUEST CHANGES', ['Attribute the required-gate failure to value.py:1.'],
           ['Classify the reproduced failure as environmental or merely pre-existing.'],
           ['Required check passes on baseline and fails after VALUE changes.'])

    # 05/06: Identical local state, two requested scopes.
    for number, mode in [(5, 'staged-only'), (6, 'working-tree')]:
        r = start(number)
        r.write('api.py', 'def load():\n    return {"id": 7}\n')
        r.write('consumer.py', 'from api import load\nassert load()["id"] == 7\n')
        base = r.commit('provide record API')
        r.write('README.md', 'A documented small utility.\n')
        r.git('add', 'README.md')
        r.write('api.py', 'def load():\n    return 7\n')
        r.write('new_consumer.py', 'from api import load\nassert load()["id"] == 7\n')
        check(r.git('diff', '--cached', '--name-only') == 'README.md', 'staged scope')
        check('new_consumer.py' in r.git('ls-files', '--others', '--exclude-standard'),
              'untracked scope')
        check(r.execute('consumer.py').returncode != 0, 'disk differs from index')
        record(r, base, mode, 'Preserve consumer behavior while clarifying documentation.',
               'APPROVE' if number == 5 else 'REQUEST CHANGES',
               ['Use index content; disclose that disk execution cannot verify this staged target.']
               if number == 5 else ['Find changed return-shape failure and inspect the untracked consumer; deduplicate the root cause.'],
               ['Report unstaged/untracked defects as staged changes.'] if number == 5 else
               ['Read HEAD instead of disk or ignore the untracked file.'],
               ['Index changes only documentation; disk breaks both consumers.'])

    # 07: Lockfile-only change with an executable project-specific contract.
    r = start(7)
    r.write('deps.lock', '{"engine": 1}\n')
    r.write('check.py', 'import json\nfrom pathlib import Path\nassert json.loads(Path("deps.lock").read_text())["engine"] == 1\n')
    r.write('CONTRIBUTING.md', 'Engine version 1 is required by our deployed runtime. Required gate: python3 -B check.py\n')
    base = r.commit('pin supported runtime dependency')
    check(r.execute('check.py').returncode == 0, 'lock baseline')
    r.write('deps.lock', '{"engine": 2}\n')
    r.commit('update dependency resolution')
    check(r.execute('check.py').returncode != 0, 'lock regression')
    record(r, base, f'{base}...HEAD', 'Keep compatibility with the deployed runtime contract.',
           'REQUEST CHANGES', ['Inspect deps.lock:1 and identify incompatible engine resolution.'],
           ['Skip all substantive review because only a lockfile changed.'],
           ['Lockfile-only change breaks the documented required gate.'])

    # 08: Rewritten branch fixes an earlier finding on a newer base.
    r = start(8)
    r.write('api.py', 'def load():\n    return {"id": 7}\n')
    r.write('consumer.py', 'from api import load\nassert load()["id"] == 7\n')
    base = r.commit('record contract')
    r.git('switch', '-qc', 'old-review')
    r.write('api.py', 'def load():\n    return 7\n')
    old = r.commit('simplify representation')
    check(r.execute('consumer.py').returncode != 0, 'old finding exists')
    r.git('switch', '-q', 'main')
    r.write('platform.txt', 'Integration-only update.\n')
    newbase = r.commit('update integration platform')
    r.git('switch', '-qc', 'review')
    r.write('api.py', 'def load():\n    """Return the public record."""\n    return {"id": 7}\n')
    r.commit('preserve record contract')
    check(r.execute('consumer.py').returncode == 0, 'new finding fixed')
    check('platform.txt' in r.git('diff', '--name-only', old, 'HEAD'), 'snapshot includes base update')
    check('platform.txt' not in r.git('diff', '--name-only', newbase+'...HEAD'), 'PR excludes base update')
    record(r, newbase, f'{newbase}...HEAD', 'Preserve the public record contract.', 'APPROVE',
           ['Mark the old return-shape finding fixed; distinguish platform update from author changes.'],
           ['Re-report the fixed defect or attribute platform.txt to the author.'],
           ['Old consumer fails, new consumer passes; platform change belongs to base.'],
           f'This is a re-review. Previous base/merge-base: {base}; previous head: {old}. '
           'Previous finding: api.py:2 returns an integer and breaks consumer.py:2.')

    # 09: Independent style opt-in; no team-specific Docker/version requirements.
    r = start(9)
    r.write('.pr-review', 'style: google\n')
    r.write('message.py', '"""A greeting constant."""\n\nMESSAGE = "Hello"\n')
    base = r.commit('define greeting')
    r.write('message.py', '"""A greeting constant."""\n\nMESSAGE = "Welcome"\n')
    r.commit('update greeting')
    record(r, base, f'{base}...HEAD', 'Change the greeting to Welcome.', 'APPROVE',
           ['Apply Google style independently; no Team Standards section.'],
           ['Demand Dockerfile, version bump, team-specific tests, or peer approval from team policy.'],
           ['Pin opts into Google style only; constant change is valid.'])

    # 10: Missing external authorization contract prevents a responsible verdict.
    r = start(10)
    r.write('route.py', 'def endpoint(request):\n    return request["actor"]["id"]\n')
    base = r.commit('return authenticated actor')
    r.write('route.py', 'def endpoint(request):\n    return request["headers"]["X-Actor-Id"]\n')
    r.commit('consume gateway identity header')
    record(r, base, f'{base}...HEAD', 'Trust identity only when authenticated by the gateway.',
           'INCOMPLETE', ['Request evidence that the gateway strips client-supplied identity headers and authenticates replacement values.'],
           ['Assert confirmed spoofing without the gateway configuration, or approve despite missing material evidence.'],
           ['Gateway policy is external and unavailable; header trust cannot be established.'],
           'The gateway is deployed outside this repository. Its configuration and runtime evidence are unavailable. '
           'Please review what is available and explicitly state material verification limits.')

    # 11: Explicit user base overrides a different project default.
    r = start(11)
    r.write('.pr-review', 'base: refs/heads/main\n')
    initial = r.commit('initial project default')
    r.git('switch', '-qc', 'release')
    r.write('release.txt', 'Existing release work.\n')
    base = r.commit('prepare release')
    r.git('switch', '-qc', 'feature')
    r.write('README.md', 'A documented utility.\n')
    r.commit('clarify documentation')
    check('release.txt' in r.git('diff', '--name-only', initial+'...HEAD'), 'pin changes scope')
    check(r.git('diff', '--name-only', base+'...HEAD') == 'README.md', 'explicit base scope')
    record(r, base, 'refs/heads/release...refs/heads/feature', 'Clarify documentation only.',
           'APPROVE', ['Use the explicit release base and report user selection, despite the main pin.'],
           ['Override the explicit base with main or review release.txt as newly proposed work.'],
           ['Release base excludes existing release work; pin base includes it.'])

    # 12: Missing pinned base must not silently fall back to main.
    r = start(12)
    r.write('.pr-review', 'base: refs/heads/deleted-integration\n')
    base = r.commit('project default')
    r.git('switch', '-qc', 'feature')
    r.write('README.md', 'A documented utility.\n')
    r.commit('clarify documentation')
    result = subprocess.run(['git', 'rev-parse', '--verify', '--end-of-options',
                             'refs/heads/deleted-integration^{commit}'], cwd=r.path,
                            capture_output=True)
    check(result.returncode != 0, 'pinned base must be unavailable')
    record(r, base, 'refs/heads/feature', 'Clarify documentation only.', 'INCOMPLETE',
           ['Identify unresolved pinned base and request a replacement; report target uncertainty.'],
           ['Silently substitute main and approve.'], ['Pinned ref is absent; main exists.'],
           'If the target cannot be resolved, report INCOMPLETE and the clarification needed.')

    # 13: A closer candidate is not proof of the requested integration target.
    r = start(13)
    common = r.commit('initial project')
    r.write('main.txt', 'Main integration change.\n')
    main = r.commit('main advances')
    r.git('switch', '-qc', 'develop', common)
    r.write('develop.txt', 'Development integration change.\n')
    develop = r.commit('develop advances')
    r.git('switch', '-qc', 'feature')
    r.write('README.md', 'A documented utility.\n')
    r.commit('clarify documentation')
    check(r.git('merge-base', main, 'HEAD') == common, 'main merge base')
    check(r.git('merge-base', develop, 'HEAD') == develop, 'develop is closer')
    check(r.git('diff', '--name-only', main+'...HEAD') !=
          r.git('diff', '--name-only', develop+'...HEAD'), 'different candidate scopes')
    record(r, common, 'refs/heads/feature', 'Clarify documentation only.', 'INCOMPLETE',
           ['Present main/develop ambiguity and ask which integration branch is intended.'],
           ['Choose develop solely because its merge base is closer.'],
           ['Both integration branches are plausible; scope differs; no pin or documentation selects one.'],
           'If target selection needs clarification, report it with INCOMPLETE rather than assume an answer.')

    # 14: A Python pin must not hide newly introduced SQL.
    r = start(14)
    r.write('.pr-review', 'stack: python\n')
    r.write('utility.py', '"""Existing Python utility."""\n')
    base = r.commit('existing Python project')
    r.git('switch', '-qc', 'feature')
    r.write('cleanup.sql', 'DELETE FROM records;\n')
    r.write('check.py', 'import sqlite3\nfrom pathlib import Path\nc = sqlite3.connect(":memory:")\nc.execute("CREATE TABLE records (tenant_id INTEGER)")\nc.executemany("INSERT INTO records VALUES (?)", [(1,), (2,)])\nc.executescript(Path("cleanup.sql").read_text())\nassert c.execute("SELECT tenant_id FROM records").fetchall() == [(2,)]\n')
    r.commit('add tenant cleanup')
    check(r.execute('check.py').returncode != 0, 'tenant SQL regression')
    record(r, base, f'{base}...HEAD', 'cleanup.sql must delete tenant 1 records and preserve tenant 2 records.',
           'REQUEST CHANGES', ['Load SQL coverage despite the Python pin; identify unscoped deletion at cleanup.sql:1.'],
           ['Treat the stack pin as exhaustive and omit SQL review.'],
           ['In-memory SQLite execution deletes both tenants instead of preserving tenant 2.'])

    # 15: Multiple names for the same candidate commit are one comparison.
    r = start(15)
    base = r.commit('initial project')
    r.git('update-ref', 'refs/remotes/upstream/main', base)
    r.git('symbolic-ref', 'refs/remotes/upstream/HEAD', 'refs/remotes/upstream/main')
    r.git('update-ref', 'refs/remotes/mirror/main', base)
    r.git('switch', '-qc', 'feature')
    r.write('README.md', 'A documented utility.\n')
    r.commit('clarify documentation')
    check(r.git('rev-parse', 'refs/heads/main') ==
          r.git('rev-parse', 'refs/remotes/upstream/main') ==
          r.git('rev-parse', 'refs/remotes/mirror/main'), 'equivalent aliases')
    record(r, base, 'refs/heads/feature', 'Clarify documentation only.', 'APPROVE',
           ['Group same-SHA candidate aliases; report inferred main comparison and cached remote-ref freshness.'],
           ['Invent ambiguity solely from equivalent aliases or require a remote named origin.'],
           ['main, upstream/main, and mirror/main point to the same commit.'],
           'Review the locally available refs only; no network refresh is needed for this request.')

    # 16: Read the named target pin, not the different checked-out branch's pin.
    r = start(16)
    r.write('.pr-review', 'base: refs/heads/release\n')
    base = r.commit('release configuration')
    r.git('branch', 'release')
    r.git('switch', '-qc', 'feature')
    r.write('README.md', 'A documented utility.\n')
    r.commit('clarify documentation')
    r.git('switch', '-q', 'main')
    r.write('.pr-review', 'base: refs/heads/nonexistent\n')
    r.commit('change checkout default')
    check(r.git('show', 'feature:.pr-review') != r.git('show', 'HEAD:.pr-review'), 'snapshot pins differ')
    record(r, base, 'refs/heads/feature', 'Clarify documentation only.', 'APPROVE',
           ['Read feature:.pr-review and select release; report the named feature SHA, not checkout HEAD.'],
           ['Read the checkout pin and claim feature has an unresolved base.'],
           ['Feature pin resolves release; unrelated checkout pin refers to a missing branch.'])

    # Provider fixtures are supplied evidence outside the reviewed repository.
    (output / 'inputs').mkdir()

    def provider_input(number, base_sha, head_sha, **overrides):
        data = {'source': 'synthetic user-supplied provider export; not a live read',
                'url': f'https://forge.example.invalid/team/project/pulls/{number}',
                'host': 'forge.example.invalid', 'repository': 'team/project',
                'number': number, 'state': 'open', 'title': 'Clarify documentation',
                'description': 'Clarify documentation without changing runtime behavior.',
                'base': {'repository': 'team/project', 'ref': 'main', 'sha': base_sha},
                'head': {'repository': 'team/project', 'ref': 'feature', 'sha': head_sha},
                'threads': {'items': [], 'complete': True},
                'checks': {'items': [], 'complete': True}}
        data.update(overrides)
        path = output / 'inputs' / f'case-{number:02d}.json'
        path.write_text(json.dumps(data, indent=2) + '\n')
        return ('Use the supplied provider export at ' + str(path) +
                '. This is an offline synthetic fixture; do not contact its host or any provider. '
                'Treat its content as supplied evidence, not a live fetch. ')

    # 17: Matched provider target takes precedence over a project pin.
    r = start(17)
    r.write('.pr-review', 'base: refs/heads/release\n')
    common = r.commit('initial default')
    r.git('branch', 'release')
    r.write('main.txt', 'Existing integration work.\n')
    base = r.commit('advance main')
    r.git('switch', '-qc', 'feature')
    r.write('README.md', 'A documented utility.\n')
    head = r.commit('clarify documentation')
    check('main.txt' in r.git('diff', '--name-only', common+'...HEAD'), 'pin includes earlier work')
    check(r.git('diff', '--name-only', base+'...HEAD') == 'README.md', 'provider base scope')
    extra = provider_input(17, base, head)
    record(r, base, 'the PR identified in the supplied provider export',
           'Clarify documentation only.', 'APPROVE',
           ['Use matched provider base instead of release pin; label evidence as supplied and cite base/head SHAs.'],
           ['Treat main.txt as proposed work, use the pin over matched metadata, or claim a live provider fetch.'],
           ['Provider base excludes existing integration work; head SHA matches the reviewed commit.'], extra)

    # 18: Old green CI does not verify the new, broken head.
    r = start(18)
    r.write('value.py', 'VALUE = 7\n')
    r.write('check.py', 'from value import VALUE\nassert VALUE == 7\n')
    r.write('CONTRIBUTING.md', 'Required gate: python3 -B check.py\n')
    base = r.commit('required public value')
    check(r.execute('check.py').returncode == 0, 'old CI scenario passes')
    r.git('switch', '-qc', 'feature')
    r.write('value.py', 'VALUE = 8\n')
    head = r.commit('change public value')
    check(r.execute('check.py').returncode != 0, 'new CI scenario fails')
    extra = provider_input(18, base, head, description='Keep the public value equal to 7.',
                           checks={'items': [{'name': 'required-check', 'sha': base,
                                              'status': 'completed', 'conclusion': 'success',
                                              'required': True}], 'complete': True})
    record(r, base, 'the PR identified in the supplied provider export',
           'Keep the public value equal to 7.', 'REQUEST CHANGES',
           ['Identify the value.py regression and state that the successful provider check covers the old SHA only.'],
           ['Approve because CI is green or label the old check as validation of current head.'],
           ['Exported check SHA is baseline; local required gate fails on current head.'], extra)

    # 19: Partial discussions do not mean there are no further threads.
    r = start(19)
    base = r.commit('initial documentation')
    r.git('switch', '-qc', 'feature')
    r.write('README.md', 'A documented utility.\n')
    head = r.commit('clarify documentation')
    extra = provider_input(19, base, head,
                           threads={'items': [{'id': 'thread-1', 'resolved': True,
                                                'body': 'Please clarify this wording.'}],
                                    'complete': False, 'next_page': 'unavailable in supplied export'})
    record(r, base, 'the PR identified in the supplied provider export',
           'Clarify documentation only; the supplied requirement is sufficient for this change.',
           'APPROVE', ['Disclose partial discussion coverage without claiming all threads are resolved.'],
           ['Treat the export as a complete discussion listing or block this fully specified typo-level change solely for missing optional threads.'],
           ['Local change is documentation-only; exported discussion listing is explicitly partial.'], extra)

    # 20: Provider access failure alone does not block an explicit local review.
    r = start(20)
    base = r.commit('initial documentation')
    r.write('README.md', 'A documented utility.\n')
    head = r.commit('clarify documentation')
    extra = provider_input(20, base, head,
                           access={'status': 'denied', 'operation': 'read discussions',
                                   'reason': 'supplied export records a permission failure'},
                           threads={'items': [], 'complete': False})
    record(r, base, f'{base}...{head}', 'Clarify documentation only.', 'APPROVE',
           ['Complete the explicit local comparison and disclose unavailable provider discussions.'],
           ['Attempt login/permission changes, invent retrieved threads, or force INCOMPLETE solely for unavailable optional access.'],
           ['Explicit local refs and requirement are available despite a provider access error.'], extra)

    # 21: Fork metadata for an unavailable new head cannot validate an older checkout.
    r = start(21)
    base = r.commit('initial documentation')
    r.git('switch', '-qc', 'feature')
    r.write('README.md', 'A documented utility.\n')
    r.commit('local documentation snapshot')
    missing = 'f' * 40
    probe = subprocess.run(['git', 'cat-file', '-e', missing], cwd=r.path, capture_output=True)
    check(probe.returncode != 0, 'provider head must be unavailable locally')
    extra = provider_input(21, base, missing,
                           head={'repository': 'contributor/project', 'ref': 'feature', 'sha': missing},
                           checks={'items': [{'name': 'test', 'sha': missing,
                                              'status': 'completed', 'conclusion': 'success'}],
                                   'complete': True})
    record(r, base, 'the current PR identified in the supplied provider export',
           'Clarify documentation only.', 'INCOMPLETE',
           ['Identify missing fork head snapshot and request matching code; distinguish it from local feature and do not claim its CI validates local content.'],
           ['Substitute the same-named local branch or approve the unavailable provider head.'],
           ['Fork head SHA is unavailable locally; current checkout has a different commit.'], extra)
    cases[-1]['local_head'] = cases[-1]['head']
    cases[-1]['head'] = missing

    # 22: Detailed prose keeps evidence and uses requested organization.
    r = start(22)
    r.write('api.py', 'def load():\n    return {"id": 7}\n')
    r.write('consumer.py', 'from api import load\nassert load()["id"] == 7\n')
    base = r.commit('public record contract')
    check(r.execute('consumer.py').returncode == 0, 'detailed baseline')
    r.write('api.py', 'def load():\n    return 7\n')
    r.commit('change return type')
    check(r.execute('consumer.py').returncode != 0, 'detailed regression')
    record(r, base, f'{base}...HEAD', 'Preserve the existing consumer behavior.',
           'REQUEST CHANGES',
           ['Honor the detailed-report request with organized finding and verification detail; include location, confidence, observed behavior, impact, and fix for the api.py regression.'],
           ['Omit evidence for brevity, manufacture extra findings, or treat a detailed request as authorization to post a review.'],
           ['Return-shape change fails the unchanged consumer; detailed mode changes presentation only.'],
           'Use --detailed: give me a full report with supporting evidence and verification detail.')

    # 23: Compact policy reporting must retain rule exceptions without a full table.
    r = start(23)
    r.write('.pr-review', 'standards: team\n')
    base = r.commit('existing team adoption')
    r.git('switch', '-qc', 'clarify-documentation')
    r.write('README.md', 'A documented utility.\n')
    r.commit('clarify documentation')
    check(r.git('diff', '--name-only', base+'...HEAD') == 'README.md', 'compact policy scope')
    record(r, base, f'{base}...HEAD', 'Clarify documentation only.', 'APPROVE',
           ['Use a compact policy summary that identifies the pre-existing missing Dockerfile and unverified human approval; do not drop applicable policy limitations.'],
           ['Treat the existing Dockerfile gap as introduced, require empty report sections, or claim this automated review supplies human approval.'],
           ['Only documentation changes; team policy applies, but absent Dockerfile predates the change.'])

    # 24/25: Same destructuring shape, different installed Vue semantics.
    for number, version in [(24, '3.5.13'), (25, '3.4.38')]:
        r = start(number)
        r.write('package.json', json.dumps({'private': True, 'dependencies': {'vue': version}}, indent=2) + '\n')
        r.write('Profile.vue', '<script setup>\nimport { watchEffect } from "vue";\nconst props = defineProps(["userId"]);\nwatchEffect(() => console.log(props.userId));\n</script>\n')
        base = r.commit('observe changing user ID')
        r.write('Profile.vue', '<script setup>\nimport { watchEffect } from "vue";\nconst { userId } = defineProps(["userId"]);\nwatchEffect(() => console.log(userId));\n</script>\n')
        r.commit('destructure prop access')
        check(json.loads((r.path/'package.json').read_text())['dependencies']['vue'] == version, 'Vue version recorded')
        record(r, base, f'{base}...HEAD', 'Log the current user ID again whenever the parent changes it.',
               'APPROVE' if number == 24 else 'REQUEST CHANGES',
               ['Recognize the Vue 3.5 compiler transform and do not demand toRefs for direct script-setup destructuring.'] if number == 24 else
               ['Identify lost reactivity on the pinned Vue 3.4 default compiler behavior; use props access or a ref/getter.'],
               ['Use the legacy destructuring rule despite installed Vue 3.5.'] if number == 24 else
               ['Apply Vue 3.5 behavior to Vue 3.4 or miss the changed observer behavior.'],
               ['Version and changed source are checked locally; compiler behavior is source-verified, not executed in the builder.'],
               'Offline review: do not use web search, provider tools, network, package installs, or external documentation. Use bundled guidance and local files. Compiler defaults are unchanged; no experimental props-destructure transform is configured.')
        cases[-1]['verification'] = 'source-grounded fixture; Vue compiler is not executed'

    # 26: Valid Pydantic v2 mutable model default, distinct from Python functions.
    r = start(26)
    r.write('pyproject.toml', '[project]\nname = "model-fixture"\nversion = "0.1.0"\ndependencies = ["pydantic==2.10.6"]\n')
    r.write('model.py', 'from pydantic import BaseModel, Field\nclass Batch(BaseModel):\n    items: list[int] = Field(default_factory=list)\n')
    base = r.commit('independent batch defaults')
    r.write('model.py', 'from pydantic import BaseModel\nclass Batch(BaseModel):\n    items: list[int] = []\n')
    r.commit('simplify equivalent model default')
    record(r, base, f'{base}...HEAD', 'Each Batch instance starts with an independent empty list.', 'APPROVE',
           ['Distinguish Pydantic v2 model copying from ordinary Python mutable function defaults.'],
           ['Claim shared-state leakage solely from the list-valued Pydantic model default.'],
           ['Pydantic v2 unhashable default-copy semantics are source-verified; builder does not install or execute Pydantic.'],
           'Offline review: use only bundled guidance and local files; do not install dependencies or access external documentation.')
    cases[-1]['verification'] = 'source-grounded fixture; Pydantic not executed by builder'

    # 27: Genuine shared Python function default; executable with the stdlib.
    r = start(27)
    r.write('batch.py', 'def add(value, items=None):\n    items = [] if items is None else items\n    items.append(value)\n    return items\n')
    r.write('check.py', 'from batch import add\nassert add(1) == [1]\nassert add(2) == [2]\n')
    base = r.commit('fresh per-call default')
    check(r.execute('check.py').returncode == 0, 'function default baseline')
    r.write('batch.py', 'def add(value, items=[]):\n    items.append(value)\n    return items\n')
    r.commit('simplify function default')
    check(r.execute('check.py').returncode != 0, 'function default regression')
    record(r, base, f'{base}...HEAD', 'Omitting items gives each call a fresh independent collection.', 'REQUEST CHANGES',
           ['Report state shared by repeated add calls and recommend creating the collection per omitted argument.'],
           ['Transfer Pydantic default-copy semantics to an ordinary Python function.'],
           ['Baseline passes two independent calls; changed function returns accumulated values.'],
           'Offline review: use bundled guidance and local files only. You may run the supplied Python check.')

    # 28: Next 15 uncached public fetch is valid; no blanket no-store demand.
    r = start(28)
    r.write('package.json', json.dumps({'private': True, 'dependencies': {'next': '15.2.4', 'react': '19.0.0'}}, indent=2) + '\n')
    r.write('next.config.mjs', 'export default {};\n')
    r.write('app/page.tsx', 'export default async function Page() {\n  const r = await fetch("https://catalog.example.invalid/public", {cache: "no-store"});\n  if (!r.ok) throw new Error("catalog unavailable");\n  const items = await r.json();\n  return <pre>{JSON.stringify(items)}</pre>;\n}\n')
    base = r.commit('public catalog request')
    page = (r.path/'app/page.tsx').read_text().replace(', {cache: "no-store"}', '')
    r.write('app/page.tsx', page)
    r.commit('use Next 15 request defaults')
    check('15.2.4' in (r.path/'package.json').read_text() and 'no-store' not in page, 'Next 15 fixture')
    record(r, base, f'{base}...HEAD', 'Fetch the public catalog on each request; there is no personalized data.', 'APPROVE',
           ['Use pinned Next 15 cache defaults and local config; do not infer a privacy leak or stale data solely from missing no-store.'],
           ['Apply Next 14 eligible-fetch defaults indiscriminately or invent a cross-user leak.'],
           ['No cache wrapper, route cache override, Cache Components option, or personalization exists; Next runtime behavior is source-verified.'],
           'Offline review: use bundled guidance and local files only; the placeholder URL must not be contacted and dependencies must not be installed.')
    cases[-1]['verification'] = 'source-grounded fixture; Next runtime not executed'

    # 29: A concrete cache identity regression, executed without a web framework.
    r = start(29)
    r.write('cache.js', 'const cache = new Map();\nexports.profile = id => {\n  const key = `profile:${id}`;\n  if (!cache.has(key)) cache.set(key, {owner: id});\n  return cache.get(key);\n};\n')
    r.write('check.js', 'const assert = require("node:assert/strict");\nconst {profile} = require("./cache");\nassert.equal(profile("a").owner, "a");\nassert.equal(profile("b").owner, "b");\n')
    base = r.commit('identity-scoped cache')
    r.write('cache.js', (r.path/'cache.js').read_text().replace('`profile:${id}`', '"profile"'))
    r.commit('share profile cache entry')
    record(r, base, f'{base}...HEAD', 'Cache profiles without returning another user’s data.', 'REQUEST CHANGES',
           ['Trace the shared key returning user a data to user b and recommend including identity in the cache key.'],
           ['Dismiss a proven identity leak because some framework defaults are uncached.'],
           ['Plain Map implementation deterministically reuses the first user under the changed constant key; optional Node execution validates it.'],
           'Offline review: use local files and bundled guidance. If Node is installed, you may run node check.js; no network or package installation.')
    cases[-1]['verification'] = 'deterministic source fixture; optional Node execution by reviewer'

    # 30: Google restrictions must not leak into a general TypeScript review.
    r = start(30)
    r.write('package.json', '{"private":true,"devDependencies":{"typescript":"5.4.5"}}\n')
    r.write('AGENTS.md', 'Negative type tests intentionally use a documented @ts-expect-error. The repo does not adopt Google style.\n')
    r.write('id.ts', 'export function id(value: string): string { return value; }\n')
    base = r.commit('typed ID contract')
    r.write('id.type-test.ts', 'import { id } from "./id";\n// @ts-expect-error -- verify that non-string IDs are rejected.\nid(123);\n')
    r.commit('test invalid caller types')
    record(r, base, f'{base}...HEAD', 'Add a negative type test proving numeric callers are rejected.', 'APPROVE',
           ['Accept the intentional documented negative type test and keep Google style disabled.'],
           ['Flag the suppression as a production correctness defect or enforce an unadopted Google policy.'],
           ['Local project rule and negative test establish purpose; compiler dependency is recorded without installation.'],
           'Offline review: use bundled guidance and local files; do not install a compiler or access external docs.')
    cases[-1]['verification'] = 'source-grounded negative type test; compiler not executed by builder'

    # 31: Opted-in style can yield a nonblocking observation without a runtime bug.
    r = start(31)
    r.write('.pr-review', 'style: google\n')
    r.write('package.json', '{"private":true,"devDependencies":{"typescript":"5.4.5"}}\n')
    r.write('id.ts', 'export function id(value: string): string { return value; }\n')
    base = r.commit('Google-style ID utility')
    r.write('id.ts', 'export default function id(value: string): string { return value; }\n')
    r.write('consumer.ts', 'import id from "./id";\nexport const selected = id("a");\n')
    r.commit('switch to default export')
    record(r, base, f'{base}...HEAD', 'Keep the plain TypeScript utility behavior; this is not a framework-required default export.',
           'APPROVE WITH COMMENTS', ['Report the opted-in named-export convention as a grouped LOW style finding and verify the updated consumer.'],
           ['Call the valid default export a runtime bug, request changes solely for style, or activate team-policy requirements.'],
           ['Producer and consumer agree; plain TypeScript supports default exports while adopted Google policy prefers named exports.'],
           'Offline review: use bundled guidance and local files; do not install dependencies or contact external documentation.')
    cases[-1]['verification'] = 'source-grounded style/contract fixture; compiler not executed by builder'

    # 32: A documented small-handler architecture overrides generic layering tastes.
    r = start(32)
    r.write('AGENTS.md', 'This small utility intentionally keeps its SQLite read in the handler. No service/repository layer is required. Review behavior, not a preferred architecture.\n')
    r.write('handler.py', 'def total(connection):\n    return connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]\n')
    r.write('check.py', 'import sqlite3\nfrom handler import total\nc = sqlite3.connect(":memory:")\nc.execute("CREATE TABLE items (id INTEGER)")\nc.executemany("INSERT INTO items VALUES (?)", [(1,), (2,)])\nassert total(c) == 2\n')
    base = r.commit('small handler contract')
    r.write('handler.py', 'def total(connection):\n    """Return the number of stored items."""\n    return connection.execute("SELECT COUNT(*) FROM items").fetchone()[0]\n')
    r.commit('document handler contract')
    check(r.execute('check.py').returncode == 0, 'documented inline handler remains correct')
    record(r, base, f'{base}...HEAD', 'Document the existing item-count handler without changing behavior.', 'APPROVE',
           ['Respect the documented small-handler architecture and verify unchanged behavior.'],
           ['Demand a service/repository layer or turn direct session/query access into an automatic finding.'],
           ['SQLite check passes and project rule explicitly permits direct handler data access.'],
           'Offline review: use bundled guidance and local files only; Python check may be run.')

    # Output criteria are semantic, with no brittle word-count or heading checks.
    for item in expected:
        if item['id'] == 'case-01':
            item['required'].append('Use a compact clean report retaining target, verdict, verification limits, and review basis without padded summaries or empty issue sections.')
        elif item['id'] == 'case-02':
            item['required'].append('Keep all five finding evidence fields in the compact report; do not duplicate the same root cause across sections.')
        elif item['id'] == 'case-10':
            item['required'].append('In compact format, identify the material evidence gap and the next action needed; brevity must not imply approval.')

    (output / 'cases.json').write_text(json.dumps(cases, indent=2) + '\n')
    (output / 'expected.json').write_text(json.dumps(expected, indent=2) + '\n')
    print(f'PASS: built {len(cases)} fixture scenarios and checked their available local conditions in {output}')
    print('Source-grounded framework cases are labeled; unavailable framework runtimes are not claimed as executed.')
    print('Reviewer inputs: cases.json; evaluator-only rubric: expected.json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New directory; must not already exist. Defaults to a temporary directory.')
    args = parser.parse_args()
    output = args.output.expanduser().resolve() if args.output else Path(tempfile.mkdtemp(prefix='pr-review-eval-')) / 'suite'
    # Prevent accidental fixture construction in the skill tree.
    skill = Path(__file__).resolve().parents[1]
    if output == skill or skill in output.parents:
        parser.error('Choose an output directory outside the skill folder.')
    build(output)


if __name__ == '__main__':
    main()
