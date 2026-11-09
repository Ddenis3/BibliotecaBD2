from flask import Flask, jsonify, render_template, request, redirect, url_for
from database import get_connection
from fixtures import initialize_fixtures
from psycopg.errors import (
    UniqueViolation,
    ForeignKeyViolation,
    CheckViolation,
    NotNullViolation
)
from werkzeug.security import generate_password_hash
from datetime import date

app = Flask(__name__)


# ==================================
# PAGINA PRINCIPALA
# ==================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/statistici")
def statistici():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM carti")
            total_carti = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM utilizatori")
            total_utilizatori = cursor.fetchone()[0]

    return jsonify({
        "carti": total_carti,
        "utilizatori": total_utilizatori
    })


# ==================================
# CRUD CATEGORII
# ==================================

@app.route("/categorii")
def categorii():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, nume, descriere
                FROM categorii
                ORDER BY id
            """)
            categorii_db = cursor.fetchall()

    return render_template(
        "categorii.html",
        categorii=categorii_db
    )


@app.route("/categorii/adauga", methods=["POST"])
def adauga_categorie():
    nume = request.form.get("nume", "").strip()
    descriere = request.form.get("descriere", "").strip()

    if not nume:
        return "Numele categoriei este obligatoriu.", 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO categorii (nume, descriere)
                    VALUES (%s, %s)
                """, (nume, descriere))

    except UniqueViolation:
        return "Exista deja o categorie cu acest nume.", 409

    return redirect(url_for("categorii"))


@app.route("/categorii/modifica/<int:id>", methods=["POST"])
def modifica_categorie(id):
    nume = request.form.get("nume", "").strip()
    descriere = request.form.get("descriere", "").strip()

    if not nume:
        return "Numele categoriei este obligatoriu.", 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE categorii
                    SET nume = %s, descriere = %s
                    WHERE id = %s
                """, (nume, descriere, id))

                if cursor.rowcount == 0:
                    return "Categoria nu exista.", 404

    except UniqueViolation:
        return "Exista deja o categorie cu acest nume.", 409

    return redirect(url_for("categorii"))


@app.route("/categorii/sterge/<int:id>", methods=["POST"])
def sterge_categorie(id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM categorii
                    WHERE id = %s
                """, (id,))

                if cursor.rowcount == 0:
                    return "Categoria nu exista.", 404

    except ForeignKeyViolation:
        return "Categoria nu poate fi stearsa deoarece are carti asociate.", 409

    return redirect(url_for("categorii"))


# ==================================
# CRUD AUTORI
# ==================================

@app.route("/autori")
def lista_autori():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    nume,
                    prenume,
                    data_nasterii,
                    nationalitate,
                    biografie
                FROM autori
                ORDER BY id
            """)
            autori_db = cursor.fetchall()

    return render_template(
        "autori.html",
        autori=autori_db
    )


@app.route("/autori/adauga", methods=["POST"])
def adauga_autor():
    nume = request.form.get("nume", "").strip()
    prenume = request.form.get("prenume", "").strip()
    data_nasterii = request.form.get("data_nasterii") or None
    nationalitate = request.form.get("nationalitate", "").strip()
    biografie = request.form.get("biografie", "").strip()

    if not nume:
        return "Numele autorului este obligatoriu.", 400

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO autori
                (
                    nume,
                    prenume,
                    data_nasterii,
                    nationalitate,
                    biografie
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                nume,
                prenume,
                data_nasterii,
                nationalitate,
                biografie
            ))

    return redirect(url_for("lista_autori"))


@app.route("/autori/modifica/<int:id>", methods=["POST"])
def modifica_autor(id):
    nume = request.form.get("nume", "").strip()
    prenume = request.form.get("prenume", "").strip()
    data_nasterii = request.form.get("data_nasterii") or None
    nationalitate = request.form.get("nationalitate", "").strip()
    biografie = request.form.get("biografie", "").strip()

    if not nume:
        return "Numele autorului este obligatoriu.", 400

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE autori
                SET nume = %s,
                    prenume = %s,
                    data_nasterii = %s,
                    nationalitate = %s,
                    biografie = %s
                WHERE id = %s
            """, (
                nume,
                prenume,
                data_nasterii,
                nationalitate,
                biografie,
                id
            ))

            if cursor.rowcount == 0:
                return "Autorul nu exista.", 404

    return redirect(url_for("lista_autori"))


@app.route("/autori/sterge/<int:id>", methods=["POST"])
def sterge_autor(id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM autori
                WHERE id = %s
            """, (id,))

            if cursor.rowcount == 0:
                return "Autorul nu exista.", 404

    return redirect(url_for("lista_autori"))


# ==================================
# FUNCTII AUXILIARE CARTI
# ==================================

def citeste_date_carte():
    titlu = request.form.get("titlu", "").strip()
    isbn = request.form.get("isbn", "").strip() or None
    editura = request.form.get("editura", "").strip()
    descriere = request.form.get("descriere", "").strip()

    try:
        categorie_id = int(request.form.get("categorie_id", ""))
    except ValueError:
        return None, "Categoria este invalida."

    an_text = request.form.get("an_publicare", "").strip()

    try:
        an_publicare = int(an_text) if an_text else None
    except ValueError:
        return None, "Anul publicarii este invalid."

    if not titlu:
        return None, "Titlul este obligatoriu."

    if len(titlu) > 200:
        return None, "Titlul este prea lung."

    if isbn and len(isbn) > 20:
        return None, "ISBN-ul este prea lung."

    if len(editura) > 150:
        return None, "Numele editurii este prea lung."

    if an_publicare is not None:
        if not 1450 <= an_publicare <= 2100:
            return None, "Anul trebuie sa fie intre 1450 si 2100."

    try:
        autor_ids = sorted(set(
            int(x) for x in request.form.getlist("autori")
        ))
    except ValueError:
        return None, "Lista autorilor este invalida."

    if not autor_ids or any(x <= 0 for x in autor_ids):
        return None, "Selecteaza cel putin un autor."

    return {
        "titlu": titlu,
        "isbn": isbn,
        "categorie_id": categorie_id,
        "editura": editura,
        "an_publicare": an_publicare,
        "descriere": descriere,
        "autori": autor_ids
    }, None


def verifica_referinte(cursor, date):
    cursor.execute("""
        SELECT COUNT(*)
        FROM categorii
        WHERE id = %s
    """, (date["categorie_id"],))

    if cursor.fetchone()[0] != 1:
        return False

    cursor.execute("""
        SELECT COUNT(*)
        FROM autori
        WHERE id = ANY(%s)
    """, (date["autori"],))

    return cursor.fetchone()[0] == len(date["autori"])


def salveaza_autorii_cartii(cursor, carte_id, autor_ids):
    cursor.execute("""
        DELETE FROM autori_carti
        WHERE carte_id = %s
    """, (carte_id,))

    for autor_id in autor_ids:
        cursor.execute("""
            INSERT INTO autori_carti (carte_id, autor_id)
            VALUES (%s, %s)
        """, (carte_id, autor_id))


# ==================================
# CRUD CARTI
# ==================================

@app.route("/carti")
def lista_carti():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    c.id,
                    c.titlu,
                    c.isbn,
                    c.categorie_id,
                    cat.nume,
                    c.editura,
                    c.an_publicare,
                    c.descriere
                FROM carti c
                JOIN categorii cat
                    ON cat.id = c.categorie_id
                ORDER BY c.id
            """)
            carti_db = cursor.fetchall()

            cursor.execute("""
                SELECT id, nume
                FROM categorii
                ORDER BY nume
            """)
            categorii_db = cursor.fetchall()

            cursor.execute("""
                SELECT id, nume, prenume
                FROM autori
                ORDER BY nume, prenume
            """)
            autori_db = cursor.fetchall()

            cursor.execute("""
                SELECT carte_id, autor_id
                FROM autori_carti
            """)
            asocieri = cursor.fetchall()

    autori_carti = {}

    for carte_id, autor_id in asocieri:
        autori_carti.setdefault(carte_id, []).append(autor_id)

    return render_template(
        "carti.html",
        carti=carti_db,
        categorii=categorii_db,
        autori=autori_db,
        autori_carti=autori_carti
    )


@app.route("/carti/adauga", methods=["POST"])
def adauga_carte():
    date_carte, eroare = citeste_date_carte()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                if not verifica_referinte(cursor, date_carte):
                    return "Categoria sau autorul nu exista.", 400

                cursor.execute("""
                    INSERT INTO carti
                    (
                        titlu,
                        isbn,
                        categorie_id,
                        editura,
                        an_publicare,
                        descriere
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    date_carte["titlu"],
                    date_carte["isbn"],
                    date_carte["categorie_id"],
                    date_carte["editura"],
                    date_carte["an_publicare"],
                    date_carte["descriere"]
                ))

                carte_id = cursor.fetchone()[0]

                salveaza_autorii_cartii(
                    cursor,
                    carte_id,
                    date_carte["autori"]
                )

    except UniqueViolation:
        return "Exista deja o carte cu acest ISBN.", 409

    except ForeignKeyViolation:
        return "Categoria sau autorul nu exista.", 409

    except CheckViolation:
        return "Datele cartii sunt invalide.", 400

    return redirect(url_for("lista_carti"))


@app.route("/carti/modifica/<int:id>", methods=["POST"])
def modifica_carte(id):
    date_carte, eroare = citeste_date_carte()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                if not verifica_referinte(cursor, date_carte):
                    return "Categoria sau autorul nu exista.", 400

                cursor.execute("""
                    UPDATE carti
                    SET titlu = %s,
                        isbn = %s,
                        categorie_id = %s,
                        editura = %s,
                        an_publicare = %s,
                        descriere = %s
                    WHERE id = %s
                """, (
                    date_carte["titlu"],
                    date_carte["isbn"],
                    date_carte["categorie_id"],
                    date_carte["editura"],
                    date_carte["an_publicare"],
                    date_carte["descriere"],
                    id
                ))

                if cursor.rowcount == 0:
                    return "Cartea nu exista.", 404

                salveaza_autorii_cartii(
                    cursor,
                    id,
                    date_carte["autori"]
                )

    except UniqueViolation:
        return "Exista deja o carte cu acest ISBN.", 409

    except ForeignKeyViolation:
        return "Categoria sau autorul nu exista.", 409

    except CheckViolation:
        return "Datele cartii sunt invalide.", 400

    return redirect(url_for("lista_carti"))


@app.route("/carti/sterge/<int:id>", methods=["POST"])
def sterge_carte(id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM carti
                    WHERE id = %s
                """, (id,))

                if cursor.rowcount == 0:
                    return "Cartea nu exista.", 404

    except ForeignKeyViolation:
        return (
            "Cartea nu poate fi stearsa deoarece are "
            "exemplare sau rezervari asociate.",
            409
        )

    return redirect(url_for("lista_carti"))


# ==================================
# CRUD EXEMPLARE
# ==================================

@app.route("/exemplare")
def lista_exemplare():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    e.id,
                    e.carte_id,
                    c.titlu,
                    e.cod_inventar,
                    e.stare,
                    e.data_achizitie
                FROM exemplare e
                JOIN carti c
                    ON c.id = e.carte_id
                ORDER BY e.id
            """)
            exemplare_db = cursor.fetchall()

            cursor.execute("""
                SELECT id, titlu
                FROM carti
                ORDER BY titlu, id
            """)
            carti_db = cursor.fetchall()

    return render_template(
        "exemplare.html",
        exemplare=exemplare_db,
        carti=carti_db
    )


def citeste_date_exemplar():
    cod_inventar = request.form.get("cod_inventar", "").strip()
    stare = request.form.get("stare", "").strip()
    data_achizitie = request.form.get("data_achizitie") or None

    try:
        carte_id = int(request.form.get("carte_id", ""))
    except ValueError:
        return None, "Cartea selectata este invalida."

    if carte_id <= 0:
        return None, "Cartea selectata este invalida."

    if not cod_inventar:
        return None, "Codul de inventar este obligatoriu."

    if len(cod_inventar) > 50:
        return None, "Codul de inventar este prea lung."

    stari_permise = [
        "disponibil",
        "imprumutat",
        "deteriorat",
        "pierdut"
    ]

    if stare not in stari_permise:
        return None, "Starea exemplarului este invalida."

    return {
        "carte_id": carte_id,
        "cod_inventar": cod_inventar,
        "stare": stare,
        "data_achizitie": data_achizitie
    }, None


@app.route("/exemplare/adauga", methods=["POST"])
def adauga_exemplar():
    date_exemplar, eroare = citeste_date_exemplar()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO exemplare
                    (
                        carte_id,
                        cod_inventar,
                        stare,
                        data_achizitie
                    )
                    VALUES (%s, %s, %s, %s)
                """, (
                    date_exemplar["carte_id"],
                    date_exemplar["cod_inventar"],
                    date_exemplar["stare"],
                    date_exemplar["data_achizitie"]
                ))

    except UniqueViolation:
        return "Exista deja un exemplar cu acest cod de inventar.", 409

    except ForeignKeyViolation:
        return "Cartea selectata nu exista.", 409

    except CheckViolation:
        return "Starea exemplarului nu este valida.", 400

    return redirect(url_for("lista_exemplare"))


@app.route("/exemplare/modifica/<int:id>", methods=["POST"])
def modifica_exemplar(id):
    date_exemplar, eroare = citeste_date_exemplar()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE exemplare
                    SET carte_id = %s,
                        cod_inventar = %s,
                        stare = %s,
                        data_achizitie = %s
                    WHERE id = %s
                """, (
                    date_exemplar["carte_id"],
                    date_exemplar["cod_inventar"],
                    date_exemplar["stare"],
                    date_exemplar["data_achizitie"],
                    id
                ))

                if cursor.rowcount == 0:
                    return "Exemplarul nu exista.", 404

    except UniqueViolation:
        return "Codul de inventar este deja utilizat.", 409

    except ForeignKeyViolation:
        return "Cartea selectata nu exista.", 409

    except CheckViolation:
        return "Starea exemplarului nu este valida.", 400

    return redirect(url_for("lista_exemplare"))


@app.route("/exemplare/sterge/<int:id>", methods=["POST"])
def sterge_exemplar(id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM exemplare
                    WHERE id = %s
                """, (id,))

                if cursor.rowcount == 0:
                    return "Exemplarul nu exista.", 404

    except ForeignKeyViolation:
        return (
            "Exemplarul nu poate fi sters deoarece "
            "are imprumuturi asociate.",
            409
        )

    return redirect(url_for("lista_exemplare"))


# ==================================
# CRUD UTILIZATORI
# ==================================

@app.route("/utilizatori")
def lista_utilizatori():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    u.id,
                    u.rol_id,
                    r.nume,
                    u.nume,
                    u.prenume,
                    u.email,
                    u.telefon,
                    u.data_inregistrare,
                    u.activ
                FROM utilizatori u
                JOIN roluri r
                    ON r.id = u.rol_id
                ORDER BY u.id
            """)
            utilizatori_db = cursor.fetchall()

            cursor.execute("""
                SELECT id, nume
                FROM roluri
                ORDER BY id
            """)
            roluri_db = cursor.fetchall()

    return render_template(
        "utilizatori.html",
        utilizatori=utilizatori_db,
        roluri=roluri_db
    )


def citeste_date_utilizator():
    nume = request.form.get("nume", "").strip()
    prenume = request.form.get("prenume", "").strip()
    email = request.form.get("email", "").strip().lower()
    telefon = request.form.get("telefon", "").strip() or None
    parola = request.form.get("parola", "")
    activ = request.form.get("activ") == "1"

    try:
        rol_id = int(request.form.get("rol_id", ""))
    except ValueError:
        return None, "Rolul selectat este invalid."

    if rol_id <= 0:
        return None, "Rolul selectat este invalid."

    if not nume or not prenume:
        return None, "Numele si prenumele sunt obligatorii."

    if not email or "@" not in email:
        return None, "Adresa de email este invalida."

    if len(nume) > 100 or len(prenume) > 100:
        return None, "Numele sau prenumele este prea lung."

    if len(email) > 255:
        return None, "Adresa de email este prea lunga."

    if telefon and len(telefon) > 30:
        return None, "Numarul de telefon este prea lung."

    return {
        "rol_id": rol_id,
        "nume": nume,
        "prenume": prenume,
        "email": email,
        "telefon": telefon,
        "parola": parola,
        "activ": activ
    }, None


@app.route("/utilizatori/adauga", methods=["POST"])
def adauga_utilizator():
    date_utilizator, eroare = citeste_date_utilizator()

    if eroare:
        return eroare, 400

    if not date_utilizator["parola"]:
        return "Parola este obligatorie la adaugare.", 400

    parola_hash = generate_password_hash(
        date_utilizator["parola"]
    )

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO utilizatori
                    (
                        rol_id,
                        nume,
                        prenume,
                        email,
                        parola_hash,
                        telefon,
                        activ
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    date_utilizator["rol_id"],
                    date_utilizator["nume"],
                    date_utilizator["prenume"],
                    date_utilizator["email"],
                    parola_hash,
                    date_utilizator["telefon"],
                    date_utilizator["activ"]
                ))

    except UniqueViolation:
        return "Exista deja un utilizator cu acest email.", 409

    except ForeignKeyViolation:
        return "Rolul selectat nu exista.", 409

    except CheckViolation:
        return "Datele utilizatorului nu sunt valide.", 400

    return redirect(url_for("lista_utilizatori"))


@app.route("/utilizatori/modifica/<int:id>", methods=["POST"])
def modifica_utilizator(id):
    date_utilizator, eroare = citeste_date_utilizator()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                if date_utilizator["parola"]:
                    parola_hash = generate_password_hash(
                        date_utilizator["parola"]
                    )

                    cursor.execute("""
                        UPDATE utilizatori
                        SET rol_id = %s,
                            nume = %s,
                            prenume = %s,
                            email = %s,
                            telefon = %s,
                            parola_hash = %s,
                            activ = %s
                        WHERE id = %s
                    """, (
                        date_utilizator["rol_id"],
                        date_utilizator["nume"],
                        date_utilizator["prenume"],
                        date_utilizator["email"],
                        date_utilizator["telefon"],
                        parola_hash,
                        date_utilizator["activ"],
                        id
                    ))

                else:
                    cursor.execute("""
                        UPDATE utilizatori
                        SET rol_id = %s,
                            nume = %s,
                            prenume = %s,
                            email = %s,
                            telefon = %s,
                            activ = %s
                        WHERE id = %s
                    """, (
                        date_utilizator["rol_id"],
                        date_utilizator["nume"],
                        date_utilizator["prenume"],
                        date_utilizator["email"],
                        date_utilizator["telefon"],
                        date_utilizator["activ"],
                        id
                    ))

                if cursor.rowcount == 0:
                    return "Utilizatorul nu exista.", 404

    except UniqueViolation:
        return "Exista deja un utilizator cu acest email.", 409

    except ForeignKeyViolation:
        return "Rolul selectat nu exista.", 409

    except CheckViolation:
        return "Datele utilizatorului nu sunt valide.", 400

    return redirect(url_for("lista_utilizatori"))


@app.route("/utilizatori/sterge/<int:id>", methods=["POST"])
def sterge_utilizator(id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM utilizatori
                    WHERE id = %s
                """, (id,))

                if cursor.rowcount == 0:
                    return "Utilizatorul nu exista.", 404

    except ForeignKeyViolation:
        return (
            "Utilizatorul nu poate fi sters deoarece "
            "are imprumuturi sau rezervari asociate.",
            409
        )

    return redirect(url_for("lista_utilizatori"))


# ==================================
# CRUD ROLURI
# ==================================

@app.route("/roluri")
def lista_roluri():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    r.id,
                    r.nume,
                    r.descriere,
                    COUNT(u.id)
                FROM roluri r
                LEFT JOIN utilizatori u
                    ON u.rol_id = r.id
                GROUP BY r.id, r.nume, r.descriere
                ORDER BY r.id
            """)
            roluri_db = cursor.fetchall()

    return render_template(
        "roluri.html",
        roluri=roluri_db
    )


def citeste_date_rol():
    nume = request.form.get("nume", "").strip()
    descriere = request.form.get("descriere", "").strip()

    if not nume:
        return None, "Numele rolului este obligatoriu."

    if len(nume) > 50:
        return None, "Numele rolului este prea lung."

    return {
        "nume": nume,
        "descriere": descriere
    }, None


@app.route("/roluri/adauga", methods=["POST"])
def adauga_rol():
    date_rol, eroare = citeste_date_rol()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO roluri (nume, descriere)
                    VALUES (%s, %s)
                """, (
                    date_rol["nume"],
                    date_rol["descriere"]
                ))

    except UniqueViolation:
        return "Exista deja un rol cu acest nume.", 409

    except CheckViolation:
        return "Datele rolului sunt invalide.", 400

    return redirect(url_for("lista_roluri"))


@app.route("/roluri/modifica/<int:id>", methods=["POST"])
def modifica_rol(id):
    date_rol, eroare = citeste_date_rol()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE roluri
                    SET nume = %s,
                        descriere = %s
                    WHERE id = %s
                """, (
                    date_rol["nume"],
                    date_rol["descriere"],
                    id
                ))

                if cursor.rowcount == 0:
                    return "Rolul nu exista.", 404

    except UniqueViolation:
        return "Exista deja un rol cu acest nume.", 409

    except CheckViolation:
        return "Datele rolului sunt invalide.", 400

    return redirect(url_for("lista_roluri"))


@app.route("/roluri/sterge/<int:id>", methods=["POST"])
def sterge_rol(id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM roluri
                    WHERE id = %s
                """, (id,))

                if cursor.rowcount == 0:
                    return "Rolul nu exista.", 404

    except ForeignKeyViolation:
        return (
            "Rolul nu poate fi sters deoarece "
            "exista utilizatori asociati.",
            409
        )

    return redirect(url_for("lista_roluri"))


# ==================================
# CRUD IMPRUMUTURI
# ==================================

@app.route("/imprumuturi")
def lista_imprumuturi():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    i.id,
                    i.cititor_id,
                    u.nume,
                    u.prenume,
                    i.exemplar_id,
                    e.cod_inventar,
                    c.titlu,
                    i.data_imprumut,
                    i.data_scadenta,
                    i.data_returnare,
                    i.status
                FROM imprumuturi i
                JOIN utilizatori u
                    ON u.id = i.cititor_id
                JOIN exemplare e
                    ON e.id = i.exemplar_id
                JOIN carti c
                    ON c.id = e.carte_id
                ORDER BY i.id
            """)
            imprumuturi_db = cursor.fetchall()

            cursor.execute("""
                SELECT id, nume, prenume, email
                FROM utilizatori
                ORDER BY nume, prenume, id
            """)
            cititori_db = cursor.fetchall()

            cursor.execute("""
                SELECT
                    e.id,
                    e.cod_inventar,
                    c.titlu
                FROM exemplare e
                JOIN carti c
                    ON c.id = e.carte_id
                ORDER BY c.titlu, e.cod_inventar
            """)
            exemplare_db = cursor.fetchall()

            cursor.execute("""
                SELECT DISTINCT status
                FROM imprumuturi
                WHERE status IS NOT NULL
                ORDER BY status
            """)
            statusuri_db = [
                rand[0] for rand in cursor.fetchall()
            ]

    return render_template(
        "imprumuturi.html",
        imprumuturi=imprumuturi_db,
        cititori=cititori_db,
        exemplare=exemplare_db,
        statusuri=statusuri_db,
        data_azi=date.today().isoformat()
    )


def citeste_date_imprumut():
    try:
        cititor_id = int(request.form.get("cititor_id", ""))
        exemplar_id = int(request.form.get("exemplar_id", ""))
    except ValueError:
        return None, "Cititorul sau exemplarul este invalid."

    if cititor_id <= 0 or exemplar_id <= 0:
        return None, "Cititorul sau exemplarul este invalid."

    data_imprumut_text = request.form.get(
        "data_imprumut", ""
    ).strip()

    data_scadenta_text = request.form.get(
        "data_scadenta", ""
    ).strip()

    data_returnare_text = request.form.get(
        "data_returnare", ""
    ).strip()

    status = request.form.get("status", "").strip()

    if not data_imprumut_text or not data_scadenta_text:
        return None, "Datele imprumutului si scadentei sunt obligatorii."

    if not status:
        return None, "Statusul este obligatoriu."

    try:
        data_imprumut = date.fromisoformat(
            data_imprumut_text
        )

        data_scadenta = date.fromisoformat(
            data_scadenta_text
        )

        data_returnare = (
            date.fromisoformat(data_returnare_text)
            if data_returnare_text
            else None
        )

    except ValueError:
        return None, "Formatul datei este invalid."

    if data_scadenta < data_imprumut:
        return None, (
            "Data scadentei nu poate fi anterioara "
            "datei imprumutului."
        )

    if data_returnare and data_returnare < data_imprumut:
        return None, (
            "Data returnarii nu poate fi anterioara "
            "datei imprumutului."
        )

    return {
        "cititor_id": cititor_id,
        "exemplar_id": exemplar_id,
        "data_imprumut": data_imprumut,
        "data_scadenta": data_scadenta,
        "data_returnare": data_returnare,
        "status": status
    }, None


@app.route("/imprumuturi/adauga", methods=["POST"])
def adauga_imprumut():
    date_imprumut, eroare = citeste_date_imprumut()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM utilizatori
                    WHERE id = %s AND activ = TRUE
                """, (date_imprumut["cititor_id"],))

                if cursor.fetchone()[0] == 0:
                    return "Cititorul nu exista sau este inactiv.", 400

                cursor.execute("""
                    INSERT INTO imprumuturi
                    (
                        cititor_id,
                        exemplar_id,
                        data_imprumut,
                        data_scadenta,
                        data_returnare,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    date_imprumut["cititor_id"],
                    date_imprumut["exemplar_id"],
                    date_imprumut["data_imprumut"],
                    date_imprumut["data_scadenta"],
                    date_imprumut["data_returnare"],
                    date_imprumut["status"]
                ))

    except ForeignKeyViolation:
        return "Cititorul sau exemplarul nu exista.", 409

    except CheckViolation:
        return "Datele sau statusul imprumutului sunt invalide.", 400

    except NotNullViolation:
        return "Lipsesc informatii obligatorii.", 400

    except UniqueViolation:
        return "Imprumutul intra in conflict cu unul existent.", 409

    return redirect(url_for("lista_imprumuturi"))


@app.route("/imprumuturi/modifica/<int:id>", methods=["POST"])
def modifica_imprumut(id):
    date_imprumut, eroare = citeste_date_imprumut()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE imprumuturi
                    SET cititor_id = %s,
                        exemplar_id = %s,
                        data_imprumut = %s,
                        data_scadenta = %s,
                        data_returnare = %s,
                        status = %s
                    WHERE id = %s
                """, (
                    date_imprumut["cititor_id"],
                    date_imprumut["exemplar_id"],
                    date_imprumut["data_imprumut"],
                    date_imprumut["data_scadenta"],
                    date_imprumut["data_returnare"],
                    date_imprumut["status"],
                    id
                ))

                if cursor.rowcount == 0:
                    return "Imprumutul nu exista.", 404

    except ForeignKeyViolation:
        return "Cititorul sau exemplarul nu exista.", 409

    except CheckViolation:
        return "Datele sau statusul imprumutului sunt invalide.", 400

    except NotNullViolation:
        return "Lipsesc informatii obligatorii.", 400

    except UniqueViolation:
        return "Modificarea intra in conflict cu un imprumut existent.", 409

    return redirect(url_for("lista_imprumuturi"))


@app.route("/imprumuturi/sterge/<int:id>", methods=["POST"])
def sterge_imprumut(id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM imprumuturi
                WHERE id = %s
            """, (id,))

            if cursor.rowcount == 0:
                return "Imprumutul nu exista.", 404

    return redirect(url_for("lista_imprumuturi"))


# ==================================
# CRUD REZERVARI
# ==================================

@app.route("/rezervari")
def lista_rezervari():
    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    r.id,
                    r.cititor_id,
                    u.nume,
                    u.prenume,
                    r.carte_id,
                    c.titlu,
                    r.data_rezervare,
                    r.data_expirare,
                    r.status
                FROM rezervari r
                JOIN utilizatori u
                    ON u.id = r.cititor_id
                JOIN carti c
                    ON c.id = r.carte_id
                ORDER BY r.id
            """)
            rezervari_db = cursor.fetchall()

            cursor.execute("""
                SELECT
                    id,
                    nume,
                    prenume,
                    email
                FROM utilizatori
                ORDER BY nume, prenume, id
            """)
            cititori_db = cursor.fetchall()

            cursor.execute("""
                SELECT id, titlu
                FROM carti
                ORDER BY titlu, id
            """)
            carti_db = cursor.fetchall()

            cursor.execute("""
                SELECT DISTINCT status
                FROM rezervari
                WHERE status IS NOT NULL
                ORDER BY status
            """)
            statusuri_db = [
                rand[0] for rand in cursor.fetchall()
            ]

    return render_template(
        "rezervari.html",
        rezervari=rezervari_db,
        cititori=cititori_db,
        carti=carti_db,
        statusuri=statusuri_db,
        data_azi=date.today().isoformat()
    )


def citeste_date_rezervare():
    try:
        cititor_id = int(request.form.get("cititor_id", ""))
        carte_id = int(request.form.get("carte_id", ""))

    except ValueError:
        return None, "Cititorul sau cartea selectata este invalida."

    if cititor_id <= 0 or carte_id <= 0:
        return None, "Cititorul sau cartea selectata este invalida."

    data_rezervare_text = request.form.get(
        "data_rezervare", ""
    ).strip()

    data_expirare_text = request.form.get(
        "data_expirare", ""
    ).strip()

    status = request.form.get("status", "").strip()

    if not data_rezervare_text:
        return None, "Data rezervarii este obligatorie."

    if not data_expirare_text:
        return None, "Data expirarii este obligatorie."

    if not status:
        return None, "Statusul rezervarii este obligatoriu."

    try:
        data_rezervare = date.fromisoformat(
            data_rezervare_text
        )

        data_expirare = date.fromisoformat(
            data_expirare_text
        )

    except ValueError:
        return None, "Formatul datei este invalid."

    if data_expirare < data_rezervare:
        return None, (
            "Data expirarii nu poate fi anterioara "
            "datei rezervarii."
        )

    return {
        "cititor_id": cititor_id,
        "carte_id": carte_id,
        "data_rezervare": data_rezervare,
        "data_expirare": data_expirare,
        "status": status
    }, None


# CREATE
@app.route("/rezervari/adauga", methods=["POST"])
def adauga_rezervare():
    date_rezervare, eroare = citeste_date_rezervare()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM utilizatori
                    WHERE id = %s
                      AND activ = TRUE
                """, (date_rezervare["cititor_id"],))

                if cursor.fetchone()[0] == 0:
                    return "Cititorul nu exista sau este inactiv.", 400

                cursor.execute("""
                    INSERT INTO rezervari
                    (
                        cititor_id,
                        carte_id,
                        data_rezervare,
                        data_expirare,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    date_rezervare["cititor_id"],
                    date_rezervare["carte_id"],
                    date_rezervare["data_rezervare"],
                    date_rezervare["data_expirare"],
                    date_rezervare["status"]
                ))

    except ForeignKeyViolation:
        return "Cititorul sau cartea nu exista.", 409

    except CheckViolation:
        return "Datele sau statusul rezervarii sunt invalide.", 400

    except NotNullViolation:
        return "Lipsesc informatii obligatorii.", 400

    except UniqueViolation:
        return "Rezervarea intra in conflict cu una existenta.", 409

    return redirect(url_for("lista_rezervari"))


# UPDATE
@app.route("/rezervari/modifica/<int:id>", methods=["POST"])
def modifica_rezervare(id):
    date_rezervare, eroare = citeste_date_rezervare()

    if eroare:
        return eroare, 400

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute("""
                    UPDATE rezervari
                    SET cititor_id = %s,
                        carte_id = %s,
                        data_rezervare = %s,
                        data_expirare = %s,
                        status = %s
                    WHERE id = %s
                """, (
                    date_rezervare["cititor_id"],
                    date_rezervare["carte_id"],
                    date_rezervare["data_rezervare"],
                    date_rezervare["data_expirare"],
                    date_rezervare["status"],
                    id
                ))

                if cursor.rowcount == 0:
                    return "Rezervarea nu exista.", 404

    except ForeignKeyViolation:
        return "Cititorul sau cartea nu exista.", 409

    except CheckViolation:
        return "Datele sau statusul rezervarii sunt invalide.", 400

    except NotNullViolation:
        return "Lipsesc informatii obligatorii.", 400

    except UniqueViolation:
        return "Modificarea intra in conflict cu o rezervare existenta.", 409

    return redirect(url_for("lista_rezervari"))


# DELETE
@app.route("/rezervari/sterge/<int:id>", methods=["POST"])
def sterge_rezervare(id):
    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute("""
                DELETE FROM rezervari
                WHERE id = %s
            """, (id,))

            if cursor.rowcount == 0:
                return "Rezervarea nu exista.", 404

    return redirect(url_for("lista_rezervari"))


# ==================================
# PORNIRE FLASK
# ==================================

if __name__ == "__main__":
    print("Pornesc aplicatia...")

    initialize_fixtures()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )