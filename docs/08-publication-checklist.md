# Prüfliste vor Veröffentlichung als öffentliches Repository

Die Sichtbarkeit eines GitHub-Repositories betrifft **auch die vollständige bisherige Commit-Historie**. Nur Dateien auf `main` auf sensible Inhalte zu prüfen reicht nicht aus.

## Inhalt prüfen

- Code, Dokumentation, Konfigurations- und Beispiel-Dateien auf echte Namen, interne Domains, E-Mail-Adressen, Kundendaten, Zugangstoken, Schlüssel, Geräte- und Pfadkennungen prüfen.
- Versehentlich getrackte Dateien in früheren Commits und Tags prüfen; auch gelöschte Dateien sind über die Git-Historie erreichbar.
- `.gitignore`-Regeln, Workflows und Build-Artefakte prüfen.
- Lizenz- und Urheberrechtsfragen für Drittinhalte und eingebundene Skills klären.

## Commit-Historie prüfen

```bash
git log --all --format='%h %an <%ae> | %cn <%ce>'
git log --all --name-only --format='COMMIT %h'
```

Achtung: Auch `users.noreply.github.com`-Adressen können einen identifizierenden Accountnamen und einen ausgeschriebenen Autorennamen enthalten. Hier wurde ein entsprechender **personenbezogener Autorenname** in der bestehenden Historie festgestellt. **Deshalb nicht ohne gesonderte Klärung auf `public` umstellen.**

Ein Umschreiben der Historie verändert Commit-Hashes und erfordert Koordination mit allen Klonen sowie eine gesonderte, bewusste Freigabe. Nicht automatisch per Installer durchführen.

## Technische Veröffentlichung

- Nach erfolgreicher Prüfung die Sichtbarkeit über GitHub Repository Settings ändern (Admin-Berechtigung erforderlich).
- Danach Installation auf einem frischen Rechner ohne GitHub-Authentifizierung mit dem dokumentierten Bootstrap testen.
- Die Aussage „keine personenbezogenen Daten“ ist ein Prüfziel und kein automatischer Sicherheitsnachweis.
