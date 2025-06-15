#!/usr/bin/env python3
"""Create the development database if it doesn't exist."""

import os
import psycopg
from psycopg import sql

def create_database():
    """Create the development database."""
    
    # Database connection parameters
    db_name = 'learntogolf_dev'
    
    try:
        # Connect to PostgreSQL server (without specifying database)
        conn = psycopg.connect(
            host='localhost',
            user=os.environ.get('USER'),  # Use current user
            password='',  # No password for local development
            dbname='postgres'  # Connect to default postgres database
        )
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # Check if database exists
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (db_name,)
            )
            
            if cur.fetchone():
                print(f"Database '{db_name}' already exists!")
            else:
                # Create the database
                cur.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(db_name)
                    )
                )
                print(f"Database '{db_name}' created successfully!")
        
        conn.close()
        
    except psycopg.OperationalError as e:
        print(f"Could not connect to PostgreSQL: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running:")
        print("   brew services start postgresql@15")
        print("2. Make sure PostgreSQL is in your PATH:")
        print("   export PATH=\"/opt/homebrew/opt/postgresql@15/bin:$PATH\"")
        raise
    
    except Exception as e:
        print(f"Error creating database: {e}")
        raise

if __name__ == '__main__':
    create_database()