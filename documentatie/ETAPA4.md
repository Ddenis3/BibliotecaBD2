\# ETAPA 4 – Performanta: indecsi si load testing



\## 1. Informatii generale



\*\*Proiect:\*\* Sistem de Gestionare a unei Biblioteci  

\*\*Disciplina:\*\* Baze de Date II  

\*\*Tehnologii:\*\* PostgreSQL 18, Python, Flask, psycopg



\### Obiectiv



Obiectivul Etapei 4 este evaluarea si imbunatatirea performantei interogarilor SQL, precum si testarea comportamentului aplicatiei sub sarcina.



Conform cerintelor proiectului, etapa include:



1\. Implementarea si justificarea indecsilor folosind planuri de executie inainte si dupa optimizare.

2\. Testarea API-ului sub sarcina, cu rezultate masurate.



Pentru analiza SQL a fost utilizat PostgreSQL 18 si comanda `EXPLAIN (ANALYZE, BUFFERS)`.



Pentru testarea aplicatiei Flask a fost implementat un script Python care simuleaza mai multe sesiuni autentificate si executa cereri HTTP concurente.



\## 2. Analiza initiala a bazei de date



Baza de date a aplicatiei contine noua tabele.



Numarul initial de inregistrari este prezentat mai jos.



| Tabel | Numar inregistrari |

|---|---:|

| autori | 15 |

| autori\_carti | 20 |

| carti | 20 |

| categorii | 8 |

| exemplare | 30 |

| imprumuturi | 10 |

| rezervari | 5 |

| roluri | 3 |

| utilizatori | 10 |

| \*\*Total\*\* | \*\*121\*\* |



Au fost identificati 15 indecsi existenti.



Majoritatea sunt asociati cheilor primare si constrangerilor `UNIQUE`.



Exista si indexul partial unic `idx\_imprumut\_activ\_unic`, utilizat pentru respectarea unei constrangeri asupra imprumuturilor active.



Acesti indecsi nu au fost eliminati sau modificati.



\### 2.1. Analiza initiala a tabelului imprumuturi



A fost executata o interogare care identifica imprumuturile unui cititor si le ordoneaza dupa data imprumutului.



Rezultatele au fost:



| Indicator | Valoare |

|---|---|

| Numar total de imprumuturi | 10 |

| Inregistrari returnate | 2 |

| Metoda de acces | Seq Scan |

| Sortare | Quicksort |

| Planning Time | 0.488 ms |

| Execution Time | 0.600 ms |



PostgreSQL a ales scanarea secventiala deoarece tabelul contine foarte putine inregistrari.



Pe un tabel atat de mic, un index suplimentar nu garanteaza o imbunatatire masurabila.



Din acest motiv, testarea indecsilor a fost realizata pe un volum mai mare de date.



\## 3. Pregatirea datelor pentru testare



Pentru evaluarea performantei a fost creat tabelul separat:



`imprumuturi\_perf\_test`



Tabelul contine urmatoarele coloane:



\- `id`

\- `cititor\_id`

\- `exemplar\_id`

\- `data\_imprumut`

\- `data\_scadenta`

\- `status`



Au fost generate \*\*100.000 de inregistrari demonstrative\*\*, folosind functia PostgreSQL `generate\_series()`.



Datele contin 1.000 de identificatori distincti de cititori si 5.000 de identificatori distincti de exemplare.



Au fost generate imprumuturi cu statusurile:



\- `activ`

\- `returnat`

\- `intarziat`



Dupa introducerea datelor a fost executata comanda:



`ANALYZE imprumuturi\_perf\_test;`



Aceasta actualizeaza statisticile utilizate de optimizatorul PostgreSQL.



\### Motivul utilizarii unui tabel separat



Tabelul de test este independent de cele noua tabele principale ale bibliotecii.



Astfel:



\- Datele existente nu sunt modificate.

\- Relatiile bazei de date nu sunt afectate.

\- Operatiile CRUD continua sa functioneze.

\- Testele pot fi reproduse fara introducerea unor imprumuturi fictive in aplicatie.



Rezultatele demonstrarii indecsilor se refera la tabelul separat de test, nu la o accelerare masurata direct asupra tabelelor principale.



Scriptul utilizat este salvat in:



`etapa4\_performanta.sql`



\## 4. Testul 1 – Index compus



\### 4.1. Obiectiv



Primul test urmareste optimizarea unei interogari care cauta imprumuturile unui anumit cititor si le ordoneaza descrescator dupa data imprumutului.



Interogarea analizata este:



```sql

SELECT

&#x20;   id,

&#x20;   cititor\_id,

&#x20;   exemplar\_id,

&#x20;   data\_imprumut,

&#x20;   data\_scadenta,

&#x20;   status

FROM imprumuturi\_perf\_test

WHERE cititor\_id = 500

ORDER BY data\_imprumut DESC;

```



\### 4.2. Rezultatul inainte de indexare



A fost executata comanda:



`EXPLAIN (ANALYZE, BUFFERS)`



Rezultatele au fost:



| Indicator | Valoare |

|---|---:|

| Inregistrari totale | 100.000 |

| Inregistrari returnate | 100 |

| Metoda de acces | Seq Scan |

| Randuri eliminate prin filtrare | 99.900 |

| Metoda de sortare | Quicksort |

| Memorie sortare | 30 KB |

| Buffers shared hit | 804 |

| Planning Time | 2.990 ms |

| Execution Time | 7.442 ms |



PostgreSQL a parcurs tabelul pentru a identifica imprumuturile cititorului 500.



Din cele 100.000 de inregistrari au fost selectate 100, iar rezultatele au fost sortate dupa data imprumutului.



\### 4.3. Crearea indexului



Pentru optimizare a fost creat urmatorul index:



```sql

CREATE INDEX idx\_perf\_imprumuturi\_cititor\_data

ON imprumuturi\_perf\_test (

&#x20;   cititor\_id,

&#x20;   data\_imprumut DESC

);

```



Este un index compus de tip B-tree.



Prima coloana, `cititor\_id`, permite identificarea imprumuturilor unui anumit cititor.



A doua coloana, `data\_imprumut DESC`, corespunde criteriului de ordonare utilizat de interogare.



Dupa crearea indexului, au fost actualizate statisticile tabelului folosind `ANALYZE`.



\### 4.4. Rezultatul dupa indexare



A fost executata aceeasi interogare.



| Indicator | Valoare |

|---|---:|

| Inregistrari returnate | 100 |

| Metoda de acces | Bitmap Index Scan + Bitmap Heap Scan |

| Sortare | Quicksort |

| Buffers shared hit | 100 |

| Buffers shared read | 2 |

| Planning Time | 0.401 ms |

| Execution Time | 0.194 ms |



PostgreSQL a utilizat indexul pentru identificarea inregistrarilor relevante.



Optimizatorul a ales `Bitmap Heap Scan`, ceea ce a necesitat mentinerea unei operatii separate de sortare.



Acest comportament nu reprezinta o eroare, deoarece PostgreSQL selecteaza planul estimat ca fiind eficient.



\### 4.5. Comparatia rezultatelor



| Indicator | Fara index | Cu index |

|---|---:|---:|

| Metoda de acces | Seq Scan | Bitmap Index Scan + Bitmap Heap Scan |

| Inregistrari returnate | 100 | 100 |

| Buffers executie | 804 hit | 100 hit + 2 read |

| Execution Time | 7.442 ms | 0.194 ms |



\*\*Accelerare observata: aproximativ 38,36 ori.\*\*



\*\*Reducerea timpului de executie: aproximativ 97,39%.\*\*



Indexul compus a redus semnificativ timpul necesar identificarii imprumuturilor cititorului.



\## 5. Testul 2 – Index partial



\### 5.1. Obiectiv



Al doilea test urmareste optimizarea cautarii imprumuturilor active care au scadenta intr-un anumit interval calendaristic.



Interogarea analizata este:



```sql

SELECT

&#x20;   id,

&#x20;   cititor\_id,

&#x20;   exemplar\_id,

&#x20;   data\_imprumut,

&#x20;   data\_scadenta,

&#x20;   status

FROM imprumuturi\_perf\_test

WHERE status = 'activ'

&#x20; AND data\_scadenta BETWEEN

&#x20;     DATE '2024-01-01'

&#x20;     AND DATE '2024-01-31'

ORDER BY data\_scadenta DESC

LIMIT 30;

```



Interogarea returneaza maximum 30 de imprumuturi active, ordonate descrescator dupa data scadentei.



\### 5.2. Rezultatul inainte de indexare



Au fost obtinute urmatoarele rezultate:



| Indicator | Valoare |

|---|---:|

| Inregistrari totale | 100.000 |

| Inregistrari care respecta filtrul | 517 |

| Inregistrari returnate | 30 |

| Metoda de acces | Seq Scan |

| Randuri eliminate prin filtrare | 99.483 |

| Metoda de sortare | Top-N Heapsort |

| Memorie sortare | 28 KB |

| Buffers shared hit | 804 |

| Planning Time | 0.116 ms |

| Execution Time | 6.486 ms |



PostgreSQL a parcurs intregul tabel si a identificat 517 imprumuturi care respectau conditiile.



Ulterior a selectat primele 30 de rezultate dupa ordonare.



\### 5.3. Crearea indexului partial



A fost creat urmatorul index:



```sql

CREATE INDEX idx\_perf\_imprumuturi\_active\_scadenta

ON imprumuturi\_perf\_test (

&#x20;   data\_scadenta DESC

)

WHERE status = 'activ';

```



Indexul este partial deoarece include numai inregistrarile cu statusul `activ`.



Aceasta abordare evita indexarea imprumuturilor cu alte statusuri, care nu sunt relevante pentru interogarea analizata.



Coloana `data\_scadenta DESC` permite parcurgerea imprumuturilor in ordinea solicitata.



\### 5.4. Rezultatul dupa indexare



Dupa crearea indexului si actualizarea statisticilor, au fost obtinute urmatoarele rezultate:



| Indicator | Valoare |

|---|---:|

| Inregistrari returnate | 30 |

| Metoda de acces | Index Scan |

| Sortare separata | Nu |

| Buffers shared hit | 30 |

| Buffers shared read | 2 |

| Planning Time | 1.680 ms |

| Execution Time | 0.116 ms |



PostgreSQL a utilizat indexul partial pentru identificarea imprumuturilor active din intervalul cautat.



Rezultatele au putut fi returnate direct in ordinea necesara, fara o operatie suplimentara de sortare.



Datorita clauzei `LIMIT 30`, executia s-a oprit dupa obtinerea numarului solicitat de rezultate.



\### 5.5. Comparatia rezultatelor



| Indicator | Fara index | Cu index |

|---|---:|---:|

| Metoda de acces | Seq Scan | Index Scan |

| Sortare separata | Da | Nu |

| Buffers executie | 804 hit | 30 hit + 2 read |

| Execution Time | 6.486 ms | 0.116 ms |



\*\*Accelerare observata: aproximativ 55,91 ori.\*\*



\*\*Reducerea timpului de executie: aproximativ 98,21%.\*\*



Indexul partial a eliminat scanarea completa a tabelului si operatia separata de sortare.



\## 6. Concluziile testarii indecsilor



Cele doua optimizari au produs urmatoarele rezultate:



| Test | Fara index | Cu index | Accelerare |

|---|---:|---:|---:|

| Imprumuturi dupa cititor | 7.442 ms | 0.194 ms | 38,36x |

| Imprumuturi active dupa scadenta | 6.486 ms | 0.116 ms | 55,91x |



Rezultatele confirma ca indecsii pot reduce timpul de executie al interogarilor care filtreaza si ordoneaza date din tabele mari.



Indexul compus este justificat prin utilizarea coloanelor `cititor\_id` si `data\_imprumut`.



Indexul partial este justificat prin filtrarea exclusiva a imprumuturilor active si ordonarea acestora dupa data scadentei.



\*\*Limitarea comparatiei:\*\* rezultatele provin din cate o executie masurata inainte si dupa indexare. Duratele pot varia in functie de cache, sistemul de operare si incarcarea serverului PostgreSQL.



Aceste valori reprezinta accelerari observate in testele efectuate, nu performante garantate.



De asemenea, indecsii au fost creati pe tabelul `imprumuturi\_perf\_test`. Nu a fost masurata o imbunatatire echivalenta pe tabelul real `imprumuturi`.



\## 7. Load testing – Testarea aplicatiei Flask



\### 7.1. Obiectiv



A doua componenta a Etapei 4 consta in testarea aplicatiei sub sarcina.



Pentru aceasta a fost creat fisierul:



`load\_test.py`



Scriptul foloseste biblioteca standard Python si `ThreadPoolExecutor` pentru trimiterea cererilor HTTP concurente.



\### 7.2. Endpointul testat



A fost ales endpointul:



`GET /carti`



Acesta permite afisarea catalogului bibliotecii.



La accesarea paginii, aplicatia executa interogari PostgreSQL pentru obtinerea cartilor, autorilor, categoriilor si asocierilor dintre carti si autori.



Rezultatul este transmis catre template-ul HTML `carti.html`.



\### 7.3. Autentificarea in timpul testului



Deoarece aplicatia utilizeaza autentificare si protectie CSRF, scriptul realizeaza autentificarea inainte de executarea cererilor.



Pentru fiecare sesiune simulata:



1\. Acceseaza pagina `/login`.

2\. Extrage tokenul CSRF.

3\. Trimite emailul, parola si tokenul.

4\. Pastreaza cookie-ul de sesiune.

5\. Executa cererile HTTP catre `/carti`.



Testele au utilizat acelasi cont demonstrativ de Administrator in sesiuni separate.



Parola nu este salvata in script.



\### 7.4. Indicatorii masurati



Au fost urmariti:



\- Numarul total de cereri.

\- Numarul cererilor reusite.

\- Numarul erorilor.

\- Timpul total de executie.

\- Timpul mediu de raspuns.

\- Timpul minim si maxim.

\- Percentila P95.

\- Throughput-ul, exprimat in cereri pe secunda.



Timpii individuali de raspuns masoara cererile catre `/carti`.



Timpul total al testului include si autentificarea sesiunilor, deoarece aceasta are loc dupa pornirea cronometrului general.



\## 8. Load test 1 – Cinci sesiuni simultane



\### 8.1. Configuratie



\- Sesiuni simultane: 5.

\- Cereri per sesiune: 20.

\- Total cereri: 100.

\- Endpoint: `GET /carti`.



\### 8.2. Rezultate



| Indicator | Valoare |

|---|---:|

| Cereri totale | 100 |

| Cereri reusite | 100 |

| Erori | 0 |

| Timp total | 4.778 s |

| Timp mediu | 184.738 ms |

| Timp minim | 106.232 ms |

| Timp maxim | 343.513 ms |

| P95 | 275.953 ms |

| Throughput | 20.93 cereri/s |



\### 8.3. Interpretare



Toate cele 100 de cereri HTTP au fost procesate cu succes.



Nu au fost inregistrate erori.



Timpul mediu de raspuns a fost de aproximativ 185 ms.



Aproximativ 95% dintre cereri au avut un timp de raspuns de cel mult 276 ms.



\## 9. Load test 2 – Zece sesiuni simultane



\### 9.1. Configuratie



\- Sesiuni simultane: 10.

\- Cereri per sesiune: 20.

\- Total cereri: 200.

\- Endpoint: `GET /carti`.



\### 9.2. Rezultate



| Indicator | Valoare |

|---|---:|

| Cereri totale | 200 |

| Cereri reusite | 200 |

| Erori | 0 |

| Timp total | 5.580 s |

| Timp mediu | 234.170 ms |

| Timp minim | 107.741 ms |

| Timp maxim | 441.944 ms |

| P95 | 331.570 ms |

| Throughput | 35.84 cereri/s |



\### 9.3. Interpretare



Aplicatia a procesat toate cele 200 de cereri fara erori.



Timpul mediu de raspuns a crescut fata de primul test, deoarece numarul sesiunilor concurente a fost mai mare.



Throughput-ul a crescut, ceea ce indica faptul ca serverul a procesat mai multe solicitari pe secunda in configuratia testata.



\## 10. Compararea testelor de incarcare



| Indicator | 5 sesiuni | 10 sesiuni |

|---|---:|---:|

| Cereri totale | 100 | 200 |

| Cereri reusite | 100 | 200 |

| Erori | 0 | 0 |

| Timp total | 4.778 s | 5.580 s |

| Timp mediu | 184.738 ms | 234.170 ms |

| Timp minim | 106.232 ms | 107.741 ms |

| Timp maxim | 343.513 ms | 441.944 ms |

| P95 | 275.953 ms | 331.570 ms |

| Throughput | 20.93 cereri/s | 35.84 cereri/s |



La dublarea numarului de sesiuni concurente:



\- Throughput-ul a crescut cu aproximativ 71,2%.

\- Timpul mediu de raspuns a crescut cu aproximativ 26,8%.

\- P95 a crescut cu aproximativ 20,2%.

\- Numarul de erori a ramas zero.



Rezultatele arata ca aplicatia a gestionat cu succes ambele niveluri de incarcare.



Cresterea concurentei a permis procesarea unui numar mai mare de cereri pe secunda, dar a determinat si cresterea timpilor individuali de raspuns.



\### Limitari



Testele au fost executate local, folosind serverul de dezvoltare Flask.



Au fost utilizate sesiuni autentificate separate, dar acelasi cont de utilizator.



Au fost testate cereri de citire a catalogului, nu operatii de scriere concurente.



Rezultatele nu reprezinta o evaluare completa a comportamentului aplicatiei intr-un mediu de productie.



Nu a fost realizata o comparatie directa a throughput-ului aplicatiei inainte si dupa crearea indecsilor de test.



\## 11. Fisierele utilizate



| Fisier | Rol |

|---|---|

| `app.py` | Aplicatia Flask |

| `database.py` | Conexiunea PostgreSQL |

| `fixtures.py` | Initializarea datelor demonstrative |

| `load\_test.py` | Testarea aplicatiei sub sarcina |

| `etapa4\_performanta.sql` | Reproducerea testelor SQL |

| `documentatie/ETAPA4.md` | Documentarea rezultatelor |



\## 12. Concluzie



In Etapa 4 au fost analizate performanta interogarilor PostgreSQL si comportamentul aplicatiei Flask sub sarcina.



Au fost implementati si evaluati doi indecsi pe un tabel demonstrativ cu 100.000 de inregistrari.



Primul index, compus, a redus timpul masurat de la 7.442 ms la 0.194 ms.



Al doilea index, partial, a redus timpul masurat de la 6.486 ms la 0.116 ms.



Planurile `EXPLAIN (ANALYZE, BUFFERS)` au demonstrat schimbarea metodelor de acces la date si reducerea numarului de pagini accesate in executiile masurate.



Au fost efectuate si doua teste de incarcare asupra endpointului `GET /carti`.



Aplicatia a procesat 100 de cereri cu 5 sesiuni simultane si 200 de cereri cu 10 sesiuni simultane, fara erori.



Rezultatele au fost obtinute prin executarea efectiva a testelor si sunt documentate pentru a permite explicarea si reproducerea acestora.

