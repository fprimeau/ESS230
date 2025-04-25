import sqlite3
import os
from datetime import datetime

def init_database(download_dir):
    """Initialize SQLite database for tracking WOA downloads"""
    db_path = os.path.join(download_dir, 'downloads.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS downloads
                 (filename TEXT PRIMARY KEY, 
                  variable TEXT,
                  download_date TEXT)''')
    conn.commit()
    conn.close()

def record_download(download_dir, filename, variable):
    """Record a new download in the database"""
    db_path = os.path.join(download_dir, 'downloads.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO downloads 
                 VALUES (?, ?, ?)''',
                 (filename, variable, datetime.now().strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()

def get_download_date(download_dir, variable):
    """Get the download date for a specific variable"""
    db_path = os.path.join(download_dir, 'downloads.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''SELECT download_date FROM downloads 
                 WHERE variable = ? 
                 ORDER BY download_date DESC LIMIT 1''', (variable,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None