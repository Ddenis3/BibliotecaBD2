from database import get_connection


def initialize_fixtures():
    with get_connection() as conn:
        with conn.cursor() as cursor:

            # 1. ROLURI
            cursor.execute("""
                INSERT INTO roluri (nume, descriere)
                VALUES
                    ('Administrator', 'Administreaza intregul sistem'),
                    ('Bibliotecar', 'Gestioneaza cartile si imprumuturile'),
                    ('Cititor', 'Poate imprumuta si rezerva carti')
                ON CONFLICT (nume) DO NOTHING;
            """)

            # 2. CATEGORII
            cursor.execute("""
                INSERT INTO categorii (nume, descriere)
                VALUES
                    ('Literatura romana', 'Opere ale autorilor romani'),
                    ('Literatura universala', 'Opere internationale'),
                    ('Science Fiction', 'Literatura SF'),
                    ('Fantasy', 'Literatura fantastica'),
                    ('Istorie', 'Carti de istorie'),
                    ('Informatica', 'Programare si tehnologie'),
                    ('Stiinta', 'Lucrari stiintifice'),
                    ('Dezvoltare personala', 'Carti de dezvoltare')
                ON CONFLICT (nume) DO NOTHING;
            """)

            # 3. UTILIZATORI
            utilizatori = [
                ("Administrator", "Popescu", "Andrei", "admin@biblioteca.ro"),
                ("Bibliotecar", "Ionescu", "Maria", "bibliotecar@biblioteca.ro"),
                ("Cititor", "Georgescu", "Alex", "alex@email.ro"),
                ("Cititor", "Dumitrescu", "Ana", "ana@email.ro"),
                ("Cititor", "Stan", "Mihai", "mihai@email.ro"),
                ("Cititor", "Radu", "Elena", "elena@email.ro"),
                ("Cititor", "Marin", "George", "george@email.ro"),
                ("Cititor", "Tudor", "Ioana", "ioana@email.ro"),
                ("Cititor", "Enache", "David", "david@email.ro"),
                ("Cititor", "Vasile", "Cristina", "cristina@email.ro"),
            ]

            for rol, nume, prenume, email in utilizatori:
                cursor.execute("""
                    INSERT INTO utilizatori
                        (rol_id, nume, prenume, email, parola_hash)
                    SELECT id, %s, %s, %s, %s
                    FROM roluri
                    WHERE nume = %s
                    ON CONFLICT (email) DO NOTHING;
                """, (nume, prenume, email, "DEMO_HASH", rol))

            # 4. AUTORI
            autori = [
                ("Eminescu", "Mihai", "Romana"),
                ("Creanga", "Ion", "Romana"),
                ("Rebreanu", "Liviu", "Romana"),
                ("Preda", "Marin", "Romana"),
                ("Orwell", "George", "Britanica"),
                ("Tolkien", "J.R.R.", "Britanica"),
                ("Rowling", "J.K.", "Britanica"),
                ("Asimov", "Isaac", "Americana"),
                ("Herbert", "Frank", "Americana"),
                ("King", "Stephen", "Americana"),
                ("Harari", "Yuval Noah", "Israeliana"),
                ("Martin", "Robert C.", "Americana"),
                ("Newport", "Cal", "Americana"),
                ("Clear", "James", "Americana"),
                ("Hawking", "Stephen", "Britanica"),
            ]

            for nume, prenume, nationalitate in autori:
                cursor.execute("""
                    INSERT INTO autori (nume, prenume, nationalitate)
                    SELECT %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1 FROM autori
                        WHERE nume = %s AND prenume = %s
                    );
                """, (nume, prenume, nationalitate, nume, prenume))

            # 5. CARTI
            carti = [
                ("Luceafarul", "9780000000001", "Literatura romana", 1883),
                ("Amintiri din copilarie", "9780000000002", "Literatura romana", 1892),
                ("Ion", "9780000000003", "Literatura romana", 1920),
                ("Morometii", "9780000000004", "Literatura romana", 1955),
                ("1984", "9780000000005", "Literatura universala", 1949),
                ("Ferma animalelor", "9780000000006", "Literatura universala", 1945),
                ("Stapanul Inelelor", "9780000000007", "Fantasy", 1954),
                ("Hobbitul", "9780000000008", "Fantasy", 1937),
                ("Harry Potter si Piatra Filosofala", "9780000000009", "Fantasy", 1997),
                ("Harry Potter si Camera Secretelor", "9780000000010", "Fantasy", 1998),
                ("Fundatia", "9780000000011", "Science Fiction", 1951),
                ("Eu, Robotul", "9780000000012", "Science Fiction", 1950),
                ("Dune", "9780000000013", "Science Fiction", 1965),
                ("The Shining", "9780000000014", "Fantasy", 1977),
                ("Sapiens", "9780000000015", "Istorie", 2014),
                ("Clean Code", "9780000000016", "Informatica", 2008),
                ("Clean Architecture", "9780000000017", "Informatica", 2017),
                ("Deep Work", "9780000000018", "Dezvoltare personala", 2016),
                ("Atomic Habits", "9780000000019", "Dezvoltare personala", 2018),
                ("A Brief History of Time", "9780000000020", "Stiinta", 1988),
            ]

            for titlu, isbn, categorie, an in carti:
                cursor.execute("""
                    INSERT INTO carti
                        (titlu, isbn, categorie_id, an_publicare)
                    SELECT %s, %s, id, %s
                    FROM categorii
                    WHERE nume = %s
                    ON CONFLICT (isbn) DO NOTHING;
                """, (titlu, isbn, an, categorie))

            # 6. ASOCIERI CARTI - AUTORI
            asocieri = [
                ("9780000000001", "Eminescu"),
                ("9780000000002", "Creanga"),
                ("9780000000003", "Rebreanu"),
                ("9780000000004", "Preda"),
                ("9780000000005", "Orwell"),
                ("9780000000006", "Orwell"),
                ("9780000000007", "Tolkien"),
                ("9780000000008", "Tolkien"),
                ("9780000000009", "Rowling"),
                ("9780000000010", "Rowling"),
                ("9780000000011", "Asimov"),
                ("9780000000012", "Asimov"),
                ("9780000000013", "Herbert"),
                ("9780000000014", "King"),
                ("9780000000015", "Harari"),
                ("9780000000016", "Martin"),
                ("9780000000017", "Martin"),
                ("9780000000018", "Newport"),
                ("9780000000019", "Clear"),
                ("9780000000020", "Hawking"),
            ]

            for isbn, autor in asocieri:
                cursor.execute("""
                    INSERT INTO autori_carti (carte_id, autor_id)
                    SELECT c.id, a.id
                    FROM carti c
                    CROSS JOIN autori a
                    WHERE c.isbn = %s AND a.nume = %s
                    ON CONFLICT (carte_id, autor_id) DO NOTHING;
                """, (isbn, autor))

            # 7. EXEMPLARE
            for nr in range(1, 31):
                numar_carte = ((nr - 1) % 20) + 1
                isbn = f"978000000{numar_carte:04d}"
                cod = f"INV-{nr:03d}"
                stare = "imprumutat" if nr <= 7 else "disponibil"

                cursor.execute("""
                    INSERT INTO exemplare
                        (carte_id, cod_inventar, stare, data_achizitie)
                    SELECT id, %s, %s, DATE '2026-01-15'
                    FROM carti
                    WHERE isbn = %s
                    ON CONFLICT (cod_inventar) DO NOTHING;
                """, (cod, stare, isbn))

            # 8. IMPRUMUTURI
            imprumuturi = [
                ("alex@email.ro", "INV-001", "2026-10-15", "2026-10-29", None, "activ"),
                ("ana@email.ro", "INV-002", "2026-10-16", "2026-10-30", None, "activ"),
                ("mihai@email.ro", "INV-003", "2026-10-17", "2026-10-31", None, "activ"),
                ("elena@email.ro", "INV-004", "2026-10-18", "2026-11-01", None, "activ"),
                ("george@email.ro", "INV-005", "2026-10-19", "2026-11-02", None, "activ"),
                ("ioana@email.ro", "INV-006", "2026-10-20", "2026-11-03", None, "activ"),
                ("david@email.ro", "INV-007", "2026-10-21", "2026-11-04", None, "activ"),
                ("cristina@email.ro", "INV-008", "2026-09-01", "2026-09-15", "2026-09-12", "returnat"),
                ("alex@email.ro", "INV-009", "2026-09-05", "2026-09-19", "2026-09-18", "returnat"),
                ("ana@email.ro", "INV-010", "2026-09-10", "2026-09-24", "2026-09-23", "returnat"),
            ]

            for email, cod, data_i, scadenta, returnare, status in imprumuturi:
                cursor.execute("""
                    INSERT INTO imprumuturi
                        (cititor_id, exemplar_id, data_imprumut,
                         data_scadenta, data_returnare, status)
                    SELECT u.id, e.id, %s, %s, %s, %s
                    FROM utilizatori u
                    CROSS JOIN exemplare e
                    WHERE u.email = %s
                      AND e.cod_inventar = %s
                      AND NOT EXISTS (
                          SELECT 1
                          FROM imprumuturi i
                          WHERE i.cititor_id = u.id
                            AND i.exemplar_id = e.id
                            AND i.data_imprumut = %s
                      );
                """, (data_i, scadenta, returnare, status, email, cod, data_i))

            # 9. REZERVARI
            rezervari = [
                ("alex@email.ro", "9780000000011", "2026-10-20", "2026-11-01"),
                ("ana@email.ro", "9780000000012", "2026-10-21", "2026-11-02"),
                ("mihai@email.ro", "9780000000013", "2026-10-22", "2026-11-03"),
                ("elena@email.ro", "9780000000014", "2026-10-23", "2026-11-04"),
                ("george@email.ro", "9780000000015", "2026-10-24", "2026-11-05"),
            ]

            for email, isbn, data_r, expirare in rezervari:
                cursor.execute("""
                    INSERT INTO rezervari
                        (cititor_id, carte_id, data_rezervare,
                         data_expirare, status)
                    SELECT u.id, c.id, %s, %s, 'activa'
                    FROM utilizatori u
                    CROSS JOIN carti c
                    WHERE u.email = %s
                      AND c.isbn = %s
                      AND NOT EXISTS (
                          SELECT 1
                          FROM rezervari r
                          WHERE r.cititor_id = u.id
                            AND r.carte_id = c.id
                            AND r.data_rezervare = %s
                      );
                """, (data_r, expirare, email, isbn, data_r))

    print("Fixtures pentru toate cele 9 tabele initializate cu succes!")