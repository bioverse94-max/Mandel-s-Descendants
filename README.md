# 🚀 BioVerse: NASA Space Biology Knowledge Engine

BioVerse is a high-performance web application built for the **NASA Space Apps Challenge 2025**. It provides an AI-powered search engine for NASA's bioscience research, enabling scientists, mission planners, and researchers to discover insights from decades of space biology experiments.

## 🌟 Key Features

- **Advanced Search Engine**: Fast, context-aware search through NASA's biological research
- **AI-Powered Analysis**: Automated research summarization and recommendations
- **Real-time Processing**: Optimized for quick response times and high throughput
- **Scalable Architecture**: Auto-scaling microservices architecture
- **Comprehensive Monitoring**: Full observability with metrics, logs, and traces
- **Enterprise-grade Security**: SSL/TLS encryption and secure communication

## 🏗️ Architecture

### Backend Services
- FastAPI REST API with async processing
- SciBERT NLP service for scientific text analysis
- Redis for high-performance caching
- ELK Stack for logging and analysis
- Prometheus + Grafana for metrics
- Jaeger for distributed tracing

### Frontend
- React + TypeScript + Vite
- Tailwind CSS for styling
- Real-time data updates
- Responsive design

## 🛠️ Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 16+
- Python 3.8+

For Windows users:
- [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/bioverse94-max/Mandel-s-Descendants.git
cd Mandel-s-Descendants
```

2. Set up security (generates SSL certificates and secure configurations):
```bash
chmod +x setup-security.sh
./setup-security.sh
```

3. Start the services:
```bash
# Using Docker Compose (recommended)
docker-compose up --build

# OR start services individually:

# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8443 --ssl-keyfile=./certs/server.key --ssl-certfile=./certs/server.crt

# Frontend
cd frontend/project
npm install
npm run dev
```

## 🚀 Production Deployment

### Using Docker Swarm

1. Initialize the swarm and deploy:
```bash
chmod +x deploy-swarm.sh
./deploy-swarm.sh
```

2. Scale services as needed:
```bash
docker service scale bioverse_backend=3
```

### Access Points

- Backend API: `https://localhost:8443`
- Frontend: `http://localhost:3000`
- Monitoring:
  - Grafana: `http://localhost:3000`
  - Prometheus: `http://localhost:9090`
  - Kibana: `http://localhost:5601`
  - Jaeger UI: `http://localhost:16686`

## 📊 Monitoring & Observability

### Metrics
- Request rates and latencies
- Error rates and types
- Resource utilization
- Cache hit/miss rates
- ML model performance

### Logging
- Structured JSON logging
- Centralized log aggregation
- Real-time log analysis
- Custom Kibana dashboards

### Tracing
- Request tracing across services
- Performance bottleneck identification
- Error chain analysis

## 🔒 Security Features

- SSL/TLS encryption for all services
- Automatic certificate management
- Rate limiting and DDoS protection
- Secure secret management
- Regular security updates

## 🎯 Performance Optimizations

- Redis caching with intelligent TTL
- Async request processing
- Batch operations support
- Response compression
- HTTP/2 support
- Load balancing

## 📝 API Documentation

- OpenAPI documentation: `https://localhost:8443/docs`
- Swagger UI: `https://localhost:8443/redoc`

## 🛡️ Environment Variables

Create a `.env` file with:

```env
# Security
SSL_CERT=/app/certs/server.crt
SSL_KEY=/app/certs/server.key
ELASTIC_PASSWORD=<secure-password>
REDIS_PASSWORD=<secure-password>
GRAFANA_PASSWORD=<secure-password>

# Service configuration
WORKERS=4
MAX_REQUESTS=1000
PORT=8443
VITE_API_URL=https://localhost:8443
```

## 📈 Scaling Guidelines

- Horizontal scaling: Add more backend/SciBERT replicas
- Vertical scaling: Increase container resources
- Cache optimization: Adjust Redis cache size and TTL
- Load balancing: Configure based on traffic patterns

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add YourFeature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NASA Space Apps Challenge
- SciBERT team for the scientific NLP model
- Open source community for various tools and libraries

---

Live Demo: [https://bioverse.vercel.app](https://bioverse.vercel.app)
API Endpoint: [https://bioverse-backend.onrender.com](https://bioverse-backend.onrender.com)










## 🌍 Deployment

### Backend (Render)

Configured with `render.yaml`. On deploy, it runs:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

Example backend URL:

```
https://bioverse-backend.onrender.com
```

### Frontend (Vercel)

* Root: `frontend/project`
* Add environment variable in Vercel:

  ```
  VITE_API_URL=https://bioverse-backend.onrender.com
  ```

Example frontend URL:

```
https://bioverse.vercel.app
```

---# 🚀 BioVerse: NASA Space Biology Knowledge Engine  

BioVerse is a web application built for the **NASA Space Apps Challenge 2025**.  
It summarizes and makes accessible NASA’s bioscience research, enabling scientists, mission planners, and curious explorers to search, learn, and discover insights from decades of space biology experiments.  

---

## ⚠️ Windows Prerequisite  
On **Windows**, you may need Microsoft C++ Build Tools to install some Python dependencies.  
Download here 👉 [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)  

---

## 🛠 Local Setup Instructions  

### 1. Clone Repository  
```bash
git clone https://github.com/YOUR_USERNAME/Nasa-Biology-Engine-.git
cd Nasa-Biology-Engine--main/Bioverse



## 🌍 Deployment

### Backend (Render)

Configured with `render.yaml`. On deploy, it runs:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

## ▶️ Run locally (quick)

You can run the backend and frontend locally using docker-compose (recommended) or individually.

- With docker-compose (starts backend on 8000 and scibert on 8080):

```bash
docker-compose up --build
```

- Run backend only (uvicorn):

```bash
# from repository root
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- Run frontend (React):

```bash
cd frontend/project
npm install
# add .env with VITE_API_URL=http://127.0.0.1:8000
npm run dev
```

Notes:
- The backend Dockerfile exposes port 8000 and docker-compose maps 8000:8000.
- Set `SCIBERT_URL` env var for the backend if running the SciBERT service elsewhere.

## Notes about sample data and SciBERT

- This repository now includes a small sample dataset at `data/nasa_bio_data.json` so the API endpoints return example results for local development.
- The `/scibert/ner` endpoint proxies to an external SciBERT service configured by `SCIBERT_URL` (docker-compose maps the included `scibert-master` service to `http://scibert:8080`). If SciBERT or its Python dependencies are not available, the endpoint will return a safe placeholder message.

Example backend URL:

```
https://bioverse-backend.onrender.com
```

### Frontend (Vercel)

* Root: `frontend/project`
* Add environment variable in Vercel:

  ```
  VITE_API_URL=https://bioverse-backend.onrender.com
  ```

Example frontend URL:

```
https://bioverse.vercel.app
```

---
