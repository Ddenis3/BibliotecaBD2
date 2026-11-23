# ETAPA 5 – Rapoarte PDF, CSV si Excel

## 1. Scop

Etapa 5 implementeaza exportul datelor din baza de date PostgreSQL in formatele PDF, CSV si Excel (.xlsx), direct din aplicatia Flask BibliotecaBD2. Nu s-au modificat cele noua tabele existente sau operatiile CRUD.

## 2. Functionalitati implementate

Pagina `/rapoarte` prezinta trei rapoarte:

| Tip raport | Continut | Coloane |
|---|---|---|
| Catalog carti | Titlurile si datele bibliografice | ID, Titlu, ISBN, Categorie, Editura, An publicare, Autori |
| Raport imprumuturi | Evidenta imprumuturilor | ID, Cititor, Carte, Cod exemplar, Data imprumut, Scadenta, Returnare, Status |
| Raport rezervari | Evidenta rezervarilor | ID, Cititor, Carte, Data rezervare, Data expirare, Status |

Fiecare card prezinta trei butoane de descarcare: PDF, Excel si CSV. Interfata foloseste designul dark mode existent.

## 3. Implementare

Logica rapoartelor este pastrata in `app.py`:

- `RAPOARTE_DISPONIBILE`: configuratia celor trei rapoarte, antetele si interogarile SQL;
- `date_raport(tip)`: executa interogarea in PostgreSQL si pregateste valorile pentru export;
- `GET /rapoarte`: afiseaza pagina `templates/rapoarte.html`;
- `GET /rapoarte/descarca/<tip>/<format_raport>`: genereaza si transmite fisierul selectat prin `send_file`.

Interogarile selecteaza numai datele necesare, folosind join-uri intre tabelele relevante. Pentru catalog, autorii sunt agregati cu `string_agg`, astfel incat o carte cu mai multi autori sa apara intr-un singur rand.

Formatele sunt realizate astfel:

- **CSV:** biblioteca standard `csv`, codificare UTF-8 cu BOM (`utf-8-sig`), utila pentru deschiderea in Excel;
- **Excel:** `openpyxl`, cu antet formatat, filtre, prima linie fixata si latimi de coloana ajustate;
- **PDF:** `reportlab`, pagini A4 landscape, tabel cu antet repetat la trecerea pe alta pagina.

Datele sunt preluate din PostgreSQL la momentul descarcarii, nu din fisiere de export salvate anterior. Pentru valorile de tip text care incep cu caractere interpretate ca formule in foile de calcul exista o prelucrare de protectie la export. Pentru PDF, textul este normalizat fara diacritice, ca sa poata fi afisat cu fontul utilizat de raport.

## 4. Securitate si acces

Accesul la pagina de rapoarte si la endpointul de descarcare este inclus in drepturile rolului **Bibliotecar**, iar rolul **Administrator** are acces la toate rutele existente. Rolul **Cititor** nu are acces la aceste endpointuri, conform regulilor de autorizare din `app.py`.

Nu au fost eliminate autentificarea, verificarile de rol sau protectia CSRF existente. Descarcarile sunt cereri GET; nu reprezinta operatii CRUD si nu modifica baza de date.

## 5. Verificari efectuate

Pagina `/rapoarte` a fost deschisa local si afisata corect, cu cele trei tipuri de raport si butoanele de descarcare pentru toate cele trei formate.

Au fost generate si furnizate pentru verificare urmatoarele **trei fisiere**, cate un exemplu din fiecare format:

| Fisier verificat | Tip | Format | Inregistrari |
|---|---|---|---:|
| `biblioteca_carti_20261123_182851.pdf` | Catalog carti | PDF | 20 |
| `biblioteca_imprumuturi_20261123_182857.xlsx` | Imprumuturi | Excel | 10 |
| `biblioteca_rezervari_20261123_182901.csv` | Rezervari | CSV | 5 |

- **PDF catalog:** doua pagini, 20 de carti, cu titlu, ISBN, categorie, editura, an si autori. Ultimul rand apare pe pagina a doua; aceasta este o observatie de paginare, nu o lipsa de date.
- **Excel imprumuturi:** 8 coloane si 10 randuri de date, plus antetul.
- **CSV rezervari:** 6 coloane si 5 randuri de date, plus antetul.

**Limita verificarii:** Nu au fost verificate individual toate cele 9 combinatii dintre cele trei rapoarte si cele trei formate. Celelalte descarcari sunt disponibile in interfata, dar nu sunt prezentate in acest document ca fiind testate. De asemenea, in aceasta verificare nu a fost furnizat un test negativ separat pentru accesul rolului Cititor.

## 6. Fisiere si dependente

| Fisier | Scop |
|---|---|
| `app.py` | Interogari SQL, generare fisiere si rute protejate |
| `templates/rapoarte.html` | Pagina de selectie a raportului |
| `static/css/etapa5_reports.css` | Stilurile paginii de rapoarte |
| `requirements.txt` | Dependentele proiectului, inclusiv `openpyxl` si `reportlab` |
| `documentatie/ETAPA5.md` | Aceasta documentatie |

Dependentele suplimentare necesare sunt `openpyxl>=3.1,<4` si `reportlab>=4.2,<5`.

## 7. Reproducere

1. Se porneste aplicatia Flask folosind mediul virtual: `.\.venv\Scripts\python.exe app.py`.
2. Se autentifica un utilizator cu rol Administrator sau Bibliotecar.
3. Se acceseaza `http://127.0.0.1:5000/rapoarte`.
4. Se alege raportul si formatul dorit.
5. Se verifica datele descarcate si corespondenta cu baza de date.

## 8. Concluzie

Etapa 5 ofera o pagina dedicata generarii rapoartelor despre carti, imprumuturi si rezervari in formatele PDF, CSV si Excel. Implementarea este integrata in aplicatia Flask si respecta structura relationala si autentificarea existente. Au fost inspectate trei exemple reale de export; testarea tuturor combinatiilor ramane o verificare suplimentara, neefectuata in aceasta etapa.
