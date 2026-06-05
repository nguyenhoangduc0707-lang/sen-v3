import React, { useCallback, useEffect, useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import TaskList from './components/TaskList';
import { getTasks, login as loginApi } from './services/api';
import { useTaskRunner } from './hooks/useTaskRunner';

const defaultTasks = [
  {
    id: 0,
    category: 'system',
    name: 'No tasks loaded',
    worker_name: 'No tasks loaded',
    status: 'PENDING',
    assignedTo: 'Unassigned',
  },
];

export default function App() {
  const [role, setRole] = useState(localStorage.getItem('role') || 'guest');
  const [username, setUsername] = useState(localStorage.getItem('username') || '');
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [tasks, setTasks] = useState([]);
  const [toast, setToast] = useState(null);
  const [activeTaskId, setActiveTaskId] = useState(null);
  const [demoQuota, setDemoQuota] = useState(5);
  const [credentials, setCredentials] = useState({ username: '', password: '' });

  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type });
    window.setTimeout(() => setToast(null), 3000);
  }, []);

  const fetchTasks = useCallback(async () => {
    try {
      const data = await getTasks();
      setTasks(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
      showToast('Khong tai duoc danh sach task', 'error');
    }
  }, [showToast]);

  const { runTask } = useTaskRunner(showToast, fetchTasks);

  useEffect(() => {
    if (role !== 'guest') fetchTasks();
  }, [fetchTasks, role]);

  const handleRunTask = async (taskId) => {
    if (!taskId) return;
    setActiveTaskId(taskId);
    await runTask(taskId);
    setActiveTaskId(null);
  };

  const handleLogin = async (event) => {
    event.preventDefault();
    try {
      const result = await loginApi(credentials.username, credentials.password);
      localStorage.setItem('access_token', result.access_token);
      localStorage.setItem('username', credentials.username);

      const nextRole = credentials.username.toLowerCase().includes('admin')
        ? 'admin'
        : credentials.username.toLowerCase().includes('manager')
          ? 'manager'
          : 'member';

      localStorage.setItem('role', nextRole);
      setUsername(credentials.username);
      setRole(nextRole);
      showToast('Dang nhap thanh cong');
    } catch (error) {
      console.error('Login failed:', error);
      showToast('Dang nhap that bai', 'error');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    setUsername('');
    setRole('guest');
    setTasks([]);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {toast && (
        <div className={`fixed right-4 top-4 z-50 rounded-lg px-4 py-3 text-sm font-semibold text-white shadow-lg ${
          toast.type === 'error' ? 'bg-rose-600' : 'bg-emerald-600'
        }`}>
          {toast.message}
        </div>
      )}

      <Header role={role} username={username} onLogout={handleLogout} />

      {role === 'guest' ? (
        <main className="mx-auto flex min-h-[70vh] max-w-md items-center px-6">
          <form onSubmit={handleLogin} className="w-full rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h1 className="mb-1 text-xl font-bold">SEN V3 Control Panel</h1>
            <p className="mb-6 text-sm text-slate-500">Dang nhap de xem va chay task trong queue.</p>
            <label className="mb-1 block text-xs font-bold uppercase text-slate-500">Username</label>
            <input
              className="mb-4 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
              value={credentials.username}
              onChange={(event) => setCredentials((prev) => ({ ...prev, username: event.target.value }))}
              required
            />
            <label className="mb-1 block text-xs font-bold uppercase text-slate-500">Password</label>
            <input
              type="password"
              className="mb-5 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
              value={credentials.password}
              onChange={(event) => setCredentials((prev) => ({ ...prev, password: event.target.value }))}
              required
            />
            <button className="w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-bold text-white hover:bg-blue-700">
              Dang nhap
            </button>
          </form>
        </main>
      ) : (
        <div className="flex min-h-[calc(100vh-64px)] flex-col md:flex-row">
          <Sidebar role={role} currentPage={currentPage} setCurrentPage={setCurrentPage} />
          <main className="flex-1 p-6">
            {currentPage === 'dashboard' ? (
              <TaskList
                tasks={tasks.length ? tasks : defaultTasks}
                role={role}
                demoQuota={demoQuota}
                activeTaskId={activeTaskId}
                showToast={showToast}
                setDemoQuota={setDemoQuota}
                onRunTask={handleRunTask}
              />
            ) : (
              <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold">Dang o trang: {currentPage}</h2>
                <p className="mt-2 text-sm text-slate-500">Man hinh nay se duoc noi API sau khi nen task queue on dinh.</p>
              </section>
            )}
          </main>
        </div>
      )}
    </div>
  );
}
