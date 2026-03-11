import requests
from functools import lru_cache

@lru_cache(maxsize=5000)
def get_bin_info_by_bin(bin_number: str):
    """
    Consulta real de BIN (cacheado por BIN)
    """
    try:
        r = requests.get(
            f"https://lookup.binlist.net/{bin_number}",
            timeout=10
        )
        if r.status_code != 200:
            return None

        data = r.json()

        return {
            "scheme": (data.get("scheme") or "N/A").upper(),
            "type": (data.get("type") or "N/A").upper(),
            "brand": (data.get("brand") or "N/A"),
            "bank": data.get("bank", {}).get("name", "N/A"),
            "country": data.get("country", {}).get("name", "N/A"),
            "emoji": data.get("country", {}).get("emoji", "🌍"),
        }

    except Exception:
        return None


def get_bin_info(cc: str):
    """
    Obtiene BIN info REAL para CADA CC
    """
    if not cc or len(cc) < 6:
        return None

    bin_number = cc[:6]
    return get_bin_info_by_bin(bin_number)
