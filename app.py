import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os

# Basic page config
st.set_page_config(
    page_title="Uber Rides Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI with gradients and 3D effects
st.markdown("""
    <style>
    /* Main content area */
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #00FF80;
        padding: 2rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #000000 0%, #1a1a1a 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Charts container */
    .stPlotlyChart {
        background: linear-gradient(45deg, #111111 0%, #1a1a1a 100%);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        transform: translateY(0);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stPlotlyChart:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
    }
    
    /* Headers with gradient text */
    h1 {
        background: linear-gradient(45deg, #FF0080, #00FF80);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem !important;
    }
    
    h2 {
        background: linear-gradient(45deg, #00FF80, #00ADB5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #FF0080;
        font-size: 1.5rem !important;
    }
    
    /* Metrics with 3D effect */
    div[data-testid="stMetricValue"] {
        background: linear-gradient(45deg, #111111, #1a1a1a);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 128, 0.2);
        box-shadow: 0 5px 15px rgba(0, 255, 128, 0.1);
        color: #00FF80 !important;
        font-size: 2rem !important;
        text-align: center;
        transform: translateZ(0);
        transition: transform 0.3s ease;
    }
    
    div[data-testid="stMetricValue"]:hover {
        transform: translateZ(10px);
        box-shadow: 0 8px 20px rgba(0, 255, 128, 0.2);
    }
    
    /* Tabs with gradient */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(90deg, #111111 0%, #1a1a1a 100%);
        border-radius: 10px;
        padding: 0.5rem;
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #00FF80 !important;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 255, 128, 0.1);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, rgba(255, 0, 128, 0.2), rgba(0, 255, 128, 0.2)) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: linear-gradient(45deg, #111111, #1a1a1a);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Selectbox and inputs with glassmorphism */
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        background: rgba(17, 17, 17, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #00FF80;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover,
    .stTextInput > div > div > input:hover {
        border-color: rgba(0, 255, 128, 0.3);
        box-shadow: 0 0 15px rgba(0, 255, 128, 0.1);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #111111;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #FF0080, #00FF80);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #00FF80, #FF0080);
    }
    </style>
""", unsafe_allow_html=True)

# Title with emoji and subtitle
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1>🚗 Uber Rides Analysis</h1>
        <p style='color: #00FF80; font-size: 1.2rem; margin-top: -1rem;'>
            Discover insights from your ride data
        </p>
    </div>
""", unsafe_allow_html=True)

# Load data
try:
    # Check if file exists
    data_file = "UberDataset.csv"
    if not os.path.exists(data_file):
        st.error(f"Error: Could not find {data_file} in the current directory: {os.getcwd()}")
        st.stop()

    # Read the data and clean it
    data = pd.read_csv(data_file)
    
    # Show data loading status
    st.sidebar.success(f"Successfully loaded {len(data):,} records")
    
    # Basic data validation
    required_columns = ['START_DATE', 'END_DATE', 'CATEGORY', 'MILES', 'PURPOSE']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"Error: Missing required columns: {', '.join(missing_columns)}")
        st.stop()
    
    # Remove any rows where START_DATE contains non-date values
    original_length = len(data)
    data = data[pd.to_datetime(data['START_DATE'], format='mixed', errors='coerce').notna()]
    if len(data) < original_length:
        st.warning(f"Removed {original_length - len(data):,} rows with invalid dates")
    
    # Now safely convert dates
    data['START_DATE'] = pd.to_datetime(data['START_DATE'], format='mixed')
    data['END_DATE'] = pd.to_datetime(data['END_DATE'], format='mixed')
    
    # Extract hour and day of week for 3D analysis
    data['Hour'] = data['START_DATE'].dt.hour
    data['DayOfWeek'] = data['START_DATE'].dt.dayofweek
    data['Month'] = data['START_DATE'].dt.month
    
    # Show data summary in sidebar
    with st.sidebar:
        st.write("### Data Summary")
        st.write(f"Date Range: {data['START_DATE'].min().date()} to {data['START_DATE'].max().date()}")
        st.write(f"Total Miles: {data['MILES'].sum():,.1f}")
        st.write(f"Categories: {', '.join(data['CATEGORY'].unique())}")

    # Create tabs with custom styling
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊  Basic Analysis  ",
        "🎯  Advanced Insights  ",
        "🌐  3D Visualizations  ",
        "🔍  Custom Query  "
    ])
    
    # Tab 1: Basic Analysis
    with tab1:
        st.header("Basic Analysis")
        
        # Key metrics in columns with descriptions
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Rides", value=f"{len(data):,}", label_visibility="collapsed")
        
        with col2:
            st.metric(label="Total Miles", value=f"{data['MILES'].sum():,.1f}", label_visibility="collapsed")
        
        with col3:
            st.metric(label="Average Distance", value=f"{data['MILES'].mean():.1f} miles", label_visibility="collapsed")
        
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
    
    # Tab 2: Advanced Insights
    with tab2:
        st.header("Advanced Insights")
        
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
    
    # Tab 3: 3D Visualizations
    with tab3:
        st.header("3D Visualizations")
        
        # 3D scatter plot of rides by hour, day, and distance
        st.subheader("Ride Patterns in 3D Space")
        
        # Create 3D scatter plot
        fig = go.Figure(data=[go.Scatter3d(
            x=data['Hour'],
            y=data['DayOfWeek'],
            z=data['MILES'],
            mode='markers',
            marker=dict(
                size=5,
                color=data['MILES'],
                colorscale='Viridis',
                opacity=0.7,
                colorbar=dict(title="Miles"),
            ),
            hovertemplate=
            '<b>Hour</b>: %{x}<br>' +
            '<b>Day</b>: %{y}<br>' +
            '<b>Miles</b>: %{z:.1f}<br>'
        )])
        
        # Update layout for better 3D view
        fig.update_layout(
            scene=dict(
                xaxis_title='Hour of Day',
                yaxis_title='Day of Week',
                zaxis_title='Miles',
                xaxis=dict(gridcolor='rgba(0,255,128,0.1)', showgrid=True),
                yaxis=dict(gridcolor='rgba(0,255,128,0.1)', showgrid=True),
                zaxis=dict(gridcolor='rgba(0,255,128,0.1)', showgrid=True),
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            template="plotly_dark",
            plot_bgcolor='black',
            paper_bgcolor='black',
            margin=dict(l=0, r=0, b=0, t=30),
            height=600,
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 3D Surface plot of average rides by hour and day
        st.subheader("Ride Density Surface")
        
        # Calculate average rides for each hour and day combination
        ride_matrix = pd.pivot_table(
            data,
            values='MILES',
            index='Hour',
            columns='DayOfWeek',
            aggfunc='count'
        ).fillna(0)
        
        # Create surface plot
        fig = go.Figure(data=[go.Surface(
            z=ride_matrix.values,
            x=ride_matrix.columns,  # Days
            y=ride_matrix.index,    # Hours
            colorscale='Viridis',
            colorbar=dict(title="Number of Rides"),
            hovertemplate=
            '<b>Day</b>: %{x}<br>' +
            '<b>Hour</b>: %{y}<br>' +
            '<b>Rides</b>: %{z:.0f}<br>'
        )])
        
        fig.update_layout(
            scene=dict(
                xaxis_title='Day of Week',
                yaxis_title='Hour of Day',
                zaxis_title='Number of Rides',
                xaxis=dict(gridcolor='rgba(0,255,128,0.1)', showgrid=True),
                yaxis=dict(gridcolor='rgba(0,255,128,0.1)', showgrid=True),
                zaxis=dict(gridcolor='rgba(0,255,128,0.1)', showgrid=True),
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            template="plotly_dark",
            plot_bgcolor='black',
            paper_bgcolor='black',
            margin=dict(l=0, r=0, b=0, t=30),
            height=600,
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 3D Monthly-Daily-Hourly heatmap
        st.subheader("Monthly Ride Patterns")
        
        # Calculate average rides for each month and hour combination
        monthly_matrix = pd.pivot_table(
            data,
            values='MILES',
            index='Month',
            columns='Hour',
            aggfunc='count'
        ).fillna(0)
        
        # Create 3D bar chart
        x, y = np.meshgrid(monthly_matrix.columns, monthly_matrix.index)
        
        fig = go.Figure(data=[go.Bar3d(
            x=x.flatten(),
            y=y.flatten(),
            z=monthly_matrix.values.flatten(),
            colorscale='Viridis',
            opacity=0.8,
            hovertemplate=
            '<b>Hour</b>: %{x}<br>' +
            '<b>Month</b>: %{y}<br>' +
            '<b>Rides</b>: %{z:.0f}<br>'
        )])
        
        fig.update_layout(
            scene=dict(
                xaxis_title='Hour of Day',
                yaxis_title='Month',
                zaxis_title='Number of Rides',
                xaxis=dict(gridcolor='rgba(0,255,128,0.1)', showgrid=True),
                yaxis=dict(gridcolor='rgba(0,255,128,0.1)', showgrid=True),
                zaxis=dict(gridcolor='rgba(0,255,128,0.1)', showgrid=True),
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            template="plotly_dark",
            plot_bgcolor='black',
            paper_bgcolor='black',
            margin=dict(l=0, r=0, b=0, t=30),
            height=600,
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Custom Query (previously Tab 3)
    with tab4:
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
