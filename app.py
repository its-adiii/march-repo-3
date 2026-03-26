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
            margin: 0 !important;
            padding: 0 !important;
            box-sizing: border-box !important;
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
            height: auto !important;
            min-height: 400px !important;
            max-height: 600px !important;
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
        
        .viz-3d-container:empty {
            display: none !important;
        }
        
        .viz-3d-container:has(> :empty) {
            display: none !important;
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
        
        /* Remove all Streamlit margins and padding */
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
        
        /* Remove blank spaces from all containers */
        .block-container {
            margin: 0 !important;
            padding: 0 !important;
            max-width: none !important;
        }
        
        .main > div {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove gaps between elements */
        div[data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        
        div[data-testid="stHorizontalBlock"] {
            gap: 0 !important;
        }
        
        /* Remove spacing from columns */
        .stColumns > div {
            gap: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Remove all form spacing */
        .stForm {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove button spacing */
        .stButton {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove header spacing */
        .stHeader {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove subheader spacing */
        .stSubheader {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove caption spacing */
        .stCaption {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove text element spacing */
        .stText {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove all gaps */
        .streamlit-container {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove gaps in vertical blocks */
        .element-container > div {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove all whitespace */
        .css-1d391kg {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .css-1lcbmhc {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .css-1y4p8pa {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove ALL Streamlit spacing */
        div[class*="css-"] {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove gaps from all containers */
        [data-testid="stVerticalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Remove spacing from all elements */
        * {
            box-sizing: border-box !important;
        }
        
        /* Force tight layout */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        
        /* Remove all internal spacing */
        .element-container > div > div {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove column gaps completely */
        .stColumns > div > div {
            padding: 0 !important;
            margin: 0 !important;
            gap: 0 !important;
        }
        
        /* Remove iframe spacing */
        iframe {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove plotly spacing */
        .plotly-graph-div {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* SUPER AGGRESSIVE - Remove ALL spacing */
        div[style*="padding"] {
            padding: 0 !important;
        }
        
        div[style*="margin"] {
            margin: 0 !important;
        }
        
        /* Remove all flex gaps */
        div[style*="gap"] {
            gap: 0 !important;
        }
        
        /* Target all Streamlit elements */
        [data-testid] {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove spacing from nested elements */
        div > div > div {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Force zero spacing on everything */
        .main > div > div > div {
            margin: 0 !important;
            padding: 0 !important;
            gap: 0 !important;
        }
        
        /* Remove all container spacing */
        .streamlit-expanderHeader {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .streamlit-expanderContent {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove spacing from all child elements */
        * > * {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Force tight layout for all containers */
        .element-container .stMarkdown {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove all white space */
        br {
            display: none !important;
        }
        
        /* Remove paragraph spacing */
        p {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove heading spacing */
        h1, h2, h3, h4, h5, h6 {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove list spacing */
        ul, ol, li {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove all spacing from main content area */
        .main .element-container {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Force zero spacing on all nested elements */
        div[data-testid="element-container"] {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove spacing from all streamlit components */
        [data-baseweb="markdown"] {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove all gaps and margins */
        .st-emotion-cache-1t3x2f {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .st-emotion-cache-1l6m5o {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .st-emotion-cache-1v0mbd {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Target all possible CSS classes */
        div[class*="st-"] {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        div[class*="emotion-"] {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Remove spacing from all elements with data attributes */
        [data-testid*="st"] {
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
        <script>
        // Remove all spacing after page loads
        document.addEventListener('DOMContentLoaded', function() {
            // Remove all margins and padding
            const allElements = document.querySelectorAll('*');
            allElements.forEach(el => {
                el.style.margin = '0';
                el.style.padding = '0';
                el.style.gap = '0';
            });
            
            // Remove all Streamlit spacing
            const streamlitElements = document.querySelectorAll('[data-testid]');
            streamlitElements.forEach(el => {
                el.style.margin = '0';
                el.style.padding = '0';
                el.style.gap = '0';
            });
            
            // Remove spacing from all containers
            const containers = document.querySelectorAll('.element-container, .block-container, .stMarkdown, .stPlotlyChart');
            containers.forEach(el => {
                el.style.margin = '0';
                el.style.padding = '0';
                el.style.gap = '0';
            });
            
            // Remove all line breaks
            const breaks = document.querySelectorAll('br');
            breaks.forEach(el => el.remove());
            
            // Hide empty containers
            const emptyContainers = document.querySelectorAll('.viz-3d-container:empty, .glass-card:empty, .element-container:empty');
            emptyContainers.forEach(el => {
                el.style.display = 'none';
            });
            
            // Force tight layout every 100ms
            setInterval(() => {
                const elements = document.querySelectorAll('*');
                elements.forEach(el => {
                    el.style.margin = '0';
                    el.style.padding = '0';
                    el.style.gap = '0';
                });
                
                // Hide empty containers continuously
                const emptyEls = document.querySelectorAll('.viz-3d-container:empty, .glass-card:empty');
                emptyEls.forEach(el => {
                    if (el.children.length === 0 || el.textContent.trim() === '') {
                        el.style.display = 'none';
                    }
                });
            }, 100);
        });
        </script>
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
        
        # Only render 3D container if we have data
        with st.container():
            st.markdown('<div class="viz-3d-container">', unsafe_allow_html=True)
            fig_3d_mesh = create_3d_mesh_plot()
            st.plotly_chart(fig_3d_mesh, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Route analysis
        st.markdown('<h2 style="text-align: center; margin: 0;">Popular Routes</h2>', unsafe_allow_html=True)
        
        with st.container():
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
        st.markdown('<h1 style="text-align: center; margin: 0;">Business Intelligence</h1>', unsafe_allow_html=True)
        
        # Load data for insights
        df = load_sample_data()
        
        # Mock data function
        def get_mock_data():
            return {
                'hours': ['12AM', '3AM', '6AM', '9AM', '12PM', '3PM', '6PM', '9PM'],
                'demand': [20, 15, 35, 65, 85, 75, 40, 25],
                'routes': ['Downtown → Airport', 'Airport → Downtown', 'City Center → Suburbs', 
                         'University → Downtown', 'Mall → Residential'],
                'route_revenue': [45.50, 42.30, 28.70, 22.10, 18.50],
                'trips': [1250, 1180, 980, 850, 720]
            }
        
        mock_data = get_mock_data()
        
        # Top Metrics KPI Cards with Delta Indicators
        st.markdown('<h2 style="text-align: center; margin: 0;">Performance Metrics</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="kpi-card" style="position: relative; overflow: hidden; text-align: center;">
                    <div class="kpi-value">2.4M</div>
                    <div class="kpi-label">Total Rides</div>
                    <div class="kpi-change positive">↑ +12.5%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="kpi-card" style="position: relative; overflow: hidden; text-align: center;">
                    <div class="kpi-value">$8.7M</div>
                    <div class="kpi-label">Revenue</div>
                    <div class="kpi-change positive">↑ +35%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="kpi-card" style="position: relative; overflow: hidden; text-align: center;">
                    <div class="kpi-value">6.2 min</div>
                    <div class="kpi-label">Avg Wait Time</div>
                    <div class="kpi-change positive">↓ -15%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="kpi-card" style="position: relative; overflow: hidden; text-align: center;">
                    <div class="kpi-value">40%</div>
                    <div class="kpi-label">Weekend Demand</div>
                    <div class="kpi-change positive">↑ +40%</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Peak Demand Radial Bar Chart
        st.markdown('<h2 style="text-align: center; margin: 0;">Peak Demand Analysis</h2>', unsafe_allow_html=True)
        
        # Create simple Bar Chart for Peak Demand
        fig_peak = go.Figure(data=[
            go.Bar(
                x=mock_data['hours'],
                y=mock_data['demand'],
                marker_color='#FFD700',
                text=mock_data['demand'],
                textposition='auto',
                textfont=dict(color='white')
            )
        ])
        
        fig_peak.update_layout(
            template='plotly_dark',
            paper_bgcolor='#00122e',
            plot_bgcolor='#00122e',
            font=dict(color='white', size=12),
            title=dict(text='Peak Demand Analysis', font=dict(color='#FFD700', size=16)),
            xaxis=dict(
                title="Time of Day",
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                title="Demand Level",
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        st.plotly_chart(fig_peak, use_container_width=True)
        
        # Airport Performance Bar Chart
        st.markdown('<h2 style="text-align: center; margin: 0;">Airport Route Performance</h2>', unsafe_allow_html=True)
        
        fig_airport = go.Figure(data=[
            go.Bar(
                x=mock_data['routes'],
                y=mock_data['route_revenue'],
                marker=dict(
                    color=mock_data['route_revenue'],
                    colorscale=[[0, '#00122e'], [0.5, '#FFA500'], [1, '#FFD700']],
                    showscale=True,
                    colorbar=dict(title="Revenue ($)", tickfont=dict(color='white'))
                ),
                text=[f"${rev:.2f}" for rev in mock_data['route_revenue']],
                textposition='auto',
                textfont=dict(color='white')
            )
        ])
        
        fig_airport.update_layout(
            template='plotly_dark',
            paper_bgcolor='#00122e',
            plot_bgcolor='#00122e',
            font=dict(color='white', size=12),
            title=dict(text='Airport Route Performance', font=dict(color='#FFD700', size=16)),
            xaxis=dict(
                title="Routes",
                titlefont=dict(color='white'),
                tickfont=dict(color='white'),
                tickangle=45
            ),
            yaxis=dict(
                title="Average Revenue per Ride ($)",
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            height=400,
            margin=dict(l=0, r=0, t=40, b=100)
        )
        
        st.plotly_chart(fig_airport, use_container_width=True)
        
        # Revenue Heatmap
        st.markdown('<h2 style="text-align: center; margin: 0;">Revenue Heatmap</h2>', unsafe_allow_html=True)
        
        # Create heatmap data
        hours = list(range(24))
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        heatmap_data = []
        
        for day in range(7):
            day_data = []
            for hour in range(24):
                # Simulate realistic revenue patterns
                base_revenue = 500 + np.random.normal(0, 100)
                if 7 <= hour <= 9 or 17 <= hour <= 19:  # Peak hours
                    base_revenue *= 2.5
                elif day >= 5:  # Weekend
                    base_revenue *= 1.4
                day_data.append(max(100, base_revenue))
            heatmap_data.append(day_data)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=hours,
            y=days,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Revenue ($)", tickfont=dict(color='white')),
            hovertemplate='Hour: %{x}<br>Day: %{y}<br>Revenue: $%{z:.2f}<extra></extra>'
        ))
        
        fig_heatmap.update_layout(
            template='plotly_dark',
            paper_bgcolor='#00122e',
            plot_bgcolor='#00122e',
            font=dict(color='white', size=12),
            title=dict(text='Revenue Heatmap', font=dict(color='#FFD700', size=16)),
            xaxis=dict(
                title="Hour of Day",
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                title="Day of Week",
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Weekend vs Weekday Comparison
        st.markdown('<h2 style="text-align: center; margin: 0;">Weekend vs Weekday Analysis</h2>', unsafe_allow_html=True)
        
        fig_comparison = go.Figure()
        
        # Add weekday data
        fig_comparison.add_trace(go.Bar(
            name='Weekday',
            x=days[:5],
            y=[120, 115, 130, 125, 140],
            marker_color='#FFA500',
            text=[120, 115, 130, 125, 140],
            textposition='auto',
            textfont=dict(color='white')
        ))
        
        # Add weekend data
        fig_comparison.add_trace(go.Bar(
            name='Weekend',
            x=days[5:],
            y=[180, 200],
            marker_color='#FFD700',
            text=[180, 200],
            textposition='auto',
            textfont=dict(color='white')
        ))
        
        fig_comparison.update_layout(
            template='plotly_dark',
            paper_bgcolor='#00122e',
            plot_bgcolor='#00122e',
            font=dict(color='white', size=12),
            title=dict(text='Weekend vs Weekday Analysis', font=dict(color='#FFD700', size=16)),
            xaxis=dict(
                title="Day of Week",
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                title="Average Demand",
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            height=300,
            margin=dict(l=0, r=0, t=40, b=0),
            barmode='group'
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Actionable Recommendation Tiles
        st.markdown('<h2 style="text-align: center; margin: 0;">Strategic Recommendations</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="glass-card" style="cursor: pointer; transition: all 0.3s ease; position: relative; overflow: hidden; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">⚡</div>
                    <h3 style="color: #FFD700; margin: 0.5rem 0;">Dynamic Pricing</h3>
                    <p style="opacity: 0.9; margin: 0;">Implement surge pricing during peak hours to increase revenue by 25%</p>
                    <div style="margin-top: 1rem;">
                        <span style="background: linear-gradient(135deg, #FFD700, #FFA500); color: #0A0E1A; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                            Simulate Impact
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="glass-card" style="cursor: pointer; transition: all 0.3s ease; position: relative; overflow: hidden; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">🚗</div>
                    <h3 style="color: #FFA500; margin: 0.5rem 0;">Driver Optimization</h3>
                    <p style="opacity: 0.9; margin: 0;">Optimize driver allocation algorithms to reduce wait times by 20%</p>
                    <div style="margin-top: 1rem;">
                        <span style="background: linear-gradient(135deg, #FFD700, #FFA500); color: #0A0E1A; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                            Simulate Impact
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
