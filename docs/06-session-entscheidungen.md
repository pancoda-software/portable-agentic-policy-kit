# 06 – Entscheidungen aus der Grill-me-Session (D-01 bis D-11)

Dieses Kapitel dokumentiert die Ergebnisse des gemeinsamen Interviews als **nachvollziehbare Entscheidungsakte**, nicht als vollständiges Gesprächsprotokoll. Es beschreibt die Motivation, verworfene Alternativen und technische Folgen. Normativ bleibt [`policy/core.md`](../policy/core.md); die maschinenlesbare Liste steht in [`policy/decisions.yaml`](../policy/decisions.yaml).

## Entscheidungsübersicht

| ID | Beschluss | Warum diese Variante? | Konsequenz |
|---|---|---|---|
| D-01 | **B – Risk-Based Autonomy** | Autonomie und strategische Kontrolle verbinden | Ein initiales Go; neu genehmigen bei Risiko-/Scope-Wechsel |
| D-02 | **B – Autonomous Local Commits** | Lokal atomar versionieren ohne ungefragten Remote-Effekt | Conventional Commits nach Gates; Push/Merge nur mit Approval |
| D-03 | **B – Adaptive Delegation** | Sub-Agenten haben Kontext-/Koordinationskosten | Kleine Tasks direkt, Delegation nur bei Vorteil |
| D-04 | **A – Claude Desktop primär** | Tatsächlicher Hauptworkflow mit Abo-Kontingent | Quota-bewusst planen, nicht API-Dollar voraussetzen |
| D-04a | **Multi-Provider** | Nicht an Claude binden | Claude Code, Codex und Ollama-Harnesses berücksichtigen |
| D-05 | **B – Capability-Based Routing** | Modellnamen und Effort-Level ändern sich | LIGHT/BALANCED/DEEP, Fähigkeiten vor Einsatz verifizieren |
| D-06 | **B – Tiered Skills** | Fehlende optionale Skills dürfen nicht blockieren | REQUIRED/PREFERRED/OPTIONAL pro Task |
| D-07 | **B – Risk-Adaptive Quality Gates** | Legacy-Baseline-Fehler sollen nicht pauschal blockieren | Reproduzierter Vorzustand, relevante Tests, Regressionen blockieren |
| D-08 | **B – Bounded Adaptive Recovery** | Endloses Debugging begrenzen | Zwei lokale, ein eskalierter Fix je Ursache |
| D-09 | **B – Layered Security** | Policy alleine ist keine Sandbox | Permissions + technische Durchsetzung + Fail-Closed |
| D-10 | **B – Three-Layer Architecture** | Portabilität bei minimaler Dopplung | Core + Runtime-Adapter + projekt-eigene Instructions |
| D-11 | **B – Portable Policy Kit** | Nutzbares Paket ohne neues Agenten-Framework | Renderer, Validator, Vorlagen, Tests, Docs |

## Was bewusst **nicht** beschlossen wurde

- Kein zwingendes Flaggschiff-Modell für jede Planung.
- Keine Pflicht, jede Codeänderung an einen Sub-Agenten zu delegieren.
- Kein vollständiger Stopp, wenn irgendein irrelevanter Skill fehlt.
- Kein stillschweigender Cloud-Provider- oder Bezahlwechsel.
- Keine Garantie, dass das Ollama-Modell selbst Tool-Security bereitstellt.
- Kein automatischer Git Push oder Merge durch die Ausführungsfreigabe.
- Keine Framework-/Sprachvorgaben: Technologieentscheidungen liegen ausschließlich beim Zielprojekt.

## Sichere Defaults der V1

| Parameter | Wert | Status |
|---|---:|---|
| Lokale Korrekturen je Ursache | 2 | D-08 beschlossen |
| Eskalierte Korrektur je Ursache | 1 | D-08 beschlossen |
| Gesamte Fix-Versuche je Task | 6 | V1-Default |
| Parallele Schreibagenten | 2 | V1-Default |
| Auto-Push | false | D-02 |
| Automatischer bezahlter Provider-Wechsel | false | D-04/D-05/D-09 |
| Dependency-Installation ohne Approval | false | D-09 |

Die Defaults können nur durch eine bewusst dokumentierte, zulässige Änderung weiterentwickelt werden. Projekt-eigene Regeln dürfen Sicherheit und Freigaben nicht eigenmächtig lockern.

## Entwicklung vom ursprünglichen Prompt zum Kit

```mermaid
flowchart LR
    ORIG["Ursprünglicher Prompt\nstarre Regeln"] --> GRILL["11 Grill-me-Runden\nEntscheidungen D-01...D-11"]
    GRILL --> CORE["Universal Core Policy"]
    CORE --> AD["Runtime Adapter"]
    CORE --> PR["Projekt-eigene Regeln"]
    AD --> KIT["Versioniertes Policy Kit"]
    PR --> KIT
    KIT --> TEST["Validator + Tests + Review"]
```

## Weiterentwicklung und Nachvollziehbarkeit

Bei einer Policy-Änderung zuerst die Entscheidung und deren Sicherheitsfolgen dokumentieren, dann `policy/core.md` und gegebenenfalls `policy/decisions.yaml` aktualisieren. Anschließend die generierten Dateien neu erzeugen, Tests laufen lassen und die Dokumentation anpassen. Änderungen an Freigaben sollten separat reviewt werden.
