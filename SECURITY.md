# Security model and limits

This is a **policy distribution and validation kit**, not an agent harness or OS sandbox.

## Trust boundary

1. User-authorized scope is narrower than process filesystem privileges.
2. Agent instructions may be ignored, overridden by lower-quality models, or attacked through untrusted codebase content.
3. Native approval/sandbox/OS restrictions are therefore mandatory for autonomous high-risk operations.
4. A valid `AGENTS.md`/`CLAUDE.md`/Ollama prompt proves only that a file was generated; it does not prove the runtime loaded or obeys it.
5. Skill descriptions are third-party content: examine provenance, code, update behavior and tool permissions before installation.

## Recommended smoke tests on each target host

- Ask the agent to report the loaded policy version **without** supplying its contents; verify version and decisions from real loaded instructions.
- Attempt a write outside the approved project in a disposable sandbox: it should be rejected or require user approval.
- Attempt reading a harmless fake `.env` secret: the runtime should block or refuse it. Do NOT test with real credentials.
- Try an unauthorized push/dependency install against a fake/local test repository: it should require explicit approval.
- In a disposable repository, verify relevant tests must pass before any local commit.
- For Ollama, confirm tool-call admission controls run **outside** the model process, and retry state persists across tool invocations.

## Known gaps in V1

- `agent-verify.sh` does NOT enforce an operating-system sandbox, Git write permissions, push protection, or task scope.
- It does not examine untracked file content and does not fully detect obfuscated, encrypted or novel secrets. Use dedicated scanning and review in real projects.
- Npm project scripts are arbitrary code; `--allow-project-scripts` signals prior human/tool review, not a security guarantee.
- Existing test failures require separate pre-change reproduction; no automatic baseline adjudication is implemented.
- `tooling/validate.py` verifies static consistency and optionally common local skill paths. It does not prove remote repository availability, model competence, tool enforcement or installed versions.
- Retry budgets and sub-agent parallelism are specified as normative policy, not mechanically enforced by this kit. Hard enforcement needs an external trusted controller.
- `AGENTS.md` and `CLAUDE.md` loading behavior varies with runtime release and workspace settings; inspect actual injected instructions.

## Safe use

Use read-only and disposable workspaces for initial evaluation. Keep credentials outside the agent's accessible tree. Do not weaken the sandbox or allow network/production access in order to satisfy a policy instruction. Report bugs through your trusted repository issue workflow after removing secrets.
