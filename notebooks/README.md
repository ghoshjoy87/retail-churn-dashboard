# Research Notebooks

This directory contains the analytical workflow used to develop the customer retention decision-support artefact.

## Notebook Sequence

### 01_Data_Exploration.ipynb

Exploratory analysis of the E-Commerce Customer Churn dataset, including data structure, missing values, distributions, class balance, and relationships between customer variables and churn.

### 02_Data_Preprocessing_and_Segmentation.ipynb

Data cleaning, transformation, feature preparation, and adapted RFM customer segmentation.

`CashbackAmount` is used as a proxy for the Monetary component because direct transaction expenditure is unavailable in the source dataset.

### 03_Model_Training_and_Evaluation.ipynb

Training and comparative evaluation of candidate machine learning models, including Logistic Regression, Random Forest, XGBoost, CatBoost, and Soft Voting Ensemble.

Random Forest was selected for integration into the final decision-support system.

### 04_SHAP_Explainability.ipynb

Global and customer-level SHAP analysis for the selected Random Forest model, including business-readable explanation generation.

### 05_Counterfactual_Recommendations.ipynb

Generation and interpretation of DiCE counterfactual explanations for high-risk customers to support actionable retention decision-making.

## Workflow

```text
Data Exploration
      ↓
Preprocessing and Segmentation
      ↓
Model Training and Evaluation
      ↓
SHAP Explainability
      ↓
Counterfactual Recommendation Generation
