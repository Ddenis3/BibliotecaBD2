# AI_LOG – Sistem de Gestionare a unei Biblioteci

## Etapa 1 – Modelare

### Instrument AI utilizat

ChatGPT – OpenAI

### Activități realizate cu asistență AI

1. Alegerea și definirea structurii bazei de date.
2. Generarea comenzilor SQL pentru crearea celor 9 tabele.
3. Stabilirea relațiilor dintre tabele.
4. Definirea constrângerilor de integritate.
5. Generarea datelor demonstrative.
6. Implementarea fișierului `fixtures.py`.
7. Configurarea conexiunii Flask–PostgreSQL.
8. Explicarea comenzilor SQL și interpretarea rezultatelor.
9. Identificarea și corectarea erorilor întâlnite în timpul dezvoltării.

### Erori identificate și corectate

**Eroarea 1 – Tranzacție SQL anulată**

În timpul introducerii datelor a apărut eroarea SQLSTATE 25P02.

S-a utilizat comanda `ROLLBACK`, iar inserările au fost reluate și verificate separat.

**Eroarea 2 – Autori duplicați**

Au fost identificate 30 de înregistrări în loc de 15, ceea ce a determinat apariția a 40 de asocieri între cărți și autori.

Înregistrările duplicate au fost eliminate, iar relațiile au fost corectate.

**Eroarea 3 – Import Python**

La pornirea aplicației a apărut o eroare deoarece funcția `get_connection` nu era disponibilă în fișierul `database.py`.

Fișierul a fost completat și salvat, iar conexiunea a fost verificată.

### Verificarea rezultatelor

Codul SQL și Python a fost executat local, utilizând PostgreSQL, pgAdmin 4 și Visual Studio Code.

Au fost verificate structura bazei de date, relațiile, constrângerile și funcționarea serviciului Flask.
