import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# 开启跨域支持
socketio = SocketIO(app, cors_allowed_origins="*")

def get_ip_info(ip):
    try:
        # 2026年依然稳定的IP解析接口
        res = requests.get(f"http://ip-api.com/json/{ip}?lang=zh-CN")
        data = res.json()
        return f"{data.get('city', '未知')} ({data.get('isp', '')})"
    except:
        return "位置未知"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    # 这是你偷偷访问的页面，用于回复客户
    return render_template('admin.html')

# 处理用户发来的消息
@socketio.on('client_msg')
def handle_client_msg(data):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    location = get_ip_info(ip)
    
    # 将消息转发给客服页面，带上IP信息
    emit('server_to_admin', {
        'user': data['name'],
        'msg': data['msg'],
        'ip': ip,
        'loc': location
    }, broadcast=True)

# 处理客服发回的消息
@socketio.on('admin_reply')
def handle_admin_reply(data):
    # 将回复发送给所有用户（简单逻辑）
    emit('server_to_client', {'msg': data['msg']}, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
