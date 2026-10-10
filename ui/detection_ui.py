import streamlit as st
import tempfile
import cv2
import time
from PIL import Image
import plotly.graph_objects as go
from core.detector import PotholeDetector
from database.db_manager import add_pothole

@st.cache_resource
def get_detector_v2():
    return PotholeDetector()

def render_interactive_image(image_path, detections):
    img = Image.open(image_path)
    width, height = img.size
    fig = go.Figure()
    fig.add_layout_image(
        dict(source=img, xref="x", yref="y", x=0, y=height, sizex=width, sizey=height, sizing="stretch", opacity=1, layer="below")
    )
    fig.update_layout(
        xaxis=dict(visible=False, range=[0, width]), yaxis=dict(visible=False, range=[0, height], scaleanchor="x"),
        margin=dict(l=0, r=0, t=0, b=0), hovermode="closest"
    )

    for d in detections:
        x1, y1, x2, y2 = d['bbox']
        sev = d['severity']
        color = "red" if sev == "High" else "orange" if sev == "Medium" else "green"
        py1, py2 = height - y1, height - y2
        cx, cy = (x1 + x2) / 2, (py1 + py2) / 2
        
        fig.add_shape(type="rect", x0=x1, y0=py1, x1=x2, y1=py2, line=dict(color=color, width=3), fillcolor=color, opacity=0.3)
        
        hover_text = f"<b>Severity:</b> {sev}<br><b>Confidence:</b> {d['confidence']*100:.1f}%<br><b>Area:</b> {d['area']:.0f} px"
        fig.add_trace(go.Scatter(
            x=[cx], y=[cy], mode="markers", marker=dict(size=40, color="rgba(0,0,0,0)"),
            hoverinfo="text", hoverlabel=dict(bgcolor=color, font_size=14, font_family="Arial", font_color="white"),
            text=hover_text, showlegend=False
        ))
    return fig

def show():
    st.title("📡 AI Detection Hub (Interactive)")
    st.markdown("Upload road imagery or dashcam footage (.mp4) to detect potholes, classify severity, and automatically log data.")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Upload Media")
        uploaded_file = st.file_uploader("Choose an image or video (JPG, PNG, MP4)", type=['jpg', 'png', 'jpeg', 'mp4'])
        
        if uploaded_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}")
            tfile.write(uploaded_file.read())
            tfile.close()
            
            is_video = uploaded_file.name.endswith('mp4')
            if not is_video:
                st.image(uploaded_file, caption="Original Image")
            else:
                st.video(uploaded_file)
                
            if st.button("Run AI Analysis", type="primary"):
                detector = get_detector_v2()
                
                if not is_video:
                    with st.spinner("Analyzing road surface & EXIF data..."):
                        frame = cv2.imread(tfile.name)
                        # Pass image_path to extract EXIF
                        detections = detector.process_frame(frame, image_path=tfile.name)
                        
                        if detections is not None:
                            st.session_state['last_img_path'] = tfile.name
                            st.session_state['last_detections'] = detections
                            st.success(f"Analysis Complete! Found {len(detections)} pothole(s).")
                else:
                    st.markdown("### 🎥 Live Video Inference")
                    cap = cv2.VideoCapture(tfile.name)
                    st_frame = st.empty() 
                    frame_count = 0
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret: break
                        frame_count += 1
                        if frame_count % 2 != 0: continue
                            
                        detections = detector.process_frame(frame)
                        annotated_frame = detector.draw_glass_boxes(frame, detections)
                        st_frame.image(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
                    cap.release()
                    st.success(f"Video Analysis Complete!")
        else:
            if 'last_detections' in st.session_state: del st.session_state['last_detections']
            if 'last_img_path' in st.session_state: del st.session_state['last_img_path']
    
    with col2:
        st.subheader("Analysis Results")
        if 'last_detections' in st.session_state and 'last_img_path' in st.session_state:
            detections = st.session_state['last_detections']
            
            fig = render_interactive_image(st.session_state['last_img_path'], detections)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            if len(detections) > 0:
                is_real = detections[0].get('is_real_gps', False)
                if not is_real:
                    st.warning("⚠️ No original GPS EXIF found in image. Simulated location applied. (Will not be eligible for Automated Maintenance API)")
                else:
                    st.success("✅ Authentic EXIF GPS Coordinates Extracted!")
                    
                st.markdown("### Detected Hazards")
                for i, d in enumerate(detections):
                    color = "🔴" if d['severity'] == "High" else "🟠" if d['severity'] == "Medium" else "🟢"
                    st.write(f"{color} **Pothole {i+1}**: {d['severity']} (Conf: {d['confidence']*100:.1f}%)")
                
                if st.button("Log to Database", type="primary"):
                    with st.spinner("Logging to DB..."):
                        for d in detections:
                            add_pothole(d['latitude'], d['longitude'], d['severity'], d['is_real_gps'])
                        time.sleep(1)
                        st.success("Successfully logged to Central Database!")
                        del st.session_state['last_detections']
                        del st.session_state['last_img_path']
                        st.rerun()
            else:
                st.success("No potholes detected in this image. Road is clear!")
