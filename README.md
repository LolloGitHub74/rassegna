# rassegna

Rassegna quotidiana di notizie, pubblicata come sito/app su GitHub Pages:
https://lollogithub74.github.io/rassegna/

- `data/AAAA-MM-GG.json`: un'edizione al giorno; `data/index.json`: elenco delle date.
- `data/themes.json`: i 7 temi, che sono anche le sezioni di ogni edizione.
- `data/threads.json`: i filoni (storie che durano più giorni), ciascuno con il suo tema.
- `data/threads/`: file generati con `python3 -I tools/build_threads.py`.
- `REDAZIONE.md`: regole della redazione e registro delle correzioni.
