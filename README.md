# AutoPothole AI: Autonomous Road Safety & Maintenance System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-yellow.svg)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://autopothole-ai.streamlit.app)

## 🌐 Live Demo
🔗 **Experience the Live Web App:** [https://autopothole-ai.streamlit.app](https://autopothole-ai.streamlit.app)  
*(Deployed on Streamlit Community Cloud)*

## 📌 Overview
Large potholes on state and national highways cause daily accidents and vehicle damage. Traditional detection relies on manual inspection rounds or citizen complaints, both of which are slow and incomplete. 

**AutoPothole AI** is an end-to-end computer vision pipeline and strategic GIS dashboard designed to autonomously detect potholes on highway stretches, geolocate them, classify their severity, and automatically generate actionable maintenance reports. 

## 🚀 Key Features

* **🧠 Advanced Computer Vision Engine:** Utilizes a custom-trained YOLOv8 model to detect surface cracks and potholes in real-time from dashcam or drone footage.
* **📏 Smart Severity Classification:** Automatically categorizes defects into `Low`, `Medium`, or `High` severity based on the bounding box area and defect density.
* **📍 EXIF Geotagging Extraction:** Seamlessly extracts real-world GPS coordinates directly from the image metadata. If GPS data is stripped, it flags the detection as simulated to prevent false automation.
* **🗺️ Live Strategic GIS Dashboard:** A premium, interactive dashboard built with Streamlit, Plotly, and Folium. It visualizes defect clusters using Point Markers and Heatmaps.
* **📊 Model Analytics & KPIs:** Embedded evaluation charts displaying 89.4% mAP@50, 45 FPS inference speeds, loss curves, and validation confusion matrices.
* **🤖 Automated API Mockup & PDF Generation:** Eliminates the need for manual data entry. High-severity detections trigger an automated API payload generation and create official, formatted PDF Maintenance Tickets for Road Authorities.

## 📂 System Architecture

```text
pothole_ai/
├── core/
│   ├── detector.py          # YOLOv8 inference, EXIF extraction, glass-box rendering
│   └── report_generator.py  # FPDF2 logic for automated Maintenance Ticket PDF generation
├── database/
│   ├── db_manager.py        # SQLite schema and query logic
│   └── pothole_ai.db        # Live local database 
├── ui/
│   ├── dashboard.py         # Folium GIS Maps & Analytics
│   ├── detection_ui.py      # Plotly interactive Image/Video processing Hub
│   ├── reports_ui.py        # Automated API triggering and PDF Downloads
│   └── analytics_ui.py      # Precision, Loss Curves, and Confusion Matrix
├── weights/
│   └── best.pt              # Custom trained YOLOv8 pothole detection weights
├── assets/                  # CSS, Fonts, and generated PDF reports
├── packages.txt             # Linux system dependencies for cloud deployment
├── requirements.txt         # Python library dependencies
├── yolov8n.pt               # Fallback YOLO weights
└── main_app.py              # Main Streamlit application entry point
```

## 💻 Tech Stack
* **Deep Learning:** Ultralytics YOLOv8, OpenCV (Computer Vision logic)
* **Frontend/UI:** Streamlit, Plotly (Interactive visuals), Folium (GIS mapping)
* **Backend:** SQLite (Data persistence)
* **Utilities:** Pillow (EXIF parsing), FPDF2 (PDF Report Generation)

## 🛠️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ayushrajput89/AutoPothole-AI.git
   cd AutoPothole-AI
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure you have PyTorch installed according to your system's CUDA configuration for optimal YOLO performance).*

3. **Run the Dashboard:**
   ```bash
   streamlit run main_app.py
   ```

4. **Workflow:**
   * Navigate to the **AI Detection Hub**.
   * Upload an Image or `.mp4` video.
   * Run Analysis to see the Interactive Plotly bounding boxes (Images) or Glass-effect inference (Video).
   * Log the data to the database.
   * Go to **Maintenance Reports** to trigger the API or download the generated PDF Ticket.

## 📈 Future Roadmap
- [ ] Implement deep-sort tracking to prevent duplicate logging of the same pothole in continuous video streams.
- [ ] Stereo-camera depth estimation for true 3D volume severity scoring.
- [ ] "Loop Closure" module to process contractor repair evidence (post-repair photos) to automatically close tickets.




