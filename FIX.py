#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os

db_path = "D:/claw-агент/claw_agent.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN plan_for_tomorrow TEXT DEFAULT ''")
        print("Column added!")
    except:
        print("Column may already exist")
    
    conn.commit()
    conn.close()
    print("Done!")
else:
    print("DB not found:", db_path)

input("Press Enter...")