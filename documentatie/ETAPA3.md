# ETAPA 3 – Autentificare si roluri

## 1. Informatii generale

**Proiect:** Sistem de Gestionare a unei Biblioteci  
**Disciplina:** Baze de Date II  
**Tehnologii:** Python, Flask, PostgreSQL, HTML, JavaScript, Flask-WTF

### Obiectiv

Obiectivul Etapei 3 este implementarea autentificarii utilizatorilor si a unui sistem de autorizare bazat pe roluri.

Aplicatia trebuie sa permita accesul utilizatorilor autentificati si sa restrictioneze operatiile in functie de drepturile asociate fiecarui rol.

Au fost utilizate cele trei roluri definite in Etapa 1:

- Administrator
- Bibliotecar
- Cititor

## 2. Implementarea autentificarii

Autentificarea este implementata in fisierul `app.py`, folosind Flask si baza de date PostgreSQL.

Pagina de autentificare este definita in:

`templates/login.html`

### 2.1. Procesul de autentificare

Utilizatorul introduce:

- Adresa de email.
- Parola.

Formularul transmite datele catre ruta:

`POST /login`

Aplicatia executa o interogare parametrizata pentru identificarea utilizatorului dupa email.

Sunt recuperate ID-ul utilizatorului, hash-ul parolei si starea contului.

Parola introdusa este verificata folosind functia:

`check_password_hash()`

Autentificarea este acceptata numai daca parola este corecta si contul este activ.

In cazul autentificarii reusite, utilizatorul este redirectionat catre pagina principala.

In cazul unor date incorecte, este afisat un mesaj de eroare.

## 3. Stocarea parolelor

Parolele sunt gestionate folosind functiile din biblioteca `werkzeug.security`.

### 3.1. Generarea hash-ului

Pentru crearea unui utilizator sau modificarea parolei este utilizata functia:

`generate_password_hash()`

Aceasta genereaza un hash al parolei, care este salvat in coloana:

`utilizatori.parola_hash`

Parola noua nu este stocata in text simplu.

### 3.2. Verificarea parolei

La autentificare este folosita functia:

`check_password_hash()`

Aceasta compara parola introdusa cu hash-ul stocat in PostgreSQL.

Nu este necesara decriptarea parolei, deoarece verificarea se realizeaza direct prin intermediul algoritmului de hashing.

### 3.3. Configurarea parolelor initiale

Pentru conturile demonstrative existente a fost implementata posibilitatea configurarii parolei din terminal.

Comanda utilizata este:

`python app.py --set-password`

Aceasta permite identificarea utilizatorului dupa email si inlocuirea parolei existente cu un hash nou.

Parola este introdusa fara afisarea caracterelor in terminal.

## 4. Gestionarea sesiunilor

Aplicatia utilizeaza mecanismul de sesiuni oferit de Flask.

Dupa autentificarea reusita, ID-ul utilizatorului este salvat in sesiune:

`session["user_id"]`

Sesiunea este mentinuta prin intermediul unui cookie semnat criptografic de Flask.

Cookie-ul nu contine parola utilizatorului.

### 4.1. Cheia secreta

Pentru semnarea sesiunilor este utilizata o cheie secreta.

Aplicatia poate prelua cheia din variabila de mediu:

`FLASK_SECRET_KEY`

In lipsa acesteia, este utilizat fisierul local:

`.flask_secret`

Fisierul este exclus din repository prin `.gitignore`.

### 4.2. Configurarea sesiunii

Au fost utilizate urmatoarele setari:

| Setare | Rol |
|---|---|
| `SESSION_COOKIE_HTTPONLY` | Impiedica accesarea cookie-ului de sesiune prin JavaScript |
| `SESSION_COOKIE_SAMESITE` | Restrictioneaza anumite situatii de transmitere a cookie-ului intre site-uri |
| `PERMANENT_SESSION_LIFETIME` | Stabileste durata sesiunii |
| `SESSION_COOKIE_SECURE` | Controleaza transmiterea cookie-ului exclusiv prin HTTPS |

Aplicatia este rulata local prin HTTP, motiv pentru care `SESSION_COOKIE_SECURE` este configurat cu valoarea `False`.

Pentru o implementare accesibila prin HTTPS, aceasta setare trebuie activata.

### 4.3. Deconectarea

Deconectarea este implementata prin ruta:

`POST /logout`

La deconectare este executata operatia:

`session.clear()`

Aceasta elimina informatiile autentificarii din sesiunea curenta.

Utilizatorul este redirectionat catre pagina de login.

## 5. Implementarea rolurilor

Rolurile sunt stocate in tabelul:

`roluri`

Fiecare utilizator este asociat unui rol prin coloana:

`utilizatori.rol_id`

Relatia este realizata printr-o cheie straina.

### 5.1. Administrator

Administratorul are acces complet la functionalitatile aplicatiei.

Poate gestiona:

- Categorii
- Autori
- Carti
- Exemplare
- Utilizatori
- Roluri
- Imprumuturi
- Rezervari

Administratorul poate realiza operatiile CRUD pentru toate aceste entitati.

### 5.2. Bibliotecar

Bibliotecarul poate administra activitatea bibliotecii.

Are acces la operatiile CRUD pentru:

- Categorii
- Autori
- Carti
- Exemplare
- Imprumuturi
- Rezervari

Bibliotecarul nu poate accesa administrarea utilizatorilor si a rolurilor.

### 5.3. Cititor

Cititorul are acces limitat la consultarea catalogului.

Poate vizualiza:

- Categorii
- Autori
- Carti

Cititorul nu poate adauga, modifica sau sterge inregistrari.

De asemenea, nu poate accesa paginile de administrare a utilizatorilor, rolurilor, exemplarelor, imprumuturilor sau rezervarilor.

## 6. Matricea drepturilor de acces

| Functionalitate | Administrator | Bibliotecar | Cititor |
|---|---|---|---|
| Vizualizare categorii | Da | Da | Da |
| Modificare categorii | Da | Da | Nu |
| Vizualizare autori | Da | Da | Da |
| Modificare autori | Da | Da | Nu |
| Vizualizare carti | Da | Da | Da |
| Modificare carti | Da | Da | Nu |
| Gestionare exemplare | Da | Da | Nu |
| Gestionare utilizatori | Da | Nu | Nu |
| Gestionare roluri | Da | Nu | Nu |
| Gestionare imprumuturi | Da | Da | Nu |
| Gestionare rezervari | Da | Da | Nu |

## 7. Verificarea drepturilor

Autorizarea este implementata in backend, in fisierul `app.py`.

Este utilizat decoratorul Flask:

`@app.before_request`

Acesta permite executarea unei verificari inaintea procesarii cererilor HTTP.

Pentru fiecare cerere protejata, aplicatia:

1. Verifica existenta ID-ului utilizatorului in sesiune.
2. Identifica utilizatorul in PostgreSQL.
3. Verifica daca utilizatorul exista si este activ.
4. Identifica rolul asociat.
5. Verifica permisiunea de acces la ruta solicitata.

Daca utilizatorul nu este autentificat, acesta este redirectionat catre pagina de login.

Daca utilizatorul este autentificat, dar nu are drepturile necesare, aplicatia returneaza:

`HTTP 403 – Acces interzis`

Restrictiile sunt aplicate in backend, nu doar prin intermediul interfetei HTML.

## 8. Adaptarea interfetei

Interfata aplicatiei a fost adaptata pentru cele trei roluri.

### 8.1. Pagina principala

Pagina `index.html` afiseaza numele, emailul si rolul utilizatorului autentificat.

Meniul este adaptat drepturilor asociate rolului.

Administratorul vede toate sectiunile.

Bibliotecarul vede sectiunile necesare administrarii activitatii bibliotecii.

Cititorul vede sectiunile dedicate consultarii catalogului.

### 8.2. Pagina Categorii

Pentru Administrator si Bibliotecar sunt disponibile operatiile CRUD.

Pentru Cititor este afisat numai tabelul cu informatiile categoriilor.

### 8.3. Pagina Autori

Administratorul si Bibliotecarul au acces la formularele CRUD.

Cititorul poate consulta informatiile autorilor, fara posibilitatea modificarii acestora.

### 8.4. Pagina Carti

Administratorul si Bibliotecarul pot adauga, modifica si sterge carti.

Cititorul poate consulta catalogul, inclusiv titlul, ISBN-ul, categoria, autorii si anul publicarii.

Campul de cautare dupa titlu este disponibil pentru toate rolurile.

Pentru Cititor, formularele si butoanele CRUD nu sunt afisate.

## 9. Protectia CSRF

Pentru protejarea formularelor HTTP POST a fost utilizata biblioteca:

`Flask-WTF`

Protectia este activata prin:

`CSRFProtect(app)`

Fiecare formular POST include un camp ascuns care transmite un token CSRF.

Exemplu:

`<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`

La primirea cererii, tokenul este verificat automat.

Cererile fara token sau cu token invalid sunt respinse.

Protectia se aplica formularelor de autentificare, deconectare si operatiilor CRUD.

## 10. Testarea functionalitatilor

Aplicatia a fost executata local prin Flask, folosind PostgreSQL.

Au fost efectuate verificari ale autentificarii si interfetelor pentru cele trei roluri.

### 10.1. Testarea accesului

| Test | Rezultat asteptat |
|---|---|
| Acces fara autentificare | Redirectionare la login |
| Login cu date corecte | Autentificare reusita |
| Login cu date incorecte | Acces respins |
| Acces administrator | Toate sectiunile |
| Acces bibliotecar | Sectiunile bibliotecii |
| Acces cititor | Consultarea catalogului |
| Acces fara permisiune | HTTP 403 |
| Logout | Eliminarea sesiunii |

### 10.2. Testarea interfetei Cititor

Au fost verificate paginile:

- `/categorii`
- `/autori`
- `/carti`

Acestea afiseaza informatiile necesare consultarii catalogului fara formularele CRUD.

### 10.3. Testarea protectiei CSRF

A fost transmisa o cerere HTTP POST catre:

`/categorii/adauga`

Cererea nu continea token CSRF.

Serverul a respins solicitarea cu mesajul:

`The CSRF token is missing.`

Rezultatul confirma activarea protectiei CSRF pentru cererea testata.

## 11. Limitari

Implementarea este destinata proiectului universitar si rularii locale.

Nu au fost implementate functionalitati suplimentare precum:

- Autentificare cu furnizori externi.
- Autentificare in doi factori.
- Recuperarea automata a parolei prin email.
- Un sistem de administrare a sesiunilor de pe mai multe dispozitive.

Aceste functionalitati nu sunt necesare pentru cerintele Etapei 3.

Pentru utilizarea intr-un mediu de productie ar fi necesare masuri suplimentare, inclusiv HTTPS si configurarea adecvata a cookie-urilor de sesiune.

## 12. Concluzie

In Etapa 3 au fost implementate autentificarea utilizatorilor si autorizarea bazata pe roluri.

Parolele noi sunt stocate sub forma de hash-uri, iar sesiunile sunt gestionate prin mecanismul oferit de Flask.

Au fost definite drepturi diferite pentru Administrator, Bibliotecar si Cititor.

Accesul la rutele aplicatiei este verificat in backend, iar interfata este adaptata rolului utilizatorului autentificat.

Formularele POST sunt protejate impotriva cererilor fara token CSRF valid.

Implementarea pastreaza structura bazei de date si operatiile CRUD realizate in etapele anterioare.