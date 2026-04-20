# -*- coding: utf-8 -*-
import sqlite3
import os

db_path = r"D:\claw-агент\claw_agent.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add the new column
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN plan_for_tomorrow TEXT DEFAULT ''")
        print("Column 'plan_for_tomorrow' added successfully!")
    except sqlite3.OperationalError as e:
        print(f"Column might already exist or error: {e}")
    
    conn.commit()
    conn.close()
    print("Database updated!")
else:
    print("Database not found!")