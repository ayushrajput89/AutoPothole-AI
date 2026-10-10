import streamlit as st
import os
import sys

# Add current directory to path so imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import init_db, migrate_from_csv
from ui import dashboard, detection_ui, reports_ui

st.set_page_config(page_title="AutoPothole AI", layout="wide", initial_sidebar_state="expanded")

# Initialize database on startup
@st.cache_resource
def setup_database_v2():
    init_db()
    migrate_from_csv()
setup_database_v2()

# Custom CSS for dark professional theme
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #1e293b; border-right: 2px solid #3b82f6; }
    h1, h2, h3, p { color: #f8fafc !important; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #3b82f6; }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h1 style='color:#3b82f6;'>🛡️ Road Safety AI</h1>", unsafe_allow_html=True)
st.sidebar.markdown("Autonomous Pothole Intelligence")
st.sidebar.markdown("---")

menu = st.sidebar.radio("NAVIGATION", ["📊 Live GIS Dashboard", "📡 AI Detection Hub", "📄 Maintenance Reports"])

st.sidebar.markdown("---")
st.sidebar.info("System Status: ACTIVE ✅\n\nDatabase: SQLite Connected")

if menu == "📊 Live GIS Dashboard":
    dashboard.show()
elif menu == "📡 AI Detection Hub":
    detection_ui.show()
elif menu == "📄 Maintenance Reports":
    reports_ui.show()
