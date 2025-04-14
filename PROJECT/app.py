from flask import Flask, render_template, request, jsonify
from modif import MODIF, RECOMMENDATIONS
from calculator import calculate_price
from data_storage import save_history, load_history

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    RESULT = None
    RECOMM = []
    SELECT = []
    USER_INFO = {}

    MODS = list(MODIF)

    if request.method == "POST":
        # Данные пользователя
        USER_INFO = {
            "имя": request.form.get("name", "").strip(),
            "компания": request.form.get("company", "").strip(),
            "номер телефона": request.form.get("phone", "").strip(),
            "email": request.form.get("email", "").strip()
        }

        RAW_SELECT = request.form.getlist("modifications")
        SELECT = [ITEM for ITEM in RAW_SELECT if ITEM in MODIF]

        # Проверяем рекомендации
        for MOD in SELECT:
            if MOD in RECOMMENDATIONS:
                REC = RECOMMENDATIONS[MOD]
                if REC not in SELECT:
                    RECOMM.append(REC)

        WANT_ADD = request.form.get("accept_recommendations")

        # Если рекомендации есть, но пользователь не подтвердил — ждём подтверждение
        if RECOMM and not WANT_ADD:
            return render_template(
                "index.html",
                MODS=MODS,
                MODIF=MODIF,
                SELECTED=SELECT,
                RECOMM=RECOMM,
                RESULT=None,
                USER_INFO=USER_INFO
            )

        # Добавляем рекомендации, если согласие получено
        if WANT_ADD:
            for R in RECOMM:
                if R not in SELECT:
                    SELECT.append(R)

        RESULT = calculate_price(SELECT)
        save_history(USER_INFO, RESULT, SELECT)

    return render_template(
        "index.html",
        MODS=MODS,
        MODIF=MODIF,
        SELECTED=SELECT,
        RECOMM=[],
        RESULT=RESULT,
        USER_INFO=USER_INFO
    )


#API

@app.route("/api/history", methods=["GET"])
def api_history():
    return jsonify(load_history())

@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    data = request.get_json()

    USER_INFO = data.get("user", {})
    SELECT = data.get("modifications", [])

    SELECT = [mod for mod in SELECT if mod in MODIF]

    for MOD in SELECT:
        if MOD in RECOMMENDATIONS:
            REC = RECOMMENDATIONS[MOD]
            if REC not in SELECT:
                SELECT.append(REC)

    RESULT = calculate_price(SELECT)
    save_history(USER_INFO, RESULT, SELECT)

    return jsonify({
        "user": USER_INFO,
        "selected": SELECT,
        "result": RESULT
    })

if __name__ == "__main__":
    app.run(debug=True)
