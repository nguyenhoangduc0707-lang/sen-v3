import React from 'react';

export default function TaskItem({ task, role, demoQuota, activeTaskId, showToast, onRunTask, setDemoQuota }) {
  const handleRun = () => {
    if (role === 'demo' && demoQuota <= 0) {
      showToast('Báº¡n Ä‘Ã£ háº¿t lÆ°á»£t dÃ¹ng thá»­! Vui lÃ²ng xem quáº£ng cÃ¡o Ä‘á»ƒ tiáº¿p tá»¥c.', 'error');
      return;
    }
    if (role === 'demo') setDemoQuota(prev => prev - 1);
    onRunTask(task.id);
  };

  return (
    <tr key={task.id} className="hover:bg-slate-50 transition">
      <td className="py-3 font-semibold text-slate-700 capitalize">{task.category}</td>
      <td className="py-3 text-slate-500">{task.name}</td>
      <td className="py-3 text-slate-600 font-medium">{task.assignedTo || 'Unassigned'}</td>
      <td className="py-3">
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold ${
          task.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-800' :
          task.status === 'RUNNING' ? 'bg-sky-100 text-sky-800' :
          task.status === 'FAILED' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
        }`}>
          {task.status}
        </span>
      </td>
      <td className="py-3 text-right">
        {task.status !== 'COMPLETED' && task.status !== 'FAILED' ? (
          <button
            onClick={handleRun}
            disabled={activeTaskId !== null}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white font-bold px-3 py-1.5 rounded-lg text-xs shadow-sm transition"
          >
            Cháº¡y ngay ðŸš€
          </button>
        ) : (
          <span className="text-xs text-slate-400 font-semibold">Káº¿t thÃºc</span>
        )}
      </td>
    </tr>
  );
}


