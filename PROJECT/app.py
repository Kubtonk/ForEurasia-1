from flask import Flask, render_template, request
from modif import MODIF, RECOMMENDATIONS
from calculator import calculate_price
from data_storage import save_history

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    RESULT = None
    RECOMM = []
    SELECT = []
    USER_INFO = {}

    MODS = list(MODIF)

    if request.method == "POST":
        USER_INFO = {
            "имя": request.form.get("name", "").strip(),
            "компания": request.form.get("company", "").strip(),
            "номер телефона": request.form.get("phone", "").strip(),
            "email": request.form.get("email", "").strip()
        }

        RAW_SELECT = request.form.getlist("modifications")
        SELECT = [ITEM for ITEM in RAW_SELECT if ITEM in MODIF]

        for MOD in SELECT:
            if MOD in RECOMMENDATIONS:
                REC = RECOMMENDATIONS[MOD]
                if REC not in SELECT:
                    RECOMM.append(REC)

        ACTION = request.form.get("recommendation_action")

        if RECOMM and not ACTION:
            return render_template(
                "index.html",
                MODS=MODS,
                MODIF=MODIF,
                SELECTED=SELECT,
                RECOMM=RECOMM,
                RESULT=None,
                USER_INFO=USER_INFO
            )

        if ACTION == "add":
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

if __name__ == "__main__":
    app.run(debug=True)
