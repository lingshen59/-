from flask import Flask, render_template, request
import requests
import os
import time

app = Flask(__name__)

# Webhook直接硬编码 (按你要求)
WEBHOOK_URL = "https://discord.com/api/webhooks/1381387383156641862/obfw1eDK3X7qGGLm_4P79MX_ghyv1HQavjRLU-IpHgk38ObIeD1cqcBH9lvb40y04mqE"

def get_client_ip():
    """安全获取客户端真实IP（IPv4格式）"""
    # 可能的IP头字段（按优先级检查）
    ip_headers = [
        'X-Real-IP',           # Nginx标准头
        'X-Forwarded-For',     # 通用代理头
        'CF-Connecting-IP',    # Cloudflare
        'HTTP_CLIENT_IP',
        'HTTP_X_FORWARDED_FOR'
    ]
    
    for header in ip_headers:
        if header in request.headers:
            ips = request.headers[header].split(',')
            # 提取第一个有效IPv4地址
            for ip in ips:
                ip = ip.strip()
                if is_valid_ipv4(ip):
                    return ip
    
    # 最后回退到直接连接IP
    remote_ip = request.remote_addr
    return remote_ip if is_valid_ipv4(remote_ip) else None

def is_valid_ipv4(ip):
    """验证是否是有效的IPv4地址"""
    if not ip or not isinstance(ip, str):
        return False
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except (ValueError, AttributeError):
        return False

@app.route("/")
def home():
    client_ip = get_client_ip()
    if not client_ip:
        return "无法获取有效IP地址", 400
        
    print(f"客户端真实IP: {client_ip}")  # 现在保证是109.92.84.93这种格式
    
    if ip_usa_vpn(client_ip):
        return render_template("blocked.html"), 403

    if request.method == "POST":
        # 获取表单数据
        form_data = {
            "Discord User": request.form.get("discord_user", "未提供"),
            "País": request.form.get("pais", "未提供"),
            "¿Qué sabes hacer?": request.form.get("skills", "未提供"),
            "Horas disponibles": request.form.get("horas", "未提供"),
            "Días disponibles": request.form.get("dias", "未提供"),
            "Edad": request.form.get("edad", "未提供"),
            "¿Tienes hacks?": request.form.get("hacks", "未提供"),
            "¿En qué vas a aportar?": request.form.get("aportar", "未提供"),
            "IP": ip,
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # 构建Discord Embed
        embed = {
            "title": "📝 Nuevo formulario enviado",
            "color": 0x00ff00,
            "fields": [{"name": k, "value": str(v)} for k, v in form_data.items()],
            "footer": {"text": "Formulario de Registro"}
        }

        # 发送到Discord
        try:
            requests.post(WEBHOOK_URL, json={"embeds": [embed]}, timeout=5)
        except Exception as e:
            print(f"Webhook发送失败: {e}")

        return "✅ Formulario enviado correctamente. Puedes cerrar esta página."

    return render_template("form.html")

@app.route("/check-vpn")
def check_vpn():
    """供前端检查VPN状态的接口"""
    return {"vpn_detected": ip_usa_vpn(get_client_ip())}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
