import { NavLink } from "react-router-dom";
import {
  HiOutlineChartBar,
  HiOutlineCurrencyDollar,
  HiOutlineUserGroup,
  HiOutlineCollection,
  HiOutlinePuzzle,
  HiOutlineDesktopComputer,
  HiOutlineCog,
} from "react-icons/hi";

const menuGroups = [
  {
    title: "Tổng quan",
    items: [
      { name: "Dashboard", icon: HiOutlineChartBar, to: "/" },
      { name: "Doanh thu", icon: HiOutlineCurrencyDollar, to: "/revenue" },
      { name: "Nhân sự", icon: HiOutlineUserGroup, to: "/staff" },
    ],
  },
  {
    title: "Chiến dịch",
    items: [
      { name: "Chiến dịch", icon: HiOutlineCollection, to: "/campaigns" },
      { name: "Kanban", icon: HiOutlineDesktopComputer, to: "/kanban" },
      { name: "Báo cáo", icon: HiOutlineChartBar, to: "/reports" },
    ],
  },
  {
    title: "Đào tạo",
    items: [
      { name: "Khóa học", icon: HiOutlinePuzzle, to: "/lms" },
      { name: "Kết quả thi", icon: HiOutlinePuzzle, to: "/quiz" },
    ],
  },
  {
    title: "Hệ thống",
    items: [
      { name: "MS Teams", icon: HiOutlineDesktopComputer, to: "/teams" },
      { name: "Cài đặt", icon: HiOutlineCog, to: "/settings" },
    ],
  },
];

export default function Sidebar() {
  return (
    <aside className="glass sticky top-0 h-screen w-1/5 p-4 overflow-y-auto">
      {/* Logo */}
      <div className="flex items-center mb-6">
        <img src="/logo.svg" alt="DTECH" className="h-8 w-8 mr-2" />
        <span className="text-xl font-bold text-white">DTECH</span>
      </div>

      {/* Menu groups */}
      {menuGroups.map((group) => (
        <div key={group.title} className="mb-4">
          <h3 className="text-sm font-medium text-gray-300 uppercase mb-2">
            {group.title}
          </h3>
          <ul>
            {group.items.map((item) => (
              <li key={item.name}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center gap-2 p-2 rounded-md transition-all duration-200 ${
                      isActive
                        ? "bg-white/10 text-white"
                        : "text-gray-400 hover:bg-white/5 hover:text-white"
                    }`
                  }
                >
                  <item.icon className="h-5 w-5" />
                  <span>{item.name}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </aside>
  );
}
