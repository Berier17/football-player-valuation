# football-player-valuation
An end-to-end Machine Learning project that predicts football player market values using data scraped from Fbref and Transfermarkt (via ScraperFC &amp; soccerdata). Deployed with Docker and Flask
# ⚽ Football Player Valuation: Moneyball ML Project

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Status](https://img.shields.io/badge/Status-Completed-green)

## 📌 Problem Description
In the modern football transfer market, player valuations are often driven by hype rather than performance. This leads to massive overspending on players who underperform relative to their cost.

**The Goal:** Build a data-driven "Moneyball" tool to objectively estimate a player's market value based on performance metrics (Expected Goals, Starts, Age, Position), helping clubs identify undervalued talent.

---

## 🏗️ Architecture



The project follows a complete Machine Learning lifecycle:
1.  **Data Collection:** Automated scraping pipeline merging stats from **Fbref** with market values from **Transfermarkt**.
2.  **Training:** XGBoost Regressor trained on 2024/2025 season data using `scikit-learn`.
3.  **Deployment:** A Flask web service containerized with Docker for production use.

---

## 🛠️ Tech Stack

* **Language:** Python 3.11
* **Data Acquisition:** `ScraperFC`, `soccerdata` (See `scraping.ipynb`)
* **ML Libraries:** `scikit-learn` (v1.8.0), `xgboost` (v3.1.1)
* **Web Framework:** Flask, Gunicorn
* **Containerization:** Docker

---

## 🚀 How to Run the Project

### Option A: Run with Docker (Recommended)
This guarantees all dependencies (including specific library versions) match exactly.

├── Dockerfile             # Blueprint for the container (Python 3.11) 
├── requirements.txt       # Dependencies (Pinned for reproducibility) 
├── train.py               # Training script (Generates model.bin) 
├── predict.py             # Flask deployment script (Web Service) 
├── test.py                # Client script to test the deployed model 
├── scraping.ipynb         # Data extraction logic (ScraperFC/soccerdata) 
├── final_dataset.csv      # The clean dataset used for training 
├── model.bin              # The trained XGBoost model + DictVectorizer 
└── README.md              # Project documentation 

**1. Build the Docker Image**
```bash
docker build -t valuation-model .
