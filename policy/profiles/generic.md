# Generic project profile

- Discover the existing framework, repository conventions, lockfile, test runners and CI checks before coding. Preserve the existing stack; do not migrate dependencies as part of unrelated work.
- Reuse established project patterns and standard-library functionality. Avoid speculative abstractions and dependencies.
- Derive exact commands from the repository. Record missing verification capabilities as UNAVAILABLE; do not invent test commands.
- For API changes, examine consumers, contracts, backward compatibility, error states and authentication implications.
- Keep changes small, accessible and documented where the behavior is non-obvious.
