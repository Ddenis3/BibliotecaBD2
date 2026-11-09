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