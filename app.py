import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Basic page config
st.set_page_config(
    page_title="Uber Rides Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with black background
st.markdown("""
    <style>
    /* Main content area */
    .main {
        background-color: #000000;
        color: #00FF80;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #000000;
    }
    
    /* Charts */
    .stPlotlyChart {
        background-color: #111111;
        border-radius: 5px;
        padding: 1rem;
        border: 1px solid #333333;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FF0080;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #00FF80;
    }
    
    /* Dataframe */
    .dataframe {
        background-color: #111111;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #111111;
        color: #00FF80;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background-color: #111111;
        color: #00FF80;
    }
    </style>
""", unsafe_allow_html=True)

# Simple title
st.title("🚗 Uber Rides Analysis")

# Load data
try:
    # Read the data and clean it
    data = pd.read_csv("UberDataset.csv")
    
    # Remove any rows where START_DATE contains non-date values
    data = data[pd.to_datetime(data['START_DATE'], format='mixed', errors='coerce').notna()]
    
    # Now safely convert dates
    data['START_DATE'] = pd.to_datetime(data['START_DATE'], format='mixed')
    data['END_DATE'] = pd.to_datetime(data['END_DATE'], format='mixed')
    
    # Create tabs with custom styling
    tab1, tab2, tab3 = st.tabs([
        "📊 Basic Analysis",
        "🗺️ Advanced Visualizations",
        "🔍 Custom Query"
    ])
    
    # Tab 1: Basic Analysis
    with tab1:
        st.header("Basic Analysis")
        
        # Key metrics in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rides", f"{len(data):,}")
        with col2:
            st.metric("Total Miles", f"{data['MILES'].sum():,.1f}")
        with col3:
            st.metric("Average Distance", f"{data['MILES'].mean():.1f} miles")
        
        # Daily rides plot
        st.subheader("Daily Rides")
        daily_rides = data.groupby(data['START_DATE'].dt.date).size().reset_index(name='count')
        fig = px.line(daily_rides, x='START_DATE', y='count',
                     title='Number of Rides per Day',
                     template="plotly_dark")
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='#00FF80')
        )
        fig.update_traces(line_color='#FF0080')
        st.plotly_chart(fig, use_container_width=True)
        
        # Category distribution
        st.subheader("Rides by Category")
        category_counts = data['CATEGORY'].value_counts()
        fig = px.pie(values=category_counts.values, 
                    names=category_counts.index,
                    title='Distribution of Ride Categories',
                    template="plotly_dark",
                    color_discrete_sequence=['#FF0080', '#00FF80', '#00ADB5', '#FFD700'])
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='#00FF80')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Advanced Visualizations
    with tab2:
        st.header("Advanced Visualizations")
        
        # Miles distribution
        st.subheader("Ride Distance Distribution")
        fig = px.histogram(data, x='MILES',
                         title='Distribution of Ride Distances',
                         template="plotly_dark",
                         color_discrete_sequence=['#FF0080'])
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='#00FF80')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Purpose analysis (excluding NaN)
        st.subheader("Rides by Purpose")
        purpose_data = data[data['PURPOSE'].notna()]
        purpose_counts = purpose_data['PURPOSE'].value_counts()
        fig = px.bar(x=purpose_counts.index, 
                    y=purpose_counts.values,
                    title='Number of Rides by Purpose',
                    template="plotly_dark",
                    color_discrete_sequence=['#00FF80'])
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='#00FF80'),
            xaxis_title="Purpose",
            yaxis_title="Number of Rides"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Custom Query
    with tab3:
        st.header("Custom Query")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            selected_category = st.selectbox(
                "Select Category",
                options=['All'] + sorted(data['CATEGORY'].unique().tolist())
            )
        
        with col2:
            selected_purpose = st.selectbox(
                "Select Purpose",
                options=['All'] + sorted(data['PURPOSE'].dropna().unique().tolist())
            )
        
        # Apply filters
        filtered_data = data.copy()
        if selected_category != 'All':
            filtered_data = filtered_data[filtered_data['CATEGORY'] == selected_category]
        if selected_purpose != 'All':
            filtered_data = filtered_data[filtered_data['PURPOSE'] == selected_purpose]
        
        # Show filtered data
        st.write(f"Showing {len(filtered_data):,} rides")
        st.dataframe(filtered_data.style.background_gradient(cmap='magma', subset=['MILES']))

except Exception as e:
    st.error(f"Error: {str(e)}")
    st.write("Please ensure UberDataset.csv is in the same directory as the app.")
