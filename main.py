import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 获取地理位置的函数（保持不变）
def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?lang=zh-CN")
        data = response.json()
        if data.get("status") == "success":
            return f"{data.get('country')} {data.get('regionName')} {data.get('city')} ({data.get('isp')})"
        return "位置信息获取失败"
    except Exception as e:
        return f"查询出错: {str(e)}"

# --- 新增：新闻获取函数 ---
def get_recent_international_news():
    # 实际应用中，这里会调用一个新闻API，例如 News API, GNews API 等
    # 为简化演示，这里返回一些模拟数据，或者你可以替换为真实API调用
    # 注意：真实API可能需要API Key，并且有调用频率限制
    
    # 示例：使用 NewsAPI (需要注册获取API_KEY，并替换 YOUR_NEWS_API_KEY)
    # news_api_key = os.environ.get('NEWS_API_KEY', 'YOUR_NEWS_API_KEY') # 建议设置为环境变量
    # url = f"https://newsapi.org/v2/top-headlines?language=en&category=general&apiKey={news_api_key}"
    # response = requests.get(url)
    # if response.status_code == 200:
    #     articles = response.json().get('articles', [])
    #     # 过滤掉没有标题或内容的文章
    #     return [a for a in articles if a.get('title') and a.get('description')]
    # return [] # 返回空列表表示获取失败

    # 简化的模拟数据
    return [
        {"title": "国际空间站新发现：火星微生物可能存在", "description": "科学家在国际空间站模拟火星环境下，发现了能存活的微生物迹象，预示着火星生命的可能性。", "url": "#"},
        {"title": "全球气候峰会达成历史性协议，聚焦减排", "description": "多国领导人签署协议，承诺在未来十年内大幅削减碳排放，应对全球变暖。", "url": "#"},
        {"title": "新兴市场经济体增长超预期，提振全球经济信心", "description": "亚洲和非洲部分国家经济表现强劲，成为拉动世界经济增长的新引擎。", "url": "#"},
        {"title": "人工智能伦理问题引发关注，各国呼吁制定国际标准", "description": "随着AI技术飞速发展，其潜在的伦理风险成为全球性议题，亟待规范。", "url": "#"},
        {"title": "中东地区局势趋缓，和平进程取得新进展", "description": "多方斡旋下，地区冲突有所降级，为和平谈判创造了条件。", "url": "#"}
    ]

@app.route('/')
def index():
    # 获取新闻数据
    news_articles = get_recent_international_news()
    # 渲染 index.html，并将新闻数据传递给模板
    return render_template('index.html', news=news_articles)

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
