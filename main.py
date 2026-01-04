import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xinwen007-special-key'
# 增加 eventlet 异步模式支持
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

def get_ip_info(ip):
    try:
        # 增加超时限制，防止网页加载卡顿
        res = requests.get(f"http://ip-api.com/json/{ip}?lang=zh-CN", timeout=2)
        data = res.json()
        return f"{data.get('city', '未知')} ({data.get('isp', '')})"
    except:
        return "查询失败"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@socketio.on('client_msg')
def handle_client_msg(data):
    sid = request.sid
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    location = get_ip_info(ip)
    emit('server_to_admin', {
        'sid': sid,
        'user': data.get('name', '读者'),
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
