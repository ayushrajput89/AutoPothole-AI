import cv2
import numpy as np
import os
import random
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from ultralytics import YOLO

def get_exif_data(image_path):
    """ Extract EXIF data from image """
    exif_data = {}
    try:
        image = Image.open(image_path)
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]
                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
    except Exception:
        pass
    return exif_data

def convert_to_degrees(value):
    """ Convert GPS coordinates format to float degrees """
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def extract_gps(image_path):
    """ Extracts decimal coordinates if available """
    exif = get_exif_data(image_path)
    if "GPSInfo" in exif:
        gps_info = exif["GPSInfo"]
        try:
            lat = convert_to_degrees(gps_info["GPSLatitude"])
            if gps_info["GPSLatitudeRef"] != "N":
                lat = 0 - lat
            lon = convert_to_degrees(gps_info["GPSLongitude"])
            if gps_info["GPSLongitudeRef"] != "E":
                lon = 0 - lon
            return lat, lon, True
        except Exception:
            pass
    
    # Simulated default coordinates as fallback
    lat = 21.161 + random.uniform(-0.01, 0.01)
    lon = 81.782 + random.uniform(-0.01, 0.01)
    return lat, lon, False

class PotholeDetector:
    def __init__(self, model_path="E:/pothole_ai/runs/detect/train/weights/best.pt"):
        if not os.path.exists(model_path):
            model_path = "E:/pothole_ai/yolov8n.pt"
        self.model = YOLO(model_path)
    
    def classify_severity(self, area):
        if area > 10000:
            return "High"
        elif area > 5000:
            return "Medium"
        return "Low"

    def process_frame(self, frame, image_path=None):
        """ Runs YOLO on a single frame. If image_path is provided, extracts EXIF GPS. """
        results = self.model.predict(frame, conf=0.3, verbose=False)
        detections = []
        
        # Determine GPS for this frame/image
        if image_path:
            lat, lon, is_real = extract_gps(image_path)
        else:
            # Video frames: simulate for now
            lat = 21.161 + random.uniform(-0.01, 0.01)
            lon = 81.782 + random.uniform(-0.01, 0.01)
            is_real = False
            
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                area = (x2 - x1) * (y2 - y1)
                
                severity = self.classify_severity(area)
                
                detections.append({
                    "severity": severity,
                    "latitude": lat,
                    "longitude": lon,
                    "is_real_gps": is_real,
                    "bbox": [x1, y1, x2, y2],
                    "confidence": conf,
                    "area": area
                })
        return detections

    def draw_glass_boxes(self, img, detections):
        """ Draws modern, translucent glass-effect boxes for video streams """
        overlay = img.copy()
        
        for d in detections:
            x1, y1, x2, y2 = map(int, d['bbox'])
            severity = d['severity']
            
            if severity == "High": color = (0, 0, 255) 
            elif severity == "Medium": color = (0, 165, 255) 
            else: color = (0, 255, 0) 
                
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
            
        alpha = 0.35  
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        
        for d in detections:
            x1, y1, x2, y2 = map(int, d['bbox'])
            severity = d['severity']
            conf = d['confidence']
            
            if severity == "High": color = (0, 0, 255) 
            elif severity == "Medium": color = (0, 165, 255) 
            else: color = (0, 255, 0)
                
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            
            label = f"{severity} ({conf*100:.0f}%)"
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.5, 1)
            cv2.rectangle(img, (x1, y1 - h - 10), (x1 + w + 10, y1), color, -1)
            cv2.putText(img, label, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
            
        return img
