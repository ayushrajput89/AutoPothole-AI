import os
from fpdf import FPDF
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_pdf_report(pothole_data, output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(BASE_DIR, "assets", "reports")
    os.makedirs(output_dir, exist_ok=True)
    
    ticket_id = pothole_data.get('id', 'N/A')
    pdf_filename = os.path.join(output_dir, f"Maintenance_Ticket_{ticket_id}.pdf")
    
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AUTONOMOUS POTHOLE INTELLIGENCE", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Road Maintenance Authority - Maintenance Ticket", ln=True, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(10)
    
    # 2. Ticket Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, txt="Ticket ID:", border=0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, txt=f"MAINT-{ticket_id.upper()}", border=0, ln=True)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, txt="Date Generated:", border=0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, txt=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), border=0, ln=True)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, txt="Reported By:", border=0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, txt="Autonomous AI Drone/Dashcam System", border=0, ln=True)
    pdf.ln(5)
    
    # 3. Hazard Details
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Hazard Details", ln=True)
    pdf.line(10, 80, 50, 80)
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, txt="Severity Level:", border=0)
    
    # Color code severity
    if pothole_data.get('severity') == "High":
        pdf.set_text_color(255, 0, 0) # Red
    elif pothole_data.get('severity') == "Medium":
        pdf.set_text_color(255, 165, 0) # Orange
    else:
        pdf.set_text_color(0, 128, 0) # Green
        
    pdf.cell(100, 10, txt=str(pothole_data.get('severity', 'Unknown')).upper(), border=0, ln=True)
    pdf.set_text_color(0, 0, 0) # Reset to black
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, txt="Latitude:", border=0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, txt=str(pothole_data.get('latitude', 'Unknown')), border=0, ln=True)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, txt="Longitude:", border=0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, txt=str(pothole_data.get('longitude', 'Unknown')), border=0, ln=True)
    pdf.ln(10)
    
    # 4. Action Request
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Requested Action:", ln=True)
    pdf.set_font("Arial", '', 12)
    action_text = "This surface defect has been automatically classified as a risk to road safety. Please dispatch an inspection/repair team to the coordinated location."
    pdf.multi_cell(0, 10, txt=action_text)
    
    # Save PDF
    pdf.output(pdf_filename)
    return pdf_filename
