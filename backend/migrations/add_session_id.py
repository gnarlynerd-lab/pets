#!/usr/bin/env python3
"""
Migration: Add session_id column to pet_states table
Date: 2025-01-17
Description: Adds session_id column to support anonymous user sessions
"""

import os
import sys
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Add project root to path so we can import from backend
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from backend.database.db_connection import DATABASE_URL, engine

def run_migration():
    """Add session_id column to pet_states table"""
    
    print("Starting migration: Add session_id column to pet_states")
    
    try:
        with engine.connect() as connection:
            # Check if column already exists
            result = connection.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'pet_states' 
                AND COLUMN_NAME = 'session_id'
            """))
            
            if result.fetchone():
                print("✓ session_id column already exists in pet_states table")
                return True
            
            # Add the column
            print("Adding session_id column to pet_states table...")
            connection.execute(text("""
                ALTER TABLE pet_states 
                ADD COLUMN session_id VARCHAR(100) NULL 
                AFTER owner_id
            """))
            
            # Commit the transaction
            connection.commit()
            
            print("✓ Successfully added session_id column to pet_states table")
            return True
            
    except OperationalError as e:
        print(f"✗ Database error during migration: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during migration: {e}")
        return False

def rollback_migration():
    """Remove session_id column from pet_states table"""
    
    print("Rolling back migration: Remove session_id column from pet_states")
    
    try:
        with engine.connect() as connection:
            # Check if column exists
            result = connection.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'pet_states' 
                AND COLUMN_NAME = 'session_id'
            """))
            
            if not result.fetchone():
                print("✓ session_id column does not exist in pet_states table")
                return True
            
            # Remove the column
            print("Removing session_id column from pet_states table...")
            connection.execute(text("""
                ALTER TABLE pet_states 
                DROP COLUMN session_id
            """))
            
            # Commit the transaction
            connection.commit()
            
            print("✓ Successfully removed session_id column from pet_states table")
            return True
            
    except OperationalError as e:
        print(f"✗ Database error during rollback: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during rollback: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        success = rollback_migration()
    else:
        success = run_migration()
    
    sys.exit(0 if success else 1)