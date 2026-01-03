# 🏦 Bank Customer Churn Prediction

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](INSERT_YOUR_STREAMLIT_LINK_HERE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Model-orange)](https://xgboost.readthedocs.io/)

## Project Overview
This project is an end-to-end Machine Learning solution designed to predict whether a bank customer is likely to churn (leave the bank). Identifying at-risk customers allows businesses to take proactive retention measures.

The solution includes a full pipeline: from data preprocessing and feature engineering to model training and deployment as an interactive web application.

### Live Demo
**Check out the deployed app here:** [Bank Churn Prediction App](https://bank-customer-churn-prediction-6jfpmjgwd8udkwwsyz3jkq.streamlit.app/)

---

## 🛠 Tech Stack & Tools
* **Language:** Python
* **Data Manipulation:** Pandas, NumPy
* **Machine Learning:** Scikit-learn, XGBoost, Imbalanced-learn
* **Visualization:** Matplotlib, Seaborn
* **Deployment:** Streamlit, Streamlit Cloud
* **Version Control:** Git, GitHub

---

## ⚙️ Key Features & Methodology

### 1. Data Preprocessing
* **Cleaning:** Handled missing values and outliers.
* **Feature Engineering:** Created new features such as loyalty scores and balance-to-salary ratios.
* **Encoding:** Applied One-Hot Encoding for categorical variables (Geography, Gender).
* **Scaling:** Standardized numerical features for better model performance.

### 2. Handling Class Imbalance
The dataset was heavily imbalanced (fewer churners than retained customers). I used **SMOTE (Synthetic Minority Over-sampling Technique)** to generate synthetic samples for the minority class, ensuring the model doesn't just predict "No Churn" by default.

### 3. Model Building
I experimented with several algorithms and built an **Ensemble Model (Voting Classifier)** combining:
* **Logistic Regression** (for baseline probability).
* **XGBoost Classifier** (hyperparameter tuned for maximum accuracy).

### 4. Performance
* **Metric:** ROC-AUC Score
* **Result:** ~0.79

---

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LMeringues/bank-customer-churn-prediction.git
   cd bank-customer-churn-prediction

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py 

