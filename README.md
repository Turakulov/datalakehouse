# 🏗️ Data Lakehouse with Modern Technologies  

![Architecture](https://github.com/user-attachments/assets/ef98d59f-56f9-41ad-a450-5818f9237a55)


## 📌 Overview  
This project demonstrates how to build a **Data Lakehouse** using modern open-source technologies.  
It integrates **Kafka**, **Spark Streaming**, **Apache Iceberg**, **Apache Nessie**, **Trino**, and **DBT** to create an efficient data pipeline.  

🔹 **Streaming Layer:** Spark Streaming / Flink processes real-time Kafka events.  
🔹 **Batch Layer:** Apache Spark and AirByte handle batch ingestion into an **S3 Minio** data lake.  
🔹 **Metadata Layer:** Apache Nessie is used as the Iceberg catalog, backed by PostgreSQL.  
🔹 **Transformation Layer:** Trino and DBT transform and store data in **Vertica** for analytics.  
🔹 **Orchestration:** Apache Airflow schedules and manages all ETL/ELT workflows.  
🔹 **Synthetic Data:** Generated with `sdv` Python library from **SalesDB_v1** dataset.  
🔹 **Visualization:** Dashboards built in **Tableau, Superset, or Power BI**.  

## 🚀 Tech Stack  
| Category          | Technology |
|------------------|------------|
| **Streaming**    | Kafka, Spark Streaming, Flink |
| **Storage**      | S3 Minio (Apache Iceberg) |
| **Metadata**     | Apache Nessie, PostgreSQL |
| **ETL/ELT**      | Airflow, DBT, Apache Spark |
| **Query Engine** | Trino, Vertica |
| **Orchestration**| Apache Airflow |
| **Dashboarding** | Tableau, Superset, Power BI |

---

## 🎯 Architecture  

### 1️⃣ **Data Ingestion**  
- Streaming events flow from **Kafka** into **Spark Streaming / Flink**.  
- Batch data is ingested via **AirByte** into **S3 Minio (Iceberg format)**.  

### 2️⃣ **Storage & Metadata Management**  
- Raw (`raw`) and Operational (`ods`) data are stored in **S3 Minio (Apache Iceberg)**.  
- Apache Nessie acts as the metadata catalog, tracking schema versions and changes.  

### 3️⃣ **Transformation & Querying**  
- **DBT + Trino** handle transformations.  
- Processed marts (`marts`) are stored in **Vertica** for BI consumption.  

### 4️⃣ **Orchestration & Visualization**  
- **Apache Airflow** schedules all ETL/ELT jobs.  
- Dashboards are created using **Tableau, Superset, or Power BI**.  

---

## 📸 Screenshots  
🔹 **Kafka UI** (Monitor real-time events)  
![kafka](https://github.com/user-attachments/assets/2a6224d8-c22a-4a64-8196-7c9ce80ebc0d)

🔹 **S3 Minio Browser** (View stored Iceberg tables)  
🔹 **Apache Nessie UI** (Track schema changes)  
🔹 **Airflow DAGs** (Monitor ETL workflows)  
🔹 **DBT Lineage Graph** (View transformation dependencies)  
🔹 **BI Dashboards** (Analytics & insights)  

---

## 🏗️ **Setup & Deployment**  
This project is fully containerized using **Docker Compose**.  

### 🔧 **Prerequisites**  
- Docker & Docker Compose  
- Python (for data generation)  

### 📥 **Clone Repository**  
```bash
git clone https://github.com/Turakulov/datalakehouse.git
cd datalakehouse
```

### ▶️ **Start the Environment**
```bash
docker-compose build

docker-compose up -d
```

### 🔎 **Verify Services**  
- **Minio Console:** [http://localhost:9001](http://localhost:9001)  
- **Trino UI:** [http://localhost:8083](http://localhost:8083)  
- **Kafka UI:** [http://localhost:9999](http://localhost:9999)  
- **Airflow UI:** [http://localhost:8090](http://localhost:8090)  
- **Vertica (SQL Access):** `jdbc:vertica://localhost:5433/db`  

---

## 🛠️ **Project Structure**  
```bash
📂 datalakehouse
├── 📂 airflow/        # Apache Airflow DAGs
├── 📂 spark/          # Spark Streaming jobs
├── 📂 kafka/          # Kafka configurations
├── 📂 trino/          # Trino catalogs
├── 📂 minio/          # Minio storage setup
├── 📂 nessie/         # Apache Nessie metadata
├── 📂 postgres/       # Postgres storage setup for Apache Iceberg metadata
├── 📂 vertica/        # Vertica storage setup for datamarts and OLAP queries
├── 📜 docker-compose.yaml  # Docker environment
└── 📜 README.md       # Project documentation
```

## 📌 **Contributing**
🔹 Fork the repo & create a feature branch.  
🔹 Submit a pull request with detailed changes.  


