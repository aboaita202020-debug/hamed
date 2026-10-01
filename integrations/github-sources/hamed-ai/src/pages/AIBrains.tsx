import { useState } from 'react';

export default function AIBrains() {
  const [selectedBrain, setSelectedBrain] = useState<string | null>('claude');

  const brains = [
    {
      id: 'claude',
      name: 'Anthropic Claude',
      nameAr: 'أنثروبيك كلود',
      icon: '🧠',
      provider: 'Anthropic',
      status: 'active',
      description: 'The main AI brain powering Hamed\'s intelligence',
      descriptionAr: 'العقل الرئيسي اللي بيغذي ذكاء حامد',
      capabilities: [
        'Natural language understanding',
        'Arabic language support',
        'Business logic reasoning',
        'Lead qualification',
        'Deal negotiation',
        'Revenue forecasting',
      ],
      capabilitiesAr: [
        'فهم اللغة الطبيعية',
        'دعم اللغة العربية',
        'التفكير في منطق الأعمال',
        'تأهيل العملاء المحتملين',
        'التفاوض على الصفقات',
        'التنبؤ بالإيرادات',
      ],
      usage: 'Primary AI for all agent decisions',
      cost: 'Pay per token',
      speed: 'Fast',
    },
    {
      id: 'orchestrator',
      name: 'HamedOrchestrator',
      nameAr: 'المنسق الرئيسي',
      icon: '🎯',
      provider: 'Custom Logic',
      status: 'active',
      description: 'Coordinates all agents and manages task dispatch',
      descriptionAr: 'ينسق كل الوكلاء ويدير توزيع المهام',
      capabilities: [
        'Agent registration',
        'Task dispatching',
        'Dependency injection',
        'Workflow management',
        'Error handling',
        'Load balancing',
      ],
      capabilitiesAr: [
        'تسجيل الوكلاء',
        'توزيع المهام',
        'حقن التبعيات',
        'إدارة سير العمل',
        'معالجة الأخطاء',
        'توزيع الحمل',
      ],
      usage: 'Central coordination of all agents',
      cost: 'Free (built-in)',
      speed: 'Instant',
    },
    {
      id: 'lead',
      name: 'LeadAgent',
      nameAr: 'وكيل العملاء المحتملين',
      icon: '🎯',
      provider: 'AI + Rules',
      status: 'active',
      description: 'Captures and qualifies incoming leads',
      descriptionAr: 'يلتأهل العملاء المحتملين الواردين',
      capabilities: [
        'Lead capture',
        'Qualification scoring',
        'CRM deduplication',
        'Source tracking',
        'Priority assignment',
        'Auto-routing',
      ],
      capabilitiesAr: [
        'التقاط العملاء',
        'تسجيل التأهيل',
        'إلغاء التكرار',
        'تتبع المصدر',
        'تعيين الأولوية',
        'التوجيه التلقائي',
      ],
      usage: 'Process every new lead automatically',
      cost: 'Free (built-in)',
      speed: 'Instant',
    },
    {
      id: 'sales',
      name: 'SalesAgent',
      nameAr: 'وكيل المبيعات',
      icon: '💼',
      provider: 'AI + Rules',
      status: 'active',
      description: 'Manages sales pipeline and deal stages',
      descriptionAr: 'يدير خط المبيعات ومراحل الصفقات',
      capabilities: [
        'Pipeline management',
        'Stage transitions',
        'Conversion tracking',
        'Deal forecasting',
        'Revenue calculation',
        'Win/loss analysis',
      ],
      capabilitiesAr: [
        'إدارة خط المبيعات',
        'انتقالات المراحل',
        'تتبع التحويل',
        'التنبؤ بالصفقات',
        'حساب الإيرادات',
        'تحليل الفوز/الخسارة',
      ],
      usage: 'Track and optimize sales process',
      cost: 'Free (built-in)',
      speed: 'Instant',
    },
    {
      id: 'opportunity',
      name: 'OpportunityHunter',
      nameAr: 'صياد الفرص',
      icon: '🔍',
      provider: 'AI + Web Search',
      status: 'active',
      description: 'Scans web and social signals for opportunities',
      descriptionAr: 'يفحص إشارات الويب ووسائل التواصل للفرص',
      capabilities: [
        'Web signal scanning',
        'Social media monitoring',
        'Market gap detection',
        'Competitor analysis',
        'Trend identification',
        'Opportunity scoring',
      ],
      capabilitiesAr: [
        'فحص إشارات الويب',
        'مراقبة وسائل التواصل',
        'اكتشاف فجوات السوق',
        'تحليل المنافسين',
        'تحديد الاتجاهات',
        'تسجيل الفرص',
      ],
      usage: 'Discover new business opportunities',
      cost: 'Free (mock) / Paid (real)',
      speed: 'Periodic scan',
    },
    {
      id: 'revenue',
      name: 'RevenueAgent',
      nameAr: 'وكيل الإيرادات',
      icon: '💰',
      provider: 'AI + Analytics',
      status: 'active',
      description: 'Tracks revenue streams and forecasts',
      descriptionAr: 'يتتبع تدفقات الإيرادات والتنبؤات',
      capabilities: [
        'Revenue tracking',
        'Forecast calculations',
        'Pricing strategy',
        'Income ideas generation',
        'Financial analysis',
        'Growth projections',
      ],
      capabilitiesAr: [
        'تتبع الإيرادات',
        'حسابات التنبؤ',
        'استراتيجية التسعير',
        'توليد أفكار الدخل',
        'التحليل المالي',
        'توقعات النمو',
      ],
      usage: 'Monitor and optimize revenue',
      cost: 'Free (built-in)',
      speed: 'Real-time',
    },
    {
      id: 'negotiation',
      name: 'NegotiationAgent',
      nameAr: 'وكيل التفاوض',
      icon: '🤝',
      provider: 'AI + Rules',
      status: 'idle',
      description: 'Handles deal negotiations with approval gates',
      descriptionAr: 'يتعامل مع مفاوضات الصفقات مع بوابات الموافقة',
      capabilities: [
        'Deal proposal generation',
        'Price negotiation',
        'Terms optimization',
        'Approval workflow',
        'Risk assessment',
        'Counter-offer handling',
      ],
      capabilitiesAr: [
        'توليد عروض الصفقات',
        'التفاوض على السعر',
        'تحسين الشروط',
        'سير عمل الموافقة',
        'تقييم المخاطر',
        'معالجة العروض المضادة',
      ],
      usage: 'Negotiate high-value deals',
      cost: 'Free (built-in)',
      speed: 'On-demand',
    },
    {
      id: 'permission',
      name: 'PermissionGate',
      nameAr: 'بوابة الصلاحيات',
      icon: '🔐',
      provider: 'Security Logic',
      status: 'active',
      description: 'Enforces approval workflows and permissions',
      descriptionAr: 'يفرض سير عمل الموافقة والصلاحيات',
      capabilities: [
        'Permission checking',
        'Approval workflows',
        'Audit logging',
        'Access control',
        'Compliance enforcement',
        'Security boundaries',
      ],
      capabilitiesAr: [
        'فحص الصلاحيات',
        'سير عمل الموافقة',
        'تسجيل التدقيق',
        'التحكم في الوصول',
        'فرض الامتثال',
        'حدود الأمان',
      ],
      usage: 'Protect sensitive operations',
      cost: 'Free (built-in)',
      speed: 'Instant',
    },
  ];

  const selected = brains.find(b => b.id === selectedBrain);

  const statusColors: Record<string, string> = {
    active: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    idle: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    error: 'bg-red-500/20 text-red-400 border-red-500/30',
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold text-white">🧠 AI Brains</h1>
        <p className="text-gray-400 mt-1">العقول اللي بتشغل النظام</p>
      </div>

      {/* Overview */}
      <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-xl border border-purple-500/30 p-5">
        <h2 className="text-lg font-semibold text-purple-400 mb-2">نظام متعدد العقول</h2>
        <p className="text-gray-300 text-sm">
          النظام بيستخدم <span className="text-emerald-400 font-bold">8 عقول</span> مختلفة:
          <br />
          • <span className="text-blue-400">عقل AI واحد</span> (Anthropic Claude) للتفكير المعقد
          <br />
          • <span className="text-emerald-400">7 عقول مدمجة</span> (Agents) للمهام المتخصصة
          <br />
          • كل عقل بيشتغل بشكل مستقل لكن منسق
        </p>
      </div>

      {/* Brains Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {brains.map((brain) => (
          <div
            key={brain.id}
            onClick={() => setSelectedBrain(brain.id)}
            className={`bg-gray-800 rounded-xl border p-5 cursor-pointer transition-all hover:scale-[1.02] ${
              selectedBrain === brain.id
                ? 'border-emerald-500/50 ring-1 ring-emerald-500/20'
                : 'border-gray-700 hover:border-gray-600'
            }`}
          >
            <div className="flex items-start justify-between mb-3">
              <span className="text-3xl">{brain.icon}</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium border ${statusColors[brain.status]}`}>
                {brain.status}
              </span>
            </div>
            <h3 className="text-white font-semibold text-sm">{brain.name}</h3>
            <p className="text-emerald-400/80 text-xs mb-2">{brain.nameAr}</p>
            <p className="text-gray-400 text-xs line-clamp-2">{brain.description}</p>
            <div className="mt-3 pt-3 border-t border-gray-700">
              <div className="text-xs text-gray-500">Provider</div>
              <div className="text-xs text-blue-400 font-medium">{brain.provider}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Selected Brain Details */}
      {selected && (
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-6">
          <div className="flex items-start gap-4 mb-6">
            <span className="text-5xl">{selected.icon}</span>
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-white">{selected.name}</h2>
              <p className="text-emerald-400 text-lg">{selected.nameAr}</p>
              <p className="text-gray-400 mt-2">{selected.description}</p>
              <p className="text-gray-500 text-sm mt-1" dir="rtl">{selected.descriptionAr}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Capabilities */}
            <div>
              <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                <span>⚡</span> Capabilities
              </h3>
              <ul className="space-y-2">
                {selected.capabilities.map((cap, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <span className="text-emerald-400 mt-0.5">✓</span>
                    <div>
                      <span className="text-gray-300">{cap}</span>
                      <br />
                      <span className="text-gray-500 text-xs">{selected.capabilitiesAr[i]}</span>
                    </div>
                  </li>
                ))}
              </ul>
            </div>

            {/* Info */}
            <div className="space-y-4">
              <div className="bg-gray-700/30 rounded-lg p-4">
                <div className="text-xs text-gray-500 mb-1">Usage</div>
                <div className="text-sm text-gray-300">{selected.usage}</div>
              </div>
              <div className="bg-gray-700/30 rounded-lg p-4">
                <div className="text-xs text-gray-500 mb-1">Cost</div>
                <div className="text-sm text-emerald-400 font-medium">{selected.cost}</div>
              </div>
              <div className="bg-gray-700/30 rounded-lg p-4">
                <div className="text-xs text-gray-500 mb-1">Speed</div>
                <div className="text-sm text-blue-400 font-medium">{selected.speed}</div>
              </div>
              <div className="bg-gray-700/30 rounded-lg p-4">
                <div className="text-xs text-gray-500 mb-1">Provider</div>
                <div className="text-sm text-purple-400 font-medium">{selected.provider}</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* AI Provider Info */}
      <div className="bg-gradient-to-r from-blue-500/10 to-cyan-500/10 rounded-xl border border-blue-500/30 p-5">
        <h3 className="text-blue-400 font-semibold mb-3">🤖 Anthropic Claude - العقل الرئيسي</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <div className="text-gray-500 mb-1">Model</div>
            <div className="text-white font-medium">Claude 3.5 Sonnet</div>
          </div>
          <div>
            <div className="text-gray-500 mb-1">Context Window</div>
            <div className="text-white font-medium">200K tokens</div>
          </div>
          <div>
            <div className="text-gray-500 mb-1">Languages</div>
            <div className="text-white font-medium">English, Arabic, +</div>
          </div>
        </div>
        <p className="text-gray-300 mt-4 text-sm">
          Claude هو العقل اللي بيفكر في القرارات المعقدة زي التفاوض، التأهيل، والتنبؤ.
          باقي العقول (Agents) مدمجة وبتشتغل بدون AI خارجي.
        </p>
      </div>

      {/* Architecture Note */}
      <div className="bg-gray-800 rounded-xl border border-gray-700 p-5">
        <h3 className="text-white font-semibold mb-3">🏗️ بنية النظام</h3>
        <div className="space-y-2 text-sm text-gray-300">
          <p>• <span className="text-emerald-400">Core</span> = Python stdlib only (بدون AI)</p>
          <p>• <span className="text-blue-400">AI Providers</span> = Optional layer (Claude, GPT, etc.)</p>
          <p>• <span className="text-purple-400">Agents</span> = Can work with or without AI</p>
          <p>• <span className="text-amber-400">Fallback</span> = Mock provider for testing</p>
        </div>
      </div>
    </div>
  );
}
