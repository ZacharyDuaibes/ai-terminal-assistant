# Import library
import sqlite3
import os

# Use an absolute path for the database file.
DB_FILE = os.path.expanduser("~/commands.db")

# Create a connection to the database commands.db 
connect = sqlite3.connect(DB_FILE)
# Database cursor in order to execute SQL statements
cursor = connect.cursor()

# Create table if it doe snot exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        command_text TEXT UNIQUE,
        description TEXT,
        first_used DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_used DATETIME DEFAULT CURRENT_TIMESTAMP,
        usage_count INTEGER DEFAULT 1
    )
    ''')

# Commit changes and close the connection
connect.commit()
connect.close()

# Debug purposes
print("Database and table has been created")

# Run python3 setup_db.py