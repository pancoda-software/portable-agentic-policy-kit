# Contributing – Markdown-first

Änderungen an dieser Policy sollten verständlich, rückwärtskompatibel und **frameworkunabhängig** bleiben.

1. **`AGENTS.md`** ist die einzige normative Quelle. Keine zweite vollständige Kopie der gleichen Regeln pflegen.
2. `CLAUDE.md` bleibt ein knapper Import-Einstieg, soweit der verwendete Claude-Code-Client ihn unterstützt.
3. Änderungen an Freigaben, Git, Security, Skill-Pflichten, Retry-Limits und Modell-Routing auf Auswirkungen prüfen.
4. Betroffene Markdown-Erklärungen und Mermaid-Diagramme in `docs/` aktualisieren.
5. Relative Links prüfen und Mermaid-Blöcke in GitHub-Vorschau sichten. Dokumentierte Verifikation von tatsächlichen Projekt-Tests unterscheiden.
6. Keine persönlichen Daten, Kundendaten, Secrets oder Rechnerpfade einreichen.
7. In Zielprojekten bestehende Instructions manuell zusammenführen; niemals automatisiert überschreiben.

**Versionierung:** PATCH für Klarstellungen, MINOR für rückwärtskompatible Erweiterungen, MAJOR für Änderungen am Integrations- oder Sicherheitsvertrag. Lokale Conventional Commits sind sinnvoll; Remote-Aktionen bleiben nach den Rechten der jeweiligen Umgebung freigabepflichtig.

Keine Python-, Installer-, Build- oder Test-Runtime ist für dieses Repository erforderlich.
