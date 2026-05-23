🐧 Part 1: WSL 2 & Alpine Linux Setup
wsl -l -v

Checks the status and version of all installed Linux distributions inside Windows Subsystem for Linux.

wsl --set-default-version 2

Forces all future Linux distributions installed on your system to run on the faster WSL 2 architecture.

wsl --install -d Ubuntu

Downloads and provisions a fresh instance of the Ubuntu Linux distribution (used before switching to Alpine).

wsl --set-version Ubuntu 2

Manually upgrades an existing Ubuntu distribution from version 1 to version 2.

📦 Part 2: Working with the Local Registry & Image Building
cd /mnt/d/k8s-voting-project/

Navigates your Alpine Linux terminal to your main project directory located on your Windows D: drive.

docker build -t my-dashboard:latest .

Packages your real-time dashboard application code into a local Docker image labeled with the standard "latest" tag.

docker build -t my-voting-app:latest .

Packages your main voting front-end application code into a local Docker image labeled with the standard "latest" tag.

docker build -t my-worker:latest .

Packages your background processing worker script into a local Docker image labeled with the standard "latest" tag.

docker images

Displays a full list of all Docker images stored inside your machine's active local registry.

docker pull redis:alpine

Bypasses the cluster's pull errors by pulling the official lightweight Redis image directly from Docker Hub to your local cache.

docker pull postgres:13-alpine

Bypasses the cluster's pull errors by pulling the official lightweight PostgreSQL image directly from Docker Hub to your local cache.

docker build -t my-voting-app:v1 .

Rebuilds your voting application using a strict version tag (v1) to solve the local "Latest Tag Bug".

docker build -t my-worker:v1 .

Rebuilds your background worker process using a strict version tag (v1) to solve the local "Latest Tag Bug".

docker build -t my-dashboard:v1 .

Rebuilds your dashboard application using a strict version tag (v1) to solve the local "Latest Tag Bug".

docker build -t my-voting-app:v2 .

Rebuilds your voting front-end with an aggressive math loop to force stress testing on your high-end processor.

docker build -t my-voting-app:v3 .

Rebuilds your voting front-end to utilize multi-threaded python processes so the cluster statistics accurately sample the spike.

🧭 Part 3: Establishing Cluster Access & Verification
mkdir -p ~/.kube

Creates a hidden configuration folder in your Alpine user profile to store Kubernetes connection settings.

cp /mnt/c/Users/mygam/.kube/config ~/.kube/config

Copies the security access credentials from Windows over to Alpine so kubectl can communicate with Docker Desktop's cluster.

kubectl get nodes

Requests the master API server to print the physical list of all active worker machine nodes in your playground cluster.

🏗️ Part 4: Managing Applications, Storage, and Base Resources
kubectl apply -f redis.yaml

Instructs Kubernetes to process your blueprint to deploy the shared Redis queue alongside its connection service.

kubectl get pods

Lists all running, creating, or failing container pods inside your default namespace.

kubectl get svc

Lists all available internal or external cluster networking service phone lines and their assigned cluster IP addresses.

kubectl describe pod <redis-pod-name>

Prints a detailed historical breakdown and chronological timeline event log for a specific pod to pinpoint engine failures.

kubectl apply -f postgres.yaml

Instructs Kubernetes to process your blueprint to deploy the PostgreSQL database deployment and service.

kubectl apply -f python-apps.yaml

Instructs Kubernetes to launch your frontend UI, background processor worker, and graphical dashboard all at once.

kubectl logs deploy/worker-deployment

Fetches and outputs the standard runtime standard console stream output from your worker to inspect python application stack trace trace-backs.

kubectl logs <worker-pod-name>

Directly extracts active app errors out of a specific background container instance when a generic deployment search loops too fast.

💥 Part 5: Testing Resiliency, Autoscaling, and Metrics Tracking
kubectl get pods -w

Streams a real-time, live terminal view of your cluster pods to watch crashes, OOMKills, and automated scaling events unfold.

kubectl autoscale deployment voting-app-deployment --cpu-percent=50 --min=1 --max=5

Deploys a Horizontal Pod Autoscaler (HPA) targeting your front-end, telling it to duplicate pods if load exceeds half a core.

kubectl get hpa -w

Stream-tails a dedicated tracking window to watch active cluster core metrics percentages change against your scale-up limits.

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

Installs the official production repository metrics components so the system can measure CPU and Memory resources.

kubectl patch deployment metrics-server -n kube-system --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'

Overrides security checks on the metrics application deployment to force it to function without TLS certificates on a local desktop.

kubectl get pods -n kube-system

Displays system-level engine infrastructure pods (like DNS, network routers, and metrics-servers) rather than your basic code.

kubectl top pods

Queries active utilization metrics to show exactly how many millicores of CPU power and megabytes of memory each individual pod consumes.

🌐 Part 6: Enterprise Traffic Routing (Ingress Layer)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

Installs the industrial-standard NGINX Reverse Proxy and Bouncer instance into your environment to act as your central receptionist.

kubectl apply -f ingress.yaml

Applies your enterprise URL routing schema rules so incoming path tokens (/ and /dashboard) send web browsers to the proper destination.

🧹 Part 7: Tear-Down & Cleaning
kubectl delete -f python-apps.yaml

Gracefully tears down your front-end web server deployments, services, and processing workers.

kubectl delete -f postgres.yaml

Safely stops and completely removes the PostgreSQL persistent database instance.

kubectl delete -f redis.yaml

Safely stops and completely removes the shared in-memory memory broker queue.

kubectl delete hpa voting-app-deployment

Disarms and removes your Horizontal Pod Autoscaler tracking policy.

kubectl delete -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

Cleans up and clears away the manual analytics tracking system to restore system overhead.

kubectl delete pods --all

Aggressively wipes out all currently existing pods, forcing their corresponding deployment blueprints to spawn fresh ones immediately.