import type { Page } from '../App';

interface SidebarProps {
  currentPage: Page;
  onNavigate: (page: Page) => void;
  isOpen: boolean;
}

const navItems: { page: Page; label: string; icon: string; labelAr: string }[] = [
  { page: 'dashboard', label: 'Dashboard', icon: '📊', labelAr: 'لوحة التحكم' },
  { page: 'agents', label: 'Agents', icon: '🤖', labelAr: 'الوكلاء' },
  { page: 'tests', label: 'Tests', icon: '✅', labelAr: 'الاختبارات' },
  { page: 'crm', label: 'CRM', icon: '📋', labelAr: 'إدارة العملاء' },
  { page: 'endpoints', label: 'API', icon: '🔌', labelAr: 'نقاط الوصول' },
  { page: 'revenue', label: 'Revenue', icon: '💰', labelAr: 'الإيرادات' },
  { page: 'architecture', label: 'Architecture', icon: '🏗️', labelAr: 'بنية النظام' },
  { page: 'console', label: 'Console', icon: '💻', labelAr: 'طرفية التحكم' },
  { page: 'mobile', label: 'Mobile', icon: '📱', labelAr: 'دليل الموبايل' },
  { page: 'ai-brains', label: 'AI Brains', icon: '🧠', labelAr: 'العقول الذكية' },
  { page: 'monetization', label: 'Monetization', icon: '💰', labelAr: 'تحقيق الدخل' },
  { page: 'money-plan', label: 'Money Plan', icon: '💵', labelAr: 'خطة الدخل' },
  { page: 'free-tools', label: 'Free Tools', icon: '🛠️', labelAr: 'أدوات مجانية' },
  { page: 'auto-business', label: 'Auto Business', icon: '🤖', labelAr: 'أعمال تلقائية' },
  { page: 'about-hamed', label: 'About Hamed', icon: '🧠', labelAr: 'عن حامد' },
  { page: 'learning', label: 'Learning', icon: '📚', labelAr: 'التعلم من التجارب' },
  { page: 'smart-strategies', label: 'Smart Strategies', icon: '🎯', labelAr: 'استراتيجيات ذكية' },
  { page: 'call-center', label: 'Call Center', icon: '📞', labelAr: 'مركز المكالمات' },
  { page: 'smart-responses', label: 'Smart Responses', icon: '🤖', labelAr: 'الردود الذكية' },
  { page: 'super-ai', label: 'Super AI', icon: '🧠', labelAr: 'الذكاء الخارق' },
  { page: 'advanced-ai', label: 'Advanced AI', icon: '🤯', labelAr: 'الذكاء المتقدم' },
  { page: 'telegram-bot', label: 'Telegram Bot', icon: '📱', labelAr: 'بوت تيليجرام' },
];

export default function Sidebar({ currentPage, onNavigate, isOpen }: SidebarProps) {
  return (
    <aside
      className={`fixed lg:static inset-y-0 left-0 z-30 w-64 bg-gray-800 border-r border-gray-700 transform transition-transform duration-200 flex flex-col ${
        isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      }`}
    >
      <div className="flex items-center gap-3 p-5 border-b border-gray-700">
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center text-xl font-bold">
          H
        </div>
        <div>
          <h1 className="text-lg font-bold text-white">Hamed AI</h1>
          <p className="text-xs text-gray-400">Business Operating System</p>
        </div>
      </div>

      <nav className="p-3 space-y-1 flex-1 overflow-y-auto">
        {navItems.map((item) => (
          <button
            key={item.page}
            onClick={() => onNavigate(item.page)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all ${
              currentPage === item.page
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
            }`}
          >
            <span className="text-lg">{item.icon}</span>
            <div className="text-left">
              <div>{item.label}</div>
              <div className="text-xs opacity-60">{item.labelAr}</div>
            </div>
          </button>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-700">
        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-700/50">
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-xs text-gray-300">System Online</span>
        </div>
        <div className="mt-2 px-3 text-xs text-gray-500">
          v1.0.0 • Multi-Agent System
        </div>
        <div className="mt-1 px-3 text-xs text-gray-500">
          📱 Mobile Ready
        </div>
      </div>
    </aside>
  );
}
