import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# --- 第一步：必须先初始化 app ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'xinwen007-secret'
# 允许跨域，确保实时通讯正常
socketio = SocketIO(app, cors_allowed_origins="*")

# --- 第二步：定义工具函数 ---
def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?lang=zh-CN", timeout=5)
        data = response.json()
        if data.get("status") == "success":
            return f"{data.get('city')} ({data.get('isp')})"
        return "未知位置"
    except:
        return "查询超时"

def get_news():
    # 模拟最新新闻数据，确保页面不空白
    return [
        {"title": "2026年全球数字经济峰会开幕", "description": "大会重点讨论了通用人工智能在跨境贸易中的应用规范。"},
        {"title": "新型超导材料实现工业化突破", "description": "该材料将使能源传输损耗降低90%，预计明年投入电网建设。"},
        {"title": "多国达成蓝色海洋保护共识", "description": "旨在恢复受损的珊瑚礁生态，并严格限制深海采矿行为。"}
    ]

# --- 第三步：定义路由 (使用 @app) ---
@app.route('/')
def index():
    news_data = get_news()
    return render_template('index.html', news=news_data)

@app.route('/admin')
def admin():
    return render_template('admin.html')

# --- 第四步：定义实时通讯 (使用 @socketio) ---
@socketio.on('client_msg')
def handle_client_msg(data):
    # 获取 IP 逻辑
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    location = get_ip_info(ip)
    
    # 将用户消息、IP、位置发送到管理后台
    emit('server_to_admin', {
        'user': data.get('name', '访客'),
        'msg': data.get('msg', ''),
        'ip': ip,
        'loc': location
    }, broadcast=True)

@socketio.on('admin_reply')
def handle_admin_reply(data):
    # 将客服回复发送给用户
    emit('server_to_client', {'msg': data.get('msg', '')}, broadcast=True)

# --- 第五步：运行程序 ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # 实时应用必须使用 socketio.run
    socketio.run(app, host='0.0.0.0', port=port)
