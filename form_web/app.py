from flask import Flask, render_template, request
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1380390969371004969/vV1CojqZppGytUNMjkybAMYI4lwBPV13aUUYk7r-bgIVFmvprs_fjfH1f2u-_6cJkdQ4"  # Reemplaza esto con tu webhook real

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        ip = request.remote_addr
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
