import os, time, redis
from flask import Flask, request, render_template_string, jsonify
import multiprocessing

app = Flask(__name__)
# Connect to Redis (Shared Resource)
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

# A global variable to intentionally cause memory leaks
memory_hog = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vote: Cats vs Dogs</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 50px; }
        .btn { padding: 20px 40px; font-size: 24px; cursor: pointer; margin: 10px; border: none; border-radius: 8px; color: white;}
        .cats { background-color: #3498db; }
        .dogs { background-color: #e74c3c; }
        .chaos { background-color: #2c3e50; font-size: 16px; padding: 10px 20px; }
        .chaos-panel { margin-top: 50px; padding: 20px; border-top: 2px dashed #ccc; }
    </style>
</head>
<body>
    <h1>What do you prefer?</h1>
    <form method="POST" action="/vote">
        <button class="btn cats" name="vote" value="Cats">Cats</button>
        <button class="btn dogs" name="vote" value="Dogs">Dogs</button>
    </form>

    <div class="chaos-panel">
        <h3>Kubernetes Chaos Testing Controls</h3>
        <p>Use these to trigger autoscaling (HPA) and self-healing in K8s.</p>
        <button class="btn chaos" onclick="fetch('/chaos/cpu')">Trigger CPU Spike</button>
        <button class="btn chaos" onclick="fetch('/chaos/mem')">Trigger Memory Leak</button>
        <button class="btn chaos" style="background: red;" onclick="fetch('/chaos/crash')">Crash Pod</button>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/vote', methods=['POST'])
def vote():
    vote = request.form.get('vote')
    if vote:
        r.lpush('votes', vote) # Push to Redis queue
    return home()

# --- KUBERNETES TESTING ENDPOINTS ---
def heavy_math():
    """A function that runs forever to max out a CPU core."""
    while True:
        _ = 123456789 * 987654321

@app.route('/chaos/cpu')
def cpu_spike():
    """Spawns multiple processes to overwhelm high-end CPUs."""
    # We spawn 4 parallel processes to ensure we hit the 500m limit
    processes = []
    for _ in range(4):
        p = multiprocessing.Process(target=heavy_math)
        p.start()
        processes.append(p)
    
    # Let them run for 40 seconds to ensure the Metrics Server sees it
    time.sleep(40)
    
    # Kill the processes so the pod doesn't stay pegged forever
    for p in processes:
        p.terminate()
        
    return jsonify({"status": "Multicore CPU Spike completed"})

@app.route('/chaos/mem')
def mem_spike():
    """Leaks ~10MB of memory per click to test memory limits/OOMKills."""
    memory_hog.append(' ' * 10**7)
    return jsonify({"status": f"Memory leaked! Array size: {len(memory_hog)}"})

@app.route('/chaos/crash')
def crash():
    """Kills the app to test K8s ReplicaSet self-healing."""
    os._exit(1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)