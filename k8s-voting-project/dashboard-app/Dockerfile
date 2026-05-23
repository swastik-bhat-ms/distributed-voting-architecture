FROM python:3.9-slim

WORKDIR /app

# Install dependencies required for psycopg2 (Postgres)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The CMD will be overridden in Kubernetes manifests, but for default:
CMD ["python", "app.py"]