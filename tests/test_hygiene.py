"""Hygiene guards: clean BLOCKED errors, branch naming contract, protocol version consistency."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'tools/frontier.py'
spec = importlib.util.spec_from_file_location('frontier', TOOL)
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)


def record(pid='MED-001', agent='claude', branch=None):
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    return {
        'round_id': 'fixture', 'problem_id': pid, 'agent': agent, 'branch': branch or f'{agent}/{pid}-baseline-r1',
        'base_sha': 'a' * 40, 'started_at': now, 'state': 'DRAFT', 'acceptance': 'Synthetic fixture.',
        'not_done': 'No science performed.', 'budget': {'wall_minutes': 10, 'usd': 0, 'max_trials': 10},
        'preflight': {
            'checked_at': now, 'verdict': 'NO_RESOLUTION_FOUND',
            'queries': [{'query': c + ' fixture', 'engine': 'unit-test-only', 'category': c, 'outcome': 'synthetic'}
                        for c in sorted(f.CATEGORIES)],
            'sources': [
                {'url': 'https://arxiv.org/abs/2602.07751', 'title': 'Fixture', 'kind': 'primary', 'supports': 'syntax'},
                {'url': 'https://lean-lang.org/doc/reference/latest/Axioms/', 'title': 'Fixture', 'kind': 'official', 'supports': 'syntax'}],
            'limitations': 'Synthetic', 'scope_comparison': 'Synthetic', 'baseline': 'Synthetic',
            **{k: True for k in ('sources_read', 'scope_compared', 'retractions_checked', 'licenses_checked',
                                'safety_checked', 'baseline_identified', 'acceptance_frozen')}}}


def card(pid='MED-001', domain='medicine'):
    return {'id': pid, 'domain': domain, 'title': 't', 'status': 'OPEN', 'priority': 'A',
            'checked_on': dt.datetime.now(dt.timezone.utc).date().isoformat(), 'statement': 's', 'known_result': 'k',
            'open_gap': 'g', 'first_task': 'f', 'evaluator': 'e', 'validation_limits': 'v', 'completion_criterion': 'c',
            'screening_note': 'n', 'screening_queries': ['q'],
            'sources': [{'title': 'x', 'url': 'https://arxiv.org/abs/2602.07751', 'kind': 'primary', 'supports': 's'}]}


class Lab:
    def __init__(self, lock_version=f.PROTOCOL_VERSION):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)
        pin = '1' * 40
        # A complete, contract-compliant lab: the pin declarations keep it valid when stricter gates are merged.
        (self.root / 'README.md').write_text(f'每輪按治理 {pin} fresh search。\n', encoding='utf-8')
        (self.root / 'AGENTS.md').write_text(f'讀治理 https://github.com/lijiabao1998/FrontierLab-Governance/tree/{pin} 。\n', encoding='utf-8')
        (self.root / 'STATUS.md').write_text('x\n', encoding='utf-8')
        workflow = self.root / '.github' / 'workflows' / 'research.yml'
        workflow.parent.mkdir(parents=True)
        workflow.write_text(f'jobs:\n  records:\n    uses: lijiabao1998/FrontierLab-Governance/.github/workflows/research.yml@{pin}\n'
                            f'    with:\n      governance_ref: {pin}\n', encoding='utf-8')
        f.save(self.root / 'lab.json', {'domain': 'medicine', 'expected_problem_count': 1})
        lock = {'repository': 'lijiabao1998/FrontierLab-Governance', 'commit': pin}
        if lock_version is not None:
            lock['protocol_version'] = lock_version
        f.save(self.root / 'GOVERNANCE.lock.json', lock)
        f.save(f.problem_path(self.root, 'MED-001'), card())
        subprocess.run(['git', '-C', str(self.root), 'init', '-q'], check=True)
        # No detached auto-maintenance writing into .git/objects while TemporaryDirectory cleans up (newer git).
        for key, value in (('gc.auto', '0'), ('maintenance.auto', 'false')):
            subprocess.run(['git', '-C', str(self.root), 'config', key, value], check=True)
        subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=f', '-c', 'user.email=f@invalid', 'commit', '-q',
                        '--allow-empty', '-m', 'base'], check=True)

    def close(self):
        self.dir.cleanup()


def cli(*args):
    return subprocess.run([sys.executable, str(TOOL), *map(str, args)], capture_output=True, text=True)


class CleanBlockedTests(unittest.TestCase):
    """checked_at / started_at problems must end as `BLOCKED: …`, exit 1, never a traceback."""

    def setUp(self):
        self.lab = Lab()
        self.addCleanup(self.lab.close)

    def admit(self, r):
        path = self.lab.root / 'runs' / 'fixture' / 'round.json'
        f.save(path, r)
        return cli('admit', self.lab.root, path)

    def assertBlocked(self, run, message):
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertNotIn('Traceback', run.stderr)
        self.assertTrue(run.stderr.startswith('BLOCKED: '), run.stderr)
        self.assertIn(message, run.stderr)

    def test_green_complete_record_is_admitted(self):
        run = self.admit(record())
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn('ADMITTED', run.stdout)

    def test_red_checked_at_null(self):
        r = record(); r['preflight']['checked_at'] = None
        self.assertBlocked(self.admit(r), 'preflight.checked_at: missing ISO 8601 timestamp')

    def test_red_checked_at_missing(self):
        r = record(); del r['preflight']['checked_at']
        self.assertBlocked(self.admit(r), 'preflight.checked_at: missing')

    def test_red_checked_at_empty_string(self):
        r = record(); r['preflight']['checked_at'] = '  '
        self.assertBlocked(self.admit(r), 'preflight.checked_at: missing')

    def test_red_checked_at_not_iso(self):
        r = record(); r['preflight']['checked_at'] = 'yesterday'
        self.assertBlocked(self.admit(r), "preflight.checked_at: not an ISO 8601 timestamp ('yesterday')")

    def test_red_checked_at_without_offset(self):
        r = record(); r['preflight']['checked_at'] = '2026-09-28T10:00:00'
        self.assertBlocked(self.admit(r), 'preflight.checked_at: timestamp must include UTC offset')

    def test_red_started_at_missing(self):
        r = record(); del r['started_at']
        self.assertBlocked(self.admit(r), 'round.started_at: missing')

    def test_red_preflight_missing(self):
        r = record(); del r['preflight']
        self.assertBlocked(self.admit(r), 'round: missing preflight object')

    def test_boundary_malformed_query_shape_is_still_clean(self):
        r = record(); r['preflight']['queries'] = ['general', 'discipline', 'solution', 'criticism']
        run = self.admit(r)
        self.assertEqual(run.returncode, 1)
        self.assertNotIn('Traceback', run.stderr)
        self.assertTrue(run.stderr.startswith('BLOCKED: '), run.stderr)

    def test_start_prints_clean_error_for_unknown_problem(self):
        run = cli('start', self.lab.root, 'MED-999', '--agent', 'claude')
        self.assertEqual(run.returncode, 1)
        self.assertNotIn('Traceback', run.stderr)


class BranchContractTests(unittest.TestCase):
    def test_green_accepted_forms(self):
        for agent, pid, branch in (('glm', 'MATH-001', 'glm/MATH-001-baseline-r1'),
                                   ('gpt', 'MATH-001', 'gpt/math-001-test'),
                                   ('claude', 'MED-001', 'claude/MED-001-round-20260928t101530123456z'),
                                   ('claude-code', 'CS-001', 'claude-code/CS-001-dependency-closure')):
            with self.subTest(branch=branch):
                self.assertTrue(f.branch_ok(branch, agent, pid))
                f.validate_preflight(record(pid, agent, branch))

    def test_red_rejected_forms(self):
        for branch, why in (('main', 'main'),
                            ('claude/med-001', 'old start default: no topic'),
                            ('claude/MED-001-', 'empty topic'),
                            ('claude/MED-001-x-', 'trailing dash'),
                            ('claude/MED-001-Baseline', 'uppercase topic'),
                            ('claude/MED-001-a_b', 'underscore'),
                            ('gpt/MED-001-baseline', 'another agent'),
                            ('CLAUDE/MED-001-baseline', 'agent case'),
                            ('claude/MED-002-baseline', 'another problem'),
                            ('claude/MED-0010-baseline', 'problem id prefix only'),
                            ('claude/x/MED-001-baseline', 'nested')):
            with self.subTest(why=why):
                self.assertFalse(f.branch_ok(branch, 'claude', 'MED-001'))
                with self.assertRaisesRegex(ValueError, 'agent branch'):
                    f.validate_preflight(record('MED-001', 'claude', branch))

    def test_red_agent_must_be_slug(self):
        with self.assertRaisesRegex(ValueError, 'agent must be a lowercase slug'):
            f.validate_preflight(record('MED-001', 'Claude', 'Claude/MED-001-x'))

    def test_start_generates_contract_branch_and_is_unique(self):
        lab = Lab()
        self.addCleanup(lab.close)
        branches = set()
        for topic in ('baseline', 'baseline', 'round'):
            f.start(lab.root, 'MED-001', 'claude', topic)
        for path in lab.root.glob('runs/*/round.json'):
            r = f.load(path)
            self.assertTrue(f.branch_ok(r['branch'], 'claude', 'MED-001'), r['branch'])
            self.assertRegex(r['branch'], r'^claude/MED-001-(baseline|round)-\d{8}t\d{12}z$')
            branches.add(r['branch'])
        self.assertEqual(len(branches), 3)

    def test_start_default_topic_via_cli(self):
        lab = Lab()
        self.addCleanup(lab.close)
        run = cli('start', lab.root, 'MED-001', '--agent', 'claude')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertRegex(run.stdout, r'git switch -c claude/MED-001-round-\d{8}t\d{12}z')

    def test_red_start_rejects_unsafe_topic(self):
        lab = Lab()
        self.addCleanup(lab.close)
        for topic in ('Baseline', 'a b', '../main', 'x' * 41, ''):
            with self.subTest(topic=topic), self.assertRaisesRegex(ValueError, 'topic must be a lowercase slug'):
                f.start(lab.root, 'MED-001', 'claude', topic)


class ProtocolVersionTests(unittest.TestCase):
    def test_green_governance_lab_json_matches_code(self):
        self.assertEqual(json.loads((ROOT / 'lab.json').read_text())['protocol_version'], f.PROTOCOL_VERSION)
        f.validate_repo(ROOT)

    def test_green_versions_document_lists_current_version(self):
        self.assertIn(f'| {f.PROTOCOL_VERSION} |', (ROOT / 'PROTOCOL_VERSIONS.md').read_text(encoding='utf-8'))

    def test_red_governance_lab_json_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ('README.md', 'AGENTS.md', 'STATUS.md'):
                (root / name).write_text('x\n')
            f.save(root / 'lab.json', {'domain': 'governance', 'protocol_version': '1.0.0'})
            with self.assertRaisesRegex(ValueError, f'lab.json protocol_version must be {f.PROTOCOL_VERSION}'):
                f.validate_repo(root)

    def test_green_research_lock_matches(self):
        lab = Lab()
        self.addCleanup(lab.close)
        f.validate_repo(lab.root)

    def test_red_research_lock_declares_other_version(self):
        lab = Lab('1.0.0')
        self.addCleanup(lab.close)
        with self.assertRaisesRegex(ValueError, r'declares protocol 1\.0\.0, but this governance checkout implements'):
            f.validate_repo(lab.root)

    def test_boundary_research_lock_without_version(self):
        lab = Lab(None)
        self.addCleanup(lab.close)
        with self.assertRaisesRegex(ValueError, 'declares protocol None'):
            f.validate_repo(lab.root)


if __name__ == '__main__':
    unittest.main()
