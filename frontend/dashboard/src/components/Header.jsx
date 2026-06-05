import React from "react";
import { HiOutlineBell, HiSearch } from "react-icons/hi";

export default function Header() {
  // Lấy ngày tháng năm hiện tại hiển thị định dạng Tiếng Việt
  const today = new Date();
  const options = { weekday: 'long', year: 'numeric', month: 'numeric', day: 'numeric' };
  const formattedDate = today.toLocaleDateString('vi-VN', options);

  return (
    <header className="w-full h-20 flex items-center justify-between px-8 bg-white/10 backdrop-blur-md border-b border-white/10 text-white sticky top-0 z-40">
      {/* Góc trái: Tiêu đề trang và ngày tháng */}
      <div>
        <h1 className="text-xl font-bold tracking-wide">Dashboard</h1>
        <p className="text-xs text-white/60 mt-0.5">{formattedDate}</p>
      </div>

      {/* Góc phải: Ô tìm kiếm, Thông báo và Avatar Admin */}
      <div className="flex items-center gap-6">
        {/* Thanh tìm kiếm nhanh */}
        <div className="relative hidden md:block">
          <input 
            type="text" 
            placeholder="Tìm kiếm tác vụ..." 
            className="w-64 h-9 pl-10 pr-4 rounded-full bg-white/5 border border-white/10 text-sm focus:outline-none focus:border-white/30 transition-all text-white placeholder-white/40"
          />
          <HiSearch className="absolute left-3.5 top-2.5 text-white/40 text-lg" />
        </div>

        {/* Nút Chuông thông báo */}
        <button className="relative p-2 rounded-full hover:bg-white/5 transition-all group">
          <HiOutlineBell className="text-xl text-white/80 group-hover:text-white" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
        </button>

        {/* Khối hồ sơ Admin */}
        <div className="flex items-center gap-3 border-l border-white/10 pl-6">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-medium">Đức Quản Trị</p>
            <p className="text-[10px] text-emerald-400 font-mono tracking-wider uppercase">Admin</p>
          </div>
          <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-between shadow-lg font-bold text-sm text-white cursor-pointer hover:scale-105 transition-all border border-white/20 select-none pl-3.5">
            AD
          </div>
        </div>
      </div>
    </header>
  );
}
