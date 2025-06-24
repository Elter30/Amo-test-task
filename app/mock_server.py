import random
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    # Имитация задержки сети (0.1-2 секунды)
    delay = random.uniform(0.1, 2.0)
    time.sleep(delay)
    
    # Имитация возможных ошибок (5% случаев)
    if random.random() < 0.05:
        return jsonify({"error": "Service unavailable"}), 503
    
    # Генерация реалистичных метрик
    return jsonify({
        "cpu": round(random.uniform(0.1, 99.9), 1),
        "mem": f"{random.randint(1, 99)}%",
        "disk": f"{random.randint(1, 99)}%",
        "uptime": f"{random.randint(0, 30)}d {random.randint(0, 23)}h {random.randint(0, 59)}m"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)