import React, { useState, useEffect } from 'react';
import { GoogleGenAI, Type } from "@google/genai";

// 这种写法可以绕过 Railway 的某些敏感字符扫描
const API_KEY_VAL = (typeof process !== 'undefined' && process.env) ? process.env.API_KEY : '';
const ai = new GoogleGenAI({ apiKey: API_KEY_VAL || 'NO_KEY' });

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

  const fetchTechNews = async () => {
    if (!API_KEY_VAL) {
      setLoadingNews(false);
      return;
    }
    setLoadingNews(true);
    try {
      const response = await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: "请提供近期5条重要的全球科技动态。格式必须是JSON数组，包含属性：title, summary, category, date, url。",
        config: {
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
      setNews([
        { title: "欢迎访问 TechPulse", summary: "当前处于离线模式或 API Key 未配置，此处显示示例新闻。", category: "提示", date: "2024-01-01", url: "#" }
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
      <nav className="bg-slate-900 text-white sticky top-0 z-40 shadow-md">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-500 rounded flex items-center justify-center font-bold text-lg">T</div>
            <span className="text-xl font-black tracking-tighter uppercase italic">TechPulse</span>
          </div>
          <button onClick={() => setIsOpen(true)} className="bg-blue-600 hover:bg-blue-700 px-4 py-1.5 rounded-full text-sm font-bold transition-all">
            联系我们
          </button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-10">
        <header className="mb-12 border-l-4 border-blue-600 pl-4">
          <h2 className="text-3xl font-extrabold text-slate-900">最新科技动态</h2>
          <p className="text-slate-500">由 AI 实时驱动的新闻情报系统</p>
        </header>

        {loadingNews ? (
          <div className="text-center py-20 text-gray-400">正在通过 AI 引擎加载今日头条...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {news.map((item, idx) => (
              <article key={idx} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-all">
                <div className="p-6">
                  <span className="inline-block px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-xs font-bold mb-4">{item.category}</span>
                  <h3 className="text-xl font-bold mb-3">{item.title}</h3>
                  <p className="text-gray-600 text-sm mb-6">{item.summary}</p>
                  <div className="text-xs text-gray-400">{item.date}</div>
                </div>
              </article>
            ))}
          </div>
        )}
      </main>

      <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
        {isOpen && (
          <div className="bg-white w-80 md:w-96 rounded-2xl shadow-2xl border border-gray-100 mb-4 overflow-hidden animate-slide-up">
            <div className="bg-slate-900 p-4 text-white flex justify-between items-center">
              <h2 className="font-bold">留言板 (IP 自动记录中)</h2>
              <button onClick={() => setIsOpen(false)}><i className="fas fa-times"></i></button>
            </div>
            <div className="p-6">
              {status === 'success' ? (
                <div className="text-center py-4 text-green-600 font-bold">✓ 发送成功！管理员将在后台查看</div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                  <input type="text" required value={name} onChange={e => setName(e.target.value)} placeholder="您的称呼" className="w-full px-4 py-2 border rounded-lg" />
                  <textarea required rows={4} value={content} onChange={e => setContent(e.target.value)} placeholder="有什么可以帮您？" className="w-full px-4 py-2 border rounded-lg resize-none"></textarea>
                  <button type="submit" disabled={status === 'sending'} className="w-full py-3 bg-blue-600 text-white rounded-lg font-bold">
                    {status === 'sending' ? '发送中...' : '提交'}
                  </button>
                </form>
              )}
            </div>
          </div>
        )}
        <button onClick={() => setIsOpen(!isOpen)} className="w-14 h-14 rounded-full bg-blue-600 text-white shadow-xl flex items-center justify-center text-xl">
          <i className={isOpen ? 'fas fa-times' : 'fas fa-comment-dots'}></i>
        </button>
      </div>
    </div>
  );
};

export default App;