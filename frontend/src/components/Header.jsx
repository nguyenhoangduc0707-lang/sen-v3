import React from 'react';

export default function Header({ role, username, onLogout }) {
  return (
    <header className="bg-slate-900 text-white px-6 py-4 flex justify-between items-center shadow-md border-b border-slate-800">
      <div className="flex items-center gap-3">
        <span className="text-2xl font-black tracking-wider text-blue-400">SEN V3</span>
        <span className="text-xs bg-slate-800 text-slate-400 px-2.5 py-1 rounded-full font-bold">PRO CONTROL PANEL</span>
      </div>
      {role !== 'guest' && (
        <div className="flex items-center gap-4">
          <span className="text-sm text-slate-300">
            User: <strong className="text-white">{username}</strong> (<strong className="text-blue-400 uppercase">{role}</strong>)
          </span>
          <button 
            onClick={onLogout}
            className="bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white px-3 py-1.5 rounded-lg text-sm transition font-medium"
          >
            Đăng xuất
          </button>
        </div>
      )}
    </header>
  );
}
