#!/usr/bin/env python3
"""Database initialization script for Learn to Golf Tracker."""

import os
from flask import Flask
from db_models import db, User, UserProfile, Round

def create_app():
    """Create Flask app with database configuration."""
    app = Flask(__name__)
    
    # Database configuration - use psycopg (not psycopg2)
    database_url = os.environ.get('DATABASE_URL', 'postgresql+psycopg://localhost:5432/learntogolf_dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    return app

def init_database():
    """Initialize database tables and indexes."""
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            
            # Create indexes for performance
            print("Creating database indexes...")
            
            # Index for rounds lookup by user and date
            db.session.execute(db.text(
                "CREATE INDEX IF NOT EXISTS idx_rounds_user_played "
                "ON rounds(user_id, played_at DESC)"
            ))
            
            # Index for user email lookup
            db.session.execute(db.text(
                "CREATE INDEX IF NOT EXISTS idx_users_email "
                "ON users(email)"
            ))
            
            # Index for rounds by user and level
            db.session.execute(db.text(
                "CREATE INDEX IF NOT EXISTS idx_rounds_user_level "
                "ON rounds(user_id, level)"
            ))
            
            db.session.commit()
            
            print("Database initialized successfully!")
            
            # Print table info
            print("\nTables created:")
            for table in db.metadata.tables.keys():
                print(f"  - {table}")
                
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

def reset_database():
    """Drop all tables and recreate them (for development)."""
    app = create_app()
    
    with app.app_context():
        try:
            print("Dropping all tables...")
            db.drop_all()
            
            print("Recreating tables...")
            init_database()
            
        except Exception as e:
            print(f"Error resetting database: {e}")
            raise

def create_test_user():
    """Create a test user for development."""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if test user already exists
            test_user = User.query.filter_by(email='test@learntogolf.com').first()
            if test_user:
                print("Test user already exists!")
                return test_user
            
            # Create test user
            user = User(email='test@learntogolf.com')
            user.set_password('password123')
            
            db.session.add(user)
            db.session.commit()
            
            # Create user profile
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)
            db.session.commit()
            
            print(f"Test user created: {user.email}")
            print("Password: password123")
            
            return user
            
        except Exception as e:
            print(f"Error creating test user: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'reset':
            reset_database()
        elif command == 'test-user':
            create_test_user()
        elif command == 'init':
            init_database()
        else:
            print("Usage: python init_db.py [init|reset|test-user]")
            print("  init      - Initialize database tables")
            print("  reset     - Drop and recreate all tables")
            print("  test-user - Create a test user account")
    else:
        init_database()