import os, psycopg2
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'postgres')
db_pass = os.getenv('DB_PASS', 'password')

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Results Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style> body { font-family: Arial; text-align: center; } .chart-container { width: 50%; margin: auto; } </style>
</head>
<body>
    <h1>Real-Time Voting Results</h1>
    <div class="chart-container">
        <canvas id="resultsChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('resultsChart').getContext('2d');
        let resultsChart = new Chart(ctx, {
            type: 'bar',
            data: { labels: ['Cats', 'Dogs'], datasets: [{ label: '# of Votes', data: [0, 0], backgroundColor: ['#3498db', '#e74c3c'] }] },
            options: { scales: { y: { beginAtZero: true } } }
        });

        // Poll the API every 2 seconds
        setInterval(async () => {
            const response = await fetch('/api/data');
            const data = await response.json();
            resultsChart.data.datasets[0].data = [data.Cats || 0, data.Dogs || 0];
            resultsChart.update();
        }, 2000);
    </script>
</body>
</html>
"""

def get_results():
    try:
        conn = psycopg2.connect(host=db_host, user=db_user, password=db_pass, dbname='postgres')
        with conn.cursor() as cur:
            cur.execute("SELECT vote, COUNT(id) FROM votes GROUP BY vote;")
            return dict(cur.fetchall())
    except:
        return {}

@app.route('/')
def home():
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/data')
def api_data():
    return jsonify(get_results())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)