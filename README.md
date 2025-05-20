# 🚀 Apache Airflow Project (via Docker + uv)

This project was initiated as a foundation for workflow orchestration using **Apache Airflow**, fully containerized with Docker Compose.

> Python dependency management is handled using **[uv](https://github.com/astral-sh/uv)** — a blazing-fast package manager that replaces `pip`, `pip-tools`, and `virtualenv`.

---

## 📦 Project Structure

```
airflow-project/
├── dags/ # Your custom DAGs
├── plugins/ # Optional plugins (custom operators, hooks, etc.)
├── docker-compose.yaml # Docker Compose configuration
├── .env.example # Example environment variables
├── requirements.txt # Additional Python dependencies (optional)
└── README.md # This file
```

---

## 🛠️ Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [uv](https://github.com/astral-sh/uv) (optional for local Python development)

---

## ▶️ How to Start

1. **Copy the example environment file and adjust if needed:**

```bash
cp .env.example .env
```

2. **Start the containers:**

```bash
docker-compose up -d --build
# or docker-compose up -d 
```

3. **Access the Airflow Web UI:**

```
http://localhost:8080
```

---
## 🧪 Testing a DAG

Place your .py DAG files inside the ./dags/ folder and restart the containers if needed. DAGs can also be activated through the Airflow UI.

---
## 🧼 Stopping the Environment
```bash
docker-compose down
```

To remove volumes and orphaned containers:

```bash
docker-compose down --volumes --remove-orphans
```

---

## 📝 Notes

* This project does not include sensitive files. The actual .env file is excluded via .gitignore.
* You can use uv locally to install additional packages required by your DAGs:

```bash
uv pip install pandas requests
```