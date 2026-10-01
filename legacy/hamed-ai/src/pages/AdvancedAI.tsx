import { useState, useEffect } from 'react';

interface GeneratedIdea {
  id: number;
  idea_type: string;
  title: string;
  description: string;
  potential_value: number;
  confidence_score: number;
  knowledge_source: string;
  created_at: string;
}

interface Negotiation {
  id: number;
  client_id: string;
  service_type: string;
  initial_offer: number;
  client_counter: number;
  final_price: number;
  strategy_used: string;
  outcome: string;
  created_at: string;
}

interface Decision {
  id: number;
  decision_type: string;
  action: string;
  reasoning: string;
  confidence: number;
  created_at: string;
}

export default function AdvancedAI() {
  const [ideas, setIdeas] = useState<GeneratedIdea[]>([]);
  const [negotiations, setNegotiations] = useState<Negotiation[]>([]);
  const [decisions, setDecisions] = useState<Decision[]>([]);
  const [activeTab, setActiveTab] = useState<'ideas' | 'negotiations' | 'decisions'>('ideas');
  const [clientContext, setClientContext] = useState({
    type: 'business',
    industry: 'ecommerce',
    budget: 'medium',
    goals: ['increase_sales', 'improve_marketing']
  });

  useEffect(() => {
    // محاكاة تحميل البيانات
    const mockIdeas: GeneratedIdea[] = [
      {
        id: 1,
        idea_type: 'marketing',
        title: 'استراتيجية Content Marketing من Neil Patel',
        description: 'المحتوى هو الملك. ركز على تقديم قيمة حقيقية قبل البيع. استخدم SEO لجذب العملاء بشكل عضوي.',
        potential_value: 2500,
        confidence_score: 0.92,
        knowledge_source: 'Neil Patel',
        created_at: '2024-01-15T10:30:00'
      },
      {
        id: 2,
        idea_type: 'sales',
        title: 'تقنية Value-Based Selling من Grant Cardone',
        description: 'لا تبيع المنتج، بل بيع النتيجة. العميل لا يريد دريل، بل يريد حفرة في الحائط.',
        potential_value: 3200,
        confidence_score: 0.88,
        knowledge_source: 'Grant Cardone',
        created_at: '2024-01-15T11:00:00'
      },
      {
        id: 3,
        idea_type: 'negotiation',
        title: 'تقنية Win-Win Negotiation من Chris Voss',
        description: 'استمع أكثر مما تتكلم. استخدم الأسئلة المفتوحة. ابحث عن حلول تفيد الطرفين.',
        potential_value: 1800,
        confidence_score: 0.85,
        knowledge_source: 'Chris Voss',
        created_at: '2024-01-15T11:30:00'
      }
    ];

    const mockNegotiations: Negotiation[] = [
      {
        id: 1,
        client_id: 'client_123',
        service_type: 'website_analysis',
        initial_offer: 65,
        client_counter: 50,
        final_price: 57.5,
        strategy_used: 'compromise',
        outcome: 'successful',
        created_at: '2024-01-15T12:00:00'
      },
      {
        id: 2,
        client_id: 'client_456',
        service_type: 'seo_optimization',
        initial_offer: 195,
        client_counter: 150,
        final_price: 172.5,
        strategy_used: 'value_based',
        outcome: 'successful',
        created_at: '2024-01-15T13:00:00'
      }
    ];

    const mockDecisions: Decision[] = [
      {
        id: 1,
        decision_type: 'pricing',
        action: 'proceed_immediately',
        reasoning: 'فرصة عالية بمخاطر منخفضة - نفذ فوراً',
        confidence: 0.95,
        created_at: '2024-01-15T14:00:00'
      },
      {
        id: 2,
        decision_type: 'client_acceptance',
        action: 'proceed',
        reasoning: 'عميل جيد بميزانية مناسبة - اقبل المشروع',
        confidence: 0.88,
        created_at: '2024-01-15T14:30:00'
      }
    ];

    setIdeas(mockIdeas);
    setNegotiations(mockNegotiations);
    setDecisions(mockDecisions);
  }, []);

  const handleGenerateIdeas = () => {
    // محاكاة توليد أفكار جديدة
    const newIdeas: GeneratedIdea[] = [
      {
        id: Date.now(),
        idea_type: 'marketing',
        title: 'استراتيجية Social Proof من Robert Cialdini',
        description: 'الناس يتبعون ما يفعله الآخرون. استخدم شهادات العملاء، الأرقام، الحالات الدراسية.',
        potential_value: 2800,
        confidence_score: 0.94,
        knowledge_source: 'Robert Cialdini',
        created_at: new Date().toISOString()
      }
    ];
    setIdeas([...newIdeas, ...ideas]);
  };

  const handleAutonomousNegotiation = () => {
    // محاكاة تفاوض ذاتي
    const newNegotiation: Negotiation = {
      id: Date.now(),
      client_id: 'client_789',
      service_type: 'content_writing',
      initial_offer: 32.5,
      client_counter: 25,
      final_price: 28.75,
      strategy_used: 'package_deal',
      outcome: 'successful',
      created_at: new Date().toISOString()
    };
    setNegotiations([newNegotiation, ...negotiations]);
  };

  const handleMakeDecision = () => {
    // محاكاة اتخاذ قرار
    const newDecision: Decision = {
      id: Date.now(),
      decision_type: 'service_offer',
      action: 'proceed_with_caution',
      reasoning: 'قيمة عالية - نفذ بحذر',
      confidence: 0.85,
      created_at: new Date().toISOString()
    };
    setDecisions([newDecision, ...decisions]);
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">
          🧠 الذكاء الاصطناعي المتقدم
        </h1>
        <p className="text-gray-400">
          نظام AI يتعلم من رواد الأعمال، يفكر، يتفاوض، ويتخذ قرارات مستقلة
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/10 border border-purple-500/30 rounded-xl p-6">
          <div className="text-purple-400 text-sm mb-1">الأفكار المولدة</div>
          <div className="text-3xl font-bold text-white">{ideas.length}</div>
          <div className="text-purple-400 text-sm mt-2">فكرة جديدة</div>
        </div>

        <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/10 border border-blue-500/30 rounded-xl p-6">
          <div className="text-blue-400 text-sm mb-1">المفاوضات الناجحة</div>
          <div className="text-3xl font-bold text-white">{negotiations.length}</div>
          <div className="text-blue-400 text-sm mt-2">تفاوض ذاتي</div>
        </div>

        <div className="bg-gradient-to-br from-emerald-500/20 to-emerald-600/10 border border-emerald-500/30 rounded-xl p-6">
          <div className="text-emerald-400 text-sm mb-1">القرارات المتخذة</div>
          <div className="text-3xl font-bold text-white">{decisions.length}</div>
          <div className="text-emerald-400 text-sm mt-2">قرار مستقل</div>
        </div>

        <div className="bg-gradient-to-br from-amber-500/20 to-amber-600/10 border border-amber-500/30 rounded-xl p-6">
          <div className="text-amber-400 text-sm mb-1">معدل الثقة</div>
          <div className="text-3xl font-bold text-white">89%</div>
          <div className="text-amber-400 text-sm mt-2">ثقة عالية</div>
        </div>
      </div>

      {/* Control Panel */}
      <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 mb-6">
        <h2 className="text-xl font-bold text-white mb-4">لوحة التحكم</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-gray-400 text-sm mb-2">نوع العميل</label>
            <select
              value={clientContext.type}
              onChange={(e) => setClientContext({...clientContext, type: e.target.value})}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500"
            >
              <option value="business">شركة</option>
              <option value="startup">شركة ناشئة</option>
              <option value="freelancer">مستقل</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-400 text-sm mb-2">الصناعة</label>
            <select
              value={clientContext.industry}
              onChange={(e) => setClientContext({...clientContext, industry: e.target.value})}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500"
            >
              <option value="ecommerce">تجارة إلكترونية</option>
              <option value="services">خدمات</option>
              <option value="technology">تكنولوجيا</option>
              <option value="education">تعليم</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-400 text-sm mb-2">الميزانية</label>
            <select
              value={clientContext.budget}
              onChange={(e) => setClientContext({...clientContext, budget: e.target.value})}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500"
            >
              <option value="low">منخفضة</option>
              <option value="medium">متوسطة</option>
              <option value="high">عالية</option>
            </select>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={handleGenerateIdeas}
            className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            💡 توليد أفكار جديدة
          </button>
          <button
            onClick={handleAutonomousNegotiation}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            🤝 تفاوض ذاتي
          </button>
          <button
            onClick={handleMakeDecision}
            className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            ⚡ اتخاذ قرار
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setActiveTab('ideas')}
          className={`px-6 py-3 rounded-lg font-medium transition-colors ${
            activeTab === 'ideas'
              ? 'bg-purple-500 text-white'
              : 'bg-gray-800 text-gray-400 hover:text-white'
          }`}
        >
          💡 الأفكار المولدة
        </button>
        <button
          onClick={() => setActiveTab('negotiations')}
          className={`px-6 py-3 rounded-lg font-medium transition-colors ${
            activeTab === 'negotiations'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-800 text-gray-400 hover:text-white'
          }`}
        >
          🤝 المفاوضات
        </button>
        <button
          onClick={() => setActiveTab('decisions')}
          className={`px-6 py-3 rounded-lg font-medium transition-colors ${
            activeTab === 'decisions'
              ? 'bg-emerald-500 text-white'
              : 'bg-gray-800 text-gray-400 hover:text-white'
          }`}
        >
          ⚡ القرارات
        </button>
      </div>

      {/* Ideas Tab */}
      {activeTab === 'ideas' && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-white mb-4">
            💡 الأفكار المولدة ({ideas.length})
          </h2>
          
          {ideas.map(idea => (
            <div
              key={idea.id}
              className="bg-gray-800 border border-gray-700 rounded-xl p-6 hover:border-purple-500/50 transition-colors"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-bold text-white">
                      {idea.title}
                    </h3>
                    <span className="bg-purple-500/20 text-purple-400 px-3 py-1 rounded-full text-sm">
                      {idea.idea_type}
                    </span>
                  </div>
                  <p className="text-gray-400 text-sm">
                    المصدر: {idea.knowledge_source}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-emerald-400">
                    ${idea.potential_value.toFixed(0)}
                  </div>
                  <div className="text-gray-400 text-sm">
                    قيمة محتملة
                  </div>
                </div>
              </div>

              <div className="bg-gray-900/50 rounded-lg p-4 mb-4">
                <p className="text-gray-300 text-sm">
                  {idea.description}
                </p>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div>
                    <div className="text-gray-400 text-xs">مستوى الثقة</div>
                    <div className="text-purple-400 font-bold">
                      {(idea.confidence_score * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-gray-400 text-xs">تاريخ الإنشاء</div>
                    <div className="text-gray-300 text-sm">
                      {new Date(idea.created_at).toLocaleDateString('ar-EG')}
                    </div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button className="bg-purple-500/20 hover:bg-purple-500/30 text-purple-400 px-4 py-2 rounded-lg text-sm transition-colors">
                    📋 تقديم للعميل
                  </button>
                  <button className="bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-400 px-4 py-2 rounded-lg text-sm transition-colors">
                    💾 حفظ
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Negotiations Tab */}
      {activeTab === 'negotiations' && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-white mb-4">
            🤝 المفاوضات الذاتية ({negotiations.length})
          </h2>
          
          {negotiations.map(negotiation => (
            <div
              key={negotiation.id}
              className="bg-gray-800 border border-gray-700 rounded-xl p-6"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-white mb-1">
                    مفاوضات مع {negotiation.client_id}
                  </h3>
                  <p className="text-gray-400 text-sm">
                    الخدمة: {negotiation.service_type}
                  </p>
                </div>
                <span className="bg-emerald-500/20 text-emerald-400 px-3 py-1 rounded-full text-sm">
                  {negotiation.outcome}
                </span>
              </div>

              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="bg-gray-900/50 rounded-lg p-3">
                  <div className="text-gray-400 text-xs mb-1">العرض المبدئي</div>
                  <div className="text-white font-bold text-lg">
                    ${negotiation.initial_offer.toFixed(2)}
                  </div>
                </div>
                <div className="bg-gray-900/50 rounded-lg p-3">
                  <div className="text-gray-400 text-xs mb-1">رد العميل</div>
                  <div className="text-amber-400 font-bold text-lg">
                    ${negotiation.client_counter.toFixed(2)}
                  </div>
                </div>
                <div className="bg-gray-900/50 rounded-lg p-3">
                  <div className="text-gray-400 text-xs mb-1">السعر النهائي</div>
                  <div className="text-emerald-400 font-bold text-lg">
                    ${negotiation.final_price.toFixed(2)}
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <span className="text-gray-400 text-sm">الاستراتيجية: </span>
                  <span className="text-blue-400 font-medium">
                    {negotiation.strategy_used}
                  </span>
                </div>
                <div className="text-gray-400 text-sm">
                  {new Date(negotiation.created_at).toLocaleDateString('ar-EG')}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Decisions Tab */}
      {activeTab === 'decisions' && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-white mb-4">
            ⚡ القرارات المستقلة ({decisions.length})
          </h2>
          
          {decisions.map(decision => (
            <div
              key={decision.id}
              className="bg-gray-800 border border-gray-700 rounded-xl p-6"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-white mb-1">
                    قرار: {decision.decision_type}
                  </h3>
                  <p className="text-emerald-400 font-medium">
                    الإجراء: {decision.action}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-emerald-400">
                    {(decision.confidence * 100).toFixed(0)}%
                  </div>
                  <div className="text-gray-400 text-sm">ثقة</div>
                </div>
              </div>

              <div className="bg-gray-900/50 rounded-lg p-4 mb-4">
                <p className="text-gray-300 text-sm">
                  {decision.reasoning}
                </p>
              </div>

              <div className="text-gray-400 text-sm">
                {new Date(decision.created_at).toLocaleString('ar-EG')}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Info Section */}
      <div className="mt-8 bg-gradient-to-br from-purple-500/10 to-blue-500/10 border border-purple-500/30 rounded-xl p-6">
        <h3 className="text-xl font-bold text-white mb-4">💡 مميزات النظام</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-800/50 rounded-lg p-4">
            <div className="text-purple-400 font-bold mb-2">🧠 التعلم من رواد الأعمال</div>
            <p className="text-gray-300 text-sm">
              يتعلم من Neil Patel, Grant Cardone, Chris Voss, Robert Cialdini وغيرهم
            </p>
          </div>
          <div className="bg-gray-800/50 rounded-lg p-4">
            <div className="text-blue-400 font-bold mb-2">💡 توليد أفكار جديدة</div>
            <p className="text-gray-300 text-sm">
              يفكر ويستنتج أفكار مخصصة لكل عميل بناءً على السياق
            </p>
          </div>
          <div className="bg-gray-800/50 rounded-lg p-4">
            <div className="text-emerald-400 font-bold mb-2">🤝 تفاوض ذاتي</div>
            <p className="text-gray-300 text-sm">
              يتفاوض مع العملاء تلقائياً ويحقق أفضل الأسعار
            </p>
          </div>
          <div className="bg-gray-800/50 rounded-lg p-4">
            <div className="text-amber-400 font-bold mb-2">⚡ قرارات مستقلة</div>
            <p className="text-gray-300 text-sm">
              يتخذ قرارات مهمة وينفذها من غير ما يرجع لك
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
