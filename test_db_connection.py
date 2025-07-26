#!/usr/bin/env python3
"""Test database connection for DKS system"""

import os
import sys
from sqlalchemy import create_engine, text

def test_connection():
    # Check if we're using SQLite
    use_sqlite = os.getenv("USE_SQLITE", "false").lower() == "true"
    
    if use_sqlite:
        print("Testing SQLite connection...")
        db_url = "sqlite:///dks_development.db"
    else:
        print("Testing MySQL connection...")
        host = os.getenv("MYSQL_HOST", "localhost")
        port = os.getenv("MYSQL_PORT", "3306")
        user = os.getenv("MYSQL_USER", "dks_user")
        password = os.getenv("MYSQL_PASSWORD", "dks_password")
        database = os.getenv("MYSQL_DATABASE", "dks_petworld")
        db_url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        print(f"Connection URL: mysql+mysqlconnector://{user}:****@{host}:{port}/{database}")
    
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
            # Try to check if tables exist
            if use_sqlite:
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            else:
                result = conn.execute(text("SHOW TABLES;"))
            
            tables = [row[0] for row in result]
            if tables:
                print(f"📊 Found {len(tables)} tables: {', '.join(tables)}")
            else:
                print("⚠️  No tables found. You may need to run database initialization.")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        
        if "No module named 'mysql'" in str(e):
            print("\n💡 Install MySQL connector: pip install mysql-connector-python")
        elif "Access denied" in str(e):
            print("\n💡 Check your MySQL credentials")
        elif "Can't connect to MySQL server" in str(e):
            print("\n💡 MySQL server is not running. Try:")
            print("   - docker-compose up -d mysql")
            print("   - Or set USE_SQLITE=true to use SQLite")
            
        return False

if __name__ == "__main__":
    print("DKS Database Connection Test")
    print("=" * 40)
    
    success = test_connection()
    sys.exit(0 if success else 1)