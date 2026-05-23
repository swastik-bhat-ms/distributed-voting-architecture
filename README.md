# Distributed-voting-architecture
A 3-tier distributed microservices application built to learn Kubernetes deployments, scaling, networking (Ingress), and self-healing through built-in chaos engineering triggers.

## 🏗️ Architecture Overview
This project simulates a classic enterprise architecture:
* **Voting App (Python/Flask):** A frontend UI to cast votes between "Cats" and "Dogs", featuring built-in "Chaos Buttons" to trigger CPU spikes, memory leaks, and pod crashes.
* **Redis (Shared Resource):** Acts as an in-memory message broker to buffer high loads of incoming votes. 
* **Worker (Python):** A background process that pulls votes from Redis and permanently stores them in PostgreSQL.
* **PostgreSQL (Database):** The persistent storage for all votes. 
* **Dashboard App (Python/Flask):** A real-time UI using Chart.js that continuously polls the database to visualize vote differences. 
* **NGINX Ingress Controller:** Acts as the "Smart Receptionist," routing traffic to the correct internal ClusterIP services based on URL paths. 

## 📋 Prerequisites
* **WSL 2** (Alpine Linux or Ubuntu recommended). 
* **Docker Desktop** with Kubernetes enabled. 
* **kubectl** and **Helm** (optional for templating) installed on your local environment. 

---

## 🚀 Step-by-Step Setup Guide

### 1. Pre-Pull Standard Images
To prevent Kubernetes `ImagePullBackOff` errors on local networks, pull the base database images directly to your local Docker cache: 
```bash
docker pull redis:alpine
docker pull postgres:13-alpine
```

### 2. Build the Application Images
```bash
cd k8s-voting-project/
docker build -t my-voting-app:v3 ./voting-app
docker build -t my-worker:v1 ./worker
docker build -t my-dashboard:v1 ./dashboard-app
```

### 3. Deploy the Foundation (Databases)
```bash
cd k8s-manifests
kubectl apply -f redis.yaml
kubectl apply -f postgres.yaml
```

Wait until kubectl get pods shows both running before proceeding.

### 4. Deploy the Python Microservices

```bash
kubectl apply -f python-apps.yaml
```

### 5. Setup Enterprise Routing (NGINX Ingress)
* Install the NGINX Ingress Controller to act as your reverse proxy, then apply your custom routing rules
```bash
# Install NGINX Ingress Controller
kubectl apply -f [https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml]

# Apply local routing rules
kubectl apply -f ingress.yaml
```

## 💥 Chaos Engineering & Autoscaling (HPA)

### 1. Install & Patch the Metrics Server
Install the Metrics Server and patch it to bypass TLS certificate checks for local development
```bash
kubectl apply -f [https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml]

kubectl patch deployment metrics-server -n kube-system --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'
```
### 2. Enable Autoscaling
Configure the HPA to duplicate the Voting App pods (up to 5) if CPU utilization exceeds 50%
```bash
kubectl autoscale deployment voting-app-deployment --cpu-percent=50 --min=1 --max=5
```
### 3. Execute the Chaos Tests
* Self-Healing: Click "Crash Pod" in the UI. Run kubectl get pods -w to watch Kubernetes instantly spin up a replacement. 

* OOMKilled: Click "Trigger Memory Leak" rapidly. Once the pod exceeds its 50Mi limit, Kubernetes will assassinate it to protect the node. 

* Autoscaling: Click "Trigger CPU Spike". Run kubectl get hpa -w. The multi-threaded script will max out the core, forcing the HPA to scale the replicas up to handle the load!

##  Tear-Down and Cleanup
```bash
# 1. Remove the Python Apps and Services
kubectl delete -f python-apps.yaml

# 2. Remove the Database and Queue
kubectl delete -f postgres.yaml
kubectl delete -f redis.yaml

# 3. Remove the Autoscaler and Metrics Server
kubectl delete hpa voting-app-deployment
kubectl delete -f [https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml]
```
