# ETAPA 2 – Operatii CRUD si descrierea interfetei

## 1. Informatii generale

**Proiect:** Sistem de Gestionare a unei Biblioteci  
**Disciplina:** Baze de Date II  
**Tehnologii utilizate:** PostgreSQL, Python, Flask, HTML, CSS, JavaScript

### Obiectiv

Obiectivul Etapei 2 este implementarea operatiilor CRUD (Create, Read, Update, Delete) pentru entitatile bazei de date si realizarea interfetelor necesare gestionarii acestora.

Aplicatia permite administrarea datelor din PostgreSQL prin intermediul unei interfete web dezvoltate cu Flask.

## 2. Structura aplicatiei

Aplicatia contine urmatoarele componente:

- `app.py` – rutele Flask si operatiile CRUD.
- `database.py` – conexiunea la baza de date PostgreSQL.
- `fixtures.py` – initializarea datelor demonstrative.
- `templates/` – paginile HTML ale aplicatiei.
- `static/` – fisierele statice.
- `documentatie/` – documentatia proiectului.

Interogarile SQL sunt executate folosind biblioteca `psycopg`.

La pornirea aplicatiei, functia `initialize_fixtures()` initializeaza datele demonstrative, daca acestea nu exista deja.

## 3. Operatiile CRUD implementate

### 3.1. Categorii

**Ruta:** `/categorii`

Pagina permite adaugarea, afisarea, modificarea si stergerea categoriilor.

Pentru fiecare categorie sunt gestionate numele si descrierea.

Numele categoriei este obligatoriu si trebuie sa fie unic.

Stergerea unei categorii care are carti asociate este restrictionata pentru respectarea integritatii referentiale.

### 3.2. Autori

**Ruta:** `/autori`

Pagina permite adaugarea, afisarea, modificarea si stergerea autorilor.

Informatiile gestionate sunt:

- Nume
- Prenume
- Data nasterii
- Nationalitate
- Biografie

Autorii pot fi asociati cu una sau mai multe carti.

### 3.3. Carti

**Ruta:** `/carti`

Pagina permite adaugarea, afisarea, modificarea si stergerea cartilor.

Informatiile gestionate sunt titlul, ISBN-ul, categoria, editura, anul publicarii si descrierea.

Pagina foloseste un tabel compact in care sunt afisate cartile existente.

Este implementata cautarea dupa titlu.

Formularele de adaugare si modificare sunt deschise in ferestre modale.

Categoria poate fi cautata dupa nume si selectata dintre categoriile existente.

Autorii pot fi cautati dupa nume si selectati individual, fiind permisa asocierea mai multor autori cu aceeasi carte.

### 3.4. Asocierea autorilor cu cartile

**Tabel:** `autori_carti`

Relatia dintre autori si carti este de tip N:M.

Gestionarea acestei relatii este integrata in pagina `carti.html`.

La adaugarea unei carti sunt create asocierile cu autorii selectati.

La modificare, lista autorilor asociati poate fi actualizata.

Eliminarea unui autor din lista unei carti determina eliminarea asocierii corespunzatoare.

Nu este necesara o pagina separata pentru tabelul de legatura.

### 3.5. Exemplare

**Ruta:** `/exemplare`

Pagina permite adaugarea, afisarea, modificarea si stergerea exemplarelor fizice.

Informatiile gestionate sunt:

- Cartea asociata
- Codul de inventar
- Starea exemplarului
- Data achizitiei

Codul de inventar este unic.

Cartea asociata poate fi cautata dupa titlu.

Pagina include cautarea exemplarelor dupa titlul cartii sau codul de inventar.

Stergerea unui exemplar care are imprumuturi asociate este restrictionata prin relatiile bazei de date.

### 3.6. Utilizatori

**Ruta:** `/utilizatori`

Pagina permite adaugarea, afisarea, modificarea si stergerea utilizatorilor.

Informatiile gestionate sunt:

- Nume
- Prenume
- Email
- Telefon
- Rol
- Parola
- Starea contului

Fiecare utilizator este asociat unui rol existent.

Parolele introduse prin interfata sunt transformate in hash folosind `generate_password_hash()`.

La modificarea unui utilizator, parola poate fi lasata necompletata pentru a pastra parola existenta.

Pagina include cautare dupa nume, prenume si email.

Stergerea utilizatorilor cu imprumuturi sau rezervari asociate este restrictionata.

### 3.7. Roluri

**Ruta:** `/roluri`

Pagina permite adaugarea, afisarea, modificarea si stergerea rolurilor.

Pentru fiecare rol sunt gestionate numele si descrierea.

Sunt afisate si numarul de utilizatori asociati fiecarui rol.

Rolurile care au utilizatori asociati nu pot fi sterse.

Pagina include cautare dupa numele rolului.

### 3.8. Imprumuturi

**Ruta:** `/imprumuturi`

Pagina permite adaugarea, afisarea, modificarea si stergerea imprumuturilor.

Informatiile gestionate sunt:

- Cititorul
- Exemplarul imprumutat
- Data imprumutului
- Data scadentei
- Data returnarii
- Statusul imprumutului

Cititorii si exemplarele pot fi cautate prin intermediul campurilor de introducere cu sugestii.

La adaugare este verificat daca utilizatorul exista si are contul activ.

Sunt validate datele calendaristice pentru a preveni introducerea unei scadente sau returnari anterioare datei imprumutului.

Pagina include cautare dupa cititor, carte si codul exemplarului.

### 3.9. Rezervari

**Ruta:** `/rezervari`

Pagina permite adaugarea, afisarea, modificarea si stergerea rezervarilor.

Informatiile gestionate sunt:

- Cititorul
- Cartea rezervata
- Data rezervarii
- Data expirarii
- Statusul rezervarii

Cititorii si cartile pot fi cautate dupa nume, respectiv titlu.

La adaugare este verificat daca utilizatorul exista si este activ.

Data expirarii nu poate fi anterioara datei rezervarii.

Pagina include cautare dupa cititor sau titlul cartii.

## 4. Descrierea paginilor interfetei

### 4.1. Pagina principala

**Ruta:** `/`

Pagina principala prezinta titlul aplicatiei si meniul de navigare catre cele opt sectiuni de administrare.

### 4.2. Pagina Categorii

Afiseaza categoriile existente si formularele necesare pentru adaugarea, modificarea si stergerea acestora.

### 4.3. Pagina Autori

Afiseaza autorii existenti si permite gestionarea informatiilor acestora prin formulare HTML.

### 4.4. Pagina Carti

Afiseaza cartile intr-un tabel compact.

Include un camp de cautare si butoane pentru adaugare, modificare si stergere.

Formularele sunt afisate in ferestre modale.

### 4.5. Pagina Exemplare

Afiseaza exemplarele impreuna cu titlul cartii, codul de inventar, starea si data achizitiei.

Include cautare si formulare modale pentru operatiile CRUD.

### 4.6. Pagina Utilizatori

Afiseaza informatiile utilizatorilor intr-un tabel.

Include cautare, selectarea rolului, gestionarea parolelor si posibilitatea activarii sau dezactivarii conturilor.

### 4.7. Pagina Roluri

Afiseaza rolurile existente, descrierile acestora si numarul utilizatorilor asociati.

Include cautare si formulare modale pentru adaugare si modificare.

### 4.8. Pagina Imprumuturi

Afiseaza imprumuturile impreuna cu cititorul, cartea, exemplarul, datele calendaristice si statusul.

Include cautare si formulare pentru operatiile CRUD.

### 4.9. Pagina Rezervari

Afiseaza rezervarile impreuna cu cititorul, cartea, datele calendaristice si statusul.

Include cautare si formulare pentru operatiile CRUD.

## 5. Validarea datelor si integritatea referentiala

Aplicatia utilizeaza validari in Flask si constrangerile definite in PostgreSQL.

Sunt tratate urmatoarele situatii:

- Campuri obligatorii necompletate.
- Date introduse in format invalid.
- Valori duplicate pentru campurile unice.
- Referinte catre inregistrari inexistente.
- Incercari de stergere a unor inregistrari referite de alte tabele.
- Date calendaristice introduse intr-o ordine incorecta.

Operatiile SQL folosesc interogari parametrizate.

## 6. Testarea operatiilor CRUD

Functionalitatile au fost testate manual in browser, utilizand aplicatia Flask conectata la PostgreSQL.

Au fost verificate operatiile de:

| Operatie | Descriere |
|---|---|
| CREATE | Adaugarea unei inregistrari |
| READ | Afisarea inregistrarilor |
| UPDATE | Modificarea unei inregistrari |
| DELETE | Stergerea unei inregistrari |

Pentru verificarea operatiilor au fost folosite inregistrari demonstrative si date create temporar.

Au fost testate succesiv paginile pentru categorii, autori, exemplare, utilizatori, roluri, imprumuturi si rezervari.

Pagina cartilor a fost implementata si reorganizata pentru imbunatatirea utilizarii interfetei.

## 7. Limitari ale implementarii

In aceasta etapa au fost implementate operatiile CRUD, fara automatizarea tuturor regulilor specifice activitatii unei biblioteci.

Nu sunt implementate:

- Actualizarea automata a starii exemplarului la imprumut sau returnare.
- Verificarea automata a imprumuturilor active suprapuse.
- Verificarea disponibilitatii unei carti inainte de rezervare.
- Prevenirea automata a rezervarilor active suprapuse.
- Autentificarea utilizatorilor si restrictionarea accesului in functie de rol.

Aceste functionalitati nu sunt prezentate ca fiind finalizate.

## 8. Concluzie

Etapa 2 a proiectului a avut ca obiectiv implementarea operatiilor CRUD si realizarea interfetelor de administrare.

Au fost implementate operatiile de creare, citire, actualizare si stergere pentru entitatile sistemului.

Relatia dintre carti si autori este gestionata direct din interfata de administrare a cartilor.

Aplicatia foloseste Flask pentru logica backend, PostgreSQL pentru stocarea datelor si HTML, CSS si JavaScript pentru realizarea interfetelor.

Functionalitatile implementate au fost verificate manual, iar mecanismul de initializare a datelor demonstrative din Etapa 1 a fost pastrat.