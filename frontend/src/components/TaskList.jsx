import React from 'react';
import TaskItem from './TaskItem';

export default function TaskList({ tasks, role, demoQuota, activeTaskId, showToast, simulateExecution, setDemoQuota , onRunTask }) {
  return (
    <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <h3 className="text-lg font-bold text-slate-800 mb-4">Nhiá»‡m vá»¥ cá»§a tÃ´i / Äá»™i nhÃ³m</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse font-sans text-sm">
          <thead>
            <tr className="border-b border-slate-100 text-slate-400 text-xs font-bold uppercase">
              <th className="pb-3">Há»‡ sinh thÃ¡i</th>
              <th className="pb-3">Worker</th>
              <th className="pb-3">NgÆ°á»i cháº¡y</th>
              <th className="pb-3">Tráº¡ng thÃ¡i</th>
              <th className="pb-3 text-right">HÃ nh Ä‘á»™ng</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {tasks.map(task => (
              <TaskItem 
                key={task.id}
                task={task}
                role={role}
                demoQuota={demoQuota}
                activeTaskId={activeTaskId}
                showToast={showToast}
                simulateExecution={simulateExecution}
                setDemoQuota={setDemoQuota}
                onRunTask={onRunTask}
              />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}


