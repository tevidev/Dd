import asyncio
from services.julie_api import JulieAPI

API_KEY_JULIE = "42f00e13-2c88-44da-8064-c945225d58bb"

GATE_ALIAS = {
    "in": "inari",
    "yu": "yurei",
    "da": "dakiniten",
}

def procesar_tarjeta(cc: str, alias: str):
    route = GATE_ALIAS.get(alias)
    if not route:
        return {
            "status": "dead",
            "message": "Invalid gate alias",
            "cc": cc
        }

    api = JulieAPI(API_KEY_JULIE)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(
            api.check_card(route, cc)
        )

        # ✅ RESPUESTA VACÍA
        if not result:
            return {
                "status": "dead",
                "message": "Empty API response",
                "cc": cc
            }

        # ✅ RESPUESTA INVÁLIDA
        if not isinstance(result, dict):
            return {
                "status": "dead",
                "message": "Non-JSON API response",
                "cc": cc
            }

        return result

    except ValueError:
        # 🔥 ESTE ES EL ERROR QUE ESTABAS VIENDO
        return {
            "status": "dead",
            "message": "Invalid JSON response (blocked / rate limit)",
            "cc": cc
        }

    except Exception as e:
        return {
            "status": "dead",
            "message": f"API Exception: {str(e)}",
            "cc": cc
        }

    finally:
        loop.close()
