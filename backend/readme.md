#### Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Run server (local machine only)

```bash
uvicorn app.main:app --reload
```

#### Run server (accessible over network)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### API Docs

* Local Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Network Swagger UI: `http://YOUR_IP:8000/docs` (replace `YOUR_IP` with your machine IP)

#### Example Queries

* `/search?q=plant`
* `/recommend?q=gravity`
* `/describe?q=bone`

---
