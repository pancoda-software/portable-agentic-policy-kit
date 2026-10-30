# Changelog

## [1.2.0] – 2026-10-30

- **Technologie- und frameworkunabhängiger Kern:** keinerlei Stack-Erkennung, Präferenz, Projektprofil oder projektspezifischer Build-Befehl mehr.
- Projektkonfiguration Schema 2 enthält nur Identifikation und Antwortsprache; Migration aus bestehenden Schema-1-Installationen.
- Rendered Entry-Points enthalten ausschließlich die Core-Policy; eigene Projektregeln bleiben außerhalb der verwalteten Blöcke.
- Universeller Quality-Gate-Helper mit expliziter, benutzerdefinierter Check-Liste statt Annahmen über Paketmanager.
- Vollständig überarbeitete Dokumentation mit stackneutralen Diagrammen und Beispielen.


## [1.1.0] – 2026-10-30

- Ein-Befehl-Installation für bestehende Projekte und neue Projektordner.
- Frühere optionale Projekttyp-Erkennung und sichere, wiederholbare Updates.
- Bestehende `AGENTS.md` und `CLAUDE.md` bleiben außerhalb markierter Blöcke unverändert.
- Drift-Schutz per Installationsstatus, Symlink-Schutz und Dry-Run/Check.
- Dokumentation zum Bootstrap und zur Privatsphäre vor Veröffentlichung.

## [1.0.0] – 2026-10-29

- Initiales Portable Agentic Policy Kit mit Universal Core, D-01 bis D-11 und D-04a Multi-Provider.
- Generator/Validator, anfängliche Projekt-Profile (in v1.2.0 entfernt), Claude/Codex/Ollama-Adapter.
- Skill-Registry, Quality-Gate-Vorlage, Unit-/Sicherheitstests und SHA-256-Dateimanifest.
- Ausführliches Handbuch mit Mermaid-Diagrammen, Praxisbeispielen, Runtime-Anleitungen, Sicherheitsmodell und Interview-Entscheidungen.
- CI-Vorlage zur automatischen Prüfung der kanonischen Policy.
