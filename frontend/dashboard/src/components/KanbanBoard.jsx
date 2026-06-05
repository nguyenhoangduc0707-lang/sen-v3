import React from "react";
import { HiOutlineCheckCircle, HiOutlineClock, HiOutlineDocumentReport } from "react-icons/hi";

export default function KanbanBoard() {
  const tasks = [
    { title: "Post 3 video TikTok", user: "@minh", tag: "Affiliate", time: "12:00", icon: HiOutlineClock, iconColor: "text-amber-400 bg-amber-400/10 border-amber-400/20" },
    { title: "Thiết kế banner T6", user: "@linh", tag: "Design", time: "14:00", icon: HiOutlineClock, iconColor: "text-amber-400 bg-amber-400/10 border-amber-400/20" },
    { title: "Báo cáo AccessTrade", user: "@an", tag: "Report", time: "Đợi duyệt", icon: HiOutlineDocumentReport, iconColor: "text-indigo-400 bg-indigo-400/10 border-indigo-400/20" },
    { title: "Setup Shopee Smartlink", user: "@minh", tag: "Done", time: "Xong ✓", icon: HiOutlineCheckCircle, iconColor: "text-emerald-400 bg-emerald-400/10 border-emerald-400/20" },
  ];

  return (
    <div className="p-6 bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl flex flex-col justify-between h-full lg:col-span-2">
      <div>
        <div className="flex justify-between items-center mb-5">
          <h3 className="text-base font-bold text-white tracking-wide">Trạng thái tác vụ (Kanban)</h3>
          <button className="text-xs bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-400 border border-indigo-500/20 px-3 py-1 rounded-xl transition-all">
            + Tác vụ mới ↗
          </button>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {tasks.map((t, idx) => {
            const Icon = t.icon;
            return (
              <div key={idx} className="p-4 bg-white/[0.02] border border-white/5 rounded-xl hover:border-white/10 transition-all flex items-start justify-between group">
                <div className="space-y-2">
                  <h4 className="text-xs font-semibold text-white/90 group-hover:text-indigo-400 transition-colors">{t.title}</h4>
                  <div className="flex items-center gap-2 text-[10px]">
                    <span className="text-white/40">{t.user}</span>
                    <span className="w-1 h-1 bg-white/20 rounded-full"></span>
                    <span className="px-1.5 py-0.5 bg-white/5 rounded text-white/60 border border-white/5">{t.tag}</span>
                  </div>
                </div>
                <div className={`p-1.5 rounded-lg border text-sm flex items-center gap-1 font-mono ${t.iconColor}`}>
                  <Icon />
                  <span className="text-[9px] font-bold uppercase">{t.time}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="mt-5 pt-4 border-t border-white/5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div className="flex items-center gap-4 text-xs text-white/50">
          <span>🎯 Xong: <strong className="text-emerald-400">4</strong></span>
          <span>⏳ Đang làm: <strong className="text-amber-400">2</strong></span>
          <span>📋 Tổng: <strong>8</strong></span>
        </div>
        <div className="w-full sm:w-auto flex gap-2">
          <button className="flex-1 sm:flex-none text-xs bg-white/5 hover:bg-white/10 border border-white/10 px-4 py-2 rounded-xl text-white font-medium transition-all">
            Lịch họp Teams
          </button>
          <button className="flex-1 sm:flex-none text-xs bg-emerald-600 hover:bg-emerald-500 rounded-xl px-4 py-2 text-white font-bold transition-all shadow-lg shadow-emerald-600/10">
            Gửi thông báo
          </button>
        </div>
      </div>
    </div>
  );
}
