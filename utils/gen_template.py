import random
from datetime import datetime

def random_year(valid=True):
    now = datetime.now().year
    return str(random.randint(now, now + 6))

def random_month():
    return f"{random.randint(1, 12):02d}"

def random_cvv():
    return f"{random.randint(100, 999)}"

def fill_x(pattern: str):
    return "".join(
        str(random.randint(0, 9)) if c.lower() == "x" else c
        for c in pattern
    )

def invalidate_luhn(card: str):
    # fuerza que NO pase luhn (último dígito)
    last = int(card[-1])
    return card[:-1] + str((last + 5) % 10)

def generate_from_template(template: str, amount=10):
    generated = set()
    results = []

    pan, mm, yy, cvv = template.split("|")

    while len(results) < amount:
        card = fill_x(pan)

        if mm.lower() == "rnd":
            mm_f = random_month()
        else:
            mm_f = mm

        if yy.lower() == "rnd":
            yy_f = random_year()
        else:
            yy_f = yy

        if cvv.lower() == "rnd":
            cvv_f = random_cvv()
        else:
            cvv_f = cvv

        card = invalidate_luhn(card)

        final = f"{card}|{mm_f}|{yy_f}|{cvv_f}"

        if final not in generated:
            generated.add(final)
            results.append(final)

    return results
