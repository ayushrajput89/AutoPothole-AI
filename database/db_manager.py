import sqlite3
import pandas as pd
import os
from datetime import datetime
import uuid

DB_PATH = 'E:/pothole_ai/database/pothole_ai.db'

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create Potholes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS potholes (
            id TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL,
            severity TEXT,
            status TEXT,
            is_real_gps INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Grievances table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grievances (
            ticket_id TEXT PRIMARY KEY,
            pothole_id TEXT,
            status TEXT,
            reference_no TEXT,
            filed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(pothole_id) REFERENCES potholes(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_pothole(latitude, longitude, severity, is_real_gps=0, status="Detected"):
    conn = get_connection()
    cursor = conn.cursor()
    pothole_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO potholes (id, latitude, longitude, severity, status, is_real_gps, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (pothole_id, latitude, longitude, severity, status, int(is_real_gps), timestamp))
    conn.commit()
    conn.close()
    return pothole_id

def get_all_potholes_df():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM potholes ORDER BY timestamp DESC", conn)
    conn.close()
    # Convert integer boolean back to boolean type for pandas
    if 'is_real_gps' in df.columns:
        df['is_real_gps'] = df['is_real_gps'].astype(bool)
    return df

def migrate_from_csv():
    # Deprecated for now since we wiped old data
    pass

if __name__ == "__main__":
    init_db()
    print("Database ready with is_real_gps schema!")
