import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
from folium.plugins import HeatMap
from database.db_manager import get_all_potholes_df

def show():
    st.title("📊 Live Strategic GIS Dashboard")
    
    df = get_all_potholes_df()
    
    # 1. Metrics
    c1, c2, c3, c4 = st.columns(4)
    total = len(df)
    high_risk = len(df[df['severity'] == 'High']) if total > 0 else 0
    resolved = len(df[df['status'] == 'Resolved']) if total > 0 else 0
    
    c1.metric("Total Detections", total)
    c2.metric("Critical (High Risk)", high_risk)
    c3.metric("Resolved Cases", resolved)
    c4.metric("Pending Audits", total - resolved)
    
    st.divider()
    
    # 2. Map Controls
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        map_style = st.selectbox("🗺️ Map Style", ["Normal Map (OpenStreetMap)", "Dark Mode (CartoDB)", "Satellite View"])
    with col_ctrl2:
        layer_type = st.radio("👁️ Layer View", ["Point Markers", "Heatmap"], horizontal=True)

    # 3. Map & Charts Layout
    col_map, col_chart = st.columns([2, 1])
    
    with col_map:
        st.subheader("📍 Geographic Distribution")
        
        # Configure map tiles based on selection
        tiles = "CartoDB dark_matter"
        attr = None
        if map_style == "Normal Map (OpenStreetMap)":
            tiles = "openstreetmap"
        elif map_style == "Satellite View":
            tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'
            attr = 'Google'
            
        m = folium.Map(location=[21.16, 81.78], zoom_start=11, tiles=tiles, attr=attr)
        
        if total > 0:
            if layer_type == "Heatmap":
                # Plot Heatmap
                heat_data = [[row['latitude'], row['longitude']] for _, row in df.iterrows()]
                HeatMap(heat_data, radius=15, blur=10).add_to(m)
            else:
                # Plot Individual Markers
                for _, r in df.iterrows():
                    color = "red" if r["severity"] == "High" else "orange" if r["severity"] == "Medium" else "green"
                    folium.CircleMarker(
                        location=[r['latitude'], r['longitude']],
                        radius=6, color=color, fill=True, fill_opacity=0.7,
                        popup=f"ID: {r['id']} | {r['severity']}"
                    ).add_to(m)
        
        st_folium(m, width=800, height=450)
        
    with col_chart:
        st.subheader("⚠️ Severity Analysis")
        if total > 0:
            fig = px.pie(df, names='severity', hole=0.6,
                         color_discrete_map={'High':'#ef4444', 'Medium':'#f59e0b', 'Low':'#10b981'})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                              font_color="white", margin=dict(t=20, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available yet.")
            
    # 4. Data Table
    st.divider()
    st.subheader("📋 Recent Detections Log")
    if total > 0:
        st.dataframe(df.head(15), use_container_width=True)
