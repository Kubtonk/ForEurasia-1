import json
from datetime import datetime

HISTORY_FILE = "history.json"

def save_history(info_from_user, calcResult, MODS):
    record = {
        "Время": datetime.now().isoformat(),
        "Пользователь": info_from_user,
        "Модификаций": MODS,
        "Расчет": calcResult
    }

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(record)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
