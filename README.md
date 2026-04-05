# 🏠 PropIQ — Real Estate Intelligence Platform

> End-to-end ML-powered real estate price prediction and analytics
> platform for the Gurgaon property market — deployed on AWS EC2.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat)
![XGBoost](https://img.shields.io/badge/XGBoost-R²=0.891-green?style=flat)
![AWS](https://img.shields.io/badge/AWS-EC2-orange?style=flat)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=flat)

---

## 📌 Live Links

| Service | URL |
|---|---|
| 🌐 Streamlit App | http://13.61.140.33:8501 |
| ⚡ FastAPI Docs  | http://13.61.140.33:8000/docs |
| 💻 GitHub        | github.com/sarthak2141/PropIQ |

---

## 🎯 Project Overview

PropIQ is a **production-grade real estate intelligence platform**
covering the complete data science lifecycle:

- **Data Cleaning & EDA** — 4,000+ raw records → 3,639 clean samples
- **Feature Engineering** — 102 features with target encoding
  and log transform
- **ML Modelling** — 11 algorithms benchmarked with 10-fold CV
- **Statistical Inference** — OLS regression with p-values and CIs
- **REST API** — FastAPI with Pydantic at sub-100ms response
- **Cloud Deployment** — Docker Compose on AWS EC2

---

## 🖥️ 4 Platform Modules

### 1. 🔮 AI Price Predictor
- Input property details → instant price estimate
- 3-tier confidence: Conservative / Expected / Optimistic (±₹22L)
- Sector comparison across 95+ Gurgaon sectors

### 2. 📊 Analysis Dashboard
- Geo-bubble map of price-per-sqft hotspots
- Sector × BHK interactive heatmap
- Price distribution charts by property type

### 3. 🤖 Smart Recommender
- Cosine similarity engine across 3,639 properties
- Configurable geo-radius (km) search

### 4. 📈 Price Insights
- OLS regression with statsmodels
- **Key findings (p < 0.0001):**
  - Servant Room: **+32.8%** price increase
  - Property Type: **+17.3%** premium
  - Each bathroom: **+6.5%**

---

## 🧠 Model Benchmarking Results

| Model | R² Score |
|---|---|
| Linear Regression | 0.800 |
| Ridge | 0.823 |
| Lasso | 0.818 |
| Decision Tree | 0.762 |
| Random Forest | 0.887 |
| Extra Trees | 0.881 |
| SVR | 0.841 |
| Gradient Boosting | 0.883 |
| MLP | 0.856 |
| **XGBoost ✅** | **0.891** |

**Final: XGBoost — R² = 0.891, MAE ≈ ₹51 Lakhs**

---

## ⚙️ Tech Stack

| Layer | Tech |
|---|---|
| ML | XGBoost, Scikit-learn, Statsmodels |
| Feature Eng | Category Encoders, Sklearn Pipeline |
| API | FastAPI, Pydantic, Uvicorn |
| Frontend | Streamlit, Plotly |
| DevOps | Docker, Docker Compose |
| Cloud | AWS EC2, EBS, Elastic IP |

---
## 🏗️ Architecture
User → Streamlit (8501) → FastAPI (8000) → XGBoost Model
Both running on AWS EC2 via Docker Compose
---

## 🚀 Run Locally
```bash
# Clone
git clone https://github.com/sarthak2141/PropIQ.git
cd PropIQ

# Run with Docker
docker-compose up -d

# Open
# App: http://localhost:8501
# API: http://localhost:8000/docs
```

---

## 📁 Project Structure

PropIQ/
├── API/                    ← FastAPI app
├── pages/                  ← Streamlit modules
│   ├── 1_Prediction.py
│   ├── 2_Analysis.py
│   ├── 3_Recommendation.py
│   └── 4_Insights.py
├── ML_Notebooks_Files/     ← EDA + model notebooks
├── Models/                 ← Trained model files
├── Utils/                  ← Styles + helpers
├── Home.py
├── Dockerfile.api
├── Dockerfile.Streamlit
├── docker-compose.yml
└── requirements.txt

---

## 🔌 API Usage
```bash
curl -X POST "http://13.61.140.33:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "property_Type": "flat",
    "sector": "sector 98",
    "bedRooms": 3,
    "bathrooms": 2,
    "balconies": "2",
    "built_up_area": 1500,
    "servent_room": 1,
    "floor_category": "High Floor",
    "store_room": 0
  }'

# Response: { "price": 1.23 }  ← Crores (₹)
```

---

## 👨‍💻 Author

**Sarthak Tiwari**
- 📧 sarthaktiwari2141@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/sarthak-tiwari-999020271)
- 📍 Delhi, India

---

⭐ **If you found this useful, please star the repo!**

