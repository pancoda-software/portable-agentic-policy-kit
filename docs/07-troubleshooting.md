# 07 – Troubleshooting und FAQ

## Agenten ignorieren die Guidelines

Prüfe Dateiname und Ort (`AGENTS.md` in der Projektwurzel, `CLAUDE.md` für Claude Code). Stelle sicher, dass die konkrete Runtime die Instructions wirklich lädt. Veraltete oder konkurrierende globale/Unterverzeichnis-Regeln können eine andere Wirkung haben. **Datei vorhanden** heißt nicht automatisch **Datei geladen**.

## Im Projekt existiert bereits eine AGENTS.md oder CLAUDE.md

**Nicht überschreiben.** Bestehende Anweisungen bewahren, neue universelle Regeln mit einem Diff vergleichen und bewusst integrieren. Falls beide Dateien Regeln enthalten, Dopplungen und Widersprüche auflösen. Sicherheitsregeln dürfen nicht unbeabsichtigt abgeschwächt werden.

## Claude Code interpretiert @AGENTS.md nicht

Prüfe die tatsächliche Version und Import-Unterstützung. Wenn der Import nicht funktioniert, die universellen Regeln manuell in eine von Claude tatsächlich geladene Instruktionsdatei übernehmen. Nicht behaupten, der Import sei aktiv, ohne ihn zu testen.

## Ollama beachtet die Policy nicht

Ollama führt primär Modellschnittstellen aus. Ein Agent-Harness muss `AGENTS.md` aktiv als Instruktion übergeben. Tool Calling und Berechtigungsgrenzen müssen ebenfalls im Harness umgesetzt sein.

## Der Agent darf keine lokalen Commits machen

Prüfe, ob `.git` in der Runtime-Sandbox beschreibbar ist und ob die Quality Gates erfolgreich sind. Keine Sandbox eigenmächtig deaktivieren; gegebenenfalls separate Berechtigung einholen oder die Änderung uncommitted übergeben.

## Ein Skill fehlt

Nur ein für den konkreten Auftrag REQUIRED-Skill blockiert die abhängige Operation. Für PREFERRED sind transparente Fallbacks erlaubt; OPTIONAL kann entfallen. Ein fehlender Skill wird nicht simuliert.

## Tests sind schon vor der Änderung fehlgeschlagen

Baseline und Fehlersymptom reproduzierbar vergleichen. Vorbestehende Fehler dürfen nur mit Belegen ausgenommen werden. Neue Regressionen blockieren autonome Commits.

## Wie aktualisiere ich die Policy in mehreren Projekten?

Neue `AGENTS.md` mit jeder projekt-eigenen Version vergleichen und Änderungen gezielt übernehmen. Eine vorhandene `CLAUDE.md` nicht erneut überschreiben. Wer eine automatisierte zentrale Verteilung braucht, kann **separates eigenes Tooling** ergänzen – es ist kein Bestandteil dieses Markdown-Kits.

## Warum gibt es keine Validator-/Installationsbefehle mehr?

Die ursprüngliche Aufgabe war ein **kopierbares Regelwerk**. Python-Installer, Test-Runner und Generatoren waren zusätzlicher Wartungsaufwand ohne unmittelbaren Nutzen für diesen Zweck. Das Kit besteht deshalb ausschließlich aus Markdown.

Beginne mit [README](../README.md), [Kopieranleitung](09-dateien-kopieren.md) und [Workflows](02-workflows.md).
