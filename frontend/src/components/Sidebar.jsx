import React from 'react';

export default function Sidebar({ role, currentPage, setCurrentPage }) {
  return (
    <aside className="w-full md:w-64 bg-slate-900 text-slate-300 flex flex-col border-t border-slate-800 md:border-t-0 shadow-xl">
      <div className="p-4 uppercase text-xs font-bold text-slate-500 tracking-wider">Trung tâm tác vụ</div>
      <nav className="flex-1 px-2 space-y-1 pb-4">
        <button 
          onClick={() => setCurrentPage('dashboard')}
          className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-semibold transition-colors ${
            currentPage === 'dashboard' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 hover:text-white'
          }`}
        >
          📊 Bảng điều khiển
        </button>

        {(role === 'admin' || role === 'manager') && (
          <button 
            onClick={() => setCurrentPage('sandbox')}
            className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-semibold transition-colors ${
              currentPage === 'sandbox' ? 'bg-amber-600 text-white' : 'hover:bg-slate-800 hover:text-white text-amber-400'
            }`}
          >
            🧪 Phòng Thử Nghiệm Sandbox
          </button>
        )}

        {role === 'admin' && (
          <>
            <button 
              onClick={() => setCurrentPage('users')}
              className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-semibold transition-colors ${
                currentPage === 'users' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 hover:text-white'
              }`}
            >
              👥 Quản lý thành viên
            </button>
            <button 
              onClick={() => setCurrentPage('tasks_assign')}
              className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-semibold transition-colors ${
                currentPage === 'tasks_assign' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 hover:text-white'
              }`}
            >
              🚀 Phân phối & Gán nhiệm vụ
            </button>
            <button 
              onClick={() => setCurrentPage('commissions')}
              className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-semibold transition-colors ${
                currentPage === 'commissions' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 hover:text-white'
              }`}
            >
              💰 Duyệt hoa hồng (3%)
            </button>
            <button 
              onClick={() => setCurrentPage('stealth')}
              className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-semibold transition-colors ${
                currentPage === 'stealth' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 hover:text-white text-rose-400'
              }`}
            >
              🕵️ Nhật ký ngầm & AZPI
            </button>
          </>
        )}

        {role === 'manager' && (
          <>
            <button 
              onClick={() => setCurrentPage('suggest_worker')}
              className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-semibold transition-colors ${
                currentPage === 'suggest_worker' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 hover:text-white'
              }`}
            >
              💡 Đề xuất Worker mới
            </button>
          </>
        )}

        <button 
          onClick={() => setCurrentPage('ai_assistant')}
          className={`w-full flex items-center px-4 py-3 rounded-lg text-sm font-semibold transition-colors ${
            currentPage === 'ai_assistant' ? 'bg-violet-600 text-white' : 'hover:bg-slate-800 hover:text-white text-violet-400'
          }`}
        >
          ✨ Trợ lý AI Copilot
        </button>
      </nav>
    </aside>
  );
}
