# Ollama agent-harness integration contract

Ollama's chat API/model is **not** an autonomous coding runtime. `SYSTEM` text by itself grants no safety, filesystem or Git protection.

To claim compatibility with this policy, the **harness** MUST provide or explicitly disable the following capabilities:

| Capability | Required harness behavior |
|---|---|
| Input and policy loading | Load the complete generated `ollama-system.txt` as system/developer instructions according to model API; do not rely on implicit file discovery. |
| File boundaries | Restrict writes to approved workspace paths, protect `.env`, key material and unrelated files. |
| Shell execution | Require an explicit tool allowlist, appropriate sandbox and independent ASK/DENY checks. |
| Network and billing | Block unsolicited external requests, paid provider substitution, auto-installs and credential export. |
| Git | Read-only Git by default; permit atomic local commits only via an authorized flow after quality gates. No push/merge without approval. |
| Approval | Enforce the current scope and high-risk approvals outside the model. |
| Retry state | Persist per-root-cause and per-task counters in reliable external state across agent turns and sessions. |
| Testing | Call a real quality-gate runner and preserve PASS/FAIL/SKIPPED/UNAVAILABLE evidence. |
| Agent delegation | If absent, execute sequentially; do not describe roleplay as true sub-agent isolation. |
| Observability | Report actual tools invoked, denials, tests and commit IDs without leaking secrets. |

**Conformance status:** This kit supplies the contract and prompts, **not** a pre-built Ollama harness or hard permission enforcement. Before autonomous writes, validate each capability on the chosen harness. Deny high-risk operations if unmet.

Relevant documentation: https://docs.ollama.com/capabilities/tool-calling and https://docs.ollama.com/modelfile
