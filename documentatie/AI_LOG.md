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


---

## Etapa 2 – Operații CRUD și interfață

### Instrument AI utilizat

ChatGPT – OpenAI

### Activități realizate cu asistență AI

1. Implementarea operațiilor CRUD pentru tabelul `categorii`.
2. Implementarea operațiilor CRUD pentru tabelul `autori`.
3. Implementarea operațiilor CRUD pentru tabelul `carti`.
4. Gestionarea relației N:M dintre cărți și autori prin tabelul `autori_carti`.
5. Implementarea operațiilor CRUD pentru tabelul `exemplare`.
6. Implementarea operațiilor CRUD pentru tabelul `utilizatori`.
7. Implementarea operațiilor CRUD pentru tabelul `roluri`.
8. Implementarea operațiilor CRUD pentru tabelul `imprumuturi`.
9. Implementarea operațiilor CRUD pentru tabelul `rezervari`.
10. Generarea rutelor Flask și a interogărilor SQL parametrizate.
11. Realizarea paginilor HTML pentru gestionarea entităților.
12. Implementarea formularelor de adăugare și modificare.
13. Implementarea căutării în tabele folosind JavaScript.
14. Implementarea validărilor pentru datele introduse.
15. Explicarea funcționalităților și a modului de testare.

### Modificări realizate în urma testării

**Modificarea 1 – Interfața pentru cărți**

Prima variantă a paginii `carti.html` afișa formularele de modificare pentru fiecare carte direct în pagină.

Această abordare ocupa mult spațiu și îngreuna utilizarea interfeței.

În urma evaluării, pagina a fost reorganizată folosind un tabel compact.

Formularele de adăugare și modificare sunt afișate în ferestre modale, doar atunci când utilizatorul solicită operația respectivă.

**Modificarea 2 – Selectarea autorilor**

Inițial, autorii unei cărți erau selectați prin intermediul unei liste de checkbox-uri.

Pentru a simplifica utilizarea, lista a fost înlocuită cu un câmp de căutare cu sugestii.

Utilizatorul poate introduce numele autorului și îl poate selecta dintre autorii existenți în baza de date.

Este permisă asocierea mai multor autori cu aceeași carte.

**Modificarea 3 – Selectarea categoriilor**

Selectarea categoriei unei cărți a fost modificată prin introducerea unui câmp text cu sugestii.

Categoria introdusă trebuie să existe în baza de date.

La salvare, aplicația identifică ID-ul categoriei selectate și îl transmite backendului Flask.

**Modificarea 4 – Reutilizarea structurii interfeței**

Structura compactă a paginii pentru cărți a fost utilizată și pentru paginile:

- Exemplare
- Utilizatori
- Roluri
- Împrumuturi
- Rezervări

Aceste pagini utilizează tabele, căutare și ferestre modale pentru operațiile de adăugare și modificare.

### Aspecte de securitate și validare

Cu ajutorul AI au fost implementate:

1. Interogări SQL parametrizate.
2. Validarea câmpurilor obligatorii.
3. Tratarea erorilor de unicitate.
4. Tratarea erorilor de integritate referențială.
5. Validarea relațiilor dintre înregistrări.
6. Validarea ordinii cronologice a datelor.
7. Generarea hash-urilor pentru parolele utilizatorilor.
8. Confirmarea operațiilor de ștergere.

Autentificarea utilizatorilor și restricționarea accesului în funcție de rol nu sunt implementate în această etapă.

### Testarea rezultatelor

Codul generat cu asistență AI a fost copiat în Visual Studio Code și executat local.

Aplicația a fost testată în browser folosind serverul Flask și baza de date PostgreSQL.

Au fost verificate manual operațiile de:

- Adăugare a înregistrărilor.
- Afișare a datelor.
- Modificare a înregistrărilor.
- Ștergere a înregistrărilor.

Pentru verificări au fost folosite datele demonstrative existente și înregistrări temporare create pentru testare.

Au fost testate succesiv paginile pentru categorii, autori, exemplare, utilizatori, roluri, împrumuturi și rezervări.

Interfața pentru cărți a fost implementată și modificată în urma observațiilor privind utilizarea acesteia.

### Limitări identificate

Operațiile CRUD pentru împrumuturi nu actualizează automat starea exemplarelor.

Nu este implementată verificarea automată a suprapunerii împrumuturilor pentru același exemplar.

Operațiile CRUD pentru rezervări nu verifică automat disponibilitatea cărților sau existența unor rezervări active suprapuse.

Aceste limitări sunt documentate și nu sunt prezentate ca funcționalități implementate.

### Responsabilitatea verificării

ChatGPT a fost utilizat ca instrument de asistență pentru generarea codului, explicarea soluțiilor și identificarea problemelor.

Codul a fost integrat și executat local, iar funcționalitățile au fost verificate manual în aplicație.

Deciziile privind organizarea interfeței și păstrarea funcționalităților au fost luate în urma evaluării rezultatelor.

---

## Etapa 3 – Autentificare si roluri

### Instrument AI utilizat

ChatGPT – OpenAI

### Activitati realizate cu asistenta AI

1. Analizarea cerintelor Etapei 3: autentificare, explicarea stocarii parolelor si minimum trei roluri cu drepturi diferite.
2. Implementarea rutelor `GET/POST /login` si `POST /logout` in fisierul existent `app.py`.
3. Implementarea verificarii parolelor prin `check_password_hash()` si pastrarea generarii de hash-uri cu `generate_password_hash()`.
4. Implementarea sesiunilor Flask prin stocarea ID-ului utilizatorului in `session["user_id"]`.
5. Implementarea verificarii autentificarii, starii contului si rolului la fiecare cerere protejata, folosind `@app.before_request`.
6. Definirea drepturilor distincte pentru Administrator, Bibliotecar si Cititor.
7. Crearea paginii `templates/login.html` si modificarea meniului din `templates/index.html` in functie de rol.
8. Adaptarea paginilor `categorii.html`, `autori.html` si `carti.html` astfel incat Cititorul sa vada doar informatiile, fara formularele CRUD.
9. Adaugarea protectiei CSRF prin Flask-WTF si a campurilor ascunse `csrf_token` in formularele POST.
10. Crearea unei copii de siguranta inainte de modificarea automata a formularelor si actualizarea dependentelor din `requirements.txt`.
11. Explicarea si documentarea modului de verificare a autentificarii, autorizarii si CSRF.

### Decizii si modificari in urma colaborarii

**Un singur fisier Python pentru logica aplicatiei.** A fost propusa initial separarea autentificarii intr-un modul `auth.py`, dar solutia a fost schimbata la cererea autorului proiectului: logica autentificarii si a drepturilor de acces a fost integrata direct in `app.py`. Fisierele HTML au ramas separate in `templates/`.

**Adaptarea interfetelor pentru Cititor.** In paginile Categorii, Autori si Carti au fost ascunse actiunile de adaugare, modificare si stergere pentru Cititor. Restrictiile de securitate sunt aplicate separat si in backend, nu doar prin ascunderea butoanelor.

**Protectie CSRF pentru formulare.** A fost utilizata biblioteca Flask-WTF (`Flask-WTF==1.3.0`). Pentru a pastra formularele CRUD existente, campurile CSRF au fost introduse in toate formularele POST identificate automat. Au fost raportate 20 de formulare actualizate in 10 fisiere HTML.

### Verificari efectuate

- Verificarea de sintaxa `python -m py_compile app.py` s-a incheiat fara erori.
- Serverul Flask a pornit pe `http://127.0.0.1:5000` si a confirmat initializarea datelor demonstrative pentru cele noua tabele.
- Au fost verificate vizual paginile Categorii, Autori si Carti pentru Cititor; formularele CRUD nu erau afisate.
- O cerere POST catre `/categorii/adauga`, trimisa fara token CSRF folosind PowerShell, a fost respinsa cu mesajul `The CSRF token is missing.`.
- Au fost parcurse testele de autentificare si de acces pe roluri in cadrul dezvoltarii locale. Verificarea negativa CSRF este confirmata explicit prin raspunsul serverului; celelalte teste trebuie pastrate in lista de verificare finala la prezentare.

### Limitari si aspecte de securitate

- Aplicatia este destinata demonstratiei locale, prin HTTP. Pentru publicare online sunt necesare HTTPS si `SESSION_COOKIE_SECURE=True`.
- Sistemul nu include autentificare cu doi factori, recuperarea parolei prin email sau autentificare cu furnizori externi; acestea nu fac parte din cerintele etapei.
- Protectia CSRF completeaza autorizarea: un token valid nu acorda drepturi de modificare unui Cititor.
- Cheia secreta pentru semnarea sesiunilor este pastrata local, in `.flask_secret`, exclus din Git; fisierul `.env` ramane de asemenea exclus din Git.

### Responsabilitatea verificarii

ChatGPT a oferit cod, explicatii si pasi de testare. Autorul proiectului a integrat modificarile, a executat aplicatia local si a verificat rezultatele afisate. Functionalitatile sunt descrise in `ETAPA3.md`.

