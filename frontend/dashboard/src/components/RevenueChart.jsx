import React from "react";
import { HiOutlineTrendingUp } from "react-icons/hi";

export default function RevenueChart() {
  const users = [
    { name: "@user_minh", amount: "1.8M", color: "from-blue-500 to-cyan-400", width: "w-[85%]" },
    { name: "@user_linh", amount: "1.2M", color: "from-purple-500 to-pink-500", width: "w-[60%]" },
    { name: "@user_tuan", amount: "0.9M", color: "from-amber-500 to-orange-500", width: "w-[45%]" },
    { name: "@user_an", amount: "0.3M", color: "from-emerald-500 to-teal-500", width: "w-[20%]" },
  ];

  return (
    <div className="p-6 bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl flex flex-col justify-between h-full">
      <div>
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-base font-bold text-white tracking-wide">Doanh thu theo nhân sự</h3>
          <button className="text-xs bg-white/5 hover:bg-white/10 border border-white/10 px-3 py-1.5 rounded-lg text-white/80 hover:text-white transition-all">
            Xuất báo cáo ↗
          </button>
        </div>
        
        <div className="space-y-4">
          {users.map((user, idx) => (
            <div key={idx} className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-white/70 font-medium">{user.name}</span>
                <span className="text-white font-bold">{user.amount}</span>
              </div>
              <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
                <div className={`h-full rounded-full bg-gradient-to-r ${user.color} ${user.width}`} />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-white/5 flex justify-between items-center text-sm">
        <div>
          <p className="text-white/40 text-xs">Tổng doanh thu team</p>
          <p className="text-lg font-bold text-white">4.2M</p>
        </div>
        <div className="text-right">
          <p className="text-emerald-400 text-xs font-medium flex items-center gap-1 justify-end">
            <HiOutlineTrendingUp /> +5% Hoa hồng Admin
          </p>
          <p className="text-lg font-bold text-emerald-400">+210K</p>
        </div>
      </div>
    </div>
  );
}
