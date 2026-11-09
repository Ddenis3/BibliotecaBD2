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