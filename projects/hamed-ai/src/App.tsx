import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Agents from './pages/Agents';
import Tests from './pages/Tests';
import CRM from './pages/CRM';
import Endpoints from './pages/Endpoints';
import Revenue from './pages/Revenue';
import Architecture from './pages/Architecture';
import Console from './pages/Console';
import MobileGuide from './pages/MobileGuide';
import AIBrains from './pages/AIBrains';
import Monetization from './pages/Monetization';
import MoneyPlan from './pages/MoneyPlan';
import FreeTools from './pages/FreeTools';
import AutoBusiness from './pages/AutoBusiness';
import AboutHamed from './pages/AboutHamed';
import LearningDashboard from './pages/LearningDashboard';
import SmartStrategies from './pages/SmartStrategies';
import CallCenter from './pages/CallCenter';
import SmartResponses from './pages/SmartResponses';
import SuperAI from './pages/SuperAI';
import AdvancedAI from './pages/AdvancedAI';
import TelegramBotStatus from './pages/TelegramBotStatus';

export type Page = 'dashboard' | 'agents' | 'tests' | 'crm' | 'endpoints' | 'revenue' | 'architecture' | 'console' | 'mobile' | 'ai-brains' | 'monetization' | 'money-plan' | 'free-tools' | 'auto-business' | 'about-hamed' | 'learning' | 'smart-strategies' | 'call-center' | 'smart-responses' | 'super-ai' | 'advanced-ai' | 'telegram-bot';

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard': return <Dashboard onNavigate={setCurrentPage} />;
      case 'agents': return <Agents />;
      case 'tests': return <Tests />;
      case 'crm': return <CRM />;
      case 'endpoints': return <Endpoints />;
      case 'revenue': return <Revenue />;
      case 'architecture': return <Architecture />;
      case 'console': return <Console />;
      case 'mobile': return <MobileGuide />;
      case 'ai-brains': return <AIBrains />;
      case 'monetization': return <Monetization />;
      case 'money-plan': return <MoneyPlan />;
      case 'free-tools': return <FreeTools />;
      case 'auto-business': return <AutoBusiness />;
      case 'about-hamed': return <AboutHamed />;
      case 'learning': return <LearningDashboard />;
      case 'smart-strategies': return <SmartStrategies />;
      case 'call-center': return <CallCenter />;
      case 'smart-responses': return <SmartResponses />;
      case 'super-ai': return <SuperAI />;
      case 'advanced-ai': return <AdvancedAI />;
      case 'telegram-bot': return <TelegramBotStatus />;
      default: return <Dashboard onNavigate={setCurrentPage} />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white overflow-hidden">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <Sidebar
        currentPage={currentPage}
        onNavigate={(page) => { setCurrentPage(page); setSidebarOpen(false); }}
        isOpen={sidebarOpen}
      />

      <main className="flex-1 overflow-y-auto">
        {/* Mobile header */}
        <div className="lg:hidden flex items-center justify-between p-4 border-b border-gray-700">
          <button
            onClick={() => setSidebarOpen(true)}
            className="text-gray-300 hover:text-white"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <h1 className="text-lg font-bold text-emerald-400">Hamed AI</h1>
          <div className="w-6" />
        </div>

        <div className="p-4 md:p-6 lg:p-8">
          {renderPage()}
        </div>
      </main>
    </div>
  );
}
