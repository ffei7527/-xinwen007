@app.route('/')
def index():
    # 专家建议：在这里放一份备用新闻数据，防止API失效
    backup_news = [
        {"title": "2026年全球科技峰会今日开幕", "description": "大会聚焦量子计算与生成式AI的深度融合，探讨未来十年人类社会的技术底座。"},
        {"title": "国际能源机构发布最新报告", "description": "报告预测，可再生能源将在今年年底前占据全球发电总量的40%以上。"},
        {"title": "新型抗病毒药物进入临床三期", "description": "该药物由全球多所大学联合开发，有望彻底改变季节性流行病的防治现状。"}
    ]
    # 尝试获取新闻（你可以根据之前学的接入News API），如果失败则使用备用数据
    news_articles = get_recent_international_news() or backup_news
    return render_template('index.html', news=news_articles)
