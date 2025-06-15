# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a complete multi-user web application for tracking progress in the Learn to Golf program. Players start at Level 1 (225 yards total course, 25 yards per hole) and advance levels by shooting 36 or better on 9-hole rounds. The course gets progressively longer with each level up to a maximum of Level 6. Each user has their own account and tracks individual progress.

## Technical Architecture

- **Backend**: Python with Flask framework, Flask-Login, and Flask-SQLAlchemy
- **Frontend**: HTMX with Jinja2 templates for dynamic interactions
- **Styling**: Tailwind CSS via CDN for responsive design
- **Database**: PostgreSQL with SQLAlchemy ORM (local development and Supabase production)
- **Authentication**: Flask-Login with secure password hashing
- **Deployment**: fly.io with Docker containerization
- **Testing**: Comprehensive unittest suite in `test_models.py`

## File Structure

```
├── app.py                      # Main Flask application with authentication routes
├── auth.py                     # Flask-Login configuration and utilities
├── db_models.py                # SQLAlchemy models (User, UserProfile, Round)
├── utils.py                    # Utility functions for calculations and validation
├── test_models.py              # Complete test suite
├── init_db.py                  # Database initialization and management
├── create_dev_db.py            # Development database creation script
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration for production deployment
├── fly.toml                    # fly.io deployment configuration
├── supabase-connection-string.txt  # Supabase database connection (gitignored)
├── templates/
│   ├── index.html             # Main dashboard template (authenticated users)
│   ├── welcome.html           # Landing page for unauthenticated users
│   ├── login.html             # User login form
│   ├── register.html          # User registration form
│   ├── progress_section.html  # Progress dashboard partial
│   ├── history_section.html   # Rounds history partial
│   └── stats_section.html     # Statistics panel partial
└── venv/                      # Virtual environment (gitignored)
```

## Key Features Implemented

### Authentication & User Management
- **User Registration**: Email + password with confirmation and validation
- **User Login**: Secure authentication with Flask-Login session management
- **User Isolation**: Complete data separation between users
- **Welcome Page**: Landing page for unauthenticated users with feature overview
- **Password Security**: Secure password hashing with Werkzeug

### Core Functionality
- **Score Entry**: 9-hole form with real-time validation and total calculation
- **Level Progression**: Automatic advancement when shooting 36 or better
- **Data Persistence**: PostgreSQL database with SQLAlchemy ORM
- **Progress Tracking**: Visual indicators and statistics per user

### User Interface
- **Responsive Design**: Mobile-first with Tailwind CSS breakpoints
- **Dynamic Updates**: HTMX-powered form submission without page reloads
- **Real-time Feedback**: Client-side validation with visual error indicators
- **Progress Dashboard**: Current level, course info, and advancement status
- **Statistics Panel**: Comprehensive metrics and performance tracking
- **Rounds History**: Last 10 rounds with detailed hole-by-hole scores

### Validation & Error Handling
- **Client-side**: Real-time input validation with visual feedback
- **Server-side**: Comprehensive error handling with user-friendly messages
- **Data Validation**: Score range checking (1-10 strokes per hole)
- **Form Validation**: Missing field detection and helpful error messages

## Key Business Logic

- **Level Progression**: Players advance when they shoot 36 or better (Par 4 × 9 holes)
- **Course Length**: L1: 225y, L2: 450y, L3: 900y, L4: 1350y, L5: 1800y, L6: 2250y
- **Score Validation**: Individual hole scores must be 1-10 strokes
- **Statistics**: Average score, best score, success rate, rounds per level

## API Routes

### Authentication Routes
- `GET /` - Welcome page (unauthenticated) or main dashboard (authenticated)
- `GET /login` - User login form
- `POST /login` - Process login credentials
- `GET /register` - User registration form
- `POST /register` - Process new user registration
- `GET /logout` - Log out current user

### Protected Routes (Login Required)
- `POST /score` - Submit round scores (returns HTML for HTMX)
- `GET /progress` - Progress section partial (HTMX)
- `GET /history` - Rounds history partial (HTMX)
- `GET /stats` - Statistics panel partial (HTMX)

## Development Commands

```bash
# Set up environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Database setup
python create_dev_db.py                # Create development database
python init_db.py init                 # Initialize tables and indexes
python init_db.py test-user            # Create test user (test@learntogolf.com / password123)
python init_db.py reset                # Reset database (drops all data!)

# Run application
python app.py                          # Local development server

# Run tests
python test_models.py

# Production deployment
flyctl deploy                          # Deploy to fly.io (requires flyctl CLI)
```

## Development Notes

### Current Implementation
- **Multi-User**: Full authentication with Flask-Login and complete user isolation
- **Database**: PostgreSQL with SQLAlchemy ORM models for all data persistence
- **Local Development**: Uses local PostgreSQL database (`learntogolf_dev`)
- **Production**: Deployed to fly.io with Supabase PostgreSQL database
- **HTMX Integration**: All form submissions and updates happen without page reloads
- **Responsive Design**: Works well on mobile devices with touch-friendly inputs

### Database Schema
- **users**: Authentication data (id, email, password_hash, created_at)
- **user_profiles**: Golf-specific data (user_id, current_level, total_rounds)
- **rounds**: Individual round data (user_id, level, holes, total, leveled_up, played_at)

### Production Deployment
- **Platform**: fly.io with Docker containerization
- **Database**: Supabase PostgreSQL (managed service)
- **Environment**: Automatic HTTPS, auto-scaling, edge deployment
- **Configuration**: Environment variables for database URL and secret key

### Security & Data Safety
- **Authentication**: Secure password hashing with Werkzeug
- **User Isolation**: Complete data separation between users
- **Session Management**: Flask-Login with secure session handling
- **Input Validation**: Comprehensive validation on both client and server sides
- **SQL Injection Prevention**: SQLAlchemy ORM usage throughout
- **Error Handling**: User-friendly error messages and proper exception handling
- **Testing**: Full test coverage with comprehensive unit tests
- **Data Safety**: Automatic database persistence with transaction management