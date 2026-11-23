import re
import time
import sys
import statistics
import getpass
import urllib.request
import urllib.parse
import http.cookiejar

from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://127.0.0.1:5000"

UTILIZATORI_SIMULTANI = int(sys.argv[1]) if len(sys.argv) > 1 else 5
CERERI_PER_UTILIZATOR = int(sys.argv[2]) if len(sys.argv) > 2 else 20

if UTILIZATORI_SIMULTANI < 1 or CERERI_PER_UTILIZATOR < 1:
    raise SystemExit("Valorile trebuie sa fie pozitive.")

email = input("Email utilizator test: ").strip()
parola = getpass.getpass("Parola: ")


def creeaza_sesiune():
    cookies = http.cookiejar.CookieJar()

    client = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookies)
    )

    with client.open(BASE_URL + "/login", timeout=15) as raspuns:
        html = raspuns.read().decode("utf-8")

    match = re.search(
        r'name=["\']csrf_token["\']\s+value=["\']([^"\']+)',
        html
    )

    if not match:
        raise RuntimeError("Tokenul CSRF nu a fost gasit.")

    date = urllib.parse.urlencode({
        "email": email,
        "parola": parola,
        "csrf_token": match.group(1)
    }).encode("utf-8")

    cerere = urllib.request.Request(
        BASE_URL + "/login",
        data=date,
        method="POST"
    )

    with client.open(cerere, timeout=15) as raspuns:
        raspuns.read()

        if not raspuns.geturl().endswith("/"):
            raise RuntimeError("Autentificarea a esuat.")

    return client


def test_utilizator(index):
    client = creeaza_sesiune()
    rezultate = []

    for _ in range(CERERI_PER_UTILIZATOR):
        inceput = time.perf_counter()

        try:
            with client.open(
                BASE_URL + "/carti",
                timeout=15
            ) as raspuns:
                raspuns.read()
                cod = raspuns.status

        except Exception:
            cod = 0

        durata = (
            time.perf_counter() - inceput
        ) * 1000

        rezultate.append((durata, cod))

    return rezultate


def main():
    print()
    print("Pornesc testul de incarcare...")
    print("Utilizatori simultani:", UTILIZATORI_SIMULTANI)
    print("Cereri per utilizator:", CERERI_PER_UTILIZATOR)

    inceput_total = time.perf_counter()
    rezultate = []

    with ThreadPoolExecutor(
        max_workers=UTILIZATORI_SIMULTANI
    ) as executor:

        taskuri = [
            executor.submit(test_utilizator, i)
            for i in range(UTILIZATORI_SIMULTANI)
        ]

        for task in as_completed(taskuri):
            rezultate.extend(task.result())

    durata_totala = time.perf_counter() - inceput_total

    timpi = sorted(r[0] for r in rezultate)

    succes = sum(1 for r in rezultate if r[1] == 200)
    erori = len(rezultate) - succes

    p95_index = min(
        len(timpi) - 1,
        max(0, int(len(timpi) * 0.95) - 1)
    )

    print()
    print("========== REZULTATE LOAD TEST ==========")
    print("Endpoint: GET /carti")
    print("Utilizatori simultani:", UTILIZATORI_SIMULTANI)
    print("Cereri totale:", len(rezultate))
    print("Cereri reusite:", succes)
    print("Erori:", erori)
    print("Timp total: %.3f secunde" % durata_totala)
    print("Timp mediu: %.3f ms" % statistics.mean(timpi))
    print("Timp minim: %.3f ms" % min(timpi))
    print("Timp maxim: %.3f ms" % max(timpi))
    print("P95: %.3f ms" % timpi[p95_index])
    print("Throughput: %.2f cereri/secunda" % (
        len(rezultate) / durata_totala
    ))
    print("=========================================")


if __name__ == "__main__":
    main()