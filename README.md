<div align="center">
  <img src="https://raw.githubusercontent.com/docker-library/docs/master/postgres/logo.png" width="100" alt="PostgreSQL Logo">
  <img src="https://airflow.apache.org/images/feature-image.png" width="150" alt="Airflow Logo">
  <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" width="150" alt="Streamlit Logo">
</div>

<div align="center">

  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](#)
  [![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=flat-square&logo=Apache%20Airflow&logoColor=white)](#)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)](#)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](#)
  [![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)](#)

</div>

## About The Project

The Weather Risk Data Pipeline is an end-to-end containerized ETL and Business Intelligence application designed for logistics monitoring[cite: 4]. Developed as a comprehensive data engineering brief at YouCode, the system automates the extraction of raw meteorological data, transforms it into actionable risk metrics, and visualizes the output through a real-time geographic dashboard[cite: 4]. 

By offloading the orchestration to Airflow and the presentation to Streamlit, the architecture completely decouples background processing from front-end analytics, providing a robust, scalable environment for operational planning.

*   **Automated ETL Orchestration:** Daily scheduled DAGs fetch, clean, and process weather API payloads without manual intervention[cite: 4].
*   **Relational Storage Bridge:** A strictly typed PostgreSQL database serves as the single source of truth connecting backend workers to front-end views[cite: 4].
*   **Interactive Geospatial Mapping:** Utilizes Plotly MapLibre to plot color-coded risk levels directly onto Moroccan transit routes[cite: 4].
*   **Dynamic Data Slicing:** Multi-variable sidebar filtering dynamically recalculates overview KPIs and time-series forecasts[cite: 4].
*   **Fully Containerized:** The entire infrastructure spins up identically on any machine via a single Docker Compose network[cite: 4].

---

## System Architecture

The project relies on three isolated Docker containers communicating via a shared internal network:

1.  **`airflow_single_node`**: Executes Python scripts to hit weather APIs, apply risk algorithms, and execute `INSERT` statements.
2.  **`postgres_db`**: Stores structured relational data mapping `cities` to multi-day `forecasts` via foreign keys.
3.  **`streamlit_dashboard`**: Queries the database via SQLAlchemy and serves a responsive UI on port `8501`.

---

## Getting Started

Follow these steps to deploy the full pipeline locally.

### Prerequisites
*   Docker Desktop installed and running.
*   Git version control.

### Installation & Deployment

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/weather-risk-data-pipeline.git](https://github.com/your-username/weather-risk-data-pipeline.git)
   cd weather-risk-data-pipeline
