from concurrent.futures import ThreadPoolExecutor
import time

# Pool global
executor = ThreadPoolExecutor(max_workers=20)

def tarea_larga(user_id):
    print(f"[HILO] Inicia usuario {user_id}")
    time.sleep(10)
    print(f"[HILO] Termina usuario {user_id}")
