from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1380390969371004969/vV1CojqZppGytUNMjkybAMYI4lwBPV13aUUYk7r-bgIVFmvprs_fjfH1f2u-_6cJkdQ4"  # Tu webhook aquí

def get_client_ip():
    if "X-Forwarded-For" in request.headers:
        return request.headers["X-Forwarded-For"].split(",")[0].strip()
    return request.remote_addr

def ip_usa_vpn(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=proxy")
        return r.json().get("proxy", False)
    except:
        return False

@app.route("/", methods=["GET", "POST"])
def form():
    ip = get_client_ip()

    if ip_usa_vpn(ip):
        return render_template("blocked.html"), 403

    if request.method == "POST":
        respuestas = {
            "Discord User": request.form.get("discord_user"),
            "País": request.form.get("pais"),
            "¿Qué sabes hacer?": request.form.get("skills"),
            "Horas disponibles y a qué hora?": request.form.get("horas"),
            "Días disponibles": request.form.get("dias"),
            "Edad": request.form.get("edad") or "No respondida",
            "¿Tienes hacks?": request.form.get("hacks") or "No respondida",
            "¿En qué vas a aportar?": request.form.get("aportar")
        }

        embed = {
            "title": "📝 Nuevo formulario enviado",
            "fields": [{"name": k, "value": v} for k, v in respuestas.items()],
            "footer": {"text": f"IP: {ip}"}
        }

        requests.post(WEBHOOK_URL, json={"embeds": [embed]})
        return "✅ Formulario enviado correctamente. Puedes cerrar esta página."

    return render_template("form.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
