import streamlit as st
import pandas as pd
import plotly.express as px

# Basic page config
st.set_page_config(page_title="Uber Rides Analysis", layout="wide")

# Simple styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🚗 Uber Rides Analysis")

try:
    # Load and process data
    data = pd.read_csv("UberDataset.csv")
    
    # Convert dates
    data['START_DATE'] = pd.to_datetime(data['START_DATE'])
    
    # Basic metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rides", f"{len(data):,}")
    with col2:
        st.metric("Total Miles", f"{data['MILES'].sum():,.1f}")
    with col3:
        st.metric("Average Distance", f"{data['MILES'].mean():.1f} miles")
    
    # Simple visualization
    st.subheader("Rides by Category")
    fig = px.pie(
        values=data['CATEGORY'].value_counts().values,
        names=data['CATEGORY'].value_counts().index,
        title='Distribution of Ride Categories'
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error: {str(e)}")
    st.write("Please ensure UberDataset.csv is in the same directory as the app.")
