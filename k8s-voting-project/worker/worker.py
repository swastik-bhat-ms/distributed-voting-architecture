import os, time, redis, psycopg2

redis_host = os.getenv('REDIS_HOST', 'localhost')
db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'postgres')
db_pass = os.getenv('DB_PASS', 'password')

r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(host=db_host, user=db_user, password=db_pass, dbname='postgres')
            # Initialize table
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS votes (id SERIAL PRIMARY KEY, vote VARCHAR(255));")
                conn.commit()
            return conn
        except Exception as e:
            print("Waiting for database...")
            time.sleep(2)

conn = get_db_connection()

print("Worker started, waiting for votes...")
while True:
    try:
        # Block until a vote is available in Redis
        _, vote = r.brpop('votes')
        with conn.cursor() as cur:
            cur.execute("INSERT INTO votes (vote) VALUES (%s)", (vote,))
            conn.commit()
            print(f"Processed vote: {vote}")
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)