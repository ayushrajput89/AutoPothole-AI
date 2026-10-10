import streamlit as st
import pandas as pd
import json
import time
import os
from database.db_manager import get_all_potholes_df
from core.report_generator import generate_pdf_report

def show():
    st.title("📄 Automated Maintenance API & Reports")
    st.markdown("This module simulates the automated API trigger to City Maintenance Portals and generates official PDF Maintenance Tickets.")
    
    df = get_all_potholes_df()
    
    if df.empty:
        st.info("No detections available to generate reports.")
        return
        
    st.subheader("Pending API Submissions (High Severity)")
    
    # Filter High severity that are "Detected" AND have real GPS
    # Note: is_real_gps comes back as boolean from our db_manager
    pending_df = df[(df['severity'] == 'High') & (df['status'] == 'Detected')]
    
    real_gps_pending = pending_df[pending_df['is_real_gps'] == True]
    fake_gps_pending = pending_df[pending_df['is_real_gps'] == False]
    
    if not fake_gps_pending.empty:
        st.warning(f"⚠️ {len(fake_gps_pending)} High-severity potholes were detected without real EXIF GPS data. They have been logged for internal analytics but are NOT eligible for automated official maintenance ticket filing.")
    
    if real_gps_pending.empty:
        st.success("All verified High Severity potholes have been processed or none exist.")
    else:
        st.dataframe(real_gps_pending[['id', 'latitude', 'longitude', 'timestamp']])
        
        selected_id = st.selectbox("Select Verified Pothole ID to process API filing", real_gps_pending['id'].tolist())
        target_row = real_gps_pending[real_gps_pending['id'] == selected_id].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Trigger Automated Maintenance API", type="primary"):
                with st.spinner("Connecting to State Maintenance Portal API..."):
                    time.sleep(2) # Simulate network delay
                    
                    payload = {
                        "ticket_id": target_row['id'],
                        "location": {
                            "lat": target_row['latitude'],
                            "lon": target_row['longitude']
                        },
                        "department": "Road Maintenance Authority",
                        "priority": "Urgent",
                        "description": "AI detected High severity pothole on highway segment.",
                        "timestamp": target_row['timestamp']
                    }
                    
                    st.success(f"API Request Successful (Status 201 Created) - Ref: MAINT-{target_row['id'][:4].upper()}")
                    
                    st.markdown("### 📤 Simulated API Payload Sent:")
                    st.json(json.dumps(payload, indent=4))
                    
        with col2:
            st.markdown("### 📥 Official PDF Report")
            # Generate PDF on the fly
            pdf_path = generate_pdf_report(target_row.to_dict())
            
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download Official Maintenance Report (PDF)",
                    data=pdf_file,
                    file_name=f"Maintenance_Ticket_{target_row['id']}.pdf",
                    mime="application/pdf"
                )
                
    st.divider()
    
    st.subheader("Resolution & Audit")
    st.markdown("Here contractors can upload repair evidence for the AI to audit.")
    st.info("Feature: 'Loop Closure' allows re-running the Detection AI on contractor photos to verify repair before closing the ticket.")
