import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 获取地理位置的函数
def get_ip_info(ip):
    try:
        # 使用 ip-api.com 免费接口
        response = requests.get(f"http://ip-api.com/json/{ip}?lang=zh-CN")
        data = response.json()
        if data.get("status") == "success":
            return f"{data.get('country')} {data.get('regionName')} {data.get('city')} ({data.get('isp')})"
        return "位置信息获取失败"
    except Exception as e:
        return f"查询出错: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    # 获取用户输入
    user_data = request.json
    username = user_data.get('name', '匿名用户')
    content = user_data.get('message', '无内容')

    # 获取真实 IP (处理 Railway 代理)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    
    # 获取地理位置
    location = get_ip_info(ip)

    # 打印到 Railway 日志 (你在控制台就能看到)
    print("\n" + "="*30)
    print(f"🔔 收到新客服咨询！")
    print(f"👤 用户姓名: {username}")
    print(f"💬 咨询内容: {content}")
    print(f"🌐 客户 IP : {ip}")
    print(f"📍 具体位置: {location}")
    print("="*30 + "\n")

    return jsonify({"status": "success", "message": "留言已收到，我们会尽快处理！"})

if __name__ == '__main__':
    # Railway 必须读取 PORT 环境变量
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
