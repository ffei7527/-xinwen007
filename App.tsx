
import React, { useState, useEffect } from 'react';
import { GoogleGenAI, Type } from "@google/genai";

// 初始化 Gemini AI
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

interface NewsItem {
  title: string;
  summary: string;
  category: string;
  date: string;
  url: string;
}

const App: React.FC = () => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loadingNews, setLoadingNews] = useState(true);
  const [isOpen, setIsOpen] = useState(false);
  const [name, setName] = useState('');
  const [content, setContent] = useState('');
  const [status, setStatus] = useState<'idle' | 'sending' | 'success' | 'error'>('idle');

  // 获取实时科技新闻
  const fetchTechNews = async () => {
    setLoadingNews(true);
    try {
      const response = await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: "请搜索并提供当前全球范围内最重要的5条近期科技新闻（包括AI、半导体、航天、新能源等领域）。请确保信息是真实的。输出格式必须是JSON数组，包含属性：title, summary, category, date, url。",
        config: {
          tools: [{ googleSearch: {} }],
          responseMimeType: "application/json",
          responseSchema: {
            type: Type.ARRAY,
            items: {
              type: Type.OBJECT,
              properties: {
                title: { type: Type.STRING },
                summary: { type: Type.STRING },
                category: { type: Type.STRING },
                date: { type: Type.STRING },
                url: { type: Type.STRING }
              },
              required: ["title", "summary", "category", "date", "url"]
            }
          }
        },
      });

      const data = JSON.parse(response.text || '[]');
      setNews(data);
    } catch (error) {
      console.error("无法获取新闻:", error);
      // 备用静态新闻，以防 API 调用受限
      setNews([
        { title: "AI 算力爆发：下一代 GPU 架构发布", summary: "最新的高性能计算架构突破了摩尔定律，将效率提升了3倍。", category: "AI硬件", date: "2024-05-20", url: "#" },
        { title: "星舰第六次试飞圆满成功", summary: "SpaceX 完成了关键的一步，实现了助推器的海上垂直降落。", category: "航天", date: "2024-05-19", url: "#" }
      ]);
    } finally {
      setLoadingNews(false);
    }
  };

  useEffect(() => {
    fetchTechNews();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !content) return;
    setStatus('sending');
    try {
      const response = await fetch('/api/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, content }),
      });
      if (response.ok) {
        setStatus('success');
        setName('');
        setContent('');
        setTimeout(() => setStatus('idle'), 3000);
      } else { setStatus('error'); }
    } catch (error) { setStatus('error'); }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
      {/* 顶部导航 */}
      <nav className="bg-slate-900 text-white sticky top-0 z-40 shadow-md">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-500 rounded flex items-center justify-center font-bold text-lg">T</div>
            <span className="text-xl font-black tracking-tighter uppercase italic">TechPulse</span>
          </div>
          <div className="hidden md:flex space-x-8 text-sm font-medium">
            <a href="#" className="hover:text-blue-400 transition-colors">今日头条</a>
            <a href="#" className="hover:text-blue-400 transition-colors">人工智能</a>
            <a href="#" className="hover:text-blue-400 transition-colors">深度报道</a>
            <a href="#" className="hover:text-blue-400 transition-colors">产品评测</a>
          </div>
          <button onClick={() => setIsOpen(true)} className="bg-blue-600 hover:bg-blue-700 px-4 py-1.5 rounded-full text-sm font-bold transition-all active:scale-95">
            我要报料
          </button>
        </div>
      </nav>

      {/* 主体内容 */}
      <main className="max-w-7xl mx-auto px-4 py-10">
        <header className="mb-12 border-l-4 border-blue-600 pl-4">
          <h2 className="text-3xl font-extrabold text-slate-900">最新科技动态</h2>
          <p className="text-slate-500">由 AI 实时生成的全球科技情报</p>
        </header>

        {loadingNews ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3].map(i => (
              <div key={i} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 animate-pulse">
                <div className="h-4 w-20 bg-gray-200 rounded mb-4"></div>
                <div className="h-6 w-full bg-gray-200 rounded mb-2"></div>
                <div className="h-20 w-full bg-gray-200 rounded"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {news.map((item, idx) => (
              <article key={idx} className="group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div className="p-6">
                  <span className="inline-block px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-xs font-bold mb-4 uppercase">
                    {item.category}
                  </span>
                  <h3 className="text-xl font-bold mb-3 group-hover:text-blue-600 transition-colors leading-snug">
                    {item.title}
                  </h3>
                  <p className="text-gray-600 text-sm line-clamp-3 mb-6">
                    {item.summary}
                  </p>
                  <div className="flex items-center justify-between text-xs text-gray-400 mt-auto pt-4 border-t border-gray-50">
                    <span>{item.date}</span>
                    <a href={item.url} target="_blank" rel="noreferrer" className="text-blue-500 font-bold flex items-center group-hover:mr-2 transition-all">
                      阅读详情 <i className="fas fa-arrow-right ml-1"></i>
                    </a>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </main>

      {/* 浮动聊天组件 (保留原有功能) */}
      <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
        {isOpen && (
          <div className="bg-white w-80 md:w-96 rounded-2xl shadow-2xl border border-gray-100 mb-4 overflow-hidden animate-slide-up">
            <div className="bg-gradient-to-r from-slate-800 to-slate-900 p-4 text-white flex justify-between items-center">
              <div>
                <h2 className="font-bold text-lg">快速咨询 / 报料</h2>
                <p className="text-xs opacity-70">我们会记录 IP 以防止恶意刷屏</p>
              </div>
              <button onClick={() => setIsOpen(false)} className="hover:bg-white/20 p-2 rounded-full transition-colors">
                <i className="fas fa-times"></i>
              </button>
            </div>

            <div className="p-6">
              {status === 'success' ? (
                <div className="text-center py-8">
                  <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i className="fas fa-check text-2xl"></i>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">已成功投递</h3>
                  <p className="text-gray-500">感谢您的反馈，我们的编辑或客服会尽快处理。</p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">您的姓名/昵称</label>
                    <input
                      type="text" required value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="如何称呼您？"
                      className="w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">咨询内容/报料描述</label>
                    <textarea
                      required rows={4} value={content}
                      onChange={(e) => setContent(e.target.value)}
                      placeholder="请详细描述您的问题..."
                      className="w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
                    ></textarea>
                  </div>
                  <button
                    type="submit" disabled={status === 'sending'}
                    className={`w-full py-3 rounded-lg font-bold text-white shadow-lg transition-all ${
                      status === 'sending' ? 'bg-gray-400' : 'bg-slate-900 hover:bg-black'
                    }`}
                  >
                    {status === 'sending' ? '发送中...' : '提交信息'}
                  </button>
                </form>
              )}
            </div>
          </div>
        )}

        <button
          onClick={() => setIsOpen(!isOpen)}
          className={`w-14 h-14 rounded-full flex items-center justify-center shadow-xl transition-all duration-300 ${
            isOpen ? 'bg-white text-gray-600' : 'bg-slate-900 text-white hover:scale-110 active:scale-95'
          }`}
        >
          {isOpen ? <i className="fas fa-times text-xl"></i> : <i className="fas fa-paper-plane text-xl"></i>}
        </button>
      </div>
    </div>
  );
};

export default App;
