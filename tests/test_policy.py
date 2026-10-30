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

    def test_render_contains_only_universal_policy(self):
        outputs = render_contents(self.config)
        self.assertEqual({"AGENTS.md", "CLAUDE.md", "ollama-system.txt"}, set(outputs))
        self.assertIn("Risk-based autonomy", outputs["AGENTS.md"])
        self.assertIn("Universal Agentic Coding Policy", outputs["AGENTS.md"])
        self.assertNotIn("Applied project profile", outputs["AGENTS.md"])
        self.assertIn("Do not choose, infer, prescribe", outputs["AGENTS.md"])
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

    def test_framework_profiles_rejected_and_project_name_validated(self):
        with tempfile.TemporaryDirectory() as td:
            config = Path(td) / "project.yaml"
            data = read_json_yaml(self.config)
            data["profile"] = "any-tech-stack"
            config.write_text(json.dumps(data))
            with self.assertRaises(PolicyError):
                project_config(config)
            del data["profile"]
            data["project_name"] = "name\n# malicious"
            config.write_text(json.dumps(data))
            with self.assertRaises(PolicyError):
                project_config(config)

    def test_render_is_same_independent_of_project_stack(self):
        with tempfile.TemporaryDirectory() as td:
            config = Path(td) / "project.yaml"
            data = read_json_yaml(self.config)
            config.write_text(json.dumps(data))
            original = render_contents(config)["AGENTS.md"]
            (Path(td) / "package.json").write_text('{"dependencies":{"not-a-framework":"1"}}')
            (Path(td) / "application.config").write_text('arbitrary stack')
            self.assertEqual(original, render_contents(config)["AGENTS.md"])

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
            self.assertIn("required test check UNAVAILABLE", result.stdout)


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
        self.assertIn("potential sensitive material", result.stdout)
        self.assertNotIn(fake, result.stdout)

    def test_project_checks_require_explicit_authorization(self):
        (self.project / '.agentic').mkdir()
        (self.project / '.agentic/checks.json').write_text(json.dumps({"schema": 1, "checks": {"test": [sys.executable, "-c", "print('should-not-run')"]}}), encoding='utf-8')
        result = self.gate("--risk", "medium")
        self.assertEqual(1, result.returncode)
        self.assertIn("command execution not authorized", result.stdout)
        self.assertNotIn("should-not-run", result.stdout)
        allowed = self.gate("--risk", "medium", "--allow-checks")
        self.assertEqual(0, allowed.returncode, allowed.stdout + allowed.stderr)
        self.assertIn("PASS test", allowed.stdout)

    def test_arbitrary_package_manager_is_not_discovered_or_invoked(self):
        (self.project / 'package.json').write_text(json.dumps({"scripts": {"test": "exit 1"}}))
        result = self.gate("--risk", "low")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("npm", result.stdout)

    def test_no_commit_or_git_write(self):
        before = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.project, text=True).strip()
        result = self.gate("--risk", "low")
        after = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.project, text=True).strip()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()

class OneCommandInstallerTest(unittest.TestCase):
    """Installer integration tests: never overwrite user-owned sections."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / 'demo'
        self.project.mkdir()
        sys.path.insert(0, str(ROOT / 'tooling'))
        from install import install, check_existing
        self.install, self.check = install, check_existing

    def test_existing_files_are_preserved_and_idempotent(self):
        (self.project / 'AGENTS.md').write_text('# My own rules\nThis stays.\n')
        (self.project / 'CLAUDE.md').write_text('# Claude details\nMore local rules.\n')
        self.install(self.project)
        agents = (self.project / 'AGENTS.md').read_text()
        self.assertTrue(agents.startswith('# My own rules\nThis stays.'))
        self.assertIn('Universal Agentic Coding Policy', agents)
        self.assertTrue((self.project / 'CLAUDE.md').read_text().startswith('# Claude details'))
        self.assertEqual([], self.check(self.project))
        self.install(self.project)
        self.assertEqual(agents, (self.project / 'AGENTS.md').read_text())

    def test_modified_managed_block_refused_but_user_additions_allowed(self):
        from common import PolicyError
        self.install(self.project)
        agents = self.project / 'AGENTS.md'
        agents.write_text(agents.read_text().replace('Risk-based autonomy', 'untrusted change'))
        with self.assertRaises(PolicyError):
            self.install(self.project)
        self.assertTrue(self.check(self.project))
        # Reinstallation does not repair tampering silently.
        self.assertIn('untrusted change', agents.read_text())

    def test_custom_user_content_outside_block_survives_upgrade(self):
        self.install(self.project)
        agents = self.project / 'AGENTS.md'
        agents.write_text('IMPORTANT LOCAL RULE\n\n' + agents.read_text())
        self.install(self.project)
        self.assertTrue(agents.read_text().startswith('IMPORTANT LOCAL RULE'))
        self.assertEqual([], self.check(self.project))

    def test_installation_does_not_inspect_or_select_framework(self):
        (self.project / 'package.json').write_text('{"dependencies":{"random-framework":"^4"}}')
        (self.project / 'app.config').write_text('database: custom')
        self.install(self.project)
        cfg = json.loads((self.project / '.agentic/project.yaml').read_text())
        self.assertEqual(2, cfg['schema'])
        self.assertNotIn('profile', cfg)
        self.assertNotIn('random-framework', (self.project / 'AGENTS.md').read_text())

    def test_migrate_schema1_without_retaining_framework_profile(self):
        self.install(self.project)
        cfg_path = self.project / '.agentic/project.yaml'
        cfg = json.loads(cfg_path.read_text())
        cfg['schema'] = 1
        cfg['profile'] = 'previous-framework-profile'
        cfg_path.write_text(json.dumps(cfg))
        self.install(self.project)
        migrated = json.loads(cfg_path.read_text())
        self.assertEqual(2, migrated['schema'])
        self.assertNotIn('profile', migrated)
        self.assertEqual([], self.check(self.project))

    def test_new_project_and_dry_run(self):
        folder = self.project / 'brand-new'
        self.assertFalse(folder.exists())
        output = self.install(folder, new=True, dry_run=True)
        self.assertIn('DRY RUN', output[0])
        self.assertFalse(folder.exists())
        self.install(folder, new=True)
        self.assertTrue((folder / 'AGENTS.md').is_file())
        self.assertEqual([], self.check(folder))

    def test_existing_unowned_quality_script_is_not_overwritten(self):
        (self.project / 'scripts').mkdir()
        gate = self.project / 'scripts/agent-verify.sh'
        gate.write_text('# user script')
        self.install(self.project)
        self.assertEqual('# user script', gate.read_text())
        self.assertTrue((self.project / '.agentic/agent-verify.sh').exists())

    def test_symlink_file_and_directory_are_refused(self):
        from common import PolicyError
        target = self.project / 'important'
        target.write_text('untouched')
        (self.project / 'AGENTS.md').symlink_to(target)
        with self.assertRaises(PolicyError):
            self.install(self.project)
        self.assertEqual('untouched', target.read_text())

    def test_legacy_generated_file_rejected(self):
        from common import PolicyError
        (self.project / 'AGENTS.md').write_text('<!-- Generated by Portable Agentic Policy Kit -->\n')
        with self.assertRaises(PolicyError):
            self.install(self.project)

    def test_installed_gate_and_ollama_changes_detected(self):
        self.install(self.project)
        gate = self.project / '.agentic/agent-verify.sh'
        gate.write_text(gate.read_text() + '# changed by user\n')
        self.assertTrue(any('.agentic/agent-verify.sh' in e for e in self.check(self.project)))

    def test_cli_checks_correct_status(self):
        script = ROOT / 'tooling/install.py'
        first = subprocess.run([sys.executable, str(script), '--project', str(self.project)], capture_output=True, text=True)
        self.assertEqual(0, first.returncode, first.stderr)
        again = subprocess.run([sys.executable, str(script), '--project', str(self.project), '--check'], capture_output=True, text=True)
        self.assertEqual(0, again.returncode, again.stderr)
