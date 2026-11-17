# My Wardrobe

Persönliche Kleiderschrank-App als PWA, eine einzige `index.html`, kostenlos über GitHub Pages.

## Was drin ist

| Datei | Wofür |
|---|---|
| `index.html` | die komplette App |
| `icon.png` | App-Icon für den Homescreen |
| `pins/` | Pins deines Pinterest-Boards (wird automatisch aktualisiert) |
| `.github/workflows/pinterest.yml` | holt alle 6 Stunden neue Pins |
| `.github/scripts/fetch_pins.py` | das Skript dazu |

Deine Kleidungsstücke, Looks und dein Gemini-Schlüssel landen **nicht** auf GitHub, sondern nur im Speicher von Safari auf deinem iPhone.

## Einmalig einrichten

1. Repository auf GitHub anlegen (öffentlich, sonst ist Pages nicht gratis) und alle Dateien hochladen.
2. **Settings → Pages** → Source: „Deploy from a branch“, Branch `main`, Ordner `/ (root)` → Save.
3. **Settings → Actions → General** → Workflow permissions: „Read and write permissions“ → Save.
4. **Actions → Pinterest-Pins abrufen → Run workflow** (einmal manuell starten).
5. Nach 1–2 Minuten: `https://DEINNAME.github.io/REPO/` in **Safari** öffnen → Teilen → **Zum Home-Bildschirm**.
6. In der App: Mehr → Einstellungen → Gemini-Schlüssel von https://aistudio.google.com/apikey einfügen, Stadt festlegen.

## Gut zu wissen

- **Backup:** Mehr → Einstellungen → Backup exportieren (z. B. nach iCloud Drive). Wenn du Safari-Daten löschst, ist sonst alles weg.
- **Weitere Pinterest-Boards:** in `.github/workflows/pinterest.yml` bei `BOARDS` mit Komma ergänzen, z. B. `maria280703/outfits,maria280703/herbst`.
- **Pins kommen nicht mehr?** GitHub pausiert geplante Workflows nach 60 Tagen ohne Aktivität. Dann unter Actions einmal „Enable workflow“ / „Run workflow“ drücken.
- **Freistellen** läuft direkt im Browser (beim ersten Mal lädt ein ~40-MB-Modell, am besten im WLAN). Für perfekte Kanten: in der Fotos-App lange auf das Teil drücken → Kopieren → in der App „Motiv einfügen“.
