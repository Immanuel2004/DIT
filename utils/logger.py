import logging
from datetime import datetime
import pandas as pd
from db import get_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DynamicImpactTool")

def log_event(event_type, username):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (action, username, timestamp) VALUES (%s, %s, %s)",
            (event_type, username, datetime.now())
        )
        conn.commit()
        cursor.close()
        conn.close()

def get_logs():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, action, username, timestamp FROM logs ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=["ID", "Action", "Username", "Timestamp"])
        cursor.close()
        conn.close()
        return df
    return None
