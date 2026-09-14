# Data Integration & Exploratory Data Analysis Pipeline

This repository contains an end-to-end Python pipeline designed to extract, integrate, and analyze data from structured and unstructured sources. 

## Architecture
* **Structured Data:** PostgreSQL (`psycopg2`) containing business entities (Users, Products, Transactions).
* **Unstructured Data:** MongoDB (`pymongo`) containing website telemetry and reviews.
* **Orchestration:** Python pipeline applying a Left Join via `pandas` to ensure revenue metrics are retained alongside sparse telemetry data.
* **Analysis:** Automated hypothesis testing (`scipy.stats`) for Exploratory Data Analysis.

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure your local or cloud database credentials.
4. Run the pipeline: `python main.py`
