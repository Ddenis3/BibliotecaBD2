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
