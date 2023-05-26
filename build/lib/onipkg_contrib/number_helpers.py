import decimal


def round_or_0(value, digits=2):
    try:
        return round(decimal.Decimal(value), digits)
    except Exception:
        return 0


def round_or_1(value, digits=2):
    try:
        qtd = round(decimal.Decimal(value), digits)
        return qtd if qtd >= 1 else 1
    except Exception:
        return 1
