"""
Database Initialization Script
Run this to set up the database
"""

from database.db_manager import DatabaseManager

if __name__ == '__main__':
    print("Initializing database...")
    db = DatabaseManager()
    db.init_db()
    print("Database setup complete!")
