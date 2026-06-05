"""
Web Dashboard - Real-time Progress
"""
import json
import time
from datetime import datetime
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

def get_progress_data():
    """Lấy dữ liệu tiến trình"""
    try:
        with open('auto_worker_report.json', 'r') as f:
            worker = json.load(f)
    except:
        worker = {'processed': 0, 'succeeded': 0, 'failed': 0, 'target': 500}
    
    try:
        with open('auto_strategy.json', 'r') as f:
            strategy = json.load(f)
    except:
        strategy = {'analysis': {}, 'total_tasks': 0}
    
    try:
        import sqlite3
        conn = sqlite3.connect('sen_v3.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM accesstrade_campaigns")
        campaigns = cursor.fetchone()[0]
        conn.close()
    except:
        campaigns = 0
    
    return {
        'processed': worker.get('processed', 0),
        'succeeded': worker.get('succeeded', 0),
        'failed': worker.get('failed', 0),
        'target': worker.get('target', 500),
        'high_value': strategy.get('analysis', {}).get('high_value_count', 0),
        'high_volume': strategy.get('analysis', {}).get('high_volume_count', 0),
        'campaigns': campaigns,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SEN V3 - Worker Monitor</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body { font-family: 'Segoe UI', Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; }
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .stat-number { font-size: 36px; font-weight: bold; }
        .stat-label { color: #666; margin-top: 10px; }
        .progress-section { background: white; border-radius: 12px; padding: 20px; margin-bottom: 30px; }
        .progress-bar { width: 100%; height: 30px; background: #e0e0e0; border-radius: 15px; overflow: hidden; margin: 15px 0; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #28a745, #20c997); transition: width 0.3s; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }
        .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .info-card { background: white; border-radius: 12px; padding: 15px; }
        .timestamp { text-align: center; color: white; margin-top: 20px; }
        .success { color: #28a745; }
        .failed { color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 SEN V3 - REAL-TIME WORKER MONITOR</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number success">{{ data.processed }}</div>
                <div class="stat-label">✅ Processed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number success">{{ data.succeeded }}</div>
                <div class="stat-label">📈 Succeeded</div>
            </div>
            <div class="stat-card">
                <div class="stat-number failed">{{ data.failed }}</div>
                <div class="stat-label">❌ Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ data.target }}</div>
                <div class="stat-label">🎯 Target/Day</div>
            </div>
        </div>
        
        <div class="progress-section">
            <h3>📊 Daily Progress</h3>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {{ (data.processed / data.target * 100) | round }}%;">
                    {{ (data.processed / data.target * 100) | round }}%
                </div>
            </div>
            <p>{{ data.processed }} / {{ data.target }} tasks completed</p>
        </div>
        
        <div class="info-grid">
            <div class="info-card">
                <h3>💰 High Value</h3>
                <p style="font-size: 24px; font-weight: bold;">{{ data.high_value }}</p>
                <small>Campaigns (vay, tín chấp)</small>
            </div>
            <div class="info-card">
                <h3>📦 High Volume</h3>
                <p style="font-size: 24px; font-weight: bold;">{{ data.high_volume }}</p>
                <small>Campaigns (e-commerce)</small>
            </div>
            <div class="info-card">
                <h3>📊 Total Campaigns</h3>
                <p style="font-size: 24px; font-weight: bold;">{{ data.campaigns }}</p>
                <small>In Database</small>
            </div>
        </div>
        
        <div class="timestamp">
            <p>🕐 Last update: {{ data.timestamp }}</p>
            <p>🔄 Auto-refresh every 3 seconds</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE, data=get_progress_data())

@app.route('/api/stats')
def api_stats():
    return jsonify(get_progress_data())

if __name__ == '__main__':
    print("=" * 60)
    print("🌐 WEB DASHBOARD STARTED")
    print("📊 Open browser: http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=False)
