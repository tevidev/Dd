import aiohttp
import asyncio
import json

API_URL_CREATE = "https://juliettechk.cc/API_Access/createCheck"
API_URL_GET = "https://juliettechk.cc/API_Access/getCheck"

# ================= PROXY CONFIG =================
PROXY_HOST = "p.webshare.io:80"
PROXY_USER = "izvhxurt-rotate"
PROXY_PASS = "acx0bzc9xbkg"

PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}"
# ================================================


def interpretar_estado(estado):
    if isinstance(estado, bool):
        return "live" if estado else "dead"

    estado = str(estado).lower()

    if "live" in estado or "approved" in estado:
        return "live"
    if "dead" in estado or "declined" in estado:
        return "dead"

    return estado


class JulieAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def _safe_json(self, response):
        """
        Evita el error:
        Expecting value: line 1 column 1 (char 0)
        """
        text = await response.text()
        if not text:
            raise Exception("Empty response from API")

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response: {text[:200]}")

    async def create_check(self, session, route, card):
        payload = {
            "api_key": self.api_key,
            "route": route,
            "card": card
        }

        async with session.post(
            API_URL_CREATE,
            json=payload,
            proxy=PROXY_URL,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as r:
            data = await self._safe_json(r)

        if data.get("success"):
            return data["task_id"]

        raise Exception(str(data))

    async def get_check(self, session, task_id):
        payload = {
            "api_key": self.api_key,
            "task_id": task_id
        }

        while True:
            async with session.post(
                API_URL_GET,
                json=payload,
                proxy=PROXY_URL,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as r:
                data = await self._safe_json(r)

            if data.get("response") == "processing_task":
                await asyncio.sleep(3)
                continue

            return data

    async def check_card(self, route, card):
        connector = aiohttp.TCPConnector(ssl=False)

        async with aiohttp.ClientSession(connector=connector) as session:
            task_id = await self.create_check(session, route, card)
            result = await self.get_check(session, task_id)

        status = interpretar_estado(result.get("status"))
        message = result.get("response", "N/A")

        return {
            "status": status,
            "message": message,
            "cc": card
        }
