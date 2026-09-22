from flask import Flask, render_template, request

from guidance import get_guidance
from risk_engine import calculate_risk

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            result = calculate_risk(url)

    return render_template("index.html", result=result)


@app.route("/guidance", methods=["POST"])
def guidance():
    money_sent = "money_sent" in request.form
    info_shared = "info_shared" in request.form
    result = get_guidance(money_sent, info_shared)
    return render_template("guidance.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
