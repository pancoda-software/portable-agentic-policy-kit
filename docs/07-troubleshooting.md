# 07 – Troubleshooting und FAQ

## `validate.py` meldet „Drift detected“

Generierte `AGENTS.md`, `CLAUDE.md` oder `ollama-system.txt` unterscheiden sich von der kanonischen Vorlage. Manuelle Änderungen nicht blind überschreiben. Erst Diff ansehen und entscheiden, ob die Änderung in die Core-Policy oder das Projektprofil gehört. Anschließend einen **neuen Ausgabeordner** rendern; `--force` nur auf zweifelsfrei vom Generator erzeugte Dateien anwenden.

## `render.py` verweigert eine Dateiüberschreibung

Erwartetes Sicherheitsverhalten. Vorhandene projektbezogene Instructions könnten User-Regeln enthalten. Ausgabeordner wechseln oder nach manueller Prüfung die geeigneten Teile zusammenführen. Symlink-Schutz nicht umgehen.

## Claude Code / Codex ignoriert Regeln

Prüfen, ob der jeweilige Entry-Point am korrekten Ort liegt, ob `@AGENTS.md` erfolgreich importiert wird und ob andere Projekt-/globale Regeln Vorrang haben. Die **tatsächlich geladenen** Instruktionen mit einem Smoke-Test abgleichen. Die bloße Existenz einer Datei beweist nichts.

## Lokales Ollama-Modell verweigert Tool Calling oder halluziniert Erfolg

Modelle unterscheiden sich stark in Tool-Unterstützung, Kontextgrenzen und Instruktionsbefolgung. Den Harness mit read-only Tools testen, kleinere Aufgaben wählen oder ein nachweislich geeigneteres Modell einsetzen. Sicherheit immer außerhalb des Modells erzwingen. **Nicht** stillschweigend eine kostenpflichtige API benutzen.

## Ein benötigter Skill wird nicht erkannt

`python3 tooling/validate.py --check-skills --project /pfad/zum/repo` ausführen. Installationsort und `SKILL.md`-Namenskonvention prüfen. Bei REQUIRED den abhängigen Task stoppen. PREFERRED kann durch einen transparenten nativen Fallback ersetzt werden. Der Validator belegt weder Skill-Sicherheit noch Funktionsfähigkeit.

## Warum kann Codex keinen lokalen Commit erzeugen?

In manchen Sandbox-Einstellungen ist `.git` nicht beschreibbar. Der Agent darf das nicht durch pauschale Deaktivierung der Sandbox umgehen. Einen dedizierten, genehmigten Commit-Pfad verwenden oder die Änderung uncommitted übergeben und um Berechtigungsfreigabe bitten.

## `agent-verify.sh` meldet fehlende Tests

Bei MEDIUM/HIGH benötigt die npm-orientierte Vorlage ein `test`-Script. Fehlt es, wird der Check als FAIL/UNAVAILABLE ausgewiesen, nicht erfunden. Für Python-, Rust- oder andere Projekte geeignete eigene Quality Gates konfigurieren. Prüfe außerdem, ob Projekt-Skripte ungewollte Seiteneffekte haben.

## Was passiert bei bereits roten Tests?

Ein Vorher-nachher-Vergleich muss belegen, dass derselbe Fehler schon vorher auftrat und nicht schlimmer wurde. Falls eine Baseline nicht reproduzierbar ist, ist die autonome Commit-Freigabe auszusetzen oder eine ausdrücklich genehmigte Alternative zu wählen.

## Darf der Agent automatisch einen Pull Request erstellen?

D-02 erlaubt lokale Commits, aber ein Remote Push bzw. Merge benötigt eine konkrete Freigabe. Die Erstellung eines Remote Pull Requests oder das Hochladen eines Branches ist daher **nicht automatisch** von der initialen Coding-Freigabe gedeckt. Ein spezifisches Go für das Repository/den Branch kann die Remote-Aktion autorisieren, ohne andere Grenzen aufzuheben.

## Warum sind die Retry-Limits nicht vom Validator erzwungen?

`validate.py` prüft die **existierenden Policy-Defaults**, nicht die dynamische Tool-Nutzung. Eine harte Zählung über Sub-Agenten, Kontextkompression oder Session-Neustarts verlangt einen externen vertrauenswürdigen State-Store und Controller. Die V1 deklariert diese Anforderung offen.

## Wo beginne ich?

1. [`README.md`](../README.md) lesen und Tests ausführen.
2. [`docs/01-architektur.md`](01-architektur.md) und [`docs/02-workflows.md`](02-workflows.md) betrachten.
3. Passendes Projektprofil wählen und in **neuen Ordner** rendern.
4. Laufzeitspezifische Sicherheitsmechanismen auf dem Zielsystem konfigurieren.
5. In einem Wegwerf-Repository die Smoke-Tests aus [`03-runtime-integration.md`](03-runtime-integration.md) durchführen.
