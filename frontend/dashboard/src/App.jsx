import React from "react";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import MetricCard from "./components/MetricCard";
import RevenueChart from "./components/RevenueChart";
import TaskTable from "./components/TaskTable";
import KanbanBoard from "./components/KanbanBoard";
import { HiOutlineCurrencyDollar, HiOutlineClipboardList, HiOutlineUsers, HiOutlineCollection } from "react-icons/hi";

export default function Dashboard() {
  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 font-sans text-white overflow-hidden antialiased">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Row 1: KPI cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              title="Doanh thu hôm nay"
              value="4.2M"
              trend="+12%"
              subtext="vs hôm qua"
              icon={HiOutlineCurrencyDollar}
              trendType="up"
            />
            <MetricCard
              title="Hoa hồng admin (5%)"
              value="210K"
              trend="+12%"
              subtext="tăng trưởng"
              icon={HiOutlineCollection}
              trendType="up"
            />
            <MetricCard
              title="Task hoàn thành"
              value="23/30"
              trend="77%"
              subtext="còn 7 task"
              icon={HiOutlineClipboardList}
              trendType="up"
            />
            <MetricCard
              title="Nhân sự active"
              value="6/8"
              trend="75%"
              subtext="2 vắng mặt"
              icon={HiOutlineUsers}
              trendType="down"
            />
          </div>

          {/* Row 2: Revenue chart & Campaign table */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1">
              <RevenueChart />
            </div>
            <div className="lg:col-span-2">
              <TaskTable />
            </div>
          </div>

          {/* Row 3: Kanban board */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <KanbanBoard />
          </div>
        </main>
      </div>
    </div>
  );
}

