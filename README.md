# Portable Agentic Policy Kit 1.0.0

**Portables, versionierbares Agentic-Coding-Regelwerk** für Claude Desktop/Claude Code, Codex und Ollama **mit geeignetem Agent-Harness**. Die universelle Policy beschreibt Freigaben, Modelle, Skills, Sub-Agenten, Git, Sicherheit, Qualität und Fehlerbehandlung. Sie ist nicht selbst eine Sandbox oder ein automatischer Modell-Router.

## Dokumentation und Architekturdiagramme

Ein ausführliches, durch GitHub gerendertes deutschsprachiges Handbuch mit Mermaid-Diagrammen, den Entscheidungen unserer Grill-me-Session sowie Praxisbeispielen findest du unter **[docs/INDEX.md](docs/INDEX.md)**.

- [Architektur / Drei-Ebenen-Modell](docs/01-architektur.md)
- [End-to-End-Flows / Mermaid-Diagramme](docs/02-workflows.md)
- [Claude Code, Codex und Ollama einrichten](docs/03-runtime-integration.md)
- [Praxisbeispiele: Nuxt, Python, Ollama](docs/04-praxisbeispiele.md)
- [Sicherheit und Quality Gates](docs/05-sicherheit-qualitaet.md)
- [Alle Grill-me-Entscheidungen D-01 bis D-11](docs/06-session-entscheidungen.md)
- [FAQ und Troubleshooting](docs/07-troubleshooting.md)

Für Änderungen siehe [CONTRIBUTING.md](CONTRIBUTING.md), für Versionshistorie [CHANGELOG.md](CHANGELOG.md).

## Inhalt

| Datei | Zweck |
|---|---|
| `policy/core.md` | Universelle Regeln D-01–D-11 (kanonisch) |
| `policy/decisions.yaml` | Entscheidungen und sichere Default-Grenzen (JSON-kompatibles YAML) |
| `policy/skill-registry.yaml` | Skill-Prioritäten, Abhängigkeiten, Quellen (kein Installationsnachweis) |
| `policy/profiles/{generic,nuxt-vue}.md` | Projektspezifische Tech-Stack-Regeln |
| `adapters/claude/CLAUDE.md.template` | Minimaler Claude-Einstieg mit `@AGENTS.md` |
| `adapters/codex/AGENTS.md.template` | Vollständige, selbständige `AGENTS.md` |
| `adapters/ollama/*` | System-Prompt-Vorlage und Harness-Sicherheitsvertrag |
| `tooling/{render,validate}.py` | Deterministischer Renderer und Validator ohne externe Python-Pakete |
| `templates/agent-verify.sh` | Read-only Git-/Secret-/npm-Qualitätsprüfungen |
| `tests/` | Automatisierte Unit- und negative Sicherheitstests |
| `examples/nuxt-project/` | Vorgefertigte, generierte Beispiel-Instructions |

## Voraussetzungen

- Python >=3.10 (Standardbibliothek) für Renderer, Validator und Runner.
- Git für projektbezogene Diff-Prüfungen.
- Für Nuxt optional Node.js/npm **nur** dann, wenn die vorhandenen Projekt-Checks per `npm run` ausgeführt werden sollen. Nicht automatisch installieren.
- Für die tatsächliche Agentenarbeit einen kompatiblen Claude-Code-, Codex- oder Ollama-Agent-Harness.

## Schnellstart (keine automatischen Änderungen am Home-Verzeichnis)

```bash
# 1. Im entpackten Kit
python3 tooling/validate.py
python3 -m unittest discover -s tests -v

# 2. Beispiel-Konfiguration anpassen (JSON-kompatibles YAML)
# templates/project.yaml: project_name, profile (generic|nuxt-vue), output_language (de|en)

# 3. In einen NEUEN Ausgabeordner rendern
python3 tooling/render.py --config templates/project.yaml --out ./dist/my-project
python3 tooling/validate.py --config templates/project.yaml --generated ./dist/my-project

# 4. Die generierten AGENTS.md und CLAUDE.md nach Review in die Projektwurzel kopieren;
# bei Ollama ollama-system.txt an den Harness übergeben (keine automatische System-Installation).
```

`render.py` überschreibt keine vorhandenen Dateien. `--force` ersetzt **nur** Dateien mit dem Generator-Marker; Symlink-Ziele werden abgelehnt. Es werden keine Prozesse im Hintergrund gestartet, keine Skills installiert, keine API-Schlüssel gelesen und keine Netzwerkanfragen gesendet.

## Runtime-Einbindung

### Claude Code / Claude Desktop Code-Tab

1. `AGENTS.md` und `CLAUDE.md` aus dem Ausgabeordner in die Projektwurzel kopieren, nachdem bestehende Dateien geprüft wurden.
2. `CLAUDE.md` importiert `@AGENTS.md`. In neueren Versionen ist direkte `AGENTS.md`-Unterstützung möglich. Prüfe mit `/memory` oder einer Kontrollfrage, dass die **gemeinsame Policy tatsächlich geladen ist**. Bei einer inkompatiblen Installation explizit die generierten Instruktionen zusammenführen – nie stumm auf Funktion hoffen.
3. Tool-Allow-/Deny-Regeln, Sandbox, Hooks und Sub-Agenten im *tatsächlich verwendeten* Claude Code konfigurieren. Die Markdown-Dateien gewähren keine Toolrechte.
4. Lokale Commits nach bestandenen Quality Gates sind Zielverhalten, keine Erlaubnis für Sandbox-Bypass.

### Codex

1. Generierte `AGENTS.md` in die Projektwurzel legen (keine Claude-spezifische Datei erforderlich).
2. Sandbox und Approval Policy separat aktivieren. Beispielsweise in einer **bewusst gewählten** Codex-Konfiguration:

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"
```

3. Schreibrechte für `.git` können im Workspace-Modus eingeschränkt sein. Für autonome lokale Commits eine gezielt autorisierte Ausführung vorsehen; nicht pauschal die Sandbox abschalten.

### Ollama

- `ollama-system.txt` ist die generierte Modellinstruktion. Ein reines Ollama-Modell führt noch keine sicheren Workspace-Operationen aus.
- Der Agent-Harness muss alle Anforderungen in `adapters/ollama/harness-contract.md` erfüllen oder nicht unterstützte Schreiboperationen deaktivieren.
- Provider- oder Cloud-Wechsel sowie Tool-Genehmigungen dürfen nicht allein durch Modelltext gesteuert werden.
- `ollama-system.txt` ist **kein** lauffertiges Modelfile. Falls dein Harness einen Ollama-Modelfile verlangt, muss er den SYSTEM-Text korrekt übernehmen und `FROM` sowie alle Modellparameter separat konfigurieren.

## Skills: Lazy Discovery und keine automatische Installation

Die `policy/skill-registry.yaml` enthält gewünschte und historisch benannte Skills, **keinen verifizierten Installationsstatus**. Verfügbare Skill-Verzeichnisse lassen sich informativ prüfen:

```bash
python3 tooling/validate.py --check-skills --project /pfad/zum/projekt
```

Ein fehlender REQUIRED-Skill blockiert nur die betroffene Operation; PREFERRED erhält einen offengelegten Fallback, OPTIONAL wird übersprungen. **Nicht blind alle Skills ausführen.** Upstream-Quellen (insbesondere früheres `graft` und einzelne `refactor`-Skills) vor Installation prüfen. Offizieller `skills`-CLI-Befehl ist `npx skills add owner/repo --skill name`, mit agent-spezifischen Flags nach Dokumentation; diese Vorlage führt ihn niemals automatisch aus.

## Quality Gates für ein Zielprojekt

`templates/agent-verify.sh` nach `scripts/agent-verify.sh` kopieren und aus der **Git-Projektwurzel** aufrufen:

```bash
bash scripts/agent-verify.sh --risk low
bash scripts/agent-verify.sh --risk medium --dry-run
# Erst package.json/scripts und ihre Lifecycle-Effekte prüfen; dann explizit erlauben:
bash scripts/agent-verify.sh --risk medium --allow-project-scripts
bash scripts/agent-verify.sh --risk high --allow-project-scripts --timeout 180
```

- LOW: `git diff --check`, Staging-Check und heuristischer Secret-Scan, optional vorhandene npm-Checks.
- MEDIUM: zusätzlich vorhandene anwendbare Lint-/Typechecks und zwingend ein konfigurierter `test`-Script.
- HIGH: zusätzlich `build` erforderlich. Für andere Frameworks Runner/Checks projektspezifisch anpassen.
- Ohne `--allow-project-scripts` werden npm-Skripte nicht gestartet. DRY-RUN liefert Exitcode **3** (kein bestandenes Gate); fehlende erforderliche Checks Exitcode **1**. Ein nicht initialisiertes Repo oder fehlender Git-HEAD liefert **2**.
- Das Skript scannt nur **getrackte Diffs**, keine neuen untracked Dateien, verwendet heuristische Secret-Erkennung und kann nicht beweisen, dass alle Regressionen ausgeschlossen sind. Es ersetzt weder dedizierte Security-Scanner noch einen Baseline-Vergleich, Code-Review, Scope-Check oder ein umfassendes CI.
- Wenn der bestehende Teststatus fehlschlägt, muss die Ursache separat gegen eine reproduzierbare Baseline geprüft werden. Keine automatische Ausnahme durch dieses Skript.

## Sicherheits- und Freigabe-Defaults

- Initiales `Go` pro Implementierungsscope; keine Unteraufgaben-Mikrofreigabe innerhalb des Scopes.
- Maximal zwei parallele schreibende Agenten; nur isoliert bei überlappenden Schreibaufgaben.
- Zwei lokale Fixes pro Root Cause, danach maximal ein eskalierter Fix; höchstens sechs Fix-Versuche pro Task.
- Lokale Conventional Commits nach relevanten Quality Gates; Push, Merge, destructive Git, Netzwerkausweitung, Dependency-Installation und Produktionsaktionen benötigen gesonderte Freigabe.
- Kein Zugriff auf Secrets, kein Sandbox-Bypass, kein stillschweigender Cloud-Wechsel oder kostenpflichtige Zusatznutzung.
- Die Limits werden **in Markdown formuliert**. Für verlässliche Durchsetzung über mehrere Agenten/Sessions hinweg wird ein äußerer Controller benötigt.

## Policy-Änderungen und Drift

1. `policy/core.md`, Profile, Registry oder Templates editieren.
2. `python3 tooling/validate.py` und Unit-Tests ausführen.
3. Ausgaben erneut generieren (`--force` nur für vom Kit erzeugte Dateien).
4. `python3 tooling/validate.py --generated <output>` prüft exakt auf Source-/Content-Drift.
5. Im Ziel-Harness das tatsächliche Laden der Instructions und die technischen Sicherheitsgrenzen testen.

`decisions.yaml` und `skill-registry.yaml` sind bewusst **JSON als YAML-1.2-Untermenge**. Damit werden keine Parser-Abhängigkeiten benötigt. Nicht beliebige YAML-Syntax verwenden, sonst meldet der Validator einen Parse-Fehler.

## Referenzdokumentation

- Claude Code Instructions: https://code.claude.com/docs/en/memory
- Claude Code Permissions: https://code.claude.com/docs/en/permissions
- Codex AGENTS.md: https://learn.chatgpt.com/docs/agent-configuration/agents-md
- Codex-Konfiguration: https://learn.chatgpt.com/docs/config-file/config-reference
- Ollama Tool Calling: https://docs.ollama.com/capabilities/tool-calling
- Ollama Modelfiles: https://docs.ollama.com/modelfile
- Skills CLI: https://www.skills.sh/docs/cli

**Status:** Kit-Generator und statische Sicherheitsprüfungen sind ausführbar; reale Claude-Code-, Codex- oder Ollama-Deployment-Tests müssen auf dem jeweiligen Zielsystem stattfinden.
