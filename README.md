# Business Intelligence and Explainable AI Decision Support System for Customer Retention in Retail SMEs

Master of Business Informatics Capstone Project – MBI908  
Yoobee College of Creative Innovation, Auckland, New Zealand

## Project Overview

This project develops a Business Intelligence and Explainable Artificial Intelligence
decision support system for customer retention in retail SMEs.

The system integrates:

- Customer churn prediction
- Random Forest machine learning
- Adapted RFM customer segmentation
- SHAP explainability
- DiCE counterfactual explanations
- Rule-based retention prioritisation
- Business-oriented retention recommendations
- Interactive Streamlit dashboard

The objective is not only to predict customer churn, but to provide managers with
transparent and actionable information explaining why customers are at risk and what
retention actions may be considered.

## Live Application

Streamlit application:

https://retail-churn-dashboard.streamlit.app/

## Research Artefact

The developed decision-support workflow combines:

Customer Data
→ Data Preparation
→ Adapted RFM Segmentation
→ Churn Prediction
→ SHAP Explainability
→ Retention Priority Classification
→ DiCE Counterfactual Analysis
→ Managerial Decision Support

## Dataset

The project uses the publicly available E-Commerce Customer Churn dataset.

The original dataset contains 5,630 customer records and a binary churn target.

Because transaction-level expenditure was not available, `CashbackAmount` was used as
a proxy for the Monetary component of the adapted RFM segmentation. This should not
be interpreted as equivalent to customer revenue, profitability, or customer lifetime value.

## Machine Learning Models

Five supervised machine learning models were evaluated:

- Logistic Regression
- Random Forest
- XGBoost
- CatBoost
- Soft Voting Ensemble

Random Forest was selected for integration into the final decision support system because
it demonstrated strong predictive performance while supporting efficient tree-based SHAP
explanations and straightforward integration with the downstream explainability and
decision-support components.

### Selected Random Forest Performance

| Metric | Result |
|---|---:|
| Accuracy | 96.18% |
| Precision | 92.00% |
| Recall | 84.74% |
| F1-score | 88.22% |
| ROC-AUC | 0.994 |

## Explainable AI

### SHAP

SHAP is used to provide:

- global model-level feature importance;
- individual customer-level explanations;
- business-readable explanations of factors increasing or reducing predicted churn risk.

### DiCE Counterfactual Explanations

DiCE is used to identify alternative feature conditions associated with lower predicted
churn risk.

Counterfactual outputs are intended as decision-support guidance rather than causal or
guaranteed retention outcomes.

## Customer Segmentation

An adapted Recency–Frequency–Monetary framework is used to provide behavioural
context alongside churn predictions.

`CashbackAmount` is used as a proxy for Monetary value because customer expenditure
is unavailable in the source dataset.

## Retention Priority Logic

Customers are classified as:

- Immediate Action
- Follow Up Soon
- Monitor

Priority is determined through a combination of predicted churn probability and customer
behaviour segment.

## Dashboard

The Streamlit dashboard includes:

- Executive Overview
- Customer Segmentation
- Retention Priority Centre
- Customer Profile
- Churn Drivers and Explainability
- Counterfactual Actions
- Churn Analysis

## Repository Structure

`app.py` – Streamlit decision-support dashboard

`notebooks/` – data exploration, preprocessing, modelling, SHAP, and counterfactual notebooks

`data/` – processed analytical outputs used by the prototype

`figures/` – model and dashboard visualisations

`architecture/` – system architecture diagrams

`report/` – final Master's capstone report

## Running the Application Locally

Clone the repository:

```bash
git clone https://github.com/ghoshjoy87/retail-churn-dashboard.git
cd retail-churn-dashboard
