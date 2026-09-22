# Business Intelligence and Explainable AI Decision Support System for Customer Retention in Retail SMEs

**Master of Business Informatics (Level 9) – MBI908 Industry-based Capstone Research Project**  
Yoobee College of Creative Innovation, Auckland, New Zealand

## Project Overview

This capstone project presents the design, development, and evaluation of a Business Intelligence and Explainable Artificial Intelligence (XAI) decision support system for customer retention in retail SMEs.

The system integrates:

- Customer churn prediction
- Random Forest machine learning
- Adapted RFM customer segmentation
- SHAP explainability
- DiCE counterfactual explanations
- Rule-based retention prioritisation
- Business-oriented retention recommendations
- Interactive Streamlit dashboard

The objective is not only to identify customers who may be at risk of churn, but also to provide transparent and actionable decision-support information that helps managers understand why a customer has been classified as at risk and what retention actions may be considered.

---

## Live Application

The deployed Streamlit prototype is available here:

**https://retail-churn-dashboard.streamlit.app/**

---

## Research Aim

The aim of this research is to design, develop, and evaluate a Business Intelligence and Explainable Artificial Intelligence-enabled decision support system that assists retail SMEs in identifying customers at risk of churn and supports transparent, evidence-based retention decision-making.

---

## Research Artefact

The developed system follows an integrated decision-support workflow:

```text
Customer Data
      ↓
Data Exploration and Preparation
      ↓
Adapted RFM Customer Segmentation
      ↓
Machine Learning Churn Prediction
      ↓
SHAP Explainability
      ↓
Retention Priority Classification
      ↓
DiCE Counterfactual Analysis
      ↓
Business-Readable Recommendations
      ↓
Streamlit Decision Support Dashboard
      ↓
Managerial Review and Decision-Making

The system is designed as a human-centred decision-support tool rather than an autonomous decision-maker.


Dataset
The project uses the publicly available E-Commerce Customer Churn Analysis and Prediction Dataset.
The original dataset contains:

5,630 customer records
20 predictor variables
One binary target variable: Churn
Numerical and categorical customer attributes
Demographic, behavioural, service, and transaction-related information
Adapted RFM Limitation

The dataset does not contain customer-level transaction revenue, total expenditure, or purchase value.
Therefore, CashbackAmount is used as a proxy for the Monetary component of the adapted RFM segmentation.

CashbackAmount should not be interpreted as equivalent to:
revenue;
customer expenditure;
profitability;
customer lifetime value.

The segmentation therefore represents relative behavioural and monetary-proxy positioning within the available dataset.

Machine Learning Development:
Five supervised machine learning models were trained and evaluated:
Logistic Regression
Random Forest
XGBoost
CatBoost
Soft Voting Ensemble

The same training and testing datasets and preprocessing procedures were used across candidate models.

Class imbalance in the training dataset was addressed using SMOTE, while the independent testing dataset remained unchanged for evaluation.

Selected Model:
Random Forest Classifier

Random Forest was selected for integration into the final decision-support system because it demonstrated strong predictive performance while supporting efficient tree-based SHAP explanations and straightforward integration with downstream explainability and recommendation components.

Random Forest Performance
Metric	Result
Accuracy	96.18%
Precision	92.00%
Recall	84.74%
F1-score	88.22%
ROC-AUC	0.994

The selected model provides both binary churn predictions and churn probability estimates for use within the explainability, prioritisation, and recommendation components.

Explainable AI
SHAP Explainability
SHAP is used to improve the transparency of the Random Forest model.

The implementation provides:
Global feature importance
SHAP summary analysis
Customer-level prediction explanations
Business-readable explanations of factors increasing or reducing predicted churn risk

SHAP outputs explain how model features contribute to predictions but should not be interpreted as evidence of causal relationships.

Counterfactual Explanations
The project uses DiCE – Diverse Counterfactual Explanations to extend explainability beyond prediction interpretation.
Counterfactual analysis identifies alternative feature conditions associated with a lower predicted churn risk.

The outputs support questions such as:
What changes are associated with a more favourable model outcome for this customer?
Counterfactual results are intended as decision-support guidance rather than guaranteed business outcomes or causal recommendations.

Customer Behaviour Segmentation
An adapted Recency–Frequency–Monetary (RFM) framework is used to provide behavioural context alongside churn predictions.
The implemented customer behaviour segments include:

High-Value Active Customers
Frequent Low-Value Customers
High-Value Occasional Customers
New and Developing Customers
Previously Valuable Customers
Frequent Customers Losing Interest
High-Value Customers Losing Interest
Inactive Customers

Behavioural segmentation does not replace churn prediction. Instead, it provides additional context for retention prioritisation.

Retention Priority Framework
Customers are classified into three operational priority categories:
Immediate Action
Follow Up Soon
Monitor

The implemented logic combines predicted churn probability with customer behaviour segment.

Priority Logic
IF churn probability >= 0.70
    Priority = Immediate Action

ELSE IF churn probability >= 0.40
    IF customer segment is:
        Previously Valuable Customers
        OR Frequent Customers Losing Interest
        OR High-Value Customers Losing Interest
        OR Inactive Customers
    THEN
        Priority = Immediate Action
    ELSE
        Priority = Follow Up Soon

ELSE
    Priority = Monitor

The thresholds are prototype-level business rules and would require organisational calibration before operational deployment.


Decision Support Dashboard
The Streamlit application integrates the analytical components into a business-oriented interface.
The main dashboard functions include:

Executive Overview
Customer Behaviour Segmentation
Retention Priority Centre
Customer Profile
Churn Drivers and Explainability
Counterfactual Actions
Churn Analysis
Processed Data Upload

The dashboard enables managers to move from organisation-level monitoring to individual customer investigation and intervention planning.


Technology Stack:
Programming and Development:
Python
Jupyter Notebook
Visual Studio Code
Data Processing
Pandas
NumPy
Machine Learning
Scikit-learn
imbalanced-learn
Random Forest
Logistic Regression
XGBoost
CatBoost
Soft Voting Ensemble
Explainable AI
SHAP
DiCE
Visualisation
Matplotlib
Plotly
Application Framework
Streamlit
Model Persistence
Joblib
Deployment
Streamlit Community Cloud


Repository Structure
retail-churn-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
├── ipynb/
│   ├── BD_01_Data_Exploration.ipynb
│   ├── V2_ BD_02_Data_Preprocessing & Segmentation.ipynb
│   ├── V2_BD_03_Model_Training_and_Evaluation.ipynb
│   ├── V2_BD_04_SHAP_Explainability.ipynb
│   └── V2_BD_05_Counterfactual_Recommendations.ipynb
│
├── Prototype Screenshots/
│
├── rfm_segmented_data.csv
├── final_recommendation_engine_output.csv
├── local_shap_reasons.csv
├── dice_counterfactual_highrisk.csv
└── shap_feature_importance.png

This structure reflects the current deployed repository. Further organisational restructuring may be undertaken without changing the analytical workflow.


Running the Application Locally
Clone the repository:

git clone https://github.com/ghoshjoy87/retail-churn-dashboard.git
cd retail-churn-dashboard

Install the required packages:

pip install -r requirements.txt

Run the Streamlit application:

streamlit run app.py

The application will then open in the local browser.

Responsible AI and Human Oversight

The prototype is designed as a human-centred decision-support system.

Predictions, explanations, priorities, and counterfactual outputs should not be treated as automatic business decisions.


Managers should consider:
Actionability
Feature mutability
Causal plausibility
Customer circumstances
Fairness
Privacy
Commercial feasibility
Organisational policy
Intervention monitoring

User-facing explanations and counterfactual recommendations focus on business-actionable variables where applicable rather than relying on immutable personal characteristics.

Ethical and Cultural Considerations
Responsible deployment requires attention to:

Transparency
Accountability
Privacy
Fairness
Human oversight
Data governance
Model monitoring

Within the New Zealand context, future implementation should also consider Māori Data Sovereignty and relevant Indigenous data governance principles, including the CARE Principles and guidance from Te Mana Raraunga.


User Evaluation:
The prototype was evaluated with 11 participants, including:

Retail managers
Business students
A small business owner
A data engineer

Participants evaluated:

Dashboard navigation
Identification of customers requiring retention action
SHAP explanations
Counterfactual recommendations
Overall usefulness for customer retention decision-making

The formative evaluation indicated positive perceptions of usability, interpretability, and practical usefulness, while also identifying opportunities for future refinement.

Research Limitations:
The project should be interpreted as a research prototype.
Key limitations include:

Use of a single historical customer dataset
Use of CashbackAmount as a proxy for the Monetary component of RFM
Static rather than real-time organisational data
Rule-based recommendation logic
No live CRM or enterprise-system integration
Limited formative user evaluation
No longitudinal evaluation of actual customer retention outcomes
SHAP explanations are associative rather than causal
Counterfactual scenarios do not guarantee successful interventions
Future Development


Potential future enhancements include:

Real-time data integration
CRM integration
Automated model retraining
Model drift monitoring
Fairness monitoring
Adaptive recommendation learning
Improved filtering
More personalised recommendations
Additional customer engagement data
Longitudinal organisational evaluation
Transaction-level monetary data for conventional RFM analysis


Capstone Report:
The complete research methodology, literature review, system design, implementation, evaluation, ethical analysis, limitations, and discussion are documented in the final Master's capstone report. [Download the Final Capstone Report](report/Sanjoy_Final_Capstone_Report.pdf)

Project title:
Business Intelligence and Explainable Artificial Intelligence Decision Support System for Customer Retention in Retail SMEs

Author

Sanjoy Kumar Ghosh
Master of Business Informatics
Yoobee College of Creative Innovation
Auckland, New Zealand


Academic Use:
This repository supports the MBI908 Industry-based Capstone Research Project.
The repository is intended to provide implementation evidence, reproducibility support, and technical documentation for the developed research artefact.


Disclaimer
This software was developed for academic research and prototype demonstration.
Predictions, explanations, counterfactual scenarios, and retention recommendations should not be treated as deterministic, causal, or automatically executable business decisions.
Operational deployment would require further organisational validation, governance, security controls, monitoring, and human oversight.
