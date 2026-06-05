import React from "react";

export default function TaskTable() {
  const campaigns = [
    { name: "Shopee 6/6", clicks: 342, conv: 28, rev: "1.8M", progress: "w-[60%]", prgText: "60%" },
    { name: "Lazada Flash", clicks: 210, conv: 19, rev: "1.1M", progress: "w-[45%]", prgText: "45%" },
    { name: "Tiki Sách", clicks: 187, conv: 15, rev: "0.8M", progress: "w-[35%]", prgText: "35%" },
    { name: "AccessTrade FIN", clicks: 87, conv: 5, rev: "0.3M", progress: "w-[15%]", prgText: "15%" },
  ];

  return (
    <div className="p-6 bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl flex flex-col justify-between h-full">
      <div>
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-base font-bold text-white tracking-wide">Chiến dịch đang chạy</h3>
          <span className="text-[10px] bg-indigo-500/20 text-indigo-300 font-medium px-2 py-0.5 rounded-full border border-indigo-500/30 uppercase tracking-wider">
            4 active
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="text-[11px] font-semibold text-white/40 uppercase tracking-wider border-b border-white/5">
                <th className="pb-3 font-medium">Chiến dịch</th>
                <th className="pb-3 font-medium text-center">Click</th>
                <th className="pb-3 font-medium text-center">Conv</th>
                <th className="pb-3 font-medium text-right">Doanh thu</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-xs text-white/80">
              {campaigns.map((c, idx) => (
                <tr key={idx} className="hover:bg-white/[0.02] transition-colors">
                  <td className="py-2.5 font-medium text-white">{c.name}</td>
                  <td className="py-2.5 text-center text-white/60">{c.clicks}</td>
                  <td className="py-2.5 text-center text-white/60">{c.conv}</td>
                  <td className="py-2.5 text-right font-bold text-indigo-400">{c.rev}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="mt-4 pt-4 border-t border-white/5 space-y-3">
        <p className="text-xs text-white/50 font-medium">Tiến độ mục tiêu tháng (Shopee 6/6)</p>
        <div className="w-full h-3 bg-white/5 rounded-full p-0.5 border border-white/5">
          <div className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full w-[60%] flex items-center justify-end pr-1.5">
            <span className="text-[8px] font-bold text-white">60%</span>
          </div>
        </div>
        <button className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 border border-indigo-500/30 rounded-xl text-xs font-bold text-white transition-all shadow-lg shadow-indigo-600/10 active:scale-[0.98]">
          + Tạo chiến dịch mới ↗
        </button>
      </div>
    </div>
  );
}
