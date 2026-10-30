# 01 – Architektur: eine Policy, mehrere Laufzeiten

Das Kit standardisiert **das Verhalten von Coding-Agenten**; es trifft keinerlei Entscheidungen über Programmiersprachen, Frameworks, Architektur, Testwerkzeuge oder Paketmanager.

## Drei logische Ebenen – zwei Dateien zum Kopieren

```mermaid
flowchart TB
    subgraph L1["Layer 1 · Universelle Guidelines"]
      P["AGENTS.md\nFreigabe · Delegation · Routing · Security · Quality · Git"]
    end
    subgraph L2["Layer 2 · Laufzeitintegration"]
      C["Codex liest AGENTS.md"]
      CC["Claude Code lädt CLAUDE.md\n→ @AGENTS.md"]
      H["Ollama: Harness injiziert Policy"]
    end
    subgraph L3["Layer 3 · Projekt-eigene Regeln"]
      PR["Vorhandene Konventionen und Tests\nkein Stack vom Kit vorgegeben"]
    end
    P --> C
    P --> CC
    P --> H
    PR -. "Ergänzung; keine Sicherheitslockerung" .-> L2
```

- **Layer 1:** Alle Entscheidungen D-01 bis D-11 stehen kompakt und normativ in [`AGENTS.md`](../AGENTS.md).
- **Layer 2:** `CLAUDE.md` ist ein Import-Einstieg. Andere Agent-Harnesses müssen die Datei selbst laden. Berechtigungen, Sandbox, Modellwechsel und Tool Calling sind Funktionen der Runtime, nicht der Markdown-Dateien.
- **Layer 3:** Projekt-eigene Konventionen bleiben getrennt und dürfen universelle Sicherheitsgrenzen nicht stillschweigend lockern.

## Autonomie und Verantwortung

```mermaid
flowchart TD
    U["User: Auftrag und Go"] --> MAIN["Hauptagent: Scope, Risiko, Fähigkeiten"]
    MAIN --> D{"Delegation vorteilhaft?"}
    D -->|Nein| SELF["Direkte Implementierung"]
    D -->|Ja| SUB["Isolierter Sub-Agent"]
    SELF --> Q["Relevante Projektprüfungen + Diff-Review"]
    SUB --> Q
    Q -->|PASS| COMMIT["Lokaler Conventional Commit"]
    Q -->|FAIL| FIX["Bounded Recovery"]
    FIX --> Q
    COMMIT --> R["Abschlussrapport"]
    R --> REMOTE{"Push / Merge?"}
    REMOTE -->|Ja| U
    REMOTE -->|Nein| DONE["Abschluss"]
```

LIGHT, BALANCED und DEEP bezeichnen *Modell-Leistungsprofile*. CRITICAL bezeichnet *Aufgabenrisiko* und erfordert zusätzliche Kontrolle. Kein Modell wird durch die Dokumentation technisch gewechselt.

## Keine versteckte Installation oder Synchronisierung

Kopieren ist eine einmalige Dateioperation. Eine spätere Aktualisierung heißt: neue `AGENTS.md` mit dem vorhandenen Projektstand vergleichen und Änderungen gezielt zusammenführen. **Es gibt keinen Generator und keine automatische Verteilung.**

Siehe [Kopieranleitung](09-dateien-kopieren.md) und [Runtime-Integration](03-runtime-integration.md).
