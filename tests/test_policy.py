import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tooling"))
from common import PolicyError, read_json_yaml, render_contents, project_config
from render import render
from validate import validate_sources, validate_generated


class PolicyKitTest(unittest.TestCase):
    def setUp(self):
        self.config = ROOT / "templates/project.yaml"

    def test_version_and_all_decisions_valid(self):
        self.assertEqual([], validate_sources(self.config))

    def test_render_contains_full_policy_and_profile(self):
        outputs = render_contents(self.config)
        self.assertEqual({"AGENTS.md", "CLAUDE.md", "ollama-system.txt"}, set(outputs))
        self.assertIn("Risk-based autonomy", outputs["AGENTS.md"])
        self.assertIn("Nuxt / Vue project profile", outputs["AGENTS.md"])
        self.assertIn("@AGENTS.md", outputs["CLAUDE.md"])
        self.assertNotIn("{{", outputs["AGENTS.md"])
        self.assertIn("harness", outputs["ollama-system.txt"])

    def test_render_drift_detection(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            render(self.config, folder)
            self.assertEqual([], validate_generated(self.config, folder))
            (folder / "AGENTS.md").write_text("tampered", encoding="utf-8")
            self.assertTrue(any("Drift" in e for e in validate_generated(self.config, folder)))

    def test_no_overwrite_of_user_files(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            (folder / "AGENTS.md").write_text("private user instructions", encoding="utf-8")
            for force in (False, True):
                with self.assertRaises(PolicyError):
                    render(self.config, folder, force=force)
            self.assertEqual("private user instructions", (folder / "AGENTS.md").read_text(encoding="utf-8"))

    def test_force_only_generated(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            render(self.config, folder)
            with self.assertRaises(PolicyError):
                render(self.config, folder)
            render(self.config, folder, force=True)
            self.assertEqual([], validate_generated(self.config, folder))

    def test_symlink_target_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            victim = folder / "do-not-touch"
            victim.write_text("sensitive")
            (folder / "AGENTS.md").symlink_to(victim)
            with self.assertRaises(PolicyError):
                render(self.config, folder, force=True)
            self.assertEqual("sensitive", victim.read_text())

    def test_invalid_profile_and_injection_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            config = Path(td) / "project.yaml"
            data = read_json_yaml(self.config)
            data["profile"] = "../../etc/passwd"
            config.write_text(json.dumps(data))
            with self.assertRaises(PolicyError):
                project_config(config)
            data["profile"] = "generic"
            data["project_name"] = "name\n# malicious"
            config.write_text(json.dumps(data))
            with self.assertRaises(PolicyError):
                project_config(config)

    def test_generic_profile_available(self):
        with tempfile.TemporaryDirectory() as td:
            config = Path(td) / "project.yaml"
            data = read_json_yaml(self.config)
            data["profile"] = "generic"
            config.write_text(json.dumps(data))
            self.assertIn("Generic project profile", render_contents(config)["AGENTS.md"])

    def test_registry_dependencies_resolve(self):
        skills = read_json_yaml(ROOT / "policy/skill-registry.yaml")["skills"]
        ids = {s["id"] for s in skills}
        self.assertIn("grilling", ids)
        for skill in skills:
            self.assertTrue(set(skill["depends_on"]).issubset(ids))

    def test_quality_runner_dry_run_cannot_pass(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            subprocess.run(["git", "-C", str(project), "-c", "user.email=test@example.invalid", "-c", "user.name=Test", "commit", "--allow-empty", "-qm", "init"], check=True)
            result = subprocess.run(["bash", str(ROOT / "templates/agent-verify.sh"), "--risk", "low", "--dry-run"], cwd=project, capture_output=True, text=True)
            self.assertEqual(3, result.returncode, result.stdout + result.stderr)
            self.assertIn("NOT VERIFIED", result.stdout)

    def test_quality_runner_blocks_missing_required_tests(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            subprocess.run(["git", "-C", str(project), "-c", "user.email=test@example.invalid", "-c", "user.name=Test", "commit", "--allow-empty", "-qm", "init"], check=True)
            result = subprocess.run(["bash", str(ROOT / "templates/agent-verify.sh"), "--risk", "medium"], cwd=project, capture_output=True, text=True)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("FAIL npm run test", result.stdout)


class QualityGateSecurityTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        subprocess.run(["git", "-C", str(self.project), "-c", "user.email=test@example.invalid", "-c", "user.name=Test", "commit", "--allow-empty", "-qm", "init"], check=True)

    def gate(self, *args):
        return subprocess.run(["bash", str(ROOT / "templates/agent-verify.sh"), *args], cwd=self.project, capture_output=True, text=True)

    def test_secret_in_tracked_diff_blocks_commit(self):
        file = self.project / "settings.txt"
        file.write_text("no credentials\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.project), "add", "settings.txt"], check=True)
        subprocess.run(["git", "-C", str(self.project), "-c", "user.email=test@example.invalid", "-c", "user.name=Test", "commit", "-qm", "baseline"], check=True)
        fake = "AKIA" + "Z" * 16
        file.write_text(f"credential={fake}\n", encoding="utf-8")
        result = self.gate("--risk", "low")
        self.assertEqual(1, result.returncode)
        self.assertIn("potential credential", result.stdout)
        self.assertNotIn(fake, result.stdout)

    def test_npm_script_requires_explicit_authorization(self):
        (self.project / "package.json").write_text(json.dumps({"scripts": {"test": "echo should-not-run"}}), encoding="utf-8")
        result = self.gate("--risk", "medium")
        self.assertEqual(1, result.returncode)
        self.assertIn("script execution not authorized", result.stdout)
        self.assertNotIn("should-not-run", result.stdout)

    def test_no_commit_or_git_write(self):
        before = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.project, text=True).strip()
        result = self.gate("--risk", "low")
        after = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.project, text=True).strip()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
