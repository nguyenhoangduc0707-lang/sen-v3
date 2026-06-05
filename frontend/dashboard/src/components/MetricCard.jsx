import React from "react";

export default function MetricCard({ title, value, subtext, trend, icon: Icon, trendType = "up" }) {
  return (
    <div className="p-6 bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl transition-all duration-300 hover:bg-white/10 hover:scale-[1.02] hover:shadow-xl hover:shadow-indigo-500/5 group flex justify-between items-start">
      <div className="space-y-2">
        <p className="text-xs font-medium text-white/50 tracking-wider uppercase">{title}</p>
        <h3 className="text-3xl font-bold text-white tracking-tight">{value}</h3>
        <p className="text-xs flex items-center gap-1.5 mt-1">
          <span className={`font-medium ${trendType === "up" ? "text-emerald-400" : "text-amber-400"}`}>
            {trend}
          </span>
          <span className="text-white/40">{subtext}</span>
        </p>
      </div>
      <div className="p-3 bg-white/5 rounded-xl border border-white/10 text-xl text-indigo-400 group-hover:text-indigo-300 group-hover:bg-indigo-500/10 transition-all duration-300">
        <Icon />
      </div>
    </div>
  );
}
