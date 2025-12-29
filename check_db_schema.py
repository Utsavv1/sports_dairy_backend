import sqlite3
import sys

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

try:
    conn = sqlite3.connect('player_app.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in database: {[t[0] for t in tables]}")
    
    # Check users table schema
    if ('users',) in tables:
        cursor.execute("PRAGMA table_info(users);")
        columns = cursor.fetchall()
        print(f"\nUsers table columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
    print("\nDatabase check complete!")
    
except Exception as e:
    print(f"Error: {e}")

