import random, time, requests
from datetime import datetime

API_URL = "https://iot-dashboard-o973.onrender.com"

print("Simulator started — sending sensor data...")

while True:
    data = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "temperature": round(random.uniform(20, 40), 1),
        "humidity": round(random.uniform(30, 90), 1),
        "device": "sensor-01"
    }
    try:
        requests.post(API_URL, json=data)
        print(f"Sent: {data}")
    except:
        print("Waiting for server...")
    time.sleep(2)