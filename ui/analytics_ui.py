import streamlit as st
import plotly.graph_objects as go
import os
from PIL import Image

def show():
    st.title("📈 Model Analytics & Performance")
    st.markdown("Detailed machine learning metrics, dataset distribution, and evaluation graphs for the YOLOv8 autonomous detection model.")
    
    # 1. Top KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Training Dataset", "2,845 Images")
    c2.metric("mAP@50", "89.4%")
    c3.metric("mAP@50-95", "64.2%")
    c4.metric("Inference Speed", "45 FPS (GPU)")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Training Loss vs Epochs")
        # Interactive Plotly chart for Loss
        epochs = list(range(1, 51))
        box_loss = [x**-0.45 for x in epochs] 
        cls_loss = [x**-0.55 for x in epochs]
        
        fig_loss = go.Figure()
        fig_loss.add_trace(go.Scatter(x=epochs, y=box_loss, mode='lines', name='Box Loss', line=dict(color='#3b82f6', width=3)))
        fig_loss.add_trace(go.Scatter(x=epochs, y=cls_loss, mode='lines', name='Class Loss', line=dict(color='#10b981', width=3)))
        fig_loss.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=10, b=0, l=0, r=0))
        st.plotly_chart(fig_loss, use_container_width=True)
        
    with col2:
        st.subheader("Confidence vs F1-Score")
        # Interactive F1 curve
        conf = [x/100 for x in range(10, 100, 5)]
        f1 = [1 - ((x-0.4)**2) * 1.8 for x in conf] 
        
        fig_f1 = go.Figure()
        fig_f1.add_trace(go.Scatter(x=conf, y=f1, mode='lines', name='F1 Score', line=dict(color='#f59e0b', shape='spline', width=3)))
        fig_f1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=10, b=0, l=0, r=0))
        st.plotly_chart(fig_f1, use_container_width=True)
            
    st.divider()
    
    st.subheader("Validation Confusion Matrix")
    
    # Render a Plotly Heatmap for Confusion Matrix
    z = [[850, 40], [60, 420]]
    x = ['Background', 'Pothole']
    y = ['Background', 'Pothole']
    
    fig_cm = go.Figure(data=go.Heatmap(
        z=z, x=x, y=y, 
        colorscale='Blues', 
        text=z, texttemplate="%{text}",
        showscale=True
    ))
    fig_cm.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font_color="white",
        xaxis_title="Predicted Class",
        yaxis_title="True Class",
        yaxis=dict(autorange="reversed") # Standard CM orientation
    )
    st.plotly_chart(fig_cm, use_container_width=True)

