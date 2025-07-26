#!/usr/bin/env python3
"""Fix user_id column size in pet_interactions table"""

import sys
from sqlalchemy import create_engine, text
from backend.database.db_connection import DATABASE_URL, USE_SQLITE

def fix_user_id_column():
    """Alter the user_id column to accommodate longer session IDs"""
    
    print(f"Connecting to database...")
    print(f"Using SQLite: {USE_SQLITE}")
    
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            if USE_SQLITE:
                # SQLite doesn't support ALTER COLUMN directly
                # We need to recreate the table
                print("SQLite doesn't support ALTER COLUMN. Skipping for now.")
                print("Consider recreating the table with the correct column size.")
            else:
                # MySQL ALTER TABLE
                print("Altering user_id column size in pet_interactions table...")
                
                # Check current column definition
                result = conn.execute(text("""
                    SELECT COLUMN_TYPE 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'pet_interactions' 
                    AND COLUMN_NAME = 'user_id'
                    AND TABLE_SCHEMA = DATABASE()
                """))
                
                current_type = result.fetchone()
                if current_type:
                    print(f"Current column type: {current_type[0]}")
                
                # Alter column to accommodate session IDs (max 60 chars to be safe)
                conn.execute(text("""
                    ALTER TABLE pet_interactions 
                    MODIFY COLUMN user_id VARCHAR(60)
                """))
                conn.commit()
                
                print("✅ Successfully altered user_id column to VARCHAR(60)")
                
                # Verify the change
                result = conn.execute(text("""
                    SELECT COLUMN_TYPE 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'pet_interactions' 
                    AND COLUMN_NAME = 'user_id'
                    AND TABLE_SCHEMA = DATABASE()
                """))
                
                new_type = result.fetchone()
                if new_type:
                    print(f"New column type: {new_type[0]}")
                
    except Exception as e:
        print(f"❌ Error altering column: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_user_id_column()