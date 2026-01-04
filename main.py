import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# 1. 【必须最先运行】初始化 Flask 和 SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'xinwen007-pro-key'
# 必须先定义 socketio 对象，后面的 @socketio 才能生效
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# 2. 定义工具函数
def get_ip_info(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?lang=zh-CN", timeout=3)
        data = res.json()
        return f"{data.get('city', '未知')} ({data.get('isp', '')})"
    except:
        return "查询失败"

# 3. 定义网页路由
@app.route('/')
def index():
    # 这里放点模拟新闻，防止页面空荡荡
    news = [
        {"title": "2026国际局势：多边贸易协定达成", "description": "全球贸易迎来新转机，关税进一步降低。"},
        {"title": "量子芯片实现量产突破", "description": "新型计算设备性能提升百倍，功耗降低50%。"}
    ]
    return render_template('index.html', news=news)

@app.route('/admin')
def admin():
    return render_template('admin.html')

# 4. 【关键】处理实时通讯逻辑
@socketio.on('client_msg')
def handle_client_msg(data):
    sid = request.sid
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    location = get_ip_info(ip)
    # 转发给后台
    emit('server_to_admin', {
        'sid': sid,
        'user': data.get('name', '访客'),
        'msg': data.get('msg', ''),
        'ip': ip,
        'loc': location
    }, broadcast=True)

@socketio.on('admin_reply')
def handle_admin_reply(data):
    target_sid = data.get('sid')
    # 只发给特定的客户窗口
    emit('server_to_client', {'msg': data.get('msg', '')}, room=target_sid)

# 5. 启动程序
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
