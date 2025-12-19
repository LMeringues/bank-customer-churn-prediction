import streamlit as st
import pandas as pd
import pickle
import numpy as np

@st.cache_resource
def load_data():
    with open ('data/processed/ansemble.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('data/processed/preprocessor.pkl', 'rb') as f:
        preprocessor = pickle.load(f)
    return model, preprocessor