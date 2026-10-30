# 02 – End-to-End Workflows und Mermaid-Diagramme

Dieses Kapitel zeigt die tatsächlich vorgesehenen Zustandsübergänge. Ein Flussdiagramm beschreibt die **Soll-Regel**, nicht automatisch eine vorhandene technische Durchsetzung.

## A. Von der Idee zum freigegebenen Auftrag

```mermaid
flowchart TD
    IDEA["Idee / Featurewunsch"] --> RESTATE["Verständnis spiegeln"]
    RESTATE --> SCOPE["Scope, Akzeptanzkriterien, Risiken"]
    SCOPE --> BIG{"Größerer Architekturwunsch?"}
    BIG -->|Ja| RFC["Kurzes RFC mit Optionen/Blind Spots"]
    BIG -->|Nein| PLAN["Kompakter Plan"]
    RFC --> PLAN
    PLAN --> GO{"Explizites Go?"}
    GO -->|Nein| WAIT["Nur analysieren, nicht implementieren"]
    GO -->|Ja| EXEC["Autonome, begrenzte Umsetzung"]
```

**Beispiel:** „Ich möchte eine bestehende Session-Erneuerung robuster machen.“ Vor dem Go benennt der Agent bestehende Session-Verantwortlichkeiten, Schnittstellen, Fehlerzustände und mögliche Race Conditions. Nach dem Go darf er nur den vereinbarten Umfang ändern.

## B. Capability-basiertes Modell- und Agentenrouting

```mermaid
flowchart TD
    T["Freigegebener Task"] --> RISK["Komplexität + Risiko unabhängig bewerten"]
    RISK --> PROFILE["LIGHT / BALANCED / DEEP"]
    PROFILE --> CAP{"Modell und Tool-Fähigkeiten geprüft?"}
    CAP -->|Ja| ROUTE["Geeignetes vorhandenes Modell verwenden"]
    CAP -->|Nein| FALL["Konservativer Fallback oder User informieren"]
    ROUTE --> DEL{"Spezialisierung/Parallelität nützt?"}
    DEL -->|Ja| SUB["Sub-Agent mit minimalen Dateien/Rechten"]
    DEL -->|Nein| MAIN["Hauptagent führt aus"]
    SUB --> VERIFY["Verifikation"]
    MAIN --> VERIFY
```

Die Empfehlung „nutze DEEP“ ist nicht dasselbe wie ein durchgeführter Modellwechsel. **CRITICAL** führt unabhängig vom Modell zu strengeren Prüfungen/Freigaben.

## C. Quality Gates vor dem lokalen Commit

```mermaid
flowchart TD
    B["Baseline und git status erfassen"] --> CHANGE["Änderung innerhalb Scope"]
    CHANGE --> TEST["Tests / Lint / Typen / Diff / Secrets"]
    TEST --> NEW{"Neue Regression?"}
    NEW -->|Ja| BLOCK["Commit blockieren"]
    NEW -->|Nein| OLD{"Bestehender Fehler?"}
    OLD -->|Ja| EVID["Vorzustand und unverändertes Symptom belegen"]
    OLD -->|Nein| REQUIRED["Erforderliche Gates PASS?"]
    EVID --> REQUIRED
    REQUIRED -->|Nein/Unklar| BLOCK
    REQUIRED -->|Ja| SCOPE["Scope und Stage-Auswahl überprüfen"]
    SCOPE --> COMMIT["Atomarer lokaler Commit"]
    BLOCK --> RECOVERY["Recovery / Eskalation"]
```

Bei MEDIUM sind anwendbare Tests und statische Prüfungen erforderlich. Bei HIGH zusätzlich erweiterte Verifikation und separate Freigaben für riskante Operationen. `agent-verify.sh` führt nur ausgewählte Checks aus und kann nicht alle Aufgabenrisiken automatisch bewerten.

## D. Fehlerbehebung mit begrenztem Retry-Budget

```mermaid
flowchart TD
    F["Fehler mit reproduzierbarer Evidenz"] --> D["Root-Cause-Hypothese und Fingerprint"]
    D --> STOP{"Sicherheits- oder Scope-Grenze verletzt?"}
    STOP -->|Ja| HALT["Sofort stoppen und berichten"]
    STOP -->|Nein| FIX1["Lokaler Fix 1 und Tests"]
    FIX1 --> OK1{"PASS?"}
    OK1 -->|Ja| GATE["Quality Gate"]
    OK1 -->|Nein| FIX2["Lokaler Fix 2 und Tests"]
    FIX2 --> OK2{"PASS?"}
    OK2 -->|Ja| GATE
    OK2 -->|Nein| CAN{"Eskalation erlaubt?\nGlobales Budget frei?"}
    CAN -->|Nein| HALT
    CAN -->|Ja| ESC["Anderes Modell / Spezialist / tieferer Check"]
    ESC --> LAST["Maximal ein eskalierter Fix"]
    LAST --> OK3{"PASS?"}
    OK3 -->|Ja| GATE
    OK3 -->|Nein| HALT
```

Beschlossene Default-Grenzen: **2 lokale + 1 eskalierter Fix pro Ursache**, **6 Korrekturen insgesamt pro Task**, **maximal 2 parallele Schreibagenten**. Diagnoseaufrufe zählen nicht als Fix. Das bloße Umbenennen einer Ursache setzt den Zähler nicht zurück. Für zuverlässige Einhaltung über Sessions hinweg braucht es externe Zustandsverwaltung.

## E. Berechtigungs- und Sicherheitsablauf

```mermaid
flowchart TD
    REQ["Tool-Aktion"] --> SCOPE{"Innerhalb autorisiertem Scope?"}
    SCOPE -->|Nein| ASK["Vorherige ausdrückliche Freigabe"]
    SCOPE -->|Ja| POLICY{"ALLOW / ASK / DENY"}
    POLICY -->|DENY| BLOCK["Sperren / kein Bypass"]
    POLICY -->|ASK| ASK
    POLICY -->|ALLOW| HOST{"Sandbox/OS/Tool-Policy erlaubt?"}
    HOST -->|Nein| BLOCK
    HOST -->|Ja| RUN["Aktion ausführen und protokollieren"]
```

Ein bestehender Projekt-Testbefehl ist nicht automatisch ungefährlich: Ein Projekt kann beliebige Lifecycle-Skripte definiert haben. Neues oder unerwartetes Skriptverhalten muss vor der Ausführung geprüft werden.

## F. Git-Ablauf vom Arbeitsauftrag bis zur Versionierung

```mermaid
sequenceDiagram
    actor User
    participant M as Hauptagent
    participant A as Coding-Agent
    participant V as Verifier
    participant G as Git
    User->>M: Scope und initiales Go
    M->>A: Task + Rechte + Akzeptanzkriterien
    A->>V: Änderungen und relevante Tests
    V-->>M: PASS/FAIL/SKIPPED/UNAVAILABLE
    alt Gates PASS
      M->>G: Nur auftragsbezogene Änderungen stagen
      G-->>M: Lokaler Conventional Commit
      M-->>User: Ergebnis + Hash + Testbericht
      opt Remote Push/Merge notwendig
        M->>User: Separate Freigabe einholen
      end
    else Neu verursachte Regression
      V-->>A: Diagnose + Budget
      A-->>M: Fix oder Failure Report
    end
```

## Beispiel für einen kurzen Abschlussrapport

```yaml
task: TASK-42
scope: "Session-Renewal Bugfix"
result: completed
checks:
  targeted_tests: PASS
  typecheck: PASS
  lint: SKIPPED # mit dokumentierter Begründung
  build: UNAVAILABLE # nicht als PASS melden
commit: "fix(auth): serialize token refresh"
remote_push: NOT_PERFORMED
outstanding_risks: ["Produktionssession nicht live verifiziert"]
```
