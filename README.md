## 🚀Our search engine is live at -
https://bioverse94-max.github.io/Mandel-s-Descendants/










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
