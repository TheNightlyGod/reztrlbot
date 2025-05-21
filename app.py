from flask import Flask, render_template_string, request, jsonify
import requests, config, htmlfiles

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template_string(htmlfiles.INDEX_HTML, site_key=config.RECAPTCHA_SITE_KEY)

@app.route("/verify", methods=["POST"])
def verify():
    recaptcha_response = request.form.get("g-recaptcha-response")
    if not recaptcha_response:
        return jsonify({"success": False, "error": "Ответ reCAPTCHA не получен."})

    payload = {
        "secret": config.RECAPTCHA_SECRET_KEY,
        "response": recaptcha_response
    }
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    result = r.json()

    if result.get("success"):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Проверка reCAPTCHA не пройдена. Попробуйте ещё раз."})

if __name__ == "__main__":
    app.run(host="localhost", port=6533)
