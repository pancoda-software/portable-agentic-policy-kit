# Sicherheitsmodell und Grenzen

Dieses Repository enthält **nur Markdown-Regeln**, keine technische Sandbox, keinen Installer und keinen ausführbaren Security-Controller.

1. **Anweisung ist keine Berechtigung:** `AGENTS.md` autorisiert keine Shell-, Netzwerk-, Git- oder Dateiaktionen. Host-Sandbox, Betriebssystemrechte und Approval-Dialoge müssen selbstständig greifen.
2. **Risk-based autonomy:** Nur der vom Nutzer freigegebene Scope darf autonom bearbeitet werden; Push/Merge, gefährliche Git-Aktionen, Installationen, neue Kosten, Produktionswirkung und Zugriffe außerhalb des Scopes brauchen weitere Genehmigungen.
3. **Sensible Daten:** Keine echten Credentials in Projektanweisungen oder Logs kopieren. Repository-Inhalte und externe Skills können Prompt-Injection enthalten und dürfen Sicherheitsregeln nicht überschreiben.
4. **Qualität:** Tests, Typprüfungen, Lint und Builds müssen aus dem vorhandenen Projekt abgeleitet werden. Ein ungetesteter Fix ist nicht verifiziert. Die Policy erzwingt keine Tests automatisch.
5. **Ollama:** Ein lokales Modell kann selbst keine Tool-Allowlist, Rechtegrenze oder zuverlässige Sitzungszustände garantieren. Der Harness muss Aufrufe kontrollieren.
6. **Bestehende Dateien:** Niemals eine projekt-eigene `AGENTS.md`/`CLAUDE.md` ohne Sichtprüfung ersetzen. Konflikte manuell auflösen.
7. **Public-Release:** Bereits vorhandene Git-Commits enthalten personenbezogene Autorenmetadaten. Vor einem Wechsel zu `public` ist eine gesonderte Überprüfung und Entscheidung notwendig; ältere Commits werden durch das Entfernen aktueller Dateien nicht unsichtbar.

## Manuelle Smoke-Tests (nur in Testprojekt ohne echte Secrets)

- Agenten nach geladenen Regeln fragen und mit `AGENTS.md` abgleichen.
- Einen nicht autorisierten Schreib-/Push-Versuch in einer isolierten Testumgebung prüfen: Er muss blockiert sein oder eine Freigabe verlangen.
- Einen bekannten Testfehler auslösen; sicherstellen, dass kein autonomer Erfolg/Commit behauptet wird.
- Prüfen, ob Änderungen außerhalb eines angenommenen Scopes an die Nutzerfreigabe zurückgeführt werden.

**Hinweis:** Ein bestandenes Smoke-Test-Szenario ist kein formaler Sicherheitsnachweis. Siehe [Sicherheits- und Qualitätskapitel](docs/05-sicherheit-qualitaet.md).
