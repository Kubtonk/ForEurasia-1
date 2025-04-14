from modif import BASE_COMBINE, MODIF

NDS = 0.20  # 20%

def calculate_price(SELECTED_MODS):
    TOTAL_MOD = sum(MODIF.get(NAME, 0) for NAME in SELECTED_MODS)

    NO_NDS_SUM = BASE_COMBINE + TOTAL_MOD

    NDS_SUM = NO_NDS_SUM * NDS

    TOTAL = NO_NDS_SUM + NDS_SUM

    return {
        "Просто Комбайн": BASE_COMBINE,
        "Модификаций": TOTAL_MOD,
        "Без НДСа": NO_NDS_SUM,
        "Сумма НДСа": NDS_SUM,
        "Вообщем": TOTAL
    }
