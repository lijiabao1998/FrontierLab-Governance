import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


ledger = module("ledger", "convergence/validate_ledger.py")
renderer = module("renderer", "audits/render_frontier_audit.py")
capture = module("capture", "convergence/capture_github.py")


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / "tests")
        self.addCleanup(self.tmp.cleanup)
        self.workspace = Path(self.tmp.name)
        self.repo = self.workspace / "FrontierMath"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "gc.auto", "0")
        (self.repo / "baseline.txt").write_text("baseline", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "baseline")
        self.old = self.git("rev-parse", "HEAD")
        (self.repo / "evidence.json").write_text("{}", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "evidence")
        self.head = self.git("rev-parse", "HEAD")
        self.data = {"entries": [{"repo": "FrontierMath", "current_head_sha": self.head,
                     "work_status": "HOLD", "evidence_paths": [{
                     "repo": "lijiabao1998/FrontierMath", "commit_sha": "BRANCH_HEAD",
                     "path": "evidence.json"}]}]}

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True).strip()

    def test_valid_immutable_reference(self):
        self.assertEqual(ledger.validate(self.data, self.workspace), [])

    def test_unrelated_checkout_cannot_supply_missing_old_file(self):
        self.data["entries"][0]["current_head_sha"] = self.old
        self.assertTrue(ledger.validate(self.data, self.workspace))

    def test_missing_clone_is_not_success(self):
        self.assertTrue(ledger.validate(self.data, self.workspace / "missing"))

    def test_linked_worktree_is_supported(self):
        linked = self.workspace / "linked"
        linked.mkdir()
        target = linked / "FrontierMath"
        self.git("worktree", "add", "--detach", str(target), self.head)
        self.assertTrue((target / ".git").is_file())
        self.assertEqual(ledger.validate(self.data, linked), [])

    def test_ready_needs_current_review(self):
        entry = self.data["entries"][0]
        entry.update(work_status="READY_FOR_OWNER_REVIEW", last_reviewed_sha="pending",
                     live_P1=0, live_P2=0, ci_state="GREEN", manifest_state="GREEN",
                     unresolved_blockers=[])
        self.assertTrue(ledger.validate(self.data, self.workspace))
        entry["last_reviewed_sha"] = self.head
        self.assertEqual(ledger.validate(self.data, self.workspace), [])

    def test_ready_rejects_known_manifest_failure_or_blockers(self):
        entry = self.data["entries"][0]
        entry.update(work_status="READY_FOR_OWNER_REVIEW", last_reviewed_sha=self.head,
                     live_P1=0, live_P2=0, ci_state="GREEN", manifest_state="FAIL_COMMITTED_BYTES",
                     unresolved_blockers=[])
        self.assertTrue(ledger.validate(self.data, self.workspace))
        entry.update(manifest_state="GREEN", unresolved_blockers=["unresolved independent verifier mismatch"])
        self.assertTrue(ledger.validate(self.data, self.workspace))

    def test_heads_and_locator_revisions_must_be_existing_commits(self):
        tree = self.git("rev-parse", "HEAD^{tree}")
        for bad in ("f" * 40, tree):
            data = copy.deepcopy(self.data)
            data["entries"][0]["current_head_sha"] = bad
            data["entries"][0]["evidence_paths"][0]["commit_sha"] = self.head
            self.assertTrue(ledger.validate(data, self.workspace))
            data["entries"][0]["current_head_sha"] = self.head
            data["entries"][0]["evidence_paths"][0]["commit_sha"] = bad
            self.assertTrue(ledger.validate(data, self.workspace))

    def test_invalid_or_mutable_locators_fail(self):
        for field, value in [("commit_sha", "HEAD"), ("commit_sha", "THIS_COMMIT"),
                             ("path", "../evidence.json"), ("path", "."),
                             ("repo", "another/FrontierMath")]:
            data = copy.deepcopy(self.data)
            data["entries"][0]["evidence_paths"][0][field] = value
            self.assertTrue(ledger.validate(data, self.workspace), (field, value))

    def test_empty_ledger_fails(self):
        self.assertTrue(ledger.validate({"entries": []}, self.workspace))


class AuditTests(unittest.TestCase):
    def test_pending_and_dismissed_reviews_are_not_current_head_reviews(self):
        path = next((ROOT / "convergence/snapshots").glob("*/FrontierBiology.json"))
        raw = json.loads(path.read_text(encoding="utf-8"))
        prs = raw["response"]["data"]["repository"]["pullRequests"]["nodes"]
        for pr in prs:
            pr["reviews"]["nodes"] = [
                {"commit": {"oid": pr["headRefOid"]}, "state": "PENDING", "submittedAt": None},
                {"commit": {"oid": pr["headRefOid"]}, "state": "DISMISSED", "submittedAt": "2026-09-29T00:00:00Z"}]
        self.assertTrue(all(not row["current_head_reviews"] for row in capture.summarise(raw)))

    def test_committed_markdown_matches_renderer(self):
        data = json.loads(renderer.JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(renderer.render(data), renderer.MD_PATH.read_text(encoding="utf-8"))

    def test_string_query_is_one_row(self):
        data = json.loads(renderer.JSON_PATH.read_text(encoding="utf-8"))
        data["problems"] = [data["problems"][0]]
        data["problems"][0]["queries"] = "reference record"
        self.assertEqual(renderer.render(data).count("| (repo-recorded) |"), 1)

    def test_source_year_is_not_hardcoded_to_2026(self):
        data = json.loads(renderer.JSON_PATH.read_text(encoding="utf-8"))
        bio = next(p for p in data["problems"] if p["problem_id"] == "BIO-001")
        self.assertEqual(bio["sources"][0]["year"], 2025)
