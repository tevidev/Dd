from config import OWNER_ID
from database.db import get_user


# =========================================================
# 👑 OWNER
# =========================================================
def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID


# =========================================================
# 🛒 SELLER
# =========================================================
def is_seller(user_id: int) -> bool:
    user = get_user(user_id)
    return bool(user and user.get("rank") == "SELLER")


# =========================================================
# ⭐ ADMIN / PRIVILEGIADO (OWNER + SELLER + ADMIN)
# =========================================================
def is_privileged(user_id: int) -> bool:
    if is_owner(user_id):
        return True

    user = get_user(user_id)
    return bool(user and user.get("rank") in ("SELLER", "ADMIN"))


# =========================================================
# 💳 QUIÉN PUEDE MANEJAR CRÉDITOS
# =========================================================
def can_manage_credits(user_id: int) -> bool:
    return is_privileged(user_id)
