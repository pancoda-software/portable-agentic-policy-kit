# Portable Agentic Policy Kit — Markdown Edition v2.0.0

**Kopieren statt installieren.** Das Kit besteht ausschließlich aus Markdown-Dateien und legt fest, **wie Coding-Agenten arbeiten**, nicht welche Programmiersprache, welches Framework, welches Modell oder welche Architektur ein Projekt verwenden muss.

## In 30 Sekunden verwenden

Kopiere aus diesem Repository in die Wurzel deines Zielprojekts:

```text
dein-projekt/
├── AGENTS.md     # Vollständige Agentic-Coding-Policy
├── CLAUDE.md     # Enthält nur: @AGENTS.md
└── ...           # Deine unveränderten Projektdateien
```

**Bestehendes Projekt:** Dateien kopieren, ohne bestehende gleichnamige Dateien zu überschreiben. Sind `AGENTS.md` oder `CLAUDE.md` schon vorhanden, die Regeln **manuell zusammenführen** und widersprüchliche Instruktionen prüfen. Bei Claude Code den Import `@AGENTS.md` nur eintragen, wenn die installierte Version diese Syntax unterstützt.

**Neues Projekt:** Verzeichnis anlegen, beide Markdown-Dateien hineinkopieren; fertig. Keine Anwendung wird erzeugt, kein Paket installiert.

Optional mit bereits lokal geklontem Policy-Kit (bei bereits vorhandenen Zieldateien werden diese von `cp -n` nicht ersetzt):

```bash
cd /pfad/zu/deinem-projekt
cp -n /pfad/zum/portable-agentic-policy-kit/AGENTS.md .
cp -n /pfad/zum/portable-agentic-policy-kit/CLAUDE.md .
```

**Das sind Kopiervorgänge, keine Installation.** Für das lokale Klonen des derzeit privaten GitHub-Repositories ist GitHub-Zugriff erforderlich; alternativ die Dateien in GitHub einzeln herunterladen.

## Wo welche Regeln stehen

| Datei | Aufgabe |
|---|---|
| [`AGENTS.md`](AGENTS.md) | **Alle universellen Regeln:** Planung und Go, Delegation, Model-Routing, Skills, Qualitätsprüfungen, Recovery, lokale Commits und Sicherheit |
| [`CLAUDE.md`](CLAUDE.md) | Schlanker Claude-Code-Einstieg: `@AGENTS.md` |
| [`docs/`](docs/INDEX.md) | Erklärungen, Mermaid-Flussdiagramme und konkrete Beispiele |
| [`SECURITY.md`](SECURITY.md) | Grenzen von Prompt-Policies und sichere Runtime-Einbindung |

**Codex** liest `AGENTS.md` entsprechend seiner Projektanweisungs-Konventionen. **Claude Code** kann `AGENTS.md` über `@AGENTS.md` aus `CLAUDE.md` importieren; prüfe die tatsächlich geladenen Instruktionen. **Ollama** ist ein Inferenz-Backend, kein Agent: Der verwendete Harness muss den Inhalt von `AGENTS.md` explizit als System-/Agent-Instruktionen laden.

## Was die Policy festlegt

- Strategische Freigabe vor nicht-trivialer Implementierung; danach risikobasierte Autonomie im Scope.
- Adaptive Delegation und fähigkeitsbasiertes, providerunabhängiges Modell-Routing.
- Pflicht-, bevorzugte und optionale Skills abhängig von der Aufgabe, ohne Installationspflicht.
- Risikoangepasste Quality Gates und lokale atomare Conventional Commits; Push/Merge nur mit Freigabe.
- Höchstens zwei lokale plus ein eskalierter Fix pro Ursache, standardmäßig sechs Fixes insgesamt pro Task.
- Layered Security: `ALLOW`, `ASK`, `DENY`; echte technische Rechte kommen **nicht** aus Markdown.

## Doku mit Diagrammen

Beginne bei [Architektur](docs/01-architektur.md) und [Workflows](docs/02-workflows.md). Die [Entscheidungsakte](docs/06-session-entscheidungen.md) enthält die D-01-bis-D-11-Beschlüsse des Grill-me-Interviews. [Manuelles Kopieren](docs/09-dateien-kopieren.md) erläutert die drei Laufzeiten und Updates.

## Grenzen

Ein Markdown-Dokument kann weder Agenten-Toolrechte erzwingen noch Modellwechsel oder persistente Retry-Zähler garantieren. Runtime-Permissions, Sandbox, Git-Rechte und Testbefehle müssen im jeweiligen Projekt bzw. Harness existieren. **Keine versteckten Tools, Installationen oder automatischen Änderungen.**

## Weiterentwicklung

Eine Policy-Änderung direkt in `AGENTS.md` vornehmen, dann Dokumentation und Beispiele auf Widersprüche prüfen und mit einem normalen Git-Commit versionieren. Vor einem Update in Zielprojekten die Änderungen per Diff vergleichen und bestehende Regeln bewusst übernehmen. Siehe [CONTRIBUTING.md](CONTRIBUTING.md).

**Das Repository bleibt privat**, bis der Inhalt *und die Git-Historie* auf personenbezogene Angaben geprüft und eine separate Public-Freigabe erteilt wurde. Hinweise: [Veröffentlichungscheckliste](docs/08-publication-checklist.md).
