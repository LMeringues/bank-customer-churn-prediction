import streamlit as st
import pandas as pd
import pickle
import numpy as np

@st.cache_resource
def load_tools():
    try:
        with open('data/processed/ansemble.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('data/processed/preprocessor.pkl', 'rb') as f:
            preprocessor = pickle.load(f)
        with open('data/processed/metadata.pkl', 'rb') as f:
            meta = pickle.load(f)
        return model, preprocessor, meta
    except FileNotFoundError as e:
        st.error(f"Critical Error: File not found ({e.filename}). Please run notebooks 04 and 05.")
        st.stop()

model, preprocessor, meta = load_tools()

st.title("Customer Churn Prediction")
st.write("Enter customer data to assess churn risk")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Profile")
    gender = st.selectbox("Gender", meta['gender'])
    marital_status = st.selectbox("Marital Status", meta['marital_status'])
    education = st.selectbox("Education Level", meta['education_level'])
    age = st.number_input("Age", 
                          min_value=int(meta['age']['min']), 
                          max_value=int(meta['age']['max']), 
                          value=int(meta['age']['default']),
                          step=1)

with col2:
    st.subheader("💳 Financials")
    income = st.number_input("Annual Income", 
                             min_value=float(meta['income']['min']), 
                             max_value=float(meta['income']['max']), 
                             value=float(meta['income']['default']),
                             step=100.0)
    
    credit_score = st.number_input("Credit Score", 
                                   min_value=int(meta['credit_score']['min']), 
                                   max_value=int(meta['credit_score']['max']), 
                                   value=int(meta['credit_score']['default']),
                                   step=1)
    
    loans = st.number_input("Outstanding Loans", 
                            min_value=float(meta['outstanding_loans']['min']), 
                            max_value=float(meta['outstanding_loans']['max']), 
                            value=float(meta['outstanding_loans']['default']),
                            step=100.0)
    
    dependents = st.number_input("Dependents", 
                                 min_value=int(meta['number_of_dependents']['min']), 
                                 max_value=int(meta['number_of_dependents']['max']), 
                                 value=int(meta['number_of_dependents']['default']),
                                 step=1)

with col3:
    st.subheader("🏦 Bank Relations")
    segment = st.selectbox("Customer Segment", meta['customer_segment'])
    
    tenure = st.number_input("Tenure (Months/Years)", 
                             min_value=int(meta['customer_tenure']['min']), 
                             max_value=int(meta['customer_tenure']['max']), 
                             value=int(meta['customer_tenure']['default']),
                             step=1)
    
    products = st.number_input("Num of Products", 
                               min_value=int(meta['numofproducts']['min']), 
                               max_value=int(meta['numofproducts']['max']), 
                               value=int(meta['numofproducts']['default']),
                               step=1)
    
    complaints = st.number_input("Num Complaints", 
                                 min_value=int(meta['numcomplaints']['min']), 
                                 max_value=int(meta['numcomplaints']['max']), 
                                 value=0,
                                 step=1)
    
    history_len = st.number_input("Credit History Len", 
                                  min_value=float(meta['credit_history_length']['min']), 
                                  max_value=float(meta['credit_history_length']['max']), 
                                  value=float(meta['credit_history_length']['default']),
                                  step=0.1)

    comm_channel = st.selectbox("Communication Channel", meta['preferred_communication_channel'])



if st.button("Analyze Risks", type='primary'):
    

    raw_data = pd.DataFrame({
        'number_of_dependents': [dependents],
        'income': [income],
        'customer_tenure': [tenure],
        'credit_score': [credit_score],
        'credit_history_length': [history_len],
        'outstanding_loans': [loans],
        'numofproducts': [products],
        'numcomplaints': [complaints],
        'age': [age],
        'gender': [gender],
        'marital_status': [marital_status],
        'education_level': [education],
        'customer_segment': [segment],
        'preferred_communication_channel': [comm_channel]
    })


    raw_data['tenure_to_age'] = raw_data['customer_tenure'] / raw_data['age']
    
    safe_tenure = raw_data['customer_tenure'].replace(0, 1)
    raw_data['products_per_year'] = raw_data['numofproducts'] / safe_tenure

    
    try:
        input_prep = preprocessor.transform(raw_data)
        prediction_prob = model.predict_proba(input_prep)[0][1]
        
        st.divider()
        st.subheader("Analysis Results")

        # Виправлено синтаксис st.columns([])
        col_res1, col_res2 = st.columns([1, 3])

        with col_res1:
            st.metric(label="Churn Probability", value=f"{prediction_prob:.1%}")
        
        with col_res2:
            if prediction_prob > 0.5:
                st.error("⚠️ **High Risk Customer**")
                st.progress(prediction_prob)
                st.write(f"This customer has a **{prediction_prob:.1%}** chance of leaving.")
            else:
                st.success("✅ **Low Risk Customer**")
                st.progress(prediction_prob)
                st.write(f"This customer is likely to stay. Risk level: **{prediction_prob:.1%}**")

            with st.expander("See processed data details"):
                st.dataframe(raw_data)
                
    except Exception as e:
        st.error(f"Error during prediction: {e}")