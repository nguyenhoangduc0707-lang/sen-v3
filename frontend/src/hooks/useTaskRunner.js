import { useCallback } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const useTaskRunner = (showToast, fetchTasks) => {
  const runTask = useCallback(async (taskId) => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        showToast('Vui long dang nhap lai', 'error');
        return;
      }

      const response = await fetch(`${API_BASE}/tasks/${taskId}/run`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        showToast('Task started successfully', 'success');
        if (fetchTasks) fetchTasks();
      } else {
        const error = await response.json().catch(() => ({}));
        showToast(error.detail || 'Failed to start task', 'error');
      }
    } catch (error) {
      console.error('Error starting task:', error);
      showToast('Network error', 'error');
    }
  }, [showToast, fetchTasks]);

  return { runTask };
};
