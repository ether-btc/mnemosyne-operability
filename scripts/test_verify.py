#!/usr/bin/env python3
"""Black-box regression tests for the project review gate; stdlib only."""
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "verify.sh"
COVERED = (
    "README.md", "PRAXIS.md", "METHODOLOGY.md", "CODEBOOK.md", "ROADMAP.md",
    "DECISIONS.md", "STATUS.md", "SOURCES.md", "EXECUTION-PROMPT.md",
    "scripts/verify.sh", "scripts/test_verify.py",
    "evidence/search/session-search-output-contract-2026-10-04.md",
    "evidence/quality/local-tool-checks-2026-10-04.md",
    "evidence/quality/bot-g0-v2-vibe-prompt.txt",
    "evidence/quality/bot-g0-v2-vibe-review.txt",
    "evidence/quality/bot-g0-v2-cofounder-prompt.txt",
    "evidence/quality/bot-g0-v2-cofounder-review.txt",
    "evidence/quality/ocr-round3-g0-v2.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReviewGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        shutil.copyfile(SOURCE, self.root / "scripts/verify.sh")
        for rel in COVERED:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if rel != "scripts/verify.sh":
                path.write_text("fixture\n", encoding="utf-8")
        (self.root / "PRAXIS.md").write_text(
            "If there is no repeated, actionable omission class, the successful disposition is **do not build**.\n",
            encoding="utf-8",
        )
        (self.root / "METHODOLOGY.md").write_text("thresholds only after observing corpus prevalence\n", encoding="utf-8")
        (self.root / "ROADMAP.md").write_text("R0\n", encoding="utf-8")
        (self.root / "STATUS.md").write_text("independent plan review is pending\n", encoding="utf-8")
        (self.root / "EXECUTION-PROMPT.md").write_text("First uncompleted task: **R0\nVerbatim resume trigger\n", encoding="utf-8")
        (self.root / "REVIEW-PROMPT.txt").write_text("review exact fixture\n", encoding="utf-8")
        (self.root / "REVIEW-RESULT.txt").write_text("VERDICT: NO-GO-WITH-CONDITIONS\n", encoding="utf-8")
        self.write_receipt("NO-GO-WITH-CONDITIONS")

    def tearDown(self):
        self.temp.cleanup()

    def write_go_result(self, unresolved=None, extra_verdict=None):
        findings = [] if unresolved is None else unresolved
        record = {"verdict": "GO", "unresolved_findings": findings}
        text = "VERDICT: GO\nGATE_RECORD_JSON: " + json.dumps(record) + "\n"
        if extra_verdict:
            text += f"VERDICT: {extra_verdict}\n"
        (self.root / "REVIEW-RESULT.txt").write_text(text, encoding="utf-8")

    def write_receipt(self, verdict):
        prompt = self.root / "REVIEW-PROMPT.txt"
        result = self.root / "REVIEW-RESULT.txt"
        reviewed_hashes = {rel: digest(self.root / rel) for rel in COVERED}
        prompt.write_text(
            "Exact file hashes under review:\n"
            + "".join(f"{reviewed_hashes[rel]}  {rel}\n" for rel in COVERED),
            encoding="utf-8",
        )
        receipt = {
            "schema_version": 2,
            "latest_review": {
                "round": 2,
                "reviewer": "independent-reviewer",
                "verdict": verdict,
                "result_path": "REVIEW-RESULT.txt",
                "result_sha256": digest(result),
                "prompt_path": "REVIEW-PROMPT.txt",
                "prompt_sha256": digest(prompt),
                "reviewed_files": reviewed_hashes,
                "unresolved_findings": [],
            },
        }
        (self.root / "review-state.json").write_text(json.dumps(receipt), encoding="utf-8")

    def run_gate(self, *args):
        return subprocess.run(
            ["bash", str(self.root / "scripts/verify.sh"), *args],
            cwd=self.root, capture_output=True, text=True, check=False,
        )

    def test_structural_mode_accepts_intact_no_go_project(self):
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NO-GO-WITH-CONDITIONS", result.stdout)

    def test_require_go_rejects_no_go_receipt(self):
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NO-GO-WITH-CONDITIONS", result.stdout + result.stderr)

    def test_require_go_accepts_exact_go_receipt(self):
        self.write_go_result()
        self.write_receipt("GO")
        result = self.run_gate("--require-go")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_require_go_rejects_changed_reviewed_file(self):
        self.write_go_result()
        self.write_receipt("GO")
        (self.root / "PRAXIS.md").write_text("changed after review\n", encoding="utf-8")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PRAXIS.md", result.stdout + result.stderr)

    def test_require_go_rejects_tampered_raw_review(self):
        self.write_go_result()
        self.write_receipt("GO")
        (self.root / "REVIEW-RESULT.txt").write_text("VERDICT: GO\nchanged\n", encoding="utf-8")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("result", result.stdout.lower() + result.stderr.lower())

    def test_require_go_rejects_unresolved_findings(self):
        self.write_go_result(["F1"])
        self.write_receipt("GO")
        receipt_path = self.root / "review-state.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["latest_review"]["unresolved_findings"] = ["F1"]
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unresolved", result.stdout.lower() + result.stderr.lower())

    def test_require_go_rejects_manifest_not_presented_to_reviewer(self):
        self.write_go_result()
        self.write_receipt("GO")
        prompt_path = self.root / "REVIEW-PROMPT.txt"
        lines = prompt_path.read_text(encoding="utf-8").splitlines()
        lines = [("0" * 64 + line[64:]) if line.endswith("  PRAXIS.md") else line for line in lines]
        prompt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        receipt_path = self.root / "review-state.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["latest_review"]["prompt_sha256"] = digest(prompt_path)
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("manifest", result.stdout.lower() + result.stderr.lower())

    def test_require_go_rejects_conflicting_raw_verdict_lines(self):
        self.write_go_result(extra_verdict="NO-GO-WITH-CONDITIONS")
        self.write_receipt("GO")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("verdict", result.stdout.lower() + result.stderr.lower())

    def test_require_go_rejects_raw_unresolved_findings_even_if_receipt_is_cleared(self):
        self.write_go_result(["R2-M1"])
        self.write_receipt("GO")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("findings", result.stdout.lower() + result.stderr.lower())

    def test_require_go_rejects_malformed_gate_record(self):
        (self.root / "REVIEW-RESULT.txt").write_text(
            "VERDICT: GO\nGATE_RECORD_JSON: not-json\n", encoding="utf-8"
        )
        self.write_receipt("GO")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("malformed", result.stdout.lower() + result.stderr.lower())

    def test_require_go_rejects_wrong_type_unresolved_findings(self):
        record = {"verdict": "GO", "unresolved_findings": "[]"}
        (self.root / "REVIEW-RESULT.txt").write_text(
            "VERDICT: GO\nGATE_RECORD_JSON: " + json.dumps(record) + "\n",
            encoding="utf-8",
        )
        self.write_receipt("GO")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("findings", result.stdout.lower() + result.stderr.lower())

    def test_structural_mode_rejects_invalid_review_state_json(self):
        (self.root / "review-state.json").write_text("{not-json", encoding="utf-8")
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid review-state.json", result.stdout.lower() + result.stderr.lower())

    def test_require_go_rejects_duplicate_gate_record_keys(self):
        record = '{"verdict":"NO-GO","verdict":"GO","unresolved_findings":[]}'
        result_path = self.root / "REVIEW-RESULT.txt"
        result_path.write_text(
            "VERDICT: GO\nGATE_RECORD_JSON: " + record + "\n", encoding="utf-8"
        )
        self.write_receipt("GO")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate", result.stdout.lower() + result.stderr.lower())

    def test_require_go_rejects_duplicate_verdict(self):
        self.write_go_result()
        with (self.root / "REVIEW-RESULT.txt").open("a", encoding="utf-8") as result_file:
            result_file.write("VERDICT: GO\n")
        self.write_receipt("GO")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly one", result.stdout.lower() + result.stderr.lower())

    def test_require_go_rejects_gate_record_verdict_mismatch(self):
        record = {"verdict": "NO-GO-WITH-CONDITIONS", "unresolved_findings": []}
        (self.root / "REVIEW-RESULT.txt").write_text(
            "VERDICT: GO\nGATE_RECORD_JSON: " + json.dumps(record) + "\n", encoding="utf-8"
        )
        self.write_receipt("GO")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("disagrees", result.stdout.lower() + result.stderr.lower())

    def test_require_go_rejects_incomplete_reviewed_file_set(self):
        self.write_go_result()
        self.write_receipt("GO")
        receipt_path = self.root / "review-state.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["latest_review"]["reviewed_files"].pop(
            "evidence/search/session-search-output-contract-2026-10-04.md"
        )
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        result = self.run_gate("--require-go")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cover", result.stdout.lower() + result.stderr.lower())

    def test_cli_rejects_unknown_option(self):
        result = self.run_gate("--force")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage:", result.stdout + result.stderr)

    def test_structural_mode_rejects_symlink_outside_project(self):
        external_dir = tempfile.TemporaryDirectory()
        self.addCleanup(external_dir.cleanup)
        external = Path(external_dir.name) / "outside.md"
        external.write_text("outside artifact\\n", encoding="utf-8")
        target = self.root / "README.md"
        target.unlink()
        target.symlink_to(external)
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("README.md", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
