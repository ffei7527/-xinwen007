import os
import requests
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'miandian-pro-2026'
# 确保在 Railway 环境下稳定运行的设置
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@socketio.on('client_msg')
def handle_client_msg(data):
    sid = request.sid
    # 抓取真实IP
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    location = "位置查询中..."
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?lang=zh-CN", timeout=2)
        loc_data = res.json()
        location = f"{loc_data.get('city','')} {loc_data.get('isp','')}"
    except:
        location = "未知位置"

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
    emit('server_to_client', {'msg': data.get('msg', '')}, room=target_sid)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
