# Contributing

Dieses Repository enthält sicherheitsrelevante Agent-Instruktionen. Änderungen an `policy/core.md`, `policy/decisions.yaml` und Runtime-Berechtigungsregeln brauchen besonders sorgfältiges Review.

## Vorgehensweise

1. Motivation, Scope und Sicherheitsfolgen der Änderung dokumentieren.
2. Kanonische Quellen statt der generierten Beispiel-Dateien bearbeiten.
3. `python3 tooling/validate.py` und `python3 -m unittest discover -s tests -v` ausführen.
4. Betroffene Beispiele mit `tooling/render.py` neu erzeugen; Drift prüfen.
5. Bei Änderungen der Workflows die Mermaid-Diagramme und Beispiele in `docs/` aktualisieren.
6. Atomaren Conventional Commit erstellen; Push und Merge nur im autorisierten Workflow.

## Versionskonvention

- **PATCH:** Klarstellungen und nicht brechende Fehlerkorrekturen.
- **MINOR:** Neue optionale Profile/Adapter mit unveränderter Core-Sicherheitssemantik.
- **MAJOR:** Änderungen an Policy-Invarianten, Freigaben oder deren Kompatibilitätsvertrag.

## Grenzen

Keine Secrets, Tokens oder echten `.env`-Dateien committen. Keine privaten Host-Details in Issues oder PRs veröffentlichen. Dieses Kit ersetzt keine Sandbox und kein Security-Audit eines Zielsystems.
