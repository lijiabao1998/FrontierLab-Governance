"""GATE_CONTRACT.md guards. Every guard has a GREEN fixture, a deliberate RED violation and a boundary case."""
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('frontier', Path(__file__).resolve().parents[1] / 'tools/frontier.py')
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)

PIN = '1' * 40
OTHER = '2' * 40


def now():
    return dt.datetime.now(dt.timezone.utc)


def card(pid, domain='medicine'):
    return {'id': pid, 'domain': domain, 'title': 'Fixture title', 'status': 'OPEN', 'priority': 'A',
            'checked_on': now().date().isoformat(), 'statement': 'Fixture statement about external validation.',
            'known_result': 'Fixture known result.', 'open_gap': 'Fixture open gap.', 'first_task': 'Fixture first task.',
            'evaluator': 'Fixture evaluator.', 'validation_limits': 'Fixture limits.',
            'completion_criterion': 'Fixture completion criterion.', 'screening_note': 'Fixture note.',
            'screening_queries': ['fixture query'],
            'sources': [{'title': 'Fixture', 'url': 'https://arxiv.org/abs/2602.07751', 'kind': 'primary', 'supports': 'syntax'}]}


def round_record(rid, pid, agent='claude', verdict='NO_RESOLUTION_FOUND', state='ADMITTED', checked_at=None):
    t = checked_at or now()
    return {
        'round_id': rid, 'problem_id': pid, 'agent': agent, 'branch': f'{agent}/{pid.lower()}-fixture',
        'base_sha': 'a' * 40, 'started_at': t.isoformat(), 'state': state,
        'acceptance': 'Synthetic fixture.', 'not_done': 'No science performed.',
        'budget': {'wall_minutes': 10, 'usd': 0, 'max_trials': 10},
        'preflight': {
            'checked_at': t.isoformat(), 'verdict': verdict,
            'queries': [{'query': c + ' fixture', 'engine': 'unit-test-only', 'category': c, 'outcome': 'synthetic'}
                        for c in sorted(f.CATEGORIES)],
            'sources': [
                {'url': 'https://arxiv.org/abs/2602.07751', 'title': 'Fixture', 'kind': 'primary', 'supports': 'syntax'},
                {'url': 'https://lean-lang.org/doc/reference/latest/ValidatingProofs/', 'title': 'Fixture', 'kind': 'official', 'supports': 'syntax'}],
            'limitations': 'Synthetic', 'scope_comparison': 'Synthetic', 'baseline': 'Synthetic',
            **{k: True for k in ('sources_read', 'scope_compared', 'retractions_checked', 'licenses_checked',
                                'safety_checked', 'baseline_identified', 'acceptance_frozen')}}}


def resolution(pid):
    return {'problem_id': pid, 'scope_statement': 'exact scope', 'basis': 'fixture', 'confirmed_by': 'fixture reviewer',
            'independent_check': 'fixture certificate', 'scope_match': True, 'independently_verified': True,
            'confirmed_at': now().isoformat(),
            'sources': [{'url': 'https://arxiv.org/abs/2602.07751', 'title': 'Fixture', 'kind': 'primary', 'supports': 'syntax'},
                        {'url': 'https://lean-lang.org/doc/reference/latest/Axioms/', 'title': 'Fixture', 'kind': 'official', 'supports': 'syntax'}]}


WORKFLOW = """name: Research records
on: [push, pull_request]
jobs:
  lean:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
  records:
    uses: lijiabao1998/FrontierLab-Governance/.github/workflows/research.yml@{uses}
    with:
      governance_ref: {ref}
"""


class Lab:
    """A throwaway research repository with one base commit."""

    def __init__(self, domain='medicine', pids=('MED-001', 'MED-002')):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)
        self.domain = domain
        self.write('lab.json', {'domain': domain, 'expected_problem_count': len(pids)})
        self.write('GOVERNANCE.lock.json', {'repository': f.GOVERNANCE_REPO, 'commit': PIN, 'protocol_version': f.PROTOCOL_VERSION})
        self.write('.github/workflows/research.yml', WORKFLOW.format(uses=PIN, ref=PIN))
        self.write('README.md', f'# Lab\n每輪按治理 {PIN} fresh search。資料集 commit {OTHER} 不是治理 pin。\n')
        self.write('AGENTS.md', f'讀治理 https://github.com/lijiabao1998/FrontierLab-Governance/tree/{PIN} 。\n')
        self.write('STATUS.md', 'status\n')
        self.write('runs/README.md', 'rounds\n')
        for pid in pids:
            self.write(f'problems/{pid}/problem.json', card(pid, domain))
        self.git('init', '-q', '-b', 'main')
        # Newer git (CI runners) runs auto-maintenance detached after commit; it can write into .git/objects while
        # TemporaryDirectory.cleanup() is deleting it ("Directory not empty: 'objects'"). Fixtures never need it.
        self.git('config', 'gc.auto', '0')
        self.git('config', 'maintenance.auto', 'false')
        self.base = self.commit('base')

    def close(self):
        self.dir.cleanup()

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
                               '-c', 'commit.gpgsign=false', *args], check=True, capture_output=True, text=True).stdout.strip()

    def write(self, rel, content):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else json.dumps(content, ensure_ascii=False, indent=2) + '\n',
                        encoding='utf-8')

    def read(self, rel):
        return json.loads((self.root / rel).read_text(encoding='utf-8'))

    def delete(self, rel):
        (self.root / rel).unlink()

    def commit(self, message='change'):
        self.git('add', '-A')
        self.git('commit', '-q', '--allow-empty', '-m', message)
        return self.git('rev-parse', 'HEAD')

    def edit_card(self, pid, **changes):
        p = self.read(f'problems/{pid}/problem.json')
        p.update(changes)
        self.write(f'problems/{pid}/problem.json', p)
        return p

    def add_round(self, pid, rid=None, **kw):
        rid = rid or f'20260928T000000000000Z-claude-{pid}-{len(list(self.root.glob("runs/*/")))}'
        r = round_record(rid, pid, **kw)
        self.write(f'runs/{rid}/round.json', r)
        return rid, r

    def add_decision(self, pid, kind, fields, did=None, **extra):
        did = did or f'20260928T000000000000Z-claude-{pid}-{kind}-{len(list(self.root.glob("decisions/*/")))}'
        d = {'decision_id': did, 'problem_id': pid, 'kind': kind, 'fields': fields, 'author': 'claude',
             'created_at': now().isoformat(), 'base_sha': self.base, 'rationale': 'fixture rationale', **extra}
        self.write(f'decisions/{did}/decision.json', d)
        return did

    def check(self):
        head = self.commit()
        return f.check_diff(self.root, self.base, head)


class LabCase(unittest.TestCase):
    domain = 'medicine'

    def setUp(self):
        self.lab = Lab(self.domain) if self.domain == 'medicine' else Lab(self.domain, ('MATH-001',))
        self.addCleanup(self.lab.close)

    def green(self):
        self.lab.check()

    def red(self, pattern):
        with self.assertRaisesRegex(ValueError, pattern):
            self.lab.check()


# ---------------------------------------------------------------- B1 pin contract
class PinContractTests(LabCase):
    def pins(self):
        return f.check_pins(self.lab.root)

    def test_green_all_four_agree(self):
        self.assertEqual(self.pins(), PIN)

    def test_red_workflow_uses_differs_from_lock(self):
        self.lab.write('.github/workflows/research.yml', WORKFLOW.format(uses=OTHER, ref=PIN))
        with self.assertRaisesRegex(ValueError, r'research\.yml: uses @2{40}'):
            self.pins()

    def test_red_workflow_governance_ref_differs_from_lock(self):
        self.lab.write('.github/workflows/research.yml', WORKFLOW.format(uses=PIN, ref=OTHER))
        with self.assertRaisesRegex(ValueError, r'governance_ref 2{40}'):
            self.pins()

    def test_red_readme_differs_from_lock(self):
        self.lab.write('README.md', f'每輪按治理 {OTHER} fresh search。\n')
        with self.assertRaisesRegex(ValueError, r'README\.md: governance prose pin 2{40}'):
            self.pins()

    def test_red_agents_differs_from_lock(self):
        self.lab.write('AGENTS.md', f'讀治理 https://github.com/lijiabao1998/FrontierLab-Governance/tree/{OTHER} 。\n')
        with self.assertRaisesRegex(ValueError, r'AGENTS\.md: governance url pin 2{40}'):
            self.pins()

    def test_red_readme_without_declaration(self):
        self.lab.write('README.md', '# Lab without a governance pin\n')
        with self.assertRaisesRegex(ValueError, r'README\.md: no governance pin declaration'):
            self.pins()

    def test_red_floating_workflow_ref(self):
        self.lab.write('.github/workflows/research.yml', WORKFLOW.format(uses='main', ref=PIN))
        with self.assertRaisesRegex(ValueError, r'uses @main'):
            self.pins()

    def test_red_workflow_from_another_owner(self):
        text = WORKFLOW.format(uses=PIN, ref=PIN).replace('lijiabao1998/FrontierLab-Governance', 'someone/FrontierLab-Governance')
        self.lab.write('.github/workflows/research.yml', text)
        with self.assertRaisesRegex(ValueError, r'uses someone/FrontierLab-Governance'):
            self.pins()

    def test_red_lock_short_sha(self):
        self.lab.write('GOVERNANCE.lock.json', {'repository': f.GOVERNANCE_REPO, 'commit': PIN[:8]})
        with self.assertRaisesRegex(ValueError, r'full 40-hex'):
            self.pins()

    def test_red_url_with_branch_ref(self):
        self.lab.write('AGENTS.md', 'https://github.com/lijiabao1998/FrontierLab-Governance/tree/main\n')
        with self.assertRaisesRegex(ValueError, r'url pin main'):
            self.pins()

    def test_boundary_unrelated_shas_are_ignored(self):
        # README fixture already mentions a dataset commit; the workflow has actions/checkout@<sha>.
        self.lab.write('README.md', f'治理 {PIN[:8]}。資料 commit {OTHER}；見 https://github.com/x/y/tree/{OTHER}\n')
        self.assertEqual(self.pins(), PIN)

    def test_boundary_prose_short_prefix_must_match(self):
        self.lab.write('README.md', f'治理 commit：`{OTHER[:8]}`\n')
        with self.assertRaisesRegex(ValueError, r'prose pin 22222222'):
            self.pins()

    def test_boundary_marker_form(self):
        self.lab.write('README.md', f'<!-- governance-pin: {PIN} -->\n')
        self.assertEqual(self.pins(), PIN)
        self.lab.write('README.md', f'<!-- governance-pin: {OTHER} -->\n')
        with self.assertRaisesRegex(ValueError, r'marker pin'):
            self.pins()

    def test_red_quoted_operative_keys_with_commented_decoys(self):
        # Review finding: quoted keys were ignored while matching declarations inside comments were accepted.
        self.lab.write('.github/workflows/research.yml', f"""jobs:
  records:
    "uses": lijiabao1998/FrontierLab-Governance/.github/workflows/research.yml@main
    with:
      "governance_ref": main
# uses: lijiabao1998/FrontierLab-Governance/.github/workflows/research.yml@{PIN}
# governance_ref: {PIN}
""")
        with self.assertRaisesRegex(ValueError, r'uses @main(?s:.*)governance_ref main'):
            self.pins()

    def test_red_declarations_only_in_comments(self):
        self.lab.write('.github/workflows/research.yml', f"""jobs: {{}}
# uses: lijiabao1998/FrontierLab-Governance/.github/workflows/research.yml@{PIN}
#   governance_ref: {PIN}
""")
        with self.assertRaisesRegex(ValueError, r'no uses:(?s:.*)no governance_ref'):
            self.pins()

    def test_green_quoted_keys_values_and_trailing_comments(self):
        self.lab.write('.github/workflows/research.yml', f"""jobs:
  records:
    "uses": "lijiabao1998/FrontierLab-Governance/.github/workflows/research.yml@{PIN}"  # pinned
    with:
      'governance_ref': '{PIN}' # same commit
""")
        self.assertEqual(self.pins(), PIN)

    def test_red_unrecognized_governance_reference(self):
        # A reference the parser does not understand (here a flow mapping) fails closed instead of being skipped.
        self.lab.write('.github/workflows/research.yml', WORKFLOW.format(uses=PIN, ref=PIN) +
                       "  extra: {uses: lijiabao1998/FrontierLab-Governance/.github/workflows/research.yml@main}\n")
        with self.assertRaisesRegex(ValueError, r'unrecognized governance reference'):
            self.pins()

    def test_validate_runs_pin_contract(self):
        self.lab.write('README.md', f'每輪按治理 {OTHER} fresh search。\n')
        with self.assertRaisesRegex(ValueError, r'governance pin mismatch'):
            f.validate_repo(self.lab.root)

    def test_red_stale_pin_next_to_a_correct_one(self):
        # Review finding: keyword case, uppercase hex and raw/owner-case URLs were not read, so one correct pin hid a stale one.
        stale = 'ab' * 20
        for text in (f'Governance Commit: {stale[:8]}', f'治理 PIN `{stale.upper()}`',
                     f'https://raw.githubusercontent.com/lijiabao1998/FrontierLab-Governance/{stale}/AGENTS.md',
                     f'https://github.com/LiJiaBao1998/frontierlab-governance/blob/{stale}/README.md'):
            with self.subTest(text=text):
                self.lab.write('README.md', f'每輪按治理 {PIN} fresh search。\n{text}\n')
                with self.assertRaisesRegex(ValueError, r'README\.md: governance (prose|url) pin ab'):
                    self.pins()

    def test_boundary_uppercase_pin_matches_lock(self):
        lock = 'ab' * 20
        self.lab.write('GOVERNANCE.lock.json', {'repository': f.GOVERNANCE_REPO, 'commit': lock, 'protocol_version': f.PROTOCOL_VERSION})
        self.lab.write('.github/workflows/research.yml', WORKFLOW.format(uses=lock, ref=lock))
        self.lab.write('README.md', f'Governance commit {lock.upper()[:10]}\n')
        self.lab.write('AGENTS.md', f'https://raw.githubusercontent.com/lijiabao1998/FrontierLab-Governance/{lock.upper()}/AGENTS.md\n')
        self.assertEqual(self.pins(), lock)

    def test_red_pins_inside_block_scalar_are_not_operative(self):
        # Review finding: `uses:` / `governance_ref:` text inside a `run: |` block counted as the job's declaration.
        self.lab.write('.github/workflows/research.yml', f"""jobs:
  records:
    runs-on: ubuntu-latest
    steps:
      - run: |
          uses: lijiabao1998/FrontierLab-Governance/.github/workflows/research.yml@{PIN}
          governance_ref: {PIN}
          git clone https://github.com/lijiabao1998/FrontierLab-Governance && python3 FrontierLab-Governance/tools/frontier.py validate .
""")
        with self.assertRaisesRegex(ValueError, r'(?s)research\.yml:6: unrecognized.*research\.yml:7: unrecognized.*no uses:.*no governance_ref'):
            self.pins()

    def test_boundary_block_scalar_ends_at_dedent(self):
        self.lab.write('.github/workflows/research.yml', WORKFLOW.format(uses=PIN, ref=PIN).replace(
            '  records:\n', '      - run: >-\n          echo "no governance here"\n  records:\n'))
        self.assertEqual(self.pins(), PIN)


# ---------------------------------------------------------------- B2 protected specification
class ProtectedSpecTests(LabCase):
    def test_green_editorial_typo_with_decision(self):
        self.lab.edit_card('MED-001', statement='Fixture statement about external validations.')
        self.lab.add_decision('MED-001', 'editorial', ['statement'])
        self.green()

    def test_red_statement_change_without_record(self):
        self.lab.edit_card('MED-001', statement='A weaker statement.')
        self.red(r"MED-001: \['statement'\] changed without a matching round or decision")

    def test_red_round_does_not_authorize_spec(self):
        self.lab.edit_card('MED-001', completion_criterion='Any benchmark gain.')
        self.lab.add_round('MED-001')
        self.red(r"\['completion_criterion'\] changed without")

    def test_red_other_problem_decision_cannot_cover(self):
        self.lab.edit_card('MED-001', statement='Fixture statement about external validations.')
        self.lab.add_decision('MED-002', 'editorial', ['statement'])
        self.red(r"MED-001: \['statement'\] changed without.*\n.*MED-002: decision record\(s\) without a matching problem card change")

    def test_red_decision_lists_unchanged_field(self):
        self.lab.edit_card('MED-001', statement='Fixture statement about external validations.')
        self.lab.add_decision('MED-001', 'editorial', ['statement', 'evaluator'])
        self.red(r"lists unchanged fields \['evaluator'\]")

    def test_boundary_editorial_size_limit(self):
        old = card('MED-001')['statement']
        self.lab.edit_card('MED-001', statement=old + 'x' * f.EDITORIAL_MAX_CHARS)
        self.lab.add_decision('MED-001', 'editorial', ['statement'])
        self.green()

    def test_red_editorial_over_limit(self):
        old = card('MED-001')['statement']
        self.lab.edit_card('MED-001', statement=old + 'x' * (f.EDITORIAL_MAX_CHARS + 1))
        self.lab.add_decision('MED-001', 'editorial', ['statement'])
        self.red(r'editorial change to statement is 13 chars')

    def test_green_spec_change_with_impact(self):
        self.lab.edit_card('MED-001', statement='Rescoped: only site-held-out calibration for one intended use.')
        self.lab.add_decision('MED-001', 'spec-change', ['statement'], impact='narrows')
        self.green()

    def test_red_spec_change_without_impact(self):
        self.lab.edit_card('MED-001', statement='Rescoped statement.')
        self.lab.add_decision('MED-001', 'spec-change', ['statement'])
        self.red(r'spec-change must declare impact')

    def test_red_spec_change_with_results_same_pr(self):
        self.lab.edit_card('MED-001', statement='Rescoped statement.')
        self.lab.add_decision('MED-001', 'spec-change', ['statement'], impact='narrows')
        self.lab.add_round('MED-001')
        self.lab.write('problems/MED-001/results/r1/metrics.json', '{}')
        self.red(r"specification fields \['statement'\] changed together with MED-001 research artifacts")

    def test_red_spec_and_status_same_pr(self):
        self.lab.edit_card('MED-001', statement='Rescoped statement.', status='PAUSED')
        self.lab.add_decision('MED-001', 'spec-change', ['statement'], impact='narrows')
        self.lab.add_decision('MED-001', 'status-change', ['status'], **{'from': 'OPEN', 'to': 'PAUSED'})
        self.red(r'specification fields .* and status changed in one change')

    def test_green_literature_update_by_round(self):
        # Same shape as a real literature round: known_result, first_task and provenance updated.
        self.lab.edit_card('MED-001', known_result='Updated known result.', first_task='Next minimal step.',
                           sources=card('MED-001')['sources'] + [{'title': 'New', 'url': 'https://doi.org/10.1/x',
                                                                     'kind': 'primary', 'supports': 'update'}])
        self.lab.add_round('MED-001', verdict='PARTIAL_PROGRESS')
        self.green()

    def test_red_literature_update_with_other_problem_round(self):
        self.lab.edit_card('MED-001', known_result='Updated known result.')
        self.lab.add_round('MED-002')
        self.red(r"MED-001: \['known_result'\] changed without")

    def test_red_blank_draft_round_is_not_a_basis(self):
        self.lab.edit_card('MED-001', known_result='Updated known result.')
        self.lab.write('runs/blank/round.json', {'round_id': 'blank', 'problem_id': 'MED-001', 'state': 'DRAFT'})
        self.red(r"MED-001: \['known_result'\] changed without")

    def test_red_blank_non_draft_round_is_rejected(self):
        self.lab.edit_card('MED-001', known_result='Updated known result.')
        self.lab.write('runs/blank/round.json', {'round_id': 'blank', 'problem_id': 'MED-001', 'state': 'ADMITTED'})
        self.red(r'runs/blank/round\.json: round: missing')

    def test_red_blocked_round_is_not_a_basis(self):
        self.lab.edit_card('MED-001', known_result='Updated known result.')
        self.lab.add_round('MED-001', verdict='BLOCKED', state='PAUSED')
        self.red(r"\['known_result'\] changed without")

    def test_red_round_id_must_match_directory(self):
        self.lab.edit_card('MED-001', known_result='Updated known result.')
        self.lab.write('runs/copied/round.json', round_record('original', 'MED-001'))
        self.red(r'round_id must match its directory name')

    def test_green_checked_on_moves_with_round_date(self):
        self.lab.edit_card('MED-001', checked_on=(now().date() + dt.timedelta(days=1)).isoformat())
        self.lab.add_round('MED-001')
        self.green()

    def test_red_checked_on_via_hygiene(self):
        self.lab.edit_card('MED-001', checked_on=(now().date() - dt.timedelta(days=5)).isoformat())
        self.lab.add_decision('MED-001', 'hygiene', ['checked_on'])
        self.red(r"cannot authorize \['checked_on'\]")

    def test_boundary_checked_on_two_days_from_round(self):
        self.lab.edit_card('MED-001', checked_on=(now().date() - dt.timedelta(days=2)).isoformat())
        self.lab.add_round('MED-001')
        self.red(r'checked_on moves only with a MED-001 round')

    def test_green_source_refresh_via_hygiene(self):
        self.lab.edit_card('MED-001', sources=[{'title': 'Fixture', 'url': 'https://doi.org/10.1/fixture', 'kind': 'primary', 'supports': 'syntax'}])
        self.lab.add_decision('MED-001', 'hygiene', ['sources'])
        self.green()

    def test_red_hygiene_cannot_touch_statement(self):
        self.lab.edit_card('MED-001', statement='Fixture statement about external validations.')
        self.lab.add_decision('MED-001', 'hygiene', ['statement'])
        self.red(r"decision kind hygiene cannot authorize \['statement'\]")

    def test_red_immutable_id(self):
        self.lab.edit_card('MED-001', domain='physics')
        self.lab.add_decision('MED-001', 'spec-change', ['domain'], impact='rescopes')
        self.red(r"cannot authorize \['domain'\]")
        self.lab.delete(next(str(p.relative_to(self.lab.root)) for p in self.lab.root.glob('decisions/*/decision.json')))
        self.red(r'MED-001: domain is immutable')

    def test_red_problem_card_deleted(self):
        self.lab.delete('problems/MED-002/problem.json')
        self.red(r'MED-002: problem cards are not deleted')

    def test_red_new_problem_without_decision_and_green_with(self):
        self.lab.write('problems/MED-003/problem.json', card('MED-003'))
        self.red(r'MED-003: a new problem card needs a new-problem decision')
        self.lab.add_decision('MED-003', 'new-problem', [])
        self.green()

    def test_red_existing_decision_is_immutable(self):
        did = self.lab.add_decision('MED-001', 'editorial', ['statement'])
        self.lab.edit_card('MED-001', statement='Fixture statement about external validations.')
        self.lab.base = self.lab.commit('merged decision')
        d = self.lab.read(f'decisions/{did}/decision.json')
        d['fields'] = ['statement', 'evaluator']
        self.lab.write(f'decisions/{did}/decision.json', d)
        self.red(r'decision records are immutable once merged')


class StatusTransitionTests(LabCase):
    def test_red_completed_external_without_round(self):
        self.lab.edit_card('MED-001', status='COMPLETED_EXTERNAL', resolution=resolution('MED-001'))
        self.red(r'COMPLETED_EXTERNAL needs a MED-001 round')

    def test_green_completed_external_as_written_by_admit(self):
        res = resolution('MED-001')
        rid, r = self.lab.add_round('MED-001', verdict='RESOLVED_EXTERNAL', state='CLOSED_EXTERNAL')
        r['preflight']['resolution'] = res
        self.lab.write(f'runs/{rid}/round.json', r)
        self.lab.edit_card('MED-001', status='COMPLETED_EXTERNAL', resolution=res)
        self.green()

    def test_red_completed_external_resolution_mismatch(self):
        res = resolution('MED-001')
        rid, r = self.lab.add_round('MED-001', verdict='RESOLVED_EXTERNAL', state='CLOSED_EXTERNAL')
        r['preflight']['resolution'] = res
        self.lab.write(f'runs/{rid}/round.json', r)
        other = copy.deepcopy(res); other['scope_statement'] = 'a different, broader scope'
        self.lab.edit_card('MED-001', status='COMPLETED_EXTERNAL', resolution=other)
        self.red(r'same resolution as the card')

    def test_red_completed_external_by_decision(self):
        self.lab.edit_card('MED-001', status='COMPLETED_EXTERNAL', resolution=resolution('MED-001'))
        self.lab.add_decision('MED-001', 'status-change', ['status', 'resolution'], **{'from': 'OPEN', 'to': 'COMPLETED_EXTERNAL'})
        self.red(r'decisions can target')

    def test_red_completed_external_with_other_problem_round(self):
        res = resolution('MED-002')
        rid, r = self.lab.add_round('MED-002', verdict='RESOLVED_EXTERNAL', state='CLOSED_EXTERNAL')
        r['preflight']['resolution'] = res
        self.lab.write(f'runs/{rid}/round.json', r)
        self.lab.edit_card('MED-001', status='COMPLETED_EXTERNAL', resolution=resolution('MED-001'))
        self.red(r'COMPLETED_EXTERNAL needs a MED-001 round')

    def test_green_pause_with_status_change(self):
        self.lab.edit_card('MED-001', status='PAUSED')
        self.lab.add_decision('MED-001', 'status-change', ['status'], **{'from': 'OPEN', 'to': 'PAUSED'})
        self.green()

    def test_red_status_change_wrong_from(self):
        self.lab.edit_card('MED-001', status='PAUSED')
        self.lab.add_decision('MED-001', 'status-change', ['status'], **{'from': 'PARTIAL', 'to': 'PAUSED'})
        self.red(r'status OPEN -> PAUSED needs a status-change decision with from=OPEN')

    def test_red_status_without_any_record(self):
        self.lab.edit_card('MED-001', status='PARTIAL')
        self.red(r'status OPEN -> PARTIAL needs')

    def test_green_partial_by_partial_progress_round(self):
        self.lab.edit_card('MED-001', status='PARTIAL')
        self.lab.add_round('MED-001', verdict='PARTIAL_PROGRESS')
        self.green()

    def test_red_claimed_resolved_needs_matching_verdict(self):
        self.lab.edit_card('MED-001', status='CLAIMED_RESOLVED')
        self.lab.add_round('MED-001', verdict='NO_RESOLUTION_FOUND')
        self.red(r'CLAIMED_RESOLVED needs a MED-001 round with that verdict')

    def internal(self, verifier):
        rid, _ = self.lab.add_round('MED-001', agent='gpt', state='FINISHED')
        self.lab.base = self.lab.commit('finished round merged earlier')
        self.lab.edit_card('MED-001', status='COMPLETED_INTERNAL', resolution=resolution('MED-001'))
        self.lab.add_decision('MED-001', 'status-change', ['status', 'resolution'],
                              **{'from': 'OPEN', 'to': 'COMPLETED_INTERNAL', 'rounds': [rid], 'verifier': verifier})

    def test_green_resolution_only_correction_by_decision(self):
        # Review finding: a status-change decision had to list status, so a resolution-only fix was impossible.
        rid, _ = self.lab.add_round('MED-001', agent='gpt', state='FINISHED')
        self.lab.edit_card('MED-001', status='COMPLETED_INTERNAL', resolution=resolution('MED-001'))
        self.lab.base = self.lab.commit('completed internally earlier')
        fixed = resolution('MED-001'); fixed['basis'] = 'corrected basis wording'
        self.lab.edit_card('MED-001', resolution=fixed)
        self.lab.add_decision('MED-001', 'status-change', ['resolution'],
                              **{'from': 'COMPLETED_INTERNAL', 'to': 'COMPLETED_INTERNAL', 'rounds': [rid], 'verifier': 'claude-verifier'})
        self.green()

    def test_red_status_move_must_list_status(self):
        self.lab.edit_card('MED-001', status='PAUSED', resolution=resolution('MED-001'))
        self.lab.add_decision('MED-001', 'status-change', ['resolution'], **{'from': 'OPEN', 'to': 'PAUSED'})
        self.red(r'status OPEN -> PAUSED: the status-change decision must list status')

    def test_green_completed_internal_with_independent_verifier(self):
        self.internal('claude-verifier')
        self.green()

    def test_red_completed_internal_self_verified(self):
        self.internal('gpt')
        self.red(r'verifier gpt is also an author')

    def test_red_completed_internal_cites_missing_round(self):
        self.lab.edit_card('MED-001', status='COMPLETED_INTERNAL', resolution=resolution('MED-001'))
        self.lab.add_decision('MED-001', 'status-change', ['status', 'resolution'],
                              **{'from': 'OPEN', 'to': 'COMPLETED_INTERNAL', 'rounds': ['nope'], 'verifier': 'x'})
        self.red(r'cites runs/nope, which is not a FINISHED MED-001 round')

    # Review findings (2026-09-29) on COMPLETED_INTERNAL, terminal states and contradictory decisions.
    def test_red_completed_internal_cites_blocked_round(self):
        rid, _ = self.lab.add_round('MED-001', agent='gpt', verdict='BLOCKED', state='FINISHED')
        self.lab.base = self.lab.commit('blocked round merged earlier')
        self.lab.edit_card('MED-001', status='COMPLETED_INTERNAL', resolution=resolution('MED-001'))
        self.lab.add_decision('MED-001', 'status-change', ['status', 'resolution'],
                              **{'from': 'OPEN', 'to': 'COMPLETED_INTERNAL', 'rounds': [rid], 'verifier': 'claude-verifier'})
        self.red(rf'cites runs/{rid}, whose verdict BLOCKED is not a research verdict')

    def test_red_completed_internal_cites_round_added_in_same_change(self):
        rid, _ = self.lab.add_round('MED-001', agent='gpt', state='FINISHED')
        self.lab.edit_card('MED-001', status='COMPLETED_INTERNAL', resolution=resolution('MED-001'))
        self.lab.add_decision('MED-001', 'status-change', ['status', 'resolution'],
                              **{'from': 'OPEN', 'to': 'COMPLETED_INTERNAL', 'rounds': [rid], 'verifier': 'claude-verifier'})
        self.red(rf'cites runs/{rid}, which is not merged yet')

    def test_red_completed_internal_verified_by_decision_author(self):
        self.internal('claude')
        self.red(r'verifier claude is the author of the decision')

    def test_red_contradictory_decision_next_to_round_transition(self):
        self.lab.edit_card('MED-001', status='PARTIAL')
        self.lab.add_round('MED-001', verdict='PARTIAL_PROGRESS')
        self.lab.add_decision('MED-001', 'status-change', ['status'], **{'from': 'PAUSED', 'to': 'OPEN'})
        self.red(r'status-change decision says PAUSED -> OPEN, but the card moves OPEN -> PARTIAL')

    def test_green_claimed_resolved_by_round(self):
        self.lab.edit_card('MED-001', status='CLAIMED_RESOLVED')
        self.lab.add_round('MED-001', verdict='CLAIMED_RESOLVED', state='PAUSED')
        self.green()

    def test_red_claimed_resolved_round_rewrites_resolution(self):
        self.lab.edit_card('MED-001', status='CLAIMED_RESOLVED', resolution=resolution('MED-001'))
        self.lab.base = self.lab.commit('claimed earlier')
        forged = resolution('MED-001'); forged['scope_statement'] = 'a much broader scope'
        self.lab.edit_card('MED-001', resolution=forged)
        self.lab.add_round('MED-001', verdict='CLAIMED_RESOLVED', state='PAUSED')
        self.red(r'MED-001: a round verdict does not change resolution')

    def completed_external_base(self):
        res = resolution('MED-001')
        rid, r = self.lab.add_round('MED-001', verdict='RESOLVED_EXTERNAL', state='CLOSED_EXTERNAL')
        r['preflight']['resolution'] = res
        self.lab.write(f'runs/{rid}/round.json', r)
        self.lab.edit_card('MED-001', status='COMPLETED_EXTERNAL', resolution=res)
        self.lab.base = self.lab.commit('completed externally earlier')

    def test_red_round_verdict_cannot_leave_terminal_status(self):
        self.completed_external_base()
        self.lab.edit_card('MED-001', status='CLAIMED_RESOLVED')
        self.lab.add_round('MED-001', verdict='CLAIMED_RESOLVED', state='PAUSED')
        self.red(r'(?s)MED-001 is COMPLETED_EXTERNAL.*status COMPLETED_EXTERNAL -> CLAIMED_RESOLVED needs a status-change decision')

    def test_red_new_research_on_completed_problem(self):
        self.completed_external_base()
        self.lab.add_round('MED-001')
        self.lab.write('problems/MED-001/results/r2/metrics.json', '{}')
        self.red(r'(?s)runs/.*MED-001 is COMPLETED_EXTERNAL.*problems/MED-001/results/r2/metrics\.json: MED-001 is COMPLETED_EXTERNAL')

    def test_green_retract_completed_problem_by_decision(self):
        self.completed_external_base()
        self.lab.edit_card('MED-001', status='RETRACTED')
        self.lab.add_decision('MED-001', 'status-change', ['status'], **{'from': 'COMPLETED_EXTERNAL', 'to': 'RETRACTED'})
        self.green()


# ---------------------------------------------------------------- B3 research path ownership
class PathContractTests(LabCase):
    def test_green_docs_and_ci_hygiene_need_no_round(self):
        self.lab.write('README.md', (self.lab.root / 'README.md').read_text() + '\n修字。\n')
        self.lab.write('STATUS.md', 'status updated\n')
        self.lab.write('.github/pull_request_template.md', '## template\n')
        self.green()

    def test_green_results_with_round(self):
        self.lab.add_round('MED-001')
        self.lab.write('problems/MED-001/results/r1/metrics.json', '{}')
        self.green()

    def test_red_results_without_round(self):
        self.lab.write('problems/MED-001/results/r1/metrics.json', '{}')
        self.red(r'MED-001: research changes lack a completed per-round search record')

    def test_red_results_covered_only_by_other_problem(self):
        self.lab.add_round('MED-002')
        self.lab.write('problems/MED-001/experiments/run.py', 'print(1)\n')
        self.red(r'MED-001: research changes lack')

    def test_red_unregistered_top_level_dirs(self):
        for rel in ('misc/result.csv', 'notes/finding.md', 'analysis/fit.py', 'scratch-result/out.json'):
            with self.subTest(rel=rel):
                self.lab.write(rel, 'x\n')
                self.red(rf'{rel}: unregistered path')
                self.lab.delete(rel)

    def test_red_unregistered_result_dir_under_problem(self):
        for rel in ('problems/MED-001/analysis/fit.py', 'problems/MED-001/results.txt', 'problems/MED-001/notes.md'):
            with self.subTest(rel=rel):
                self.lab.write(rel, 'x\n')
                self.red(rf'{rel}: unregistered path')
                self.lab.delete(rel)

    def test_boundary_case_and_id_variants_are_unregistered(self):
        # Pure classification, so the result does not depend on a case-insensitive filesystem (Windows/macOS).
        for rel in ('Problems/MED-001/results/x.json', 'problems/med-001/results/x.json', 'problems/MED-001/Results/x.json',
                    'problems/MED-1/results/x.json', 'problems/MED-001/results', 'decisions/x/notes.md'):
            with self.subTest(rel=rel):
                self.assertEqual(f.classify(rel, 'medicine'), ('unregistered', None))
        self.assertEqual(f.classify('problems/MED-001/results/deep/x.md', 'medicine'), ('artifact', 'MED-001'))
        self.assertEqual(f.classify('runs/r1/sub/log.txt', 'medicine'), ('attachment', 'r1'))
        self.assertEqual(f.classify('runs/README.md', 'medicine'), ('infra', None))

    def test_red_move_results_out_and_rename_extension(self):
        self.lab.add_round('MED-001')
        self.lab.write('problems/MED-001/results/r1/metrics.csv', 'a,b\n')
        self.lab.base = self.lab.commit('merged round with results')
        (self.lab.root / 'notes').mkdir()
        (self.lab.root / 'problems/MED-001/results/r1/metrics.csv').rename(self.lab.root / 'notes/metrics.md')
        self.red(r'(?s)notes/metrics\.md: unregistered path.*MED-001: research changes lack')

    def test_red_round_attachment_with_draft_round(self):
        rid, _ = self.lab.add_round('MED-001', state='DRAFT')
        self.lab.write(f'runs/{rid}/stdout.txt', 'output\n')
        self.red(rf'runs/{rid}/: 1 attachment\(s\) need')

    def test_green_round_attachment_with_admitted_round(self):
        rid, _ = self.lab.add_round('MED-001', verdict='BLOCKED', state='PAUSED')
        self.lab.write(f'runs/{rid}/FAILURE_LOG.md', 'no network\n')
        self.green()

    def test_red_attachment_added_to_old_round(self):
        rid, _ = self.lab.add_round('MED-001')
        self.lab.base = self.lab.commit('merged round')
        self.lab.write(f'runs/{rid}/late_result.csv', '1\n')
        self.red(rf'runs/{rid}/: 1 attachment')

    def test_red_round_record_deleted(self):
        rid, _ = self.lab.add_round('MED-001')
        self.lab.base = self.lab.commit('merged round')
        self.lab.delete(f'runs/{rid}/round.json')
        self.red(r'round records are append-only')

    # Review finding (2026-09-29): a merged round could be rewritten into fresh authorization for another problem.
    def test_red_merged_round_rewritten(self):
        rid, r = self.lab.add_round('MED-001', verdict='BLOCKED', state='PAUSED')
        self.lab.base = self.lab.commit('blocked round merged')
        r['problem_id'] = 'MED-002'
        r['preflight']['verdict'] = 'NO_RESOLUTION_FOUND'
        r['state'] = 'ADMITTED'
        self.lab.write(f'runs/{rid}/round.json', r)
        self.lab.write('problems/MED-002/results/r1/metrics.json', '{}')
        self.red(rf'runs/{rid}/round\.json: an admitted round keeps its identity and search; changed \[\'preflight\', \'problem_id\'\]')

    def test_green_merged_round_finished_later(self):
        rid, r = self.lab.add_round('MED-001')
        self.lab.base = self.lab.commit('admitted round merged')
        r.update(state='FINISHED', result={'summary': 'baseline reproduced'})
        self.lab.write(f'runs/{rid}/round.json', r)
        self.lab.write('problems/MED-001/results/r1/metrics.json', '{}')
        self.green()

    def test_green_merged_draft_round_admitted_later(self):
        rid, r = self.lab.add_round('MED-001', state='DRAFT')
        r['preflight'] = {'checked_at': None, 'verdict': 'BLOCKED', 'queries': [], 'sources': []}
        self.lab.write(f'runs/{rid}/round.json', r)
        self.lab.base = self.lab.commit('draft merged')
        self.lab.add_round('MED-001', rid=rid)
        self.lab.write('problems/MED-001/results/r1/metrics.json', '{}')
        self.green()

    def test_red_validate_blocked_round_does_not_cover_artifacts(self):
        # Review finding: validate treated a PAUSED/BLOCKED round as research authorization; check-diff did not.
        self.lab.add_round('MED-001', verdict='BLOCKED', state='PAUSED')
        self.lab.write('problems/MED-001/results/r1/metrics.json', '{}')
        self.lab.commit('direct push')
        with self.assertRaisesRegex(ValueError, r'research artifact without an admitted MED-001 round'):
            f.validate_repo(self.lab.root)

    def test_green_validate_blocked_round_keeps_its_attachments(self):
        rid, _ = self.lab.add_round('MED-001', verdict='BLOCKED', state='PAUSED')
        self.lab.write(f'runs/{rid}/FAILURE_LOG.md', 'no network\n')
        self.lab.commit('blocked round with its log')
        f.validate_repo(self.lab.root)

    def test_boundary_deleting_legacy_unregistered_file_is_allowed(self):
        self.lab.write('misc/legacy.txt', 'x\n')
        self.lab.base = self.lab.commit('legacy')
        self.lab.delete('misc/legacy.txt')
        self.green()

    def test_red_validate_catches_unregistered_tracked_file(self):
        self.lab.write('notes/claim.md', 'we solved it\n')
        self.lab.commit('direct push')
        with self.assertRaisesRegex(ValueError, r'notes/claim\.md: unregistered path'):
            f.validate_repo(self.lab.root)

    def test_red_validate_catches_artifact_without_round(self):
        self.lab.write('problems/MED-001/results/r1/metrics.json', '{}')
        self.lab.commit('direct push')
        with self.assertRaisesRegex(ValueError, r'research artifact without an admitted MED-001 round'):
            f.validate_repo(self.lab.root)

    def test_green_validate_with_admitted_round(self):
        self.lab.add_round('MED-001')
        self.lab.write('problems/MED-001/results/r1/metrics.json', '{}')
        self.lab.commit('round')
        f.validate_repo(self.lab.root)


class MathPathTests(LabCase):
    domain = 'math'

    def test_green_math_lean_infrastructure(self):
        self.lab.write('FrontierMath/Smoke.lean', 'theorem t : True := trivial\n')
        self.lab.write('lakefile.toml', 'name = "x"\n')
        self.green()

    def test_red_new_lean_file_outside_problem(self):
        self.lab.write('FrontierMath/NewTheorem.lean', 'theorem t : True := trivial\n')
        self.red(r'FrontierMath/NewTheorem\.lean: unregistered path')

    def test_red_math_infra_is_domain_scoped(self):
        lab = Lab('medicine')
        self.addCleanup(lab.close)
        lab.write('FrontierMath/Smoke.lean', 'x\n')
        head = lab.commit()
        with self.assertRaisesRegex(ValueError, r'FrontierMath/Smoke\.lean: unregistered path'):
            f.check_diff(lab.root, lab.base, head)


ROOT = 'FrontierMath/Research/MATH001/'


class ArtifactRootTests(LabCase):
    """GATE_CONTRACT.md §3.4: repo-declared research roots stay under the round provenance gate."""

    def setUp(self):
        self.lab = Lab('math', ('MATH-001', 'MATH-002'))
        self.addCleanup(self.lab.close)

    def declare(self, roots=None):
        lab = self.lab.read('lab.json')
        lab['artifact_roots'] = roots if roots is not None else [{'path': ROOT, 'problem_id': 'MATH-001', 'kind': 'proofs'}]
        self.lab.write('lab.json', lab)

    def declared_base(self):
        self.declare()
        self.lab.base = self.lab.commit('declare artifact root (separate, merged PR)')

    def test_green_root_declaration_alone(self):
        self.declare()
        self.green()

    def test_green_proof_in_root_with_round(self):
        self.declared_base()
        self.lab.add_round('MATH-001')
        self.lab.write(ROOT + 'Probe.lean', 'theorem probe : True := trivial\n')
        self.green()

    def test_red_proof_in_root_without_round(self):
        self.declared_base()
        self.lab.write(ROOT + 'Probe.lean', 'theorem probe : True := trivial\n')
        self.red(r'MATH-001: research changes lack a completed per-round search record')

    def test_red_proof_in_root_with_other_problem_round(self):
        self.declared_base()
        self.lab.add_round('MATH-002')
        self.lab.write(ROOT + 'Probe.lean', 'theorem probe : True := trivial\n')
        self.red(r'MATH-001: research changes lack')

    def test_red_root_declared_in_same_change_as_proof(self):
        self.declare()
        self.lab.add_round('MATH-001')
        self.lab.write(ROOT + 'Probe.lean', 'theorem probe : True := trivial\n')
        self.red(r'FrontierMath/Research/MATH001/Probe\.lean: unregistered path')

    def test_boundary_sibling_prefix_is_not_inside_root(self):
        self.declared_base()
        self.lab.add_round('MATH-001')
        self.lab.write('FrontierMath/Research/MATH0010/Probe.lean', 'theorem probe : True := trivial\n')
        self.red(r'FrontierMath/Research/MATH0010/Probe\.lean: unregistered path')

    def test_red_deleting_root_artifact_needs_round(self):
        self.declared_base()
        self.lab.add_round('MATH-001')
        self.lab.write(ROOT + 'Probe.lean', 'theorem probe : True := trivial\n')
        self.lab.base = self.lab.commit('merged proof')
        self.lab.delete(ROOT + 'Probe.lean')
        self.red(r'MATH-001: research changes lack')

    def test_validate_tree_root_artifact(self):
        self.declare()
        self.lab.write(ROOT + 'Probe.lean', 'theorem probe : True := trivial\n')
        self.lab.commit('direct push without a round')
        with self.assertRaisesRegex(ValueError, r'Probe\.lean: research artifact without an admitted MATH-001 round'):
            f.validate_repo(self.lab.root)
        self.lab.add_round('MATH-001')
        self.lab.commit('round')
        f.validate_repo(self.lab.root)

    def test_red_removed_root_leaves_unregistered_files(self):
        self.declare()
        self.lab.add_round('MATH-001')
        self.lab.write(ROOT + 'Probe.lean', 'theorem probe : True := trivial\n')
        self.lab.commit('root, round and proof')
        f.validate_repo(self.lab.root)
        self.declare([])
        self.lab.commit('root removed')
        with self.assertRaisesRegex(ValueError, r'Probe\.lean: unregistered path'):
            f.validate_repo(self.lab.root)

    def test_red_invalid_root_declarations(self):
        good = {'path': ROOT, 'problem_id': 'MATH-001', 'kind': 'proofs'}
        cases = (
            ({**good, 'path': '../outside/'}, r'relative directory'),
            ({**good, 'path': '/abs/'}, r'relative directory'),
            ({**good, 'path': 'FrontierMath/Research/MATH001'}, r'relative directory'),
            ({**good, 'path': '.hidden/'}, r'relative directory'),
            ({**good, 'path': 'FrontierMath/../problems/'}, r'relative directory'),
            ({**good, 'path': 'problems/MATH-001/lean/'}, r'reserved directory'),
            ({**good, 'path': '.github/x/'}, r'relative directory'),
            ({**good, 'path': 'runs/r/'}, r'reserved directory'),
            ({**good, 'path': 'FrontierMath/'}, r'would contain infrastructure files'),
            ({**good, 'problem_id': 'MATH-099'}, r'MATH-099 is not a problem in this repository'),
            ({**good, 'problem_id': 'math-001'}, r'invalid problem_id'),
            ({**good, 'kind': 'notes'}, r'kind must be one of'),
        )
        for entry, pattern in cases:
            with self.subTest(entry=entry):
                with self.assertRaisesRegex(ValueError, pattern):
                    f.artifact_roots({'domain': 'math', 'artifact_roots': [entry]}, {'MATH-001', 'MATH-002'})
        with self.assertRaisesRegex(ValueError, r'nests with'):
            f.artifact_roots({'domain': 'math', 'artifact_roots': [
                good, {'path': ROOT + 'Sub/', 'problem_id': 'MATH-002', 'kind': 'proofs'}]})
        with self.assertRaisesRegex(ValueError, r'must be a list'):
            f.artifact_roots({'domain': 'math', 'artifact_roots': good})
        self.assertEqual(f.artifact_roots({'domain': 'math', 'artifact_roots': [good]}), ((ROOT, 'MATH-001', 'proofs'),))

    # Review finding (2026-09-29): an invalid root at the merge base blocked every PR, including the one fixing it.
    def invalid_base_root(self):
        self.declare([{'path': ROOT, 'problem_id': 'MATH-001', 'kind': 'notes'}])
        self.lab.base = self.lab.commit('root that a newer gate rejects')

    def test_green_fixing_invalid_base_root(self):
        self.invalid_base_root()
        self.declare()
        self.green()

    def test_red_invalid_root_still_blocks_other_changes(self):
        self.invalid_base_root()
        self.lab.write('STATUS.md', 'status updated\n')
        self.red(r'lab\.json artifact_roots\[0\]: kind must be one of')

    def test_red_files_under_invalid_base_root_are_unregistered(self):
        self.invalid_base_root()
        self.declare()
        self.lab.add_round('MATH-001')
        self.lab.write(ROOT + 'Probe.lean', 'theorem probe : True := trivial\n')
        self.red(r'FrontierMath/Research/MATH001/Probe\.lean: unregistered path')


class DomainIdentityTests(LabCase):
    """Review finding: a research PR must not turn the gates off by declaring domain governance."""

    def test_red_check_diff_domain_flip_to_governance(self):
        lab = self.lab.read('lab.json'); lab['domain'] = 'governance'; lab['protocol_version'] = f.PROTOCOL_VERSION
        self.lab.write('lab.json', lab)
        self.lab.write('misc/result.csv', '1\n')
        self.red(r'lab\.json: domain is immutable \(medicine -> governance\)')

    def test_red_validate_research_repo_declaring_governance(self):
        lab = self.lab.read('lab.json'); lab['domain'] = 'governance'; lab['protocol_version'] = f.PROTOCOL_VERSION
        self.lab.write('lab.json', lab)
        with self.assertRaisesRegex(ValueError, r'research repository .* cannot declare domain governance'):
            f.validate_repo(self.lab.root)

    def test_red_check_diff_domain_change_between_research_domains(self):
        lab = self.lab.read('lab.json'); lab['domain'] = 'physics'
        self.lab.write('lab.json', lab)
        self.red(r'lab\.json: domain is immutable \(medicine -> physics\)')

    def test_red_governance_domain_when_merge_base_has_no_lab_json(self):
        # Review finding (2026-09-29): with no lab.json at the merge base the immutability check had nothing to compare.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            git = lambda *a: subprocess.run(['git', '-C', d, '-c', 'user.name=x', '-c', 'user.email=x@invalid', *a],
                                            check=True, capture_output=True, text=True).stdout.strip()
            git('init', '-q', '-b', 'main'); git('config', 'gc.auto', '0'); git('config', 'maintenance.auto', 'false')
            git('commit', '-q', '--allow-empty', '-m', 'initial commit before bootstrap')
            base = git('rev-parse', 'HEAD')
            for rel in ('lab.json', 'GOVERNANCE.lock.json', 'README.md', 'AGENTS.md', 'STATUS.md', 'problems/MED-001/problem.json'):
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_bytes((self.lab.root / rel).read_bytes())
            f.save(root / 'lab.json', {'domain': 'governance', 'protocol_version': f.PROTOCOL_VERSION})
            (root / 'misc').mkdir(); (root / 'misc/result.csv').write_text('1\n')
            git('add', '-A'); git('commit', '-q', '-m', 'research repo claiming governance')
            with self.assertRaisesRegex(ValueError, r'research repository .* cannot declare domain governance'):
                f.check_diff(root, base, git('rev-parse', 'HEAD'))


class GovernanceRepoTests(unittest.TestCase):
    def test_governance_repo_skips_research_contract(self):
        root = Path(__file__).resolve().parents[1]
        try:
            head = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
        except (subprocess.CalledProcessError, OSError):
            self.skipTest('not a git checkout')
        f.check_diff(root, head, head)


class DecideCommandTests(LabCase):
    def test_decide_writes_valid_record_and_passes(self):
        path = f.decide(self.lab.root, 'MED-001', 'hygiene', 'claude', ['sources'], 'URL moved to DOI', {})
        self.assertTrue(path.is_file())
        self.lab.edit_card('MED-001', sources=[{'title': 'Fixture', 'url': 'https://doi.org/10.1/fixture', 'kind': 'primary', 'supports': 'syntax'}])
        self.green()

    def test_decide_refuses_unauthorized_field(self):
        with self.assertRaisesRegex(ValueError, r"cannot authorize \['statement'\]"):
            f.decide(self.lab.root, 'MED-001', 'hygiene', 'claude', ['statement'], 'r', {})


if __name__ == '__main__':
    unittest.main()
