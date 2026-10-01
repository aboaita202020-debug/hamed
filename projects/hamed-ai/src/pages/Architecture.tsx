export default function Architecture() {
  const layers = [
    {
      name: 'Channels Layer',
      nameAr: 'طبقة القنوات',
      color: 'from-cyan-500 to-blue-500',
      items: [
        { name: 'Telegram Adapter', status: 'active' },
        { name: 'WhatsApp Adapter', status: 'planned' },
        { name: 'Web Dashboard', status: 'active' },
        { name: 'REST API', status: 'active' },
      ],
    },
    {
      name: 'Orchestration Layer',
      nameAr: 'طبقة التنسيق',
      color: 'from-purple-500 to-indigo-500',
      items: [
        { name: 'HamedOrchestrator', status: 'active' },
        { name: 'Task Dispatcher', status: 'active' },
        { name: 'Dependency Injection', status: 'active' },
      ],
    },
    {
      name: 'Agent Layer',
      nameAr: 'طبقة الوكلاء',
      color: 'from-emerald-500 to-teal-500',
      items: [
        { name: 'LeadAgent', status: 'active' },
        { name: 'SalesAgent', status: 'active' },
        { name: 'OpportunityHunter', status: 'active' },
        { name: 'RevenueAgent', status: 'active' },
        { name: 'NegotiationAgent', status: 'idle' },
        { name: 'PermissionGate', status: 'active' },
      ],
    },
    {
      name: 'Tools Layer',
      nameAr: 'طبقة الأدوات',
      color: 'from-amber-500 to-orange-500',
      items: [
        { name: 'CRMTool', status: 'active' },
        { name: 'WebSearchTool', status: 'active' },
        { name: 'Tool Registry', status: 'active' },
      ],
    },
    {
      name: 'AI Providers Layer',
      nameAr: 'طبقة مزودي الذكاء الاصطناعي',
      color: 'from-pink-500 to-rose-500',
      items: [
        { name: 'Anthropic Claude', status: 'active' },
        { name: 'Provider Router', status: 'active' },
        { name: 'Fallback System', status: 'active' },
      ],
    },
    {
      name: 'Data Layer',
      nameAr: 'طبقة البيانات',
      color: 'from-gray-500 to-gray-600',
      items: [
        { name: 'SQLite Repository', status: 'active' },
        { name: 'CRM Dedup Engine', status: 'active' },
        { name: 'Audit Log', status: 'active' },
      ],
    },
  ];

  const fileStructure = [
    {
      folder: 'app/',
      description: 'Core application code',
      files: [
        { name: 'config.py', desc: 'Environment variable configuration' },
        { name: 'db/', desc: 'SQLite + Repository + CRM Dedup + Audit Log' },
        { name: 'permissions/', desc: 'Permission Layer / Approval Gate' },
        { name: 'tools/', desc: 'Tool Registry + WebSearchTool + CRMTool' },
        { name: 'agents/', desc: 'All agents + Orchestrator' },
        { name: 'ai_providers/', desc: 'Router + Fallback between providers' },
        { name: 'channels/', desc: 'Telegram adapter (optional)' },
        { name: 'api/', desc: 'FastAPI server (optional)' },
      ],
    },
    {
      folder: 'scripts/',
      description: 'Entry points',
      files: [
        { name: 'run_server.py', desc: 'Dashboard/Webhook server' },
        { name: 'run_telegram.py', desc: 'Telegram bot (polling)' },
      ],
    },
    {
      folder: 'tests/',
      description: '23 unittest tests (stdlib only)',
      files: [
        { name: 'test_orchestrator.py', desc: 'Orchestrator tests' },
        { name: 'test_lead_agent.py', desc: 'Lead agent tests' },
        { name: 'test_sales_agent.py', desc: 'Sales agent tests' },
        { name: 'test_tools.py', desc: 'Tool tests' },
        { name: 'test_db.py', desc: 'Database tests' },
      ],
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold text-white">System Architecture</h1>
        <p className="text-gray-400 mt-1">Multi-Agent Business Operating System • Layered Design</p>
      </div>

      {/* Architecture Diagram */}
      <div className="bg-gray-800 rounded-xl border border-gray-700 p-6">
        <h2 className="text-lg font-semibold text-white mb-6">System Layers</h2>
        <div className="space-y-4">
          {layers.map((layer, i) => (
            <div key={layer.name} className="relative">
              <div className={`bg-gradient-to-r ${layer.color} rounded-xl p-4 border border-white/10`}>
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h3 className="text-white font-semibold">{layer.name}</h3>
                    <p className="text-white/70 text-sm">{layer.nameAr}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-white/60 text-sm">Layer {i + 1}</span>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  {layer.items.map((item) => (
                    <div
                      key={item.name}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                        item.status === 'active'
                          ? 'bg-white/20 text-white'
                          : 'bg-white/10 text-white/60'
                      }`}
                    >
                      {item.name}
                      {item.status === 'idle' && <span className="ml-1 text-xs">(idle)</span>}
                      {item.status === 'planned' && <span className="ml-1 text-xs">(planned)</span>}
                    </div>
                  ))}
                </div>
              </div>
              {i < layers.length - 1 && (
                <div className="flex justify-center my-2">
                  <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* File Structure */}
      <div className="bg-gray-800 rounded-xl border border-gray-700 p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Project Structure</h2>
        <div className="space-y-4">
          {fileStructure.map((section) => (
            <div key={section.folder} className="border border-gray-700 rounded-lg overflow-hidden">
              <div className="bg-gray-700/50 px-4 py-3 flex items-center justify-between">
                <div>
                  <code className="text-emerald-400 font-mono">{section.folder}</code>
                  <span className="text-gray-400 text-sm ml-3">{section.description}</span>
                </div>
              </div>
              <div className="p-4 space-y-2">
                {section.files.map((file) => (
                  <div key={file.name} className="flex items-start gap-3 text-sm">
                    <code className="text-blue-400 font-mono whitespace-nowrap">{file.name}</code>
                    <span className="text-gray-400">— {file.desc}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Design Principles */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gradient-to-br from-blue-500/10 to-blue-600/5 rounded-xl border border-blue-500/30 p-5">
          <h3 className="text-blue-400 font-semibold mb-3">🔄 Dependency Injection</h3>
          <p className="text-sm text-gray-300 mb-2">
            Every Agent and Tool is injected, not imported directly. This allows:
          </p>
          <ul className="text-sm text-gray-400 space-y-1">
            <li>• Adding new agents without modifying existing code</li>
            <li>• Swapping database implementations easily</li>
            <li>• Testing each component in isolation</li>
          </ul>
        </div>

        <div className="bg-gradient-to-br from-emerald-500/10 to-emerald-600/5 rounded-xl border border-emerald-500/30 p-5">
          <h3 className="text-emerald-400 font-semibold mb-3">🧪 Zero External Dependencies</h3>
          <p className="text-sm text-gray-300 mb-2">
            The core system uses Python stdlib only. This means:
          </p>
          <ul className="text-sm text-gray-400 space-y-1">
            <li>• No pip install required for core functionality</li>
            <li>• 23 tests run without any external packages</li>
            <li>• Works on Windows 7 with Python 3.8</li>
          </ul>
        </div>

        <div className="bg-gradient-to-br from-purple-500/10 to-purple-600/5 rounded-xl border border-purple-500/30 p-5">
          <h3 className="text-purple-400 font-semibold mb-3">🔌 Optional Layers</h3>
          <p className="text-sm text-gray-300 mb-2">
            Telegram, Dashboard API, and AI Providers are optional:
          </p>
          <ul className="text-sm text-gray-400 space-y-1">
            <li>• Core works without Telegram bot token</li>
            <li>• AI providers can be mocked for testing</li>
            <li>• Dashboard is JSON-only by default</li>
          </ul>
        </div>

        <div className="bg-gradient-to-br from-amber-500/10 to-amber-600/5 rounded-xl border border-amber-500/30 p-5">
          <h3 className="text-amber-400 font-semibold mb-3">📊 Audit & Permissions</h3>
          <p className="text-sm text-gray-300 mb-2">
            Built-in security and tracking:
          </p>
          <ul className="text-sm text-gray-400 space-y-1">
            <li>• Every action logged to audit trail</li>
            <li>• Permission gates for high-value deals</li>
            <li>• Approval workflows for sensitive operations</li>
          </ul>
        </div>
      </div>

      {/* Deployment Options */}
      <div className="bg-gray-800 rounded-xl border border-gray-700 p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Deployment Options</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg bg-gray-700/30 border border-gray-600">
            <div className="text-2xl mb-2">🐳</div>
            <h3 className="text-white font-medium mb-2">Docker</h3>
            <p className="text-sm text-gray-400 mb-3">Full containerized deployment with volume persistence</p>
            <code className="text-xs text-emerald-400">docker-compose up</code>
          </div>
          <div className="p-4 rounded-lg bg-gray-700/30 border border-gray-600">
            <div className="text-2xl mb-2">🐍</div>
            <h3 className="text-white font-medium mb-2">Python Direct</h3>
            <p className="text-sm text-gray-400 mb-3">Run directly with venv, works on Windows 7+</p>
            <code className="text-xs text-emerald-400">python scripts/run_server.py</code>
          </div>
          <div className="p-4 rounded-lg bg-gray-700/30 border border-gray-600">
            <div className="text-2xl mb-2">☁️</div>
            <h3 className="text-white font-medium mb-2">Cloud (Railway/Koyeb)</h3>
            <p className="text-sm text-gray-400 mb-3">Deploy to free cloud platforms with GitHub Actions</p>
            <code className="text-xs text-emerald-400">git push origin main</code>
          </div>
        </div>
      </div>
    </div>
  );
}
