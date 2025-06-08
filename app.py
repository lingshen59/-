from flask import Flask, render_template, request
import requests
import time
import os

app = Flask(__name__)

# Discord Webhook (替换为你自己的URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1381387383156641862/obfw1eDK3X7qGGLm_4P79MX_ghyv1HQavjRLU-IpHgk38ObIeD1cqcBH9lvb40y04mqE"

def get_client_ip():
    """安全获取客户端真实IPv4地址"""
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip:
        for candidate in ip.split(','):
            candidate = candidate.strip()
            if candidate.replace('.', '').isdigit() and 7 <= len(candidate) <= 15:
                return candidate
    return request.remote_addr

def ip_usa_vpn(ip):
    """改进的VPN检测函数"""
    if not ip or not ip.replace('.', '').isdigit():
        return False
        
    try:
        response = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,proxy,hosting",
            timeout=3
        )
        data = response.json()
        return data.get('proxy', False) or data.get('hosting', False)
    except:
        return False

@app.route("/", methods=["GET", "POST"])
def form():
    try:
        ip = get_client_ip()
        print(f"访问IP: {ip}")  # 调试日志

        # VPN检测
        if ip_usa_vpn(ip):
            return render_template("blocked.html"), 403

        if request.method == "POST":
            form_data = {
                "Discord User": request.form.get("discord_user", "未提供"),
                "País": request.form.get("pais", "未提供"),
                "Habilidades": request.form.get("skills", "未提供"),
                "Horas disponibles": request.form.get("horas", "未提供"),
                "Días disponibles": request.form.get("dias", "未提供"),
                "Edad": request.form.get("edad", "未提供"),
                "Hacks": request.form.get("hacks", "未提供"),
                "Aportes": request.form.get("aportar", "未提供"),
                "IP": ip,
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            # 发送到Discord (错误时静默失败)
            try:
                if WEBHOOK_URL.startswith("http"):
                    embed = {
                        "title": "📝 Nuevo formulario",
                        "color": 0x00ff00,
                        "fields": [{"name": k, "value": v} for k, v in form_data.items()]
                    }
                    requests.post(WEBHOOK_URL, json={"embeds": [embed]}, timeout=3)
            except:
                pass

            return "✅ Formulario enviado. Puedes cerrar esta página."

        return render_template("form.html")
    except Exception as e:
        print(f"服务器错误: {e}")
        return "⚠️ Error interno del servidor", 500

@app.route("/check-vpn")
def check_vpn():
    """供前端检查VPN状态的接口"""
    return {"vpn": ip_usa_vpn(get_client_ip())}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    
