import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Customer Churn Decision Support Dashboard",
    layout="wide"
)

st.title("Customer Churn Decision Support Dashboard")
st.markdown(
    "Business-friendly decision support prototype for churn risk, customer behaviour segments, "
    "retention priorities, SHAP explanations, and counterfactual actions."
)

# ============================================================
# LOAD DATA
# ============================================================

st.sidebar.subheader("Data Source")

data_mode = st.sidebar.radio(
    "Choose data source",
    ["Use default project data", "Upload processed data"]
)

@st.cache_data
def load_default_data():
    recommendation_df = pd.read_csv("final_recommendation_engine_output.csv")
    rfm_df = pd.read_csv("rfm_segmented_data.csv")

    if os.path.exists("dice_counterfactual_highrisk.csv"):
        dice_df = pd.read_csv("dice_counterfactual_highrisk.csv")
    else:
        dice_df = pd.DataFrame()

    return recommendation_df, rfm_df, dice_df


if data_mode == "Use default project data":
    recommendation_df, rfm_df, dice_df = load_default_data()

else:
    st.sidebar.info(
        "Prototype upload mode: please upload processed CSV files only. Raw Excel upload is not supported in this version."
    )
    
    uploaded_recommendation = st.sidebar.file_uploader(
        "Upload final_recommendation_engine_output.csv",
        type=["csv"]
    )

    uploaded_rfm = st.sidebar.file_uploader(
        "Upload rfm_segmented_data.csv",
        type=["csv"]
    )

    uploaded_dice = st.sidebar.file_uploader(
        "Optional: Upload dice_counterfactual_highrisk.csv",
        type=["csv"]
    )

    if uploaded_recommendation is not None and uploaded_rfm is not None:
        recommendation_df = pd.read_csv(uploaded_recommendation)
        rfm_df = pd.read_csv(uploaded_rfm)

        if uploaded_dice is not None:
            dice_df = pd.read_csv(uploaded_dice)
        else:
            dice_df = pd.DataFrame()

        st.sidebar.success("Uploaded data loaded successfully.")

    else:
        st.warning("Please upload the recommendation CSV and RFM CSV to continue.")
        st.stop()

# Column names from final recommendation engine
segment_col = "Customer_Behaviour_Segment"
risk_col = "Churn_Risk"
recommendation_col = "Final_Manager_Action"

priority_segments = [
    "Previously Valuable Customers",
    "Frequent Customers Losing Interest",
    "High-Value Customers Losing Interest",
    "Inactive Customers"
]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def display_actions(action_text):
    actions = str(action_text).split("|")
    for action in actions:
        action = action.strip()
        if action:
            st.markdown(f"✅ {action}")


def risk_colour_label(risk):
    if risk == "High Churn Risk":
        return "🔴 High Churn Risk"
    elif risk == "Medium Churn Risk":
        return "🟠 Medium Churn Risk"
    else:
        return "🟢 Low Churn Risk"


def priority_colour_label(priority):
    if priority == "Immediate Action":
        return "🔴 Immediate Action"
    elif priority == "Follow Up Soon":
        return "🟠 Follow Up Soon"
    else:
        return "🟢 Monitor"


recommendation_df["Risk_Display"] = recommendation_df[risk_col].apply(risk_colour_label)
recommendation_df["Priority_Display"] = recommendation_df["Priority_Label"].apply(priority_colour_label)

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Customer Segments",
        "Retention Priority Centre",
        "Customer Profile",
        "Counterfactual Actions",
        "Churn Drivers"
    ]
)

# ============================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.header("Executive Overview")

    total_customers = len(recommendation_df)
    high_risk = len(recommendation_df[recommendation_df[risk_col] == "High Churn Risk"])
    avg_churn = recommendation_df["Churn_Probability"].mean()

    Customers_in_Retention_Target_Segments = len(
        recommendation_df[
            recommendation_df[segment_col].isin(priority_segments)
        ]
    )

    immediate_action_count = len(
        recommendation_df[recommendation_df["Priority_Label"] == "Immediate Action"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)
    col2.metric("High Churn Risk Customers", high_risk)
    col3.metric("Customers in Retention Target Segments", Customers_in_Retention_Target_Segments)
    col4.metric("Average Churn Probability", f"{avg_churn:.2%}")

    st.info(
        f"""
        **How to read this dashboard**

        - **Churn Risk** is predicted by the Random Forest model.
        - **Customer Behaviour Segment** is based on RFM behaviour patterns.
        - **Priority Score** combines churn probability and customer behaviour segment.
        - **Final Manager Action** recommends what the manager should do next.
        - **Counterfactual Actions** explain what behavioural changes may reduce churn risk.
        """
    )

    st.warning(
        f"{immediate_action_count} customers currently require immediate retention action."
    )

    col5, col6 = st.columns(2)

    with col5:
        risk_counts = recommendation_df[risk_col].value_counts().reset_index()
        risk_counts.columns = ["Churn Risk", "Count"]

        fig_risk = px.pie(
            risk_counts,
            names="Churn Risk",
            values="Count",
            title="Customer Churn Risk Distribution",
            hole=0.4
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with col6:
        segment_counts = recommendation_df[segment_col].value_counts().reset_index()
        segment_counts.columns = ["Customer Behaviour Segment", "Count"]

        fig_segment = px.bar(
            segment_counts,
            x="Customer Behaviour Segment",
            y="Count",
            title="Customer Behaviour Segment Distribution"
        )
        st.plotly_chart(fig_segment, use_container_width=True)

    st.subheader("Top 10 Customers Requiring Immediate Retention Action")

    top_priority = recommendation_df.sort_values(
        "Priority_Score",
        ascending=False
    ).head(10)

    st.dataframe(
        top_priority[
            [
                "Customer_Index",
                segment_col,
                "Risk_Display",
                "Churn_Probability",
                "Priority_Score",
                "Priority_Display",
                recommendation_col
            ]
        ],
        use_container_width=True
    )

# ============================================================
# PAGE 2: CUSTOMER SEGMENTS
# ============================================================

elif page == "Customer Segments":

    st.header("Customer Behaviour Segments")

    st.markdown(
        """
        Customers are grouped using behaviour-based RFM segmentation.  
        These segment names describe customer behaviour directly so managers can understand the customer type quickly.
        """
    )

    segment_counts = recommendation_df[segment_col].value_counts().reset_index()
    segment_counts.columns = ["Customer Behaviour Segment", "Count"]

    fig = px.bar(
        segment_counts,
        x="Customer Behaviour Segment",
        y="Count",
        title="Customer Behaviour Segment Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

    segment_summary = pd.DataFrame({
        "Customer Behaviour Segment": [
            "High-Value Active Customers",
            "Frequent Low-Value Customers",
            "High-Value Occasional Customers",
            "New and Developing Customers",
            "Previously Valuable Customers",
            "Frequent Customers Losing Interest",
            "High-Value Customers Losing Interest",
            "Inactive Customers"
        ],
        "Business Meaning": [
            "Recent, frequent, and high-value customers.",
            "Customers who purchase often but generate lower value.",
            "Customers who generate high value but purchase less frequently.",
            "Recent customers still developing frequency and value.",
            "Customers who were valuable before but are now less active.",
            "Customers with strong past frequency but declining recent activity.",
            "High-value customers whose recent activity is declining.",
            "Customers with weak recent activity, low frequency, and low value."
        ],
        "Suggested Action": [
            "Reward and retain with VIP benefits.",
            "Increase basket value through bundles and cross-sell.",
            "Encourage more frequent purchases with personalised offers.",
            "Nurture through onboarding and welcome incentives.",
            "Recover through personalised win-back campaigns.",
            "Re-engage with loyalty incentives and reminder offers.",
            "Prioritise premium retention and personal outreach.",
            "Use low-cost automated reactivation or monitor."
        ]
    })

    st.subheader("Segment Meaning and Business Action")
    st.dataframe(segment_summary, use_container_width=True)

    selected_segment = st.selectbox(
        "Select Customer Behaviour Segment",
        recommendation_df[segment_col].unique()
    )

    selected_df = recommendation_df[
        recommendation_df[segment_col] == selected_segment
    ].sort_values("Priority_Score", ascending=False)

    st.subheader(f"Customers in: {selected_segment}")

    st.dataframe(
        selected_df[
            [
                "Customer_Index",
                segment_col,
                "Risk_Display",
                "Churn_Probability",
                "Priority_Score",
                "Priority_Display",
                recommendation_col
            ]
        ],
        use_container_width=True
    )

# ============================================================
# PAGE 3: RETENTION PRIORITY CENTRE
# ============================================================

elif page == "Retention Priority Centre":

    st.header("Retention Priority Centre")

    st.info(
        "This page helps managers identify which customers should be contacted first."
    )

    risk_filter = st.multiselect(
        "Select Churn Risk",
        recommendation_df[risk_col].unique(),
        default=["High Churn Risk"]
    )

    segment_filter = st.multiselect(
        "Select Behaviour Segment",
        recommendation_df[segment_col].unique(),
        default=[s for s in priority_segments if s in recommendation_df[segment_col].unique()]
    )

    filtered_df = recommendation_df[
        (recommendation_df[risk_col].isin(risk_filter)) &
        (recommendation_df[segment_col].isin(segment_filter))
    ].sort_values("Priority_Score", ascending=False)

    col1, col2, col3 = st.columns(3)

    col1.metric("Selected Customers", len(filtered_df))

    if len(filtered_df) > 0:
        col2.metric("Average Churn Probability", f"{filtered_df['Churn_Probability'].mean():.2%}")
    else:
        col2.metric("Average Churn Probability", "0%")

    col3.metric(
        "Immediate Actions",
        len(filtered_df[filtered_df["Priority_Label"] == "Immediate Action"])
    )

    st.subheader("Priority Retention List")

    st.dataframe(
        filtered_df[
            [
                "Customer_Index",
                segment_col,
                "Risk_Display",
                "Churn_Probability",
                "Priority_Score",
                "Priority_Display",
                recommendation_col
            ]
        ],
        use_container_width=True
    )

    st.download_button(
        "Download Retention Target List",
        filtered_df.to_csv(index=False),
        "retention_target_list.csv",
        "text/csv"
    )

# ============================================================
# PAGE 4: CUSTOMER PROFILE
# ============================================================

elif page == "Customer Profile":

    st.header("Customer Profile")

    customer_options = recommendation_df.sort_values(
        "Priority_Score",
        ascending=False
    )["Customer_Index"].tolist()

    customer_id = st.selectbox(
        "Select Customer",
        customer_options
    )

    customer = recommendation_df[
        recommendation_df["Customer_Index"] == customer_id
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Customer Index", customer["Customer_Index"])
    col2.metric("Churn Probability", f"{customer['Churn_Probability']:.2%}")
    col3.metric("Priority Score", customer["Priority_Score"])

    st.subheader("Customer Behaviour Segment")
    st.write(customer[segment_col])

    st.subheader("Churn Risk")

    if customer[risk_col] == "High Churn Risk":
        st.error("High Churn Risk: this customer should be reviewed for immediate retention action.")
    elif customer[risk_col] == "Medium Churn Risk":
        st.warning("Medium Churn Risk: this customer should be followed up and monitored.")
    else:
        st.success("Low Churn Risk: this customer is currently stable.")

    st.subheader("Retention Priority")

    if customer["Priority_Label"] == "Immediate Action":
        st.error("Immediate Action Required")
    elif customer["Priority_Label"] == "Follow Up Soon":
        st.warning("Follow Up Soon")
    else:
        st.success("Monitor")

    st.subheader("Recommended Manager Action")
    display_actions(customer[recommendation_col])

    if not dice_df.empty:
        customer_dice = dice_df[dice_df["Customer_Index"] == customer_id]

        if len(customer_dice) > 0:
            st.subheader("Counterfactual Actions for This Customer")

            st.dataframe(
                customer_dice[
                    [
                        "Original_Probability",
                        "Target_Probability",
                        "Feature_To_Change",
                        "Counterfactual_Manager_Action"
                    ]
                ],
                use_container_width=True
            )
        else:
            st.info("No DiCE counterfactual action is available for this customer.")

# ============================================================
# PAGE 5: COUNTERFACTUAL ACTIONS
# ============================================================

elif page == "Counterfactual Actions":

    st.header("Counterfactual Actions")

    st.markdown(
        """
        Counterfactual explanations show which customer behaviour changes may reduce churn risk.  
        The technical DiCE model uses scaled values internally, but this dashboard presents business-readable actions for managers.
        """
    )

    if dice_df.empty:
        st.warning(
            "No DiCE file found. Please place 'dice_counterfactual_highrisk.csv' in the same folder as app.py."
        )

    else:
        st.success("Counterfactual actions are available for high churn risk customers.")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Counterfactual Recommendations", len(dice_df))
        col2.metric("Customers with Counterfactual Plan", dice_df["Customer_Index"].nunique())
        col3.metric("Behaviour Factors Identified", dice_df["Feature_To_Change"].nunique())

        feature_counts = dice_df["Feature_To_Change"].value_counts().reset_index()
        feature_counts.columns = ["Behaviour Factor", "Count"]

        fig_features = px.bar(
            feature_counts,
            x="Count",
            y="Behaviour Factor",
            orientation="h",
            title="Most Common Behaviour Factors Suggested by Counterfactual Analysis",
            category_orders={
                "Behaviour Factor": feature_counts["Behaviour Factor"].tolist()
    }
        )

        st.plotly_chart(fig_features, use_container_width=True)

        selected_customer = st.selectbox(
            "Select Customer with Counterfactual Output",
            sorted(dice_df["Customer_Index"].unique())
        )

        customer_cf = dice_df[dice_df["Customer_Index"] == selected_customer]

        st.subheader(f"Counterfactual Actions for Customer {selected_customer}")

        display_cols = [
            "Customer_Index",
            "Original_Probability",
            "Target_Probability",
            "Feature_To_Change",
            "Counterfactual_Manager_Action",
        ]

        st.dataframe(
            customer_cf[display_cols],
            use_container_width=True
        )

        st.subheader("Manager-Friendly Counterfactual Actions")

        for _, row in customer_cf.iterrows():
            st.markdown(f"✅ {row['Counterfactual_Manager_Action']}")

        st.info(
            """
            Note: Scaled DiCE values are not shown here because they are technical model values.  
            Managers should use the business-readable counterfactual actions instead.
            """
        )

# ============================================================
# PAGE 6: CHURN DRIVERS
# ============================================================

elif page == "Churn Drivers":

    st.header("Churn Drivers and Explainability")

    st.markdown(
        """
        This page explains the main factors influencing customer churn predictions.  
        These drivers are based on the SHAP explainability analysis from the selected Random Forest model.
        """
    )

    shap_drivers = pd.DataFrame({
        "Rank": [1, 2, 3, 4, 5],
        "Churn Driver": [
            "Tenure",
            "Complaint History",
            "Number of Addresses",
            "Cashback Amount",
            "Days Since Last Order"
        ],
        "Business Interpretation": [
            "Newer customers are more likely to churn.",
            "Customers with complaints have higher churn risk.",
            "Multiple addresses may indicate unstable or changing purchase behaviour.",
            "Cashback and reward behaviour influence retention.",
            "Longer time since last order indicates disengagement."
        ],
        "Possible Management Action": [
            "Improve onboarding and early relationship building.",
            "Resolve complaints quickly and follow up.",
            "Monitor inconsistent customer behaviour.",
            "Use targeted cashback or loyalty rewards.",
            "Send re-engagement campaigns."
        ]
    })

    st.subheader("Top Business Drivers of Customer Churn")
    st.dataframe(shap_drivers, use_container_width=True)

    st.subheader("How to Interpret These Drivers")

    st.info("""
    The drivers shown above are ranked by their influence on the Random Forest model's churn prediction.

    • A higher-ranked driver has a stronger impact on predicting customer churn.

    • These drivers explain the model's behaviour across all customers rather than for an individual customer.

    • They should be used to guide retention strategy and operational improvements, not as direct causes of churn.
    """)


    st.subheader("Key Management Insight")

    st.success("""
    Customer churn is influenced by multiple behavioural factors rather than a single issue.
    Improving customer onboarding, resolving complaints promptly, encouraging repeat purchases,
    and increasing customer engagement are expected to reduce churn risk across the customer base.
    """)

