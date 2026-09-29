import copy
import datetime as dt
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('frontier', Path(__file__).resolve().parents[1] / 'tools/frontier.py')
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)


def record():
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    return {
        'round_id': 'test-round', 'problem_id': 'MATH-001', 'agent': 'gpt',
        'branch': 'gpt/math-001-test', 'base_sha': 'a' * 40, 'started_at': now,
        'state': 'ADMITTED', 'acceptance': 'An intentionally synthetic unit-test fixture.',
        'not_done': 'No scientific work performed by this fixture.',
        'budget': {'wall_minutes': 10, 'usd': 0, 'max_trials': 10},
        'preflight': {
            'checked_at': now, 'verdict': 'NO_RESOLUTION_FOUND',
            'queries': [{'query': c + ' synthetic fixture', 'engine': 'unit-test-only',
                         'category': c, 'outcome': 'Synthetic: not a real search'} for c in sorted(f.CATEGORIES)],
            'sources': [
                {'url': 'https://arxiv.org/abs/2602.07751', 'title': 'Fixture reference', 'kind': 'primary', 'supports': 'URL syntax only'},
                {'url': 'https://lean-lang.org/doc/reference/latest/ValidatingProofs/', 'title': 'Fixture reference', 'kind': 'official', 'supports': 'URL syntax only'}],
            'limitations': 'Synthetic fixture only', 'scope_comparison': 'Fixture scope', 'baseline': 'Fixture baseline',
            **{k: True for k in ('sources_read', 'scope_compared', 'retractions_checked', 'licenses_checked',
                                'safety_checked', 'baseline_identified', 'acceptance_frozen')}
        }
    }


class GateTests(unittest.TestCase):
    def test_valid_fixture(self):
        self.assertEqual(f.validate_preflight(record(), fresh=True), 'NO_RESOLUTION_FOUND')

    def test_missing_each_check_rejected(self):
        for flag in ('sources_read', 'scope_compared', 'retractions_checked', 'licenses_checked',
                     'safety_checked', 'baseline_identified', 'acceptance_frozen'):
            with self.subTest(flag=flag):
                r = record(); r['preflight'][flag] = False
                with self.assertRaises(ValueError): f.validate_preflight(r)

    def test_stale_search_rejected(self):
        r = record(); old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=2)).isoformat()
        r['started_at'] = old; r['preflight']['checked_at'] = old
        with self.assertRaises(ValueError): f.validate_preflight(r, fresh=True)

    def test_prior_round_search_rejected(self):
        r = record(); r['preflight']['checked_at'] = (dt.datetime.now(dt.timezone.utc)-dt.timedelta(days=1)).isoformat()
        with self.assertRaises(ValueError): f.validate_preflight(r)

    def test_missing_criticism_rejected(self):
        r = record(); r['preflight']['queries'] = r['preflight']['queries'][:3]
        with self.assertRaises(ValueError): f.validate_preflight(r)

    def test_duplicate_sources_rejected(self):
        r = record(); r['preflight']['sources'][1] = copy.deepcopy(r['preflight']['sources'][0])
        with self.assertRaises(ValueError): f.validate_preflight(r)

    def test_no_primary_rejected(self):
        r = record(); r['preflight']['sources'][0]['kind'] = 'secondary'
        with self.assertRaises(ValueError): f.validate_preflight(r)

    def test_main_rejected(self):
        r = record(); r['branch'] = 'main'
        with self.assertRaises(ValueError): f.validate_preflight(r)

    def test_unbounded_budget_rejected(self):
        r = record(); r['budget']['wall_minutes'] = 10000
        with self.assertRaises(ValueError): f.validate_preflight(r)

    def test_unsupported_completion_rejected(self):
        r = record(); r['preflight']['verdict'] = 'RESOLVED_EXTERNAL'
        with self.assertRaises(ValueError): f.validate_preflight(r)

    def test_subcase_does_not_close_parent(self):
        x = {'problem_id': 'MATH-001', 'scope_statement': 'small n only', 'basis': 'fixture',
             'confirmed_by': 'fixture reviewer', 'independent_check': 'fixture',
             'scope_match': False, 'independently_verified': True}
        with self.assertRaises(ValueError): f.validate_resolution(x, 'MATH-001')

    def test_bad_id_rejected(self):
        with self.assertRaises(ValueError): f.problem_path(Path('.'), '../main')

    def test_extended_problem_prefixes_accepted(self):
        for pid in ('CS-001','STAT-001','MAT-001','ASTRO-001','EARTH-001','NEURO-001','ECON-001','ENG-001','MED-001','SOC-001','META-001'):
            self.assertEqual(f.problem_path(Path('.'), pid).parts[-2:], (pid, 'problem.json'))

    def test_incomplete_repo_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); f.save(root/'lab.json', {'domain':'math', 'expected_problem_count':10})
            with self.assertRaises(ValueError): f.validate_repo(root)

    def test_external_completion_is_recorded(self):
        r = record()
        r['preflight']['verdict'] = 'RESOLVED_EXTERNAL'
        r['preflight']['resolution'] = {
            'problem_id': 'MATH-001', 'scope_statement': 'synthetic exact scope', 'basis': 'unit test only',
            'confirmed_by': 'fixture reviewer', 'independent_check': 'fixture certificate',
            'scope_match': True, 'independently_verified': True,
            'sources': r['preflight']['sources'], 'confirmed_at': r['started_at']}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); f.save(f.problem_path(root, 'MATH-001'), {'status':'OPEN'})
            f.save(root/'round.json',r); f.admit(root,root/'round.json')
            self.assertEqual(f.load(f.problem_path(root,'MATH-001'))['status'],'COMPLETED_EXTERNAL')
            self.assertEqual(f.load(root/'round.json')['state'],'CLOSED_EXTERNAL')

    def test_resolution_claim_pauses_not_completes(self):
        r=record(); r['preflight']['verdict']='CLAIMED_RESOLVED'
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); f.save(f.problem_path(root,'MATH-001'),{'status':'OPEN'}); f.save(root/'round.json',r)
            with self.assertRaises(ValueError): f.admit(root,root/'round.json')
            self.assertEqual(f.load(f.problem_path(root,'MATH-001'))['status'],'OPEN')
            self.assertEqual(f.load(root/'round.json')['state'],'PAUSED')

if __name__ == '__main__': unittest.main()
