from flask import Flask, jsonify
from database import get_connection
from fixtures import initialize_fixtures

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "proiect": "Sistem de Gestionare a unei Biblioteci",
        "status": "functional",
        "etapa": "Etapa 1 - Modelare"
    })


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


if __name__ == "__main__":
    print("Pornesc aplicatia...", flush=True)

    initialize_fixtures()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )