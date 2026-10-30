# Portable Agentic Policy Kit 1.2.0

**Einheitliche, framework- und sprachunabhängige Agentic-Coding-Guidelines** für Claude Code, Codex und Ollama mit geeignetem Agent-Harness. Das Kit regelt **wie Agenten arbeiten**, nicht **mit welchen Technologien ein Projekt umgesetzt wird**.

Es enthält keine Framework-Erkennung, keine Stack-Präferenz und keine vorgegebenen Test-/Build-Tools. Bestehende Projekte behalten ihre eigenen Architektur- und Technologieentscheidungen. Projektregeln werden außerhalb der verwalteten Policy-Blöcke gepflegt.

## Installieren

**Bestehendes Projekt** (lokal heruntergeladenes Kit):

```bash
python3 /pfad/zum/kit/tooling/install.py --project .
```

**Neuer, leerer Projektordner nur mit Agentic-Guidelines:**

```bash
python3 /pfad/zum/kit/tooling/install.py --new meine-app
```

**Privates GitHub-Repository:** Nach `gh auth login`, aus dem Zielprojektordner:

```bash
(tmp=$(mktemp -d); trap 'rm -rf -- "$tmp"' EXIT; gh repo clone pancoda-software/portable-agentic-policy-kit "$tmp/kit" -- --depth 1 --quiet && python3 "$tmp/kit/tooling/install.py" --project .)
```

**Nach öffentlicher Freigabe und Veröffentlichung von v1.2.0:**

```bash
curl -fsSL https://raw.githubusercontent.com/pancoda-software/portable-agentic-policy-kit/main/bootstrap.sh | bash -s -- --project .
```

Der öffentliche Remote-Befehl funktioniert **erst**, wenn das Repository tatsächlich öffentlich ist und v1.2.0 auf `main` liegt. Das ungeprüfte Ausführen von Remote-Skripten ist riskant; Repository klonen und `install.py` lokal prüfen ist die sicherere Variante.

**Updates:** denselben Installationsbefehl erneut ausführen. Das Kit bewahrt Inhalte außerhalb verwalteter Blöcke und stoppt bei manuell veränderten verwalteten Inhalten.

## Was das Kit tut – und nicht tut

| Das Kit regelt | Das Kit regelt **nicht** |
|---|---|
| Scope-Freigaben und Risk-Based Autonomy | Framework- oder Sprachauswahl |
| Modellprofile LIGHT/BALANCED/DEEP | Modellanbieter oder Modellversion |
| Adaptive Sub-Agent-Delegation | Pflicht zur Installation eines Orchestrators |
| Skill-Tiers und Fallbacks | Installation bestimmter Skills/Packages |
| Retry-Budgets und Failure-Reports | Testframework, Build- oder Paketmanager |
| Quality Gates und lokale Commits | Datenbanken, State-Management oder UI-Komponenten |
| Security, Approval und Sandbox-Prinzipien | Sandbox-Einrichtung durch Markdown allein |

**Modellprofile sind keine Projekt-/Technologieprofile.** `CRITICAL` bezeichnet Risiko und verlangt zusätzliche Verifikation, nicht automatisch ein anderes Modell.

## Installationsergebnis

```text
projekt/
├── AGENTS.md                    # Policy im gekennzeichneten Block
├── CLAUDE.md                    # Claude-Einstieg mit @AGENTS.md
└── .agentic/
    ├── project.yaml             # Projektkennung + Antwortsprache
    ├── policy-install.json      # Update-/Drift-Status
    ├── agent-verify.sh          # Frameworkneutraler Zusatzcheck
    └── ollama-system.txt        # Instruktionen für Agent-Harness
```

Andere Projektdateien werden nicht angefasst; es erfolgt kein Git-Commit, kein Push, kein automatisches Scaffolding und keine Dependency-Installation.

## Verifizieren

```bash
python3 tooling/validate.py
python3 -m unittest discover -s tests -v
python3 tooling/install.py --project /pfad/zum/projekt --check
bash /pfad/zum/projekt/.agentic/agent-verify.sh --risk low
```

Die Quality-Gate-Vorlage prüft Git-Diffs und heuristische Secret-Muster ohne bestimmte Build-Tools. Bei MEDIUM/HIGH verlangt sie einen projektspezifisch definierten `test`-Check (ohne irgendein Framework vorzugeben). Beispiel für `.agentic/checks.json`:

```json
{
  "schema": 1,
  "checks": {
    "test": ["dein-test-befehl", "dein-argument"],
    "lint": ["dein-lint-befehl"]
  }
}
```

Nach **vorheriger Prüfung** der Befehle:

```bash
bash .agentic/agent-verify.sh --risk medium --allow-checks
```

Ohne explizite Freigabe werden solche Projektbefehle nicht gestartet. Ein `--dry-run` ist ausdrücklich kein erfolgreicher Quality-Gate-Nachweis. Der Helper ist ergänzend; er kann keine vollständigen Regressions- oder Sicherheitsgarantien geben.

## Migration von 1.1.0

Der Installer erkennt zuvor installierte Konfigurationen mit Schema 1 und entfernt deren fest codierte Technologieprofile bei der Migration zu Schema 2. Dabei validiert er weiterhin die vorhandenen verwalteten Policy-Blöcke und verweigert unerkannte Änderungen. **Eigene Projektregeln außerhalb der Blöcke bleiben bewusst unangetastet**, auch wenn sie technologiespezifisch sind; sie gehören dem jeweiligen Projekt, nicht dem Kit.

## Struktur und Dokumentation

- [`policy/core.md`](policy/core.md): einzige universelle Policy-Quelle, Entscheidungen D-01 bis D-11.
- [`policy/decisions.yaml`](policy/decisions.yaml): sichere Grenzwerte und Entscheidungsregister.
- [`policy/skill-registry.yaml`](policy/skill-registry.yaml): optionale Skill-Discovery-Hinweise, keine Installationspflicht.
- [`adapters/`](adapters): minimaler Runtime-Adapter für Claude Code, Codex und Ollama-Agent-Harnesses.
- [`tooling/install.py`](tooling/install.py), [`render.py`](tooling/render.py), [`validate.py`](tooling/validate.py): dependencyfreie Python-Werkzeuge.
- [`templates/agent-verify.sh`](templates/agent-verify.sh): frameworkneutraler, rein lokaler Zusatzcheck.
- [`docs/INDEX.md`](docs/INDEX.md): ausführliches deutsches Handbuch mit Mermaid-Flussdiagrammen.
- [`docs/04-praxisbeispiele.md`](docs/04-praxisbeispiele.md): Beispiele, die auf alle Projektstacks übertragbar sind.
- [`SECURITY.md`](SECURITY.md): Sicherheitsgrenzen und Einschränkungen.

**Voraussetzungen:** Python 3.10+ für Installation/Validierung; Git für den optionalen Quality-Gate-Helper; der gewünschte Agent-Harness für tatsächliche Agentenaktionen. Keine externen Python-Packages.

Die Regeln sind deklarativ: Eine tatsächliche Sandbox, Freigaben, persistente Retry-Zähler und Berechtigungen muss die jeweilige Laufzeit technisch bereitstellen. Projektanweisungen dürfen globale Sicherheitsgrenzen nicht stillschweigend aufheben.
