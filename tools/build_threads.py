#!/usr/bin/env python3
"""Ricostruisce i file dei filoni a partire dalle edizioni.

Fonte di verità:
  - data/threads.json      metadati dei filoni (titolo, riassunto, stato, collegati)
  - data/AAAA-MM-GG.json   ogni notizia può avere "thread": {"id": ..., "added": ...}

Genera (non modificarli a mano):
  - data/threads/index.json   elenco dei filoni con conteggi e date
  - data/threads/<id>.json    linea del tempo di ogni filone

Esce con codice 1 e un messaggio se trova incoerenze.
Uso: python3 -I tools/build_threads.py
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "threads")
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STATUSES = {"aperto", "chiuso"}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def main():
    errors = []
    meta = load(os.path.join(DATA, "threads.json"))["threads"]
    threads = {}
    for t in meta:
        tid = t.get("id", "")
        if not ID_RE.match(tid):
            errors.append(f"id filone non valido: {tid!r}")
        if tid in threads:
            errors.append(f"id filone duplicato: {tid}")
        for k in ("title", "summary"):
            if not str(t.get(k, "")).strip():
                errors.append(f"{tid}: campo {k} vuoto")
        if t.get("status") not in STATUSES:
            errors.append(f"{tid}: status deve essere uno di {sorted(STATUSES)}")
        if not DATE_RE.match(str(t.get("created", ""))):
            errors.append(f"{tid}: created non è una data AAAA-MM-GG")
        threads[tid] = t
    for t in meta:
        for r in t.get("related", []):
            if r not in threads:
                errors.append(f"{t['id']}: filone collegato inesistente {r!r}")
            elif r == t["id"]:
                errors.append(f"{t['id']}: collegato a se stesso")

    entries = {tid: [] for tid in threads}
    for path in sorted(glob.glob(os.path.join(DATA, "[0-9]" * 4 + "-*.json"))):
        doc = load(path)
        date = doc["date"]
        for sec in doc["sections"]:
            for it in sec["items"]:
                th = it.get("thread")
                if th is None:
                    continue
                tid = th.get("id") if isinstance(th, dict) else None
                if tid not in threads:
                    errors.append(f"{date}: notizia «{it.get('title')}» punta al filone inesistente {tid!r}")
                    continue
                added = th.get("added", "")
                if not DATE_RE.match(added):
                    errors.append(f"{date}: «{it.get('title')}» ha thread.added non valido")
                entries[tid].append({
                    "added": added,
                    "date": date,
                    "section": sec["title"],
                    "source": it["source"],
                    "summary": it["summary"],
                    "title": it["title"],
                    "url": it["url"],
                })

    if errors:
        print("Errori nei filoni:", *errors, sep="\n  - ")
        sys.exit(1)

    os.makedirs(OUT, exist_ok=True)
    index = []
    for tid, t in threads.items():
        items = sorted(entries[tid], key=lambda e: e["date"])
        related = [{"id": r, "title": threads[r]["title"]} for r in t.get("related", [])]
        write(os.path.join(OUT, f"{tid}.json"), {
            "created": t["created"],
            "id": tid,
            "items": items,
            "related": related,
            "status": t["status"],
            "summary": t["summary"],
            "title": t["title"],
        })
        index.append({
            "count": len(items),
            "created": t["created"],
            "first": items[0]["date"] if items else None,
            "id": tid,
            "last": items[-1]["date"] if items else None,
            "status": t["status"],
            "title": t["title"],
        })
        if not items:
            print(f"Avviso: il filone {tid} non ha ancora notizie")
    index.sort(key=lambda x: x["last"] or "", reverse=True)
    index.sort(key=lambda x: x["status"] != "aperto")
    write(os.path.join(OUT, "index.json"), {"threads": index})

    keep = {f"{tid}.json" for tid in threads} | {"index.json"}
    for name in os.listdir(OUT):
        if name.endswith(".json") and name not in keep:
            os.remove(os.path.join(OUT, name))
            print(f"Rimosso file di un filone eliminato: {name}")
    print(f"OK: {len(threads)} filoni, {sum(len(v) for v in entries.values())} collegamenti")


if __name__ == "__main__":
    main()
