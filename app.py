from flask import Flask, render_template, request
import requests
import os
import time

app = Flask(__name__)

# Webhook直接硬编码 (按你要求)
WEBHOOK_URL = "https://discord.com/api/webhooks/1380390969371004969/vV1CojqZppGytUNMjkybAMYI4lwBPV13aUUYk7r-bgIVFmvprs_fjfH1f2u-_6cJkdQ4"

def get_client_ip():
    """获取客户端真实IP"""
    if "X-Forwarded-For" in request.headers:
        return request.headers["X-Forwarded-For"].split(",")[0].strip()
    return request.remote_addr

def ip_usa_vpn(ip):
    """改进的VPN检测函数"""
    try:
        # 使用更全面的检测参数
        response = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,message,proxy,hosting,isp",
            timeout=3
        )
        data = response.json()
        
        # 调试输出（实际部署时可移除）
        print(f"IP检测结果: {data}")
        
        # 检查是否成功获取数据
        if data.get('status') != 'success':
            return False
            
        # 多重条件判断（代理/数据中心/ISP包含VPN关键词）
        is_proxy = data.get('proxy', False)
        is_hosting = data.get('hosting', False)
        isp = data.get('isp', '').lower()
        
        vpn_keywords = ['vpn', 'proxy', 'tor', 'anonymous']
        is_suspicious_isp = any(kw in isp for kw in vpn_keywords)
        
        return is_proxy or is_hosting or is_suspicious_isp
        
    except Exception as e:
        print(f"VPN检测错误: {e}")
        return False  # 出错时默认允许访问

@app.route("/", methods=["GET", "POST"])
def form():
    ip = get_client_ip()
    print(f"访问IP: {ip}")  # 调试日志

    # VPN检测
    if ip_usa_vpn(ip):
        print(f"已阻止VPN访问: {ip}")
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
