# Sistem de Gestionare a unei Biblioteci

## Etapa 1 – Modelarea bazei de date

### 1. Descrierea proiectului

Proiectul „Sistem de Gestionare a unei Biblioteci” are ca scop dezvoltarea unei aplicații web pentru administrarea activităților unei biblioteci.

Sistemul permite organizarea cărților, autorilor și categoriilor, gestionarea exemplarelor fizice, evidența utilizatorilor, înregistrarea împrumuturilor și administrarea rezervărilor.

Aplicația utilizează o bază de date relațională PostgreSQL și un backend realizat în Python, folosind frameworkul Flask.

### 2. Structura bazei de date

Baza de date se numește `biblioteca` și conține 9 tabele.

| Tabel        | Descriere                                       |
| ------------ | ----------------------------------------------- |
| roluri       | Definește rolurile utilizatorilor               |
| utilizatori  | Stochează informațiile despre utilizatori       |
| categorii    | Organizează cărțile după categorie              |
| autori       | Stochează informațiile despre autori            |
| carti        | Conține informațiile bibliografice ale cărților |
| autori_carti | Realizează asocierea dintre cărți și autori     |
| exemplare    | Evidențiază exemplarele fizice ale cărților     |
| imprumuturi  | Înregistrează împrumuturile și returnările      |
| rezervari    | Gestionează rezervările cărților                |

### 3. Relațiile dintre tabele

Baza de date conține relații de tip 1:N și N:M.

Relațiile implementate sunt:

* roluri – utilizatori (1:N)
* categorii – carti (1:N)
* carti – autori_carti (1:N)
* autori – autori_carti (1:N)
* carti – exemplare (1:N)
* utilizatori – imprumuturi (1:N)
* exemplare – imprumuturi (1:N)
* utilizatori – rezervari (1:N)
* carti – rezervari (1:N)

Relația dintre cărți și autori este de tip N:M, fiind implementată prin tabelul intermediar `autori_carti`.

### 4. Constrângeri de integritate

Pentru asigurarea corectitudinii datelor au fost implementate:

**PRIMARY KEY:** identificarea unică a înregistrărilor.

**FOREIGN KEY:** menținerea relațiilor dintre tabele.

**NOT NULL:** obligativitatea completării anumitor câmpuri.

**UNIQUE:** prevenirea duplicatelor pentru valori precum emailul, ISBN-ul și codul de inventar.

**CHECK:** validarea valorilor introduse, inclusiv stările exemplarelor, stările împrumuturilor și anumite condiții privind datele calendaristice.

**ON DELETE RESTRICT:** împiedicarea ștergerii unor înregistrări care sunt referite de alte tabele.

**ON DELETE CASCADE:** eliminarea automată a unor asocieri atunci când înregistrarea corespunzătoare este ștearsă.

### 5. Date demonstrative – Fixtures

Pentru testarea bazei de date a fost implementat un mecanism de inițializare automată a datelor demonstrative.

Acesta este definit în fișierul `fixtures.py` și este apelat la pornirea aplicației Flask.

Setul inițial conține:

| Tabel        | Înregistrări |
| ------------ | -----------: |
| roluri       |            3 |
| utilizatori  |           10 |
| categorii    |            8 |
| autori       |           15 |
| carti        |           20 |
| autori_carti |           20 |
| exemplare    |           30 |
| imprumuturi  |           10 |
| rezervari    |            5 |
| **Total**    |      **121** |

Mecanismul verifică existența datelor înainte de inserare, pentru a evita duplicarea acestora la repornirea serviciului.

### 6. Tehnologii utilizate

* PostgreSQL – sistem relațional de gestionare a bazei de date.
* pgAdmin 4 – administrarea și verificarea bazei de date.
* Python – limbajul utilizat pentru backend.
* Flask – framework pentru dezvoltarea serviciului web.
* psycopg – conectarea aplicației Python la PostgreSQL.
* Visual Studio Code – mediul de dezvoltare.

### 7. Verificarea implementării

Au fost realizate teste pentru verificarea:

* Existenței celor 9 tabele.
* Relațiilor dintre tabele.
* Constrângerilor de integritate.
* Existenței celor 121 de înregistrări demonstrative.
* Inițializării fixtures la pornirea aplicației.
* Conexiunii dintre Flask și PostgreSQL.
* Consistenței datelor privind împrumuturile.

Rezultatele testelor efectuate au fost conforme cu valorile așteptate.

### 8. Diagrama ERD

Diagrama ERD a fost generată utilizând instrumentul integrat în pgAdmin 4.

Aceasta prezintă cele 9 tabele, cheile primare, cheile străine și relațiile dintre entități.

Fișier asociat: `diagrama_ERD.png`.

### 9. Conc
