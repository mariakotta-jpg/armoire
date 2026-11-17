"""Holt die neuesten Pins der Boards (öffentlicher RSS-Feed) und legt sie in pins/ ab.
Läuft per GitHub Action – so kann die App die Bilder ohne CORS-Probleme laden."""
import hashlib, json, os, re, time, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

BOARDS = [b.strip() for b in os.environ.get("BOARDS", "").split(",") if b.strip()]
OUT = "pins"
IMG = os.path.join(OUT, "img")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) ArmoirePinFetcher/1.0"}
os.makedirs(IMG, exist_ok=True)

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

path = os.path.join(OUT, "pins.json")
try:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    data = {"pins": []}
known = {p["id"]: p for p in data.get("pins", [])}

for board in BOARDS:
    try:
        xml = get(f"https://www.pinterest.com/{board}.rss")
    except Exception as e:
        print("Board nicht ladbar:", board, e)
        continue
    for item in ET.fromstring(xml).iter("item"):
        link = (item.findtext("link") or "").strip()
        desc = item.findtext("description") or ""
        m = re.search(r'src="([^"]+)"', desc)
        if not link or not m:
            continue
        pid = hashlib.sha1(link.encode()).hexdigest()[:16]
        img = re.sub(r"/\d+x/", "/736x/", m.group(1))
        fname = os.path.join(IMG, pid + ".jpg")
        if not os.path.exists(fname):
            try:
                with open(fname, "wb") as f:
                    f.write(get(img))
                time.sleep(0.3)
            except Exception as e:
                print("Bild fehlgeschlagen:", img, e)
                continue
        if pid not in known:
            known[pid] = {"id": pid, "board": board, "link": link, "img": img,
                          "file": f"pins/img/{pid}.jpg", "date": item.findtext("pubDate") or ""}

def ts(p):
    try:
        return datetime.strptime(p["date"], "%a, %d %b %Y %H:%M:%S %Z").timestamp()
    except Exception:
        return 0

pins = sorted(known.values(), key=ts, reverse=True)[:600]
with open(path, "w", encoding="utf-8") as f:
    json.dump({"updated": datetime.now(timezone.utc).isoformat(), "pins": pins}, f, ensure_ascii=False, indent=1)
print(len(pins), "Pins gespeichert")
