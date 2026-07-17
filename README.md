# MLOPS-drift-detection-pipeline

An end-to-end MLOps pipeline built on the Titanic dataset. Covers data ingestion from GCP/PostgreSQL via Apache Airflow, feature engineering with a Redis feature store, model training, a Flask prediction API, real-time data drift detection, and Prometheus + Grafana monitoring.

## Architecture

```
GCS Bucket
    └── Airflow DAG (extract_titanic_data)
            └── PostgreSQL
                    └── DataIngestion (src/)
                            └── DataProcessing → Redis Feature Store
                                    └── ModelTraining → artifacts/models/
                                            └── Flask App (application.py)
                                                    ├── KSDrift Detection (alibi-detect)
                                                    └── Prometheus Metrics → Grafana
```

## Project Structure

```
├── application.py          # Flask prediction API + drift detection + Prometheus metrics
├── pipeline/
│   └── training_pipeline.py   # Orchestrates ingestion → processing → training
├── src/
│   ├── data_ingestion.py   # Pulls data from PostgreSQL, splits into train/test
│   ├── data_processing.py  # Feature engineering
│   ├── model_training.py   # Trains Random Forest classifier
│   ├── feature_store.py    # Redis-backed feature store
│   ├── logger.py
│   └── custom_exception.py
├── dags/
│   └── extract_data_from_gcp.py   # Airflow DAG: GCS → PostgreSQL
├── config/
│   ├── database_config.py
│   └── paths_config.py
├── artifacts/
│   ├── models/             # Saved model (.pkl) — generated at runtime
│   └── raw/                # Raw train/test CSVs — generated at runtime
├── notebooks/
│   └── titanic.ipynb       # Exploratory analysis
├── static/                 # Flask static assets
├── templates/              # Flask HTML templates
├── docker-compose.yml      # Prometheus + Grafana monitoring stack
├── prometheus.yml          # Prometheus scrape config
├── Dockerfile
└── requirements.txt
```

## Setup

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- PostgreSQL instance with Titanic data loaded (via the Airflow DAG)
- Redis instance running locally or remotely
- Apache Airflow (Astro CLI recommended)

### Install dependencies

```bash
pip install -r requirements.txt
python setup.py install
```

### Configure environment

Create a `.env` file (see `.gitignore` — never commit this):

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Run the training pipeline

```bash
python pipeline/training_pipeline.py
```

This runs data ingestion from PostgreSQL → feature processing → model training. The trained model is saved to `artifacts/models/random_forest_model.pkl`.

### Start the Flask app

```bash
python application.py
```

- Prediction UI: http://localhost:5000  
- Prometheus metrics: http://localhost:5000/metrics

### Start monitoring stack

```bash
docker-compose up -d
```

- Prometheus: http://localhost:9090  
- Grafana: http://localhost:3000 (default password: `admin`)

### Run the Airflow DAG

Use the Astro CLI to start Airflow and trigger the `extract_titanic_data` DAG to pull the dataset from GCS into PostgreSQL.

## Key Components

**Data drift detection** — uses `alibi-detect` KSDrift on incoming prediction requests. When drift is detected, a `drift_count` Prometheus counter increments and a warning is logged.

**Redis Feature Store** — processed features are cached in Redis for fast serving, keyed by entity ID.

**Prometheus metrics** — `prediction_count` and `drift_count` counters are exposed at `/metrics` and scraped by Prometheus.
