import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    layout='wide',
    initial_sidebar_state='collapsed',
    page_title="Ridelytics - Premium Ride Analytics",
    page_icon="R"
)

# Custom CSS for Premium SaaS Look
def set_branding():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&display=swap');
        
        * {
            font-family: 'Cormorant Garamond', serif !important;
        }
        
        /* App Background with premium gradient */
        .stApp {
            background: linear-gradient(135deg, #0A0E1A 0%, #1A1F35 25%, #0F1419 50%, #1A1F35 75%, #0A0E1A 100%) !important;
            background-attachment: fixed !important;
        }
        
        .main {
            background: transparent !important;
            color: #ffffff !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Streamlit default elements to premium dark */
        .stApp > div {
            background: transparent !important;
        }
        
        .block-container {
            background: transparent !important;
            color: #ffffff !important;
            padding: 0 !important;
            margin: 0 !important;
            max-width: none !important;
        }
        
        /* Premium Ridelytics Logo */
        .ridelytics-logo {
            font-family: 'Cinzel', serif !important;
            font-weight: 900 !important;
            font-size: 2.5rem !important;
            background: linear-gradient(135deg, #FFD700, #FFA500, #FFD700) !important;
            background-size: 200% 200% !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            animation: goldGradient 3s ease infinite !important;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.5) !important;
            letter-spacing: 3px !important;
        }
        
        @keyframes goldGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Premium Hero Section */
        .hero-section {
            min-height: 75vh !important;
            background: linear-gradient(135deg, 
                rgba(255, 215, 0, 0.05) 0%, 
                rgba(255, 165, 0, 0.03) 25%, 
                rgba(255, 215, 0, 0.05) 50%, 
                rgba(255, 165, 0, 0.03) 75%, 
                rgba(255, 215, 0, 0.05) 100%) !important;
            position: relative !important;
            overflow: hidden !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 !important;
            border-radius: 30px !important;
            border: 2px solid rgba(255, 215, 0, 0.2) !important;
            backdrop-filter: blur(20px) !important;
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.1),
                0 0 100px rgba(255, 215, 0, 0.1) !important;
        }
        
        .hero-section::before {
            content: '' !important;
            position: absolute !important;
            top: -50% !important;
            left: -50% !important;
            width: 200% !important;
            height: 200% !important;
            background: linear-gradient(45deg, 
                transparent, 
                rgba(255, 215, 0, 0.1), 
                transparent) !important;
            animation: shimmer 3s infinite !important;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .hero-content {
            text-align: center !important;
            z-index: 2 !important;
            max-width: 900px !important;
            padding: 2rem !important;
            position: relative !important;
        }
        
        .hero-title {
            font-family: 'Playfair Display', serif !important;
            font-size: 5rem !important;
            font-weight: 900 !important;
            margin-bottom: 1.5rem !important;
            background: linear-gradient(135deg, #FFD700, #FFA500, #FFD700, #FFA500) !important;
            background-size: 300% 300% !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            animation: premiumGradient 4s ease infinite !important;
            line-height: 1.1 !important;
            text-shadow: 0 0 50px rgba(255, 215, 0, 0.5) !important;
            letter-spacing: 2px !important;
        }
        
        @keyframes premiumGradient {
            0% { background-position: 0% 50%; }
            25% { background-position: 100% 50%; }
            50% { background-position: 100% 100%; }
            75% { background-position: 0% 100%; }
            100% { background-position: 0% 50%; }
        }
        
        .hero-subtitle {
            font-family: 'Cormorant Garamond', serif !important;
            font-size: 1.5rem !important;
            color: rgba(255, 255, 255, 0.9) !important;
            margin-bottom: 2.5rem !important;
            font-weight: 400 !important;
            line-height: 1.7 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }
        
        .hero-cta {
            display: inline-flex !important;
            gap: 1.5rem !important;
            justify-content: center !important;
            flex-wrap: wrap !important;
        }
        
        .cta-button {
            padding: 1.2rem 3rem !important;
            border-radius: 50px !important;
            font-weight: 600 !important;
            text-decoration: none !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            border: none !important;
            cursor: pointer !important;
            font-size: 1.1rem !important;
            position: relative !important;
            overflow: hidden !important;
            font-family: 'Playfair Display', serif !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        .cta-primary {
            background: linear-gradient(135deg, #FFD700, #FFA500) !important;
            color: #0A0E1A !important;
            box-shadow: 
                0 15px 35px rgba(255, 215, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        }
        
        .cta-primary::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: -100% !important;
            width: 100% !important;
            height: 100% !important;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent) !important;
            transition: left 0.5s ease !important;
        }
        
        .cta-primary:hover::before {
            left: 100% !important;
        }
        
        .cta-primary:hover {
            transform: translateY(-5px) scale(1.05) !important;
            box-shadow: 
                0 25px 50px rgba(255, 215, 0, 0.6),
                inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        }
        
        .cta-secondary {
            background: rgba(255, 255, 255, 0.1) !important;
            color: #FFD700 !important;
            border: 2px solid rgba(255, 215, 0, 0.3) !important;
            backdrop-filter: blur(15px) !important;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        }
        
        .cta-secondary:hover {
            background: rgba(255, 215, 0, 0.2) !important;
            border-color: #FFD700 !important;
            transform: translateY(-5px) scale(1.05) !important;
            box-shadow: 
                0 20px 40px rgba(255, 215, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Premium 3D Visualization Container */
        .viz-3d-container {
            height: 500px !important;
            border-radius: 25px !important;
            overflow: hidden !important;
            border: 2px solid rgba(255, 215, 0, 0.2) !important;
            background: linear-gradient(135deg, 
                rgba(255, 215, 0, 0.05), 
                rgba(255, 165, 0, 0.02)) !important;
            position: relative !important;
            margin: 0 !important;
            backdrop-filter: blur(20px) !important;
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.1),
                0 0 50px rgba(255, 215, 0, 0.1) !important;
        }
        
        .viz-3d-container::before {
            content: '' !important;
            position: absolute !important;
            top: -2px !important;
            left: -2px !important;
            right: -2px !important;
            bottom: -2px !important;
            background: linear-gradient(45deg, #FFD700, #FFA500, #FFD700) !important;
            border-radius: 25px !important;
            z-index: -1 !important;
            opacity: 0.3 !important;
        }
        
        /* Enhanced Premium KPI Cards */
        .kpi-card {
            background: linear-gradient(135deg, 
                rgba(255, 215, 0, 0.1), 
                rgba(255, 165, 0, 0.05),
                rgba(255, 215, 0, 0.02)) !important;
            border: 2px solid rgba(255, 215, 0, 0.3) !important;
            border-radius: 25px !important;
            padding: 2rem !important;
            backdrop-filter: blur(20px) !important;
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            height: 100% !important;
            position: relative !important;
            overflow: hidden !important;
            margin: 0 !important;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        }
        
        .kpi-card::before {
            content: '' !important;
            position: absolute !important;
            top: -50% !important;
            left: -50% !important;
            width: 200% !important;
            height: 200% !important;
            background: linear-gradient(45deg, 
                transparent, 
                rgba(255, 215, 0, 0.3), 
                transparent) !important;
            transition: all 0.8s ease !important;
            opacity: 0 !important;
        }
        
        .kpi-card:hover::before {
            opacity: 1 !important;
            animation: cardShimmer 1s ease !important;
        }
        
        @keyframes cardShimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .kpi-card:hover {
            transform: translateY(-10px) scale(1.02) !important;
            box-shadow: 
                0 25px 50px rgba(255, 215, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            border-color: #FFD700 !important;
        }
        
        .kpi-value {
            font-family: 'Playfair Display', serif !important;
            font-size: 3rem !important;
            font-weight: 900 !important;
            color: #FFD700 !important;
            margin: 0 !important;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.5) !important;
            letter-spacing: 1px !important;
        }
        
        .kpi-label {
            font-family: 'Cormorant Garamond', serif !important;
            font-size: 1rem !important;
            color: rgba(255, 255, 255, 0.9) !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 3px !important;
            margin: 0.75rem 0 0 0 !important;
        }
        
        .kpi-change {
            font-family: 'Playfair Display', serif !important;
            font-size: 1rem !important;
            margin-top: 1rem !important;
            font-weight: 600 !important;
        }
        
        .kpi-change.positive {
            color: #00FF88 !important;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5) !important;
        }
        
        .kpi-change.negative {
            color: #FF6B6B !important;
            text-shadow: 0 0 10px rgba(255, 107, 107, 0.5) !important;
        }
        
        /* Hide Streamlit elements */
        .stAppHeader, .stSidebar {
            display: none !important;
        }
        
        /* Premium Streamlit buttons */
        .stButton > button {
            font-family: 'Playfair Display', serif !important;
            background: linear-gradient(135deg, 
                rgba(255, 215, 0, 0.1), 
                rgba(255, 165, 0, 0.05)) !important;
            border: 2px solid rgba(255, 215, 0, 0.3) !important;
            color: #FFD700 !important;
            font-weight: 600 !important;
            padding: 1rem 1.5rem !important;
            border-radius: 15px !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            backdrop-filter: blur(15px) !important;
            font-size: 1.1rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, 
                rgba(255, 215, 0, 0.2), 
                rgba(255, 165, 0, 0.1)) !important;
            border-color: #FFD700 !important;
            color: #FFFFFF !important;
            transform: translateY(-3px) scale(1.05) !important;
            box-shadow: 
                0 15px 35px rgba(255, 215, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Remove all margins and padding */
        .element-container {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stMarkdown {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stPlotlyChart {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Premium glass cards */
        .glass-card {
            background: linear-gradient(135deg, 
                rgba(255, 215, 0, 0.08), 
                rgba(255, 165, 0, 0.04)) !important;
            backdrop-filter: blur(20px) !important;
            border: 2px solid rgba(255, 215, 0, 0.2) !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
            margin: 0 !important;
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Premium Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Playfair Display', serif !important;
            color: #FFFFFF !important;
            margin: 0.5rem 0 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }
        
        h1 {
            font-size: 3rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #FFD700, #FFA500) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.5) !important;
            letter-spacing: 2px !important;
        }
        
        h2 {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            color: #FFD700 !important;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.4) !important;
            letter-spacing: 1px !important;
        }
        
        h3 {
            font-size: 1.7rem !important;
            font-weight: 600 !important;
            color: #FFA500 !important;
            text-shadow: 0 0 15px rgba(255, 165, 0, 0.3) !important;
        }
        
        /* Force all text to be premium */
        p, span, div, label {
            font-family: 'Cormorant Garamond', serif !important;
            color: rgba(255, 255, 255, 0.95) !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Custom Navigation Header
def render_navigation():
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    
    # Simple logo display
    st.markdown("""
        <div style="text-align: center; margin: 0;">
            <div class="ridelytics-logo">
                Ridelytics
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Home", key="nav_home", use_container_width=True):
            st.session_state.current_page = 'Home'
            st.rerun()
    
    with col2:
        if st.button("Analytics", key="nav_analytics", use_container_width=True):
            st.session_state.current_page = 'Analytics'
            st.rerun()
    
    with col3:
        if st.button("Routes", key="nav_routes", use_container_width=True):
            st.session_state.current_page = 'Routes'
            st.rerun()
    
    with col4:
        if st.button("Revenue", key="nav_revenue", use_container_width=True):
            st.session_state.current_page = 'Revenue'
            st.rerun()
    
    with col5:
        if st.button("Insights", key="nav_insights", use_container_width=True):
            st.session_state.current_page = 'Insights'
            st.rerun()

# Custom KPI Card Component
def kpi_card(title, value, change=None, change_type="positive"):
    change_class = "positive" if change_type == "positive" else "negative"
    change_symbol = "↑" if change_type == "positive" else "↓"
    change_color = "#00C853" if change_type == "positive" else "#FF5252"
    
    if change:
        change_html = f'<div class="kpi-change {change_class}">{change_symbol} {change}</div>'
    else:
        change_html = ''
    
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{title}</div>
            {change_html}
        </div>
    """, unsafe_allow_html=True)

# 3D Visualization Functions
def create_3d_scatter_plot():
    df = load_sample_data()
    
    # Create 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=df['rides'],
        y=df['revenue'],
        z=df['avg_wait_time'],
        mode='markers',
        marker=dict(
            size=5,
            color=df['completion_rate'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Completion Rate (%)"),
            opacity=0.8
        ),
        text=[f'Rides: {r}<br>Revenue: ${rev}<br>Wait: {wt:.1f}min' 
              for r, rev, wt in zip(df['rides'], df['revenue'], df['avg_wait_time'])],
        hovertemplate='%{text}<extra></extra>'
    )])
    
    fig.update_layout(
        title="3D Ride Analysis: Rides vs Revenue vs Wait Time",
        scene=dict(
            xaxis_title="Number of Rides",
            yaxis_title="Revenue ($)",
            zaxis_title="Avg Wait Time (min)",
            bgcolor='rgba(0,0,0,0)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF'),
        height=500,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def create_3d_surface_plot():
    df = load_sample_data()
    
    # Create data for surface plot
    hours = sorted(df['timestamp'].dt.hour.unique())
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Create matrix data
    z_data = []
    for day in range(7):
        day_data = df[df['timestamp'].dt.dayofweek == day]
        hourly_avg = []
        for hour in range(24):
            hour_data = day_data[day_data['timestamp'].dt.hour == hour]
            if not hour_data.empty:
                hourly_avg.append(hour_data['rides'].mean())
            else:
                hourly_avg.append(0)
        z_data.append(hourly_avg)
    
    fig = go.Figure(data=[go.Surface(
        z=z_data,
        x=hours,
        y=days,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Average Rides"),
        opacity=0.9
    )])
    
    fig.update_layout(
        title="3D Surface: Weekly Hourly Ride Patterns",
        scene=dict(
            xaxis_title="Hour of Day",
            yaxis_title="Day of Week",
            zaxis_title="Average Rides",
            bgcolor='rgba(0,0,0,0)',
            camera=dict(
                eye=dict(x=1.2, y=1.2, z=0.8)
            )
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF'),
        height=500,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

def create_3d_mesh_plot():
    # Create a 3D mesh visualization for route analysis
    fig = go.Figure()
    
    # Generate mesh data for route efficiency
    x = np.linspace(0, 10, 20)
    y = np.linspace(0, 10, 20)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y) + np.random.normal(0, 0.1, X.shape)
    
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Plasma',
        showscale=True,
        colorbar=dict(title="Route Efficiency"),
        opacity=0.8
    ))
    
    fig.update_layout(
        title="3D Route Efficiency Analysis",
        scene=dict(
            xaxis_title="Distance (mi)",
            yaxis_title="Time (min)",
            zaxis_title="Efficiency Score",
            bgcolor='rgba(0,0,0,0)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF'),
        height=500,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

# Load sample data
@st.cache_data
def load_sample_data():
    # Generate realistic ride data
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', '2024-12-31', freq='H')
    data = {
        'timestamp': dates,
        'rides': np.random.poisson(25, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 24) * 10 + 15,
        'revenue': np.random.normal(45, 15, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 24) * 20 + 50,
        'active_drivers': np.random.randint(50, 200, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 24) * 30 + 100,
        'avg_wait_time': np.random.normal(8, 3, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 24) * 4 + 8,
        'completion_rate': np.random.beta(10, 2, len(dates)) * 100
    }
    
    # Add some realistic patterns
    for i in range(len(data['timestamp'])):
        hour = data['timestamp'][i].hour
        if 7 <= hour <= 9 or 17 <= hour <= 19:  # Rush hours
            data['rides'][i] *= 1.5
            data['revenue'][i] *= 1.4
            data['avg_wait_time'][i] *= 1.3
        elif 22 <= hour or hour <= 5:  # Late night
            data['rides'][i] *= 0.4
            data['revenue'][i] *= 0.5
            data['avg_wait_time'][i] *= 0.7
    
    return pd.DataFrame(data)

# Main App
def main():
    set_branding()
    render_navigation()
    
    # Get current page from session state
    current_page = st.session_state.get('current_page', 'Home')
    
    if current_page == "Home":
        # Premium Hero Section
        st.markdown("""
            <div class="hero-section">
                <div class="hero-content">
                    <h1 class="hero-title">Ridelytics</h1>
                    <p class="hero-subtitle">
                        Transform your ride data into actionable insights with our premium analytics platform. 
                        Real-time visualizations, 3D analysis, and intelligent forecasting at your fingertips.
                    </p>
                    <div class="hero-cta">
                        <div class="cta-button cta-primary">Explore Analytics</div>
                        <div class="cta-button cta-secondary">View Routes</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 3D Visualizations Showcase
        st.markdown('<h2 style="text-align: center; margin: 0;">Advanced 3D Analytics</h2>', unsafe_allow_html=True)
        
        # Display 3D visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="viz-3d-container">', unsafe_allow_html=True)
            fig_3d_scatter = create_3d_scatter_plot()
            st.plotly_chart(fig_3d_scatter, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="viz-3d-container">', unsafe_allow_html=True)
            fig_3d_surface = create_3d_surface_plot()
            st.plotly_chart(fig_3d_surface, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced KPI Cards
        st.markdown('<h2 style="text-align: center; margin: 0;">Performance Metrics</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            kpi_card("Total Rides", "2.4M", "+12.5%", "positive")
        
        with col2:
            kpi_card("Revenue", "$8.7M", "+18.2%", "positive")
        
        with col3:
            kpi_card("Active Drivers", "1,245", "+5.3%", "positive")
        
        with col4:
            kpi_card("Avg Wait Time", "6.2 min", "-8.1%", "positive")
        
        # Additional 3D visualization
        st.markdown('<h2 style="text-align: center; margin: 0;">Route Intelligence</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="viz-3d-container">', unsafe_allow_html=True)
        fig_3d_mesh = create_3d_mesh_plot()
        st.plotly_chart(fig_3d_mesh, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif current_page == "Analytics":
        st.markdown('<h1 style="text-align: center; margin: 0;">Advanced Analytics</h1>', unsafe_allow_html=True)
        
        df = load_sample_data()
        
        # 3D Analytics Showcase
        st.markdown('<h2 style="text-align: center; margin: 0;">3D Predictive Analytics</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="viz-3d-container">', unsafe_allow_html=True)
            fig_3d_scatter = create_3d_scatter_plot()
            st.plotly_chart(fig_3d_scatter, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="viz-3d-container">', unsafe_allow_html=True)
            fig_3d_surface = create_3d_surface_plot()
            st.plotly_chart(fig_3d_surface, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Time series analysis
        st.markdown('<h2 style="text-align: center; margin: 0;">Trend Analysis</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Ride Trends")
            
            # Weekly pattern
            df['day_of_week'] = df['timestamp'].dt.day_name()
            weekly_avg = df.groupby('day_of_week')['rides'].mean().reindex([
                'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
            ])
            
            fig = go.Figure(data=[
                go.Bar(
                    x=weekly_avg.index,
                    y=weekly_avg.values,
                    marker_color='#FFD700'
                )
            ])
            
            fig.update_layout(
                title="Average Rides by Day",
                xaxis_title="Day of Week",
                yaxis_title="Average Rides",
                template='plotly_dark',
                paper_bgcolor='rgba(00,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FFFFFF'),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Peak Hours Analysis")
            
            # Hourly distribution
            hourly_avg = df.groupby(df['timestamp'].dt.hour)['rides'].mean()
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=hourly_avg.index,
                    y=hourly_avg.values,
                    mode='lines+markers',
                    line=dict(color='#FFA500', width=3),
                    fill='tonexty',
                    fillcolor='rgba(255, 165, 0, 0.2)'
                )
            ])
            
            fig.update_layout(
                title="Average Rides by Hour",
                xaxis_title="Hour of Day",
                yaxis_title="Average Rides",
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FFFFFF'),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif current_page == "Routes":
        st.markdown('<h1 style="text-align: center; margin: 0;">Route Intelligence</h1>', unsafe_allow_html=True)
        
        # 3D Route Analysis
        st.markdown('<h2 style="text-align: center; margin: 0;">3D Route Analysis</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="viz-3d-container">', unsafe_allow_html=True)
        fig_3d_mesh = create_3d_mesh_plot()
        st.plotly_chart(fig_3d_mesh, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Route analysis
        st.markdown('<h2 style="text-align: center; margin: 0;">Popular Routes</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Sample route data
        routes = pd.DataFrame({
            'route': ['Downtown → Airport', 'Airport → Downtown', 'City Center → Suburbs', 
                     'University → Downtown', 'Mall → Residential Area'],
            'trips': [1250, 1180, 980, 850, 720],
            'avg_revenue': [45.50, 42.30, 28.70, 22.10, 18.50]
        })
        
        fig = px.scatter(
            routes,
            x='trips',
            y='avg_revenue',
            size='trips',
            hover_name='route',
            title="Route Performance Analysis",
            template='plotly_dark',
            color_discrete_sequence=['#FFD700']
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif current_page == "Revenue":
        st.markdown('<h1 style="text-align: center; margin: 0;">Revenue Analytics</h1>', unsafe_allow_html=True)
        
        df = load_sample_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Revenue Trends")
            
            # Monthly revenue
            df['month'] = df['timestamp'].dt.month
            monthly_revenue = df.groupby('month')['revenue'].sum()
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=monthly_revenue.index,
                    y=monthly_revenue.values,
                    mode='lines+markers',
                    line=dict(color='#00FF88', width=3),
                    fill='tonexty',
                    fillcolor='rgba(0, 255, 136, 0.2)'
                )
            ])
            
            fig.update_layout(
                title="Monthly Revenue Trends",
                xaxis_title="Month",
                yaxis_title="Revenue ($)",
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FFFFFF'),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Revenue Per Ride")
            
            # Revenue per ride analysis
            fig = go.Figure(data=[
                go.Histogram(
                    x=df['revenue'],
                    nbinsx=30,
                    marker_color='#FFD700'
                )
            ])
            
            fig.update_layout(
                title="Revenue Distribution Per Ride",
                xaxis_title="Revenue ($)",
                yaxis_title="Frequency",
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FFFFFF'),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif current_page == "Insights":
        st.markdown('<h1 style="text-align: center; margin: 0;">Business Insights</h1>', unsafe_allow_html=True)
        
        # Insights cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Key Findings")
            
            insights = [
                "Peak demand hours are 7-9 AM and 5-7 PM",
                "Revenue increases by 35% during rush hours",
                "Average wait time reduced by 15% this month",
                "Airport routes generate highest revenue per ride",
                "Weekend demand 40% higher than weekdays"
            ]
            
            for insight in insights:
                st.markdown(f"• {insight}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Recommendations")
            
            recommendations = [
                "Increase driver availability during peak hours",
                "Implement dynamic pricing for rush hours",
                "Launch mobile app for faster booking",
                "Focus marketing on high-revenue routes",
                "Optimize dispatch algorithm for efficiency"
            ]
            
            for rec in recommendations:
                st.markdown(f"• {rec}")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
