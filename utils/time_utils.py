from datetime import datetime

def tiempo_relativo(fecha):
    if not fecha:
        return "Nunca"

    diff = datetime.utcnow() - fecha
    segundos = diff.total_seconds()

    if segundos < 60:
        return "activo ahora"
    elif segundos < 3600:
        return f"activo hace {int(segundos//60)} min"
    elif segundos < 86400:
        return f"activo hace {int(segundos//3600)} horas"
    elif segundos < 2592000:
        return f"activo hace {int(segundos//86400)} días"
    else:
        return f"activo hace {int(segundos//2592000)} meses"
