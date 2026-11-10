# Regole della redazione

Questo file raccoglie le regole della rassegna e le correzioni del proprietario.
La redazione automatica lo rilegge prima di ogni edizione e le regole qui scritte
prevalgono sulle abitudini precedenti.

## Obiettivo e pubblico

- Un unico posto, non dispersivo, per informarsi in modo corretto.
- Pubblico: dalla quinta superiore all'università, e chiunque voglia informarsi.
- Tono adulto: spiegare il contesto, non le cose ovvie. Spiegare sigle e termini tecnici.

## Sezioni e temi

Dal 2026-11-11 le sezioni di ogni edizione coincidono con i temi del sito
(`data/themes.json`), in questo ordine (key | title):

1. politica | Politica interna — governo, Parlamento, partiti, nomine, elezioni
2. economia | Economia e lavoro — manovra, industria, lavoro, banche, costo della vita
3. sicurezza | Sicurezza e giustizia — cronaca, processi, decreti sicurezza, attacchi informatici
4. esteri | Politica estera — conflitti, diplomazia, decisioni dell'Ue
5. tech | Tecnologia e AI
6. ambiente | Ambiente e clima — clima, maltempo, transizione energetica, inquinamento
7. societa | Società — scuola, università, sanità, diritti

- Da 0 a 3 notizie per sezione; puntare a 3 nelle prime cinque. Ambiente e Società
  possono restare vuote (`"items": []`).
- Il sito è nazionale: niente sezione o preferenza per una singola città. Le notizie
  locali entrano solo se hanno rilevanza nazionale.
- **Energia:** bollette, prezzo del gas e costo dell'energia vanno in Economia;
  rinnovabili, nucleare, emissioni e transizione energetica vanno in Ambiente.
- **Cronaca nera:** solo casi di rilevanza pubblica (impatto su leggi o dibattito,
  processi importanti, fenomeni ricorrenti come i femminicidi). Mai dettagli macabri,
  mai nomi di vittime minorenni.
- Le edizioni fino al 2026-11-10 restano con le sezioni di allora.

## Fonti e verifica

- Solo testate affidabili; sempre l'URL dell'articolo specifico, mai la home page.
- Mai inventare URL, titoli, fatti o citazioni. Meglio una sezione con meno notizie
  che una notizia non verificata.

## Filoni

Ogni vicenda che dura più di un giorno diventa un filone, con una pagina che
mostra «La storia finora» e la linea del tempo di tutte le notizie collegate.

### Dove stanno i dati

- `data/threads.json`: elenco dei filoni. Per ognuno, in ordine alfabetico:
  `created` (data di creazione), `id` (minuscole e trattini, es. `ex-ilva`),
  `related` (id di filoni collegati), `status` (`aperto` o `chiuso`),
  `summary` («La storia finora»), `theme` (id di un tema di `data/themes.json`), `title`.
- Ogni filone appartiene a un solo tema, di solito quello della sezione delle sue notizie.
  Sul sito un filone è «in corso» se è aperto e ha avuto notizie negli ultimi 14 giorni;
  gli altri finiscono nell'archivio del tema.
- Nelle edizioni, una notizia collegata ha il campo
  `"thread": {"added": "AAAA-MM-GG", "id": "..."}`, dove `added` è il giorno in cui
  è stato creato il collegamento. Chiavi della notizia in ordine alfabetico:
  source, summary, thread, title, update, url.
- `data/threads/`: file generati da `python3 -I tools/build_threads.py`.
  Non vanno modificati a mano.

### Ogni edizione

1. Leggi `data/threads.json` per conoscere i filoni aperti.
2. Collega ogni notizia che continua un filone aperto (`added` = OGGI).
3. Se una notizia apre una storia che continuerà, o si lega a notizie delle
   edizioni passate, crea un nuovo filone. Puoi collegare anche le notizie passate
   pertinenti aggiungendo solo il campo `thread`, senza toccare altro.
4. Niente filone per le notizie isolate: un filone ha senso con almeno due puntate
   o con uno sviluppo atteso a breve.
5. Aggiorna «La storia finora» quando c'è uno sviluppo importante: 2-4 frasi,
   solo fatti presenti nelle notizie collegate.
6. `related` solo quando il legame è chiaro (causa, effetto, stessa vicenda più ampia).
7. Metti `status: chiuso` quando la vicenda è conclusa o dopo 21 giorni senza notizie.
8. Esegui `python3 -I tools/build_threads.py`: deve stampare `OK`.

### Revisione del proprietario

- Il sito mostra «da verificare» per 3 giorni dalla data `added` del collegamento
  o `created` del filone (il proprietario controlla ogni due giorni).
- Se il proprietario segnala un errore: correggi o rimuovi il collegamento dalla
  prossima edizione, anche se già confermato. Se il collegamento viene spostato su un
  altro filone, `added` diventa la data della correzione.
- Ogni correzione va annotata nel registro in fondo a questo file, con la regola
  che ne deriva.

### File che la redazione può modificare

`data/` (edizioni, `index.json`, `threads.json`, `threads/`) e il registro delle
correzioni in questo file. Nient'altro senza il permesso del proprietario.

## Chi ne parla (in progetto)

- Solo politici e figure istituzionali; per ora niente influencer.
- Solo citazioni testuali, brevi, tra « », sentite al tg o riportate dai giornali,
  e sempre con il link alla pagina o al video della testata.
- Nome, ruolo, data e fonte per ogni citazione.
- La posizione si descrive senza giudizi (es. «favorevole», «contraria»,
  «chiede chiarimenti»), mai «attacca» o «mente».
- Nei temi politici, mostrare governo e opposizione se entrambi si sono espressi.

## Correzioni del proprietario

Registro delle segnalazioni, dalla più recente. Formato: data, cosa era sbagliato,
regola che ne deriva.

- (nessuna correzione per ora)
