# 在 handle_client_msg 中，加入 sid (Session ID) 来区分客户
@socketio.on('client_msg')
def handle_client_msg(data):
    # 获取唯一的会话ID
    sid = request.sid 
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    location = get_ip_info(ip)
    
    # 转发给后台，带上 sid
    emit('server_to_admin', {
        'sid': sid,
        'user': data.get('name', '访客'),
        'msg': data.get('msg', ''),
        'ip': ip,
        'loc': location
    }, broadcast=True)

# 增加：客服指定回复某个客户
@socketio.on('admin_reply')
def handle_admin_reply(data):
    target_sid = data.get('sid')
    # 只发给特定的客户
    emit('server_to_client', {'msg': data.get('msg', '')}, room=target_sid)
