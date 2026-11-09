# DECISIONS – Sistem de Gestionare a unei Biblioteci

## Etapa 1 – Modelare

### 1. Alegerea PostgreSQL

A fost ales PostgreSQL deoarece este un sistem de gestionare a bazelor de date relaționale, gratuit și potrivit pentru implementarea relațiilor, constrângerilor și operațiilor SQL avansate.

### 2. Alegerea Python și Flask

Python și Flask au fost alese pentru dezvoltarea backendului datorită structurii relativ simple și posibilității de conectare la PostgreSQL.

### 3. Utilizarea a 9 tabele

Au fost definite 9 tabele pentru separarea logică a informațiilor și reducerea redundanței.

Această organizare permite gestionarea independentă a utilizatorilor, cărților, autorilor, exemplarelor, împrumuturilor și rezervărilor.

### 4. Separarea cărților de exemplare

Tabelul `carti` conține informațiile bibliografice ale unei cărți.

Tabelul `exemplare` conține informațiile despre fiecare exemplar fizic disponibil în bibliotecă.

Această separare permite gestionarea mai multor exemplare ale aceleiași cărți.

### 5. Relația dintre cărți și autori

A fost utilizat tabelul intermediar `autori_carti` deoarece relația este de tip N:M.

O carte poate avea mai mulți autori, iar un autor poate fi asociat cu mai multe cărți.

### 6. Gestionarea utilizatorilor și rolurilor

Rolurile au fost separate într-un tabel dedicat, pentru a permite atribuirea drepturilor de acces în etapele următoare.

Au fost definite trei roluri: Administrator, Bibliotecar și Cititor.

### 7. Implementarea fixtures

A fost creat fișierul `fixtures.py`, care introduce automat datele demonstrative la pornirea aplicației.

Mecanismul verifică existența înregistrărilor pentru a evita duplicarea datelor.

### 8. Constrângeri de integritate

Au fost utilizate chei primare, chei străine și constrângeri precum NOT NULL, UNIQUE și CHECK pentru prevenirea datelor invalide.

Aceste reguli asigură integritatea modelului relațional și reduc riscul apariției înregistrărilor inconsistente.


---

## Etapa 2 – Operații CRUD și interfață

### 9. Implementarea CRUD pentru toate entitățile

S-a decis implementarea operațiilor Create, Read, Update și Delete pentru toate entitățile sistemului.

Această decizie respectă cerința proiectului privind administrarea completă a datelor.

Au fost implementate operații CRUD pentru:

- Categorii
- Autori
- Cărți
- Exemplare
- Utilizatori
- Roluri
- Împrumuturi
- Rezervări

Relația dintre autori și cărți este gestionată separat la nivelul datelor, dar integrată în interfața pentru cărți.

### 10. Utilizarea rutelor Flask

Pentru fiecare entitate au fost definite rute Flask pentru afișare, adăugare, modificare și ștergere.

Această organizare permite separarea operațiilor și simplifică identificarea funcționalităților.

### 11. Utilizarea interogărilor parametrizate

Operațiile SQL utilizează parametri în locul concatenării directe a valorilor introduse de utilizator.

Această abordare reduce riscul de SQL injection și permite transmiterea controlată a datelor către PostgreSQL.

### 12. Separarea paginilor CRUD

Fiecare entitate principală are propria pagină HTML.

Această organizare permite administrarea independentă a informațiilor și facilitează navigarea în aplicație.

### 13. Gestionarea relației autori–cărți

S-a decis integrarea gestionării tabelului `autori_carti` în pagina `carti.html`.

Motivul este că asocierea autorilor reprezintă o operație naturală în cadrul administrării unei cărți.

Astfel, nu este necesară o pagină separată pentru tabelul de legătură.

Utilizatorul poate selecta unul sau mai mulți autori atunci când adaugă sau modifică o carte.

### 14. Utilizarea tabelelor compacte

Prima variantă a interfeței pentru cărți afișa toate formularele de modificare direct în pagină.

Această soluție a fost considerată nepractică deoarece ocupa prea mult spațiu.

S-a decis afișarea înregistrărilor într-un tabel compact, cu acțiuni separate pentru fiecare rând.

Aceeași structură a fost adoptată pentru celelalte pagini CRUD dezvoltate ulterior.

### 15. Utilizarea ferestrelor modale

Pentru paginile cu tabele compacte, formularele de adăugare și modificare sunt afișate în ferestre modale.

Această soluție permite păstrarea unei interfețe simple și evită afișarea permanentă a formularelor.

### 16. Implementarea căutării

S-a decis utilizarea JavaScript pentru filtrarea înregistrărilor afișate în interfață.

Căutarea permite identificarea mai rapidă a cărților, exemplarelor, utilizatorilor, rolurilor, împrumuturilor și rezervărilor.

Filtrarea este realizată la nivelul datelor deja încărcate în pagină.

### 17. Selectarea autorilor prin căutare

Lista inițială de checkbox-uri a fost înlocuită cu un câmp de căutare cu sugestii.

Această variantă este mai practică atunci când există un număr mare de autori.

Autorii selectați sunt transformați în ID-uri și transmiși backendului.

### 18. Selectarea categoriilor existente

Categoria unei cărți este introdusă într-un câmp text cu sugestii.

Aplicația acceptă selectarea unei categorii existente în baza de date și transmite ID-ul corespunzător.

Această decizie păstrează relația dintre `carti` și `categorii` și evită crearea accidentală a unor categorii duplicate.

Categoriile noi sunt gestionate din pagina dedicată.

### 19. Utilizarea căutării pentru entitățile asociate

În formularele pentru exemplare, împrumuturi și rezervări, înregistrările asociate pot fi căutate după informații relevante.

Exemple:

- Carte după titlu.
- Cititor după nume.
- Exemplar după titlul cărții și codul de inventar.

În interfață sunt utilizate etichete care includ ID-ul înregistrării pentru identificarea corectă a elementului selectat.

### 20. Gestionarea parolelor

S-a decis utilizarea funcției `generate_password_hash()` pentru parolele introduse prin interfața de administrare a utilizatorilor.

Parolele noi nu sunt salvate în text simplu.

La modificarea unui utilizator, parola existentă este păstrată dacă nu este introdusă o parolă nouă.

### 21. Tratarea erorilor de integritate

S-a decis utilizarea constrângerilor PostgreSQL și a tratării excepțiilor în Flask.

Sunt tratate situații precum:

- Valori duplicate.
- Referințe inexistente.
- Încălcarea constrângerilor CHECK.
- Lipsa informațiilor obligatorii.

Pentru anumite înregistrări, ștergerea este restricționată atunci când există date asociate.

### 22. Validarea datelor calendaristice

Pentru împrumuturi și rezervări au fost introduse verificări privind ordinea datelor.

În cazul împrumuturilor:

- Data scadenței nu poate fi anterioară datei împrumutului.
- Data returnării nu poate fi anterioară datei împrumutului.

În cazul rezervărilor:

- Data expirării nu poate fi anterioară datei rezervării.

Aceste reguli sunt verificate înainte de salvarea datelor.

### 23. Păstrarea mecanismului fixtures

S-a decis păstrarea funcției `initialize_fixtures()` din Etapa 1.

Aceasta este apelată la pornirea aplicației pentru a permite inițializarea datelor demonstrative.

Nu a fost necesară modificarea structurii bazei de date pentru implementarea operațiilor CRUD.

### 24. Separarea funcționalităților CRUD de regulile suplimentare

Etapa 2 urmărește implementarea operațiilor CRUD și a interfețelor corespunzătoare.

S-a decis documentarea separată a unor reguli de business care nu sunt încă implementate.

Exemple:

- Actualizarea automată a stării exemplarelor la împrumut și returnare.
- Prevenirea împrumuturilor active suprapuse.
- Verificarea disponibilității cărților înainte de rezervare.
- Prevenirea rezervărilor active suprapuse.

Aceste funcționalități nu sunt considerate finalizate în Etapa 2.

### 25. Amânarea designului vizual final

S-a decis prioritizarea funcționalităților CRUD și a unei interfețe utilizabile.

Designul vizual final, inclusiv culorile, fonturile și organizarea generală a meniurilor, poate fi realizat ulterior.

Această abordare permite verificarea funcționalităților înainte de aplicarea stilizării finale.

---

## Etapa 3 – Autentificare si roluri

### 26. Pastrarea logicii Python intr-un singur fisier

S-a decis integrarea autentificarii si autorizarii in `app.py`, fara un modul Python separat pentru acestea.

Motivul este usurinta intelegerii, urmaririi si prezentarii codului in contextul proiectului universitar. Paginile HTML raman organizate separat in `templates/`.

### 27. Autentificare cu email si parola

S-a ales autentificarea pe baza adresei de email si a parolei, folosind datele existente in tabelul `utilizatori`.

Nu au fost necesare tabele suplimentare sau un serviciu extern de autentificare.

### 28. Stocarea parolelor sub forma de hash

Parolele noi sunt procesate folosind `generate_password_hash()`, iar la autentificare sunt verificate folosind `check_password_hash()` din Werkzeug.

Astfel, aplicatia nu trebuie sa stocheze parola in text simplu si nici sa o decripteze pentru verificare.

### 29. Utilizarea sesiunilor Flask in locul tokenurilor JWT

S-a ales mecanismul de sesiuni Flask deoarece aplicatia este o interfata web locala, cu formulare HTML si navigare obisnuita.

Dupa login este retinut numai ID-ul utilizatorului in `session["user_id"]`. Cookie-ul este semnat criptografic cu o cheie secreta persistenta; parola nu este salvata in sesiune.

### 30. Cheie secreta separata de cod

S-a ales pastrarea cheii de semnare a sesiunilor in variabila de mediu `FLASK_SECRET_KEY` sau in fisierul local `.flask_secret`.

Fisierul este exclus din Git pentru a evita publicarea secretului. Pe mediul local, cookie-ul nu este marcat `Secure`, deoarece serverul ruleaza prin HTTP; in productie trebuie folosit HTTPS.

### 31. Autorizare pe baza celor trei roluri existente

Au fost pastrate rolurile din baza de date: Administrator, Bibliotecar si Cititor.

Drepturile adoptate sunt:

- **Administrator:** acces la toate sectiunile si operatiile CRUD.
- **Bibliotecar:** gestionarea categoriilor, autorilor, cartilor, exemplarelor, imprumuturilor si rezervarilor; fara administrarea utilizatorilor si rolurilor.
- **Cititor:** vizualizarea categoriilor, autorilor si cartilor, fara operatii de modificare.

Aceste diferente respecta cerinta privind minimum trei roluri cu drepturi distincte.

### 32. Verificarea drepturilor in backend

S-a ales verificarea drepturilor inainte de procesarea fiecarei cereri protejate, prin `@app.before_request`.

La fiecare cerere se verifica utilizatorul din sesiune, existenta si starea contului in PostgreSQL, precum si rolul actual. Accesul nepermis returneaza HTTP 403.

Ascunderea butoanelor in HTML este doar o adaptare a interfetei si nu inlocuieste verificarea permisiunilor pe server.

### 33. Interfata adaptata rolului Cititor

S-a decis afisarea doar a informatiilor de catalog in paginile `categorii.html`, `autori.html` si `carti.html` pentru Cititor.

Administratorul si Bibliotecarul pastreaza formularele CRUD. Aceasta separare reduce confuzia in interfata si corespunde drepturilor efective aplicate in backend.

### 34. Protectia CSRF pentru formularele POST

S-a decis utilizarea Flask-WTF si a componentei `CSRFProtect(app)` pentru verificarea tokenurilor trimise in formularele POST.

Au fost adaugate campuri ascunse `csrf_token` in formularele existente, inclusiv login, logout si operatiile CRUD. O cerere POST fara token a fost respinsa de server, confirmand activarea protectiei.

### 35. Pastrarea compatibilitatii cu etapele anterioare

Nu a fost modificata schema PostgreSQL. Au fost pastrate datele demonstrative, conexiunea existenta si rutele CRUD implementate in Etapa 2.

Au fost actualizate dependentele proiectului pentru a include Flask-WTF, iar documentatia a fost completata cu `ETAPA3.md`.

### 36. Limitarea implementarii la cerintele proiectului

Nu s-au introdus JWT, OAuth, autentificare cu doi factori sau recuperare a parolei prin email, deoarece nu sunt necesare pentru cerintele Etapei 3.

S-a prioritizat o implementare simpla, care poate fi explicata si verificata la prezentarea proiectului.

