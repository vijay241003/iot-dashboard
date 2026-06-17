from flask import Flask, jsonify, render_template_string
from collections import deque
from datetime import datetime
import random, threading, time

app = Flask(__name__)
data_store = deque(maxlen=20)

def auto_generate():
    while True:
        data_store.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "temperature": round(random.uniform(20, 40), 1),
            "humidity": round(random.uniform(30, 90), 1),
            "device": "sensor-01"
        })
        time.sleep(2)

thread = threading.Thread(target=auto_generate, daemon=True)
thread.start()

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>IoT Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body { font-family: Arial; max-width: 900px; margin: 30px auto; padding: 0 20px; }
    .cards { display: flex; gap: 20px; margin: 20px 0; }
    .card { flex: 1; background: #f5f5f5; padding: 20px; border-radius: 10px; text-align: center; }
    .card h2 { font-size: 36px; margin: 10px 0; color: #333; }
  </style>
</head>
<body>
  <h1>Live IoT Sensor Dashboard</h1>
  <div class="cards">
    <div class="card"><p>Temperature</p><h2 id="temp">--</h2><p>°C</p></div>
    <div class="card"><p>Humidity</p><h2 id="hum">--</h2><p>%</p></div>
    <div class="card"><p>Device</p><h2 style="font-size:20px" id="dev">--</h2></div>
  </div>
  <canvas id="chart" height="100"></canvas>
  <script>
    const ctx = document.getElementById('chart').getContext('2d');
    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          { label: 'Temperature (°C)', data: [], borderColor: '#e74c3c', tension: 0.4 },
          { label: 'Humidity (%)', data: [], borderColor: '#3498db', tension: 0.4 }
        ]
      }
    });
    async function update() {
      const res = await fetch('/api/data');
      const d = await res.json();
      if (d.length === 0) return;
      const latest = d[d.length - 1];
      document.getElementById('temp').textContent = latest.temperature;
      document.getElementById('hum').textContent = latest.humidity;
      document.getElementById('dev').textContent = latest.device;
      chart.data.labels = d.map(x => x.timestamp);
      chart.data.datasets[0].data = d.map(x => x.temperature);
      chart.data.datasets[1].data = d.map(x => x.humidity);
      chart.update();
    }
    setInterval(update, 2000);
    update();
  </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML)

@app.route('/api/data')
def get_data():
    return jsonify(list(data_store))

if __name__ == '__main__':
    app.run(debug=True)
