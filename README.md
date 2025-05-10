# Spotify ETL Pipeline with Airflow & Docker

This project extracts data from the Spotify API, transforms it, and loads it into a PostgreSQL database. It's orchestrated using Apache Airflow running inside Docker containers.

---

##  Features

-  **ETL Pipeline** triggered by Airflow DAG
-  Pulls artist and track data from Spotify API
-  Cleans and enriches data (e.g., genre, followers, updated_at)
-  Loads data into PostgreSQL using UPSERT logic
-  Fully containerized with Docker Compose
-  Secrets managed via `.env` file

---

## 🗂 Project Structure

```
spotify_etl/
├── dags/                # Airflow DAG definitions
│   └── spotify_etl_dag.py
├── scripts/             # Custom Python modules
│   ├── spotify_etl.py
│   └── utils_sql.py
├── logs/                # Airflow logs (shared volume)
├── Dockerfile           # Custom Airflow image with dependencies
├── requirements.txt     # Python packages (pandas, requests, etc.)
├── docker-compose.yml   # All services (Airflow, Postgres)
└── .env                 # API secrets and connection strings
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/spotify-etl.git
cd spotify-etl
```

### 2. Add your environment variables

Create a `.env` file in the project root:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
ETL_DB_URI=postgresql://etl_user:etl_pass@postgres_etl:5432/etl_db
```

> **Note**: Your `.env` is used in the containers and loaded via `env_file:` in `docker-compose.yml`.

---

### 3. Build and start all containers

```bash
docker-compose up --build
```

Then visit the Airflow UI at: [http://localhost:8080](http://localhost:8080)  
**Username/Password:** `admin / admin`

---

### 4. Trigger the DAG

In the Airflow UI:
1. Turn on the DAG named `spotify_etl_pipeline`
2. Click “Trigger DAG” to run it manually

## 5. Final Result

![image](https://github.com/user-attachments/assets/7904e129-c85f-48f2-8fdd-a54a1e06d860)


---

## 🛠 Customization

- Edit `spotify_etl.py` to change the data source, transformation, or Spotify endpoint
- Adjust `utils_sql.py` if your schema or upsert logic changes
- Extend the DAG to schedule daily/weekly runs

---

## 📋 Requirements

- Docker + Docker Compose
- Spotify Developer API access
- Python 3.8+ (inside container)


