import { useState } from 'react';

interface Agent {
  name: string;
  nameAr: string;
  description: string;
  status: 'active' | 'idle' | 'error';
  lastRun: string;
  tasksCompleted: number;
  successRate: number;
  icon: string;
}

const agents: Agent[] = [
  {
    name: 'HamedOrchestrator',
    nameAr: 'المنسق الرئيسي',
    description: 'Coordinates all agents, manages task dispatch and dependency injection',
    status: 'active',
    lastRun: 'Just now',
    tasksCompleted: 156,
    successRate: 99.2,
    icon: '🧠',
  },
  {
    name: 'LeadAgent',
    nameAr: 'وكيل العملاء المحتملين',
    description: 'Captures, qualifies, and routes incoming leads through the CRM pipeline',
    status: 'active',
    lastRun: '2 min ago',
    tasksCompleted: 89,
    successRate: 94.5,
    icon: '🎯',
  },
  {
    name: 'SalesAgent',
    nameAr: 'وكيل المبيعات',
    description: 'Manages sales pipeline, deal stages, and conversion tracking',
    status: 'active',
    lastRun: '5 min ago',
    tasksCompleted: 67,
    successRate: 91.0,
    icon: '💼',
  },
  {
    name: 'OpportunityHunter',
    nameAr: 'صياد الفرص',
    description: 'Scans web and social signals to discover new business opportunities',
    status: 'idle',
    lastRun: '15 min ago',
    tasksCompleted: 34,
    successRate: 88.2,
    icon: '🔍',
  },
  {
    name: 'RevenueAgent',
    nameAr: 'وكيل الإيرادات',
    description: 'Tracks revenue streams, calculates forecasts, and manages pricing',
    status: 'active',
    lastRun: '8 min ago',
    tasksCompleted: 45,
    successRate: 96.8,
    icon: '💰',
  },
  {
    name: 'NegotiationAgent',
    nameAr: 'وكيل التفاوض',
    description: 'Handles deal negotiations with approval gates for high-value transactions',
    status: 'idle',
    lastRun: '30 min ago',
    tasksCompleted: 23,
    successRate: 87.0,
    icon: '🤝',
  },
  {
    name: 'PermissionGate',
    nameAr: 'بوابة الصلاحيات',
    description: 'Enforces approval workflows and permission boundaries across all agents',
    status: 'active',
    lastRun: '1 min ago',
    tasksCompleted: 210,
    successRate: 100,
    icon: '🔐',
  },
];

export default function Agents() {
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [filter, setFilter] = useState<'all' | 'active' | 'idle' | 'error'>('all');

  const filtered = filter === 'all' ? agents : agents.filter(a => a.status === filter);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-white">Agents</h1>
          <p className="text-gray-400 mt-1">Multi-Agent System • {agents.length} agents registered</p>
        </div>
        <div className="flex gap-2">
          {(['all', 'active', 'idle', 'error'] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                filter === f
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'bg-gray-700/50 text-gray-400 hover:text-white'
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {filtered.map((agent) => (
          <div
            key={agent.name}
            onClick={() => setSelectedAgent(selectedAgent?.name === agent.name ? null : agent)}
            className={`bg-gray-800 rounded-xl border p-5 cursor-pointer transition-all hover:scale-[1.02] ${
              selectedAgent?.name === agent.name
                ? 'border-emerald-500/50 ring-1 ring-emerald-500/20'
                : 'border-gray-700 hover:border-gray-600'
            }`}
          >
            <div className="flex items-start justify-between mb-3">
              <span className="text-3xl">{agent.icon}</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                agent.status === 'active' ? 'bg-emerald-500/20 text-emerald-400' :
                agent.status === 'idle' ? 'bg-amber-500/20 text-amber-400' :
                'bg-red-500/20 text-red-400'
              }`}>
                {agent.status}
              </span>
            </div>
            <h3 className="text-white font-semibold">{agent.name}</h3>
            <p className="text-emerald-400/80 text-sm mb-2">{agent.nameAr}</p>
            <p className="text-gray-400 text-sm line-clamp-2">{agent.description}</p>

            <div className="mt-4 grid grid-cols-3 gap-2 text-center">
              <div className="bg-gray-700/30 rounded-lg p-2">
                <div className="text-lg font-bold text-white">{agent.tasksCompleted}</div>
                <div className="text-xs text-gray-500">Tasks</div>
              </div>
              <div className="bg-gray-700/30 rounded-lg p-2">
                <div className="text-lg font-bold text-white">{agent.successRate}%</div>
                <div className="text-xs text-gray-500">Success</div>
              </div>
              <div className="bg-gray-700/30 rounded-lg p-2">
                <div className="text-xs font-medium text-gray-300 mt-1">{agent.lastRun}</div>
                <div className="text-xs text-gray-500">Last Run</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Stats */}
      <div className="bg-gray-800 rounded-xl border border-gray-700 p-5">
        <h2 className="text-lg font-semibold text-white mb-3">📊 Agent Performance Summary</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-lg bg-gray-700/30 text-center">
            <div className="text-2xl font-bold text-emerald-400">{agents.filter(a => a.status === 'active').length}</div>
            <div className="text-xs text-gray-400 mt-1">Active Agents</div>
          </div>
          <div className="p-4 rounded-lg bg-gray-700/30 text-center">
            <div className="text-2xl font-bold text-white">{agents.reduce((acc, a) => acc + a.tasksCompleted, 0)}</div>
            <div className="text-xs text-gray-400 mt-1">Total Tasks</div>
          </div>
          <div className="p-4 rounded-lg bg-gray-700/30 text-center">
            <div className="text-2xl font-bold text-blue-400">
              {(agents.reduce((acc, a) => acc + a.successRate, 0) / agents.length).toFixed(1)}%
            </div>
            <div className="text-xs text-gray-400 mt-1">Avg Success Rate</div>
          </div>
          <div className="p-4 rounded-lg bg-gray-700/30 text-center">
            <div className="text-2xl font-bold text-purple-400">24/7</div>
            <div className="text-xs text-gray-400 mt-1">Uptime</div>
          </div>
        </div>
      </div>
    </div>
  );
}
