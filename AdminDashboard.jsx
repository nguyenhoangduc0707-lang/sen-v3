// Trong component cha
import { useAuth } from '../context/AuthContext'; // hoặc lấy token từ localStorage

const handleRunTask = async (taskId) => {
  try {
    const token = localStorage.getItem('access_token');
    const response = await fetch(`http://localhost:8000/api/v1/tasks/${taskId}/run`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    if (response.ok) {
      showToast('Task started successfully', 'success');
      // Tải lại danh sách task (gọi API GET /tasks)
      fetchTasks(); // bạn cần có hàm này
    } else {
      const error = await response.json();
      showToast(error.detail || 'Failed to start task', 'error');
    }
  } catch (error) {
    console.error('Error starting task:', error);
    showToast('Network error', 'error');
  }
};

// Trong phần render TaskItem:
<TaskItem
  key={task.id}
  task={task}
  role={role}
  demoQuota={demoQuota}
  activeTaskId={activeTaskId}
  showToast={showToast}
  onRunTask={handleRunTask}      // 👈 thay vì simulateExecution
  setDemoQuota={setDemoQuota}
/>