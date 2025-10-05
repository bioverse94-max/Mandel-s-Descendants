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