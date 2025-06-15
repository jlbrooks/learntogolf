# Learn to Golf Tracker - Specification

## Overview
A multi-user web application for tracking progress in the Learn to Golf program. Players start at Level 1 (225 yards total course) and advance levels by shooting 36 or better on 9-hole rounds. Each user has their own account and tracks their individual progress through 6 levels.

## Technical Stack
- **Backend**: Python Flask with Flask-Login and Flask-SQLAlchemy
- **Frontend**: HTMX with Jinja2 templates for dynamic interactions
- **Styling**: Tailwind CSS via CDN for responsive design
- **Database**: PostgreSQL (local development and Supabase for production)
- **Deployment**: fly.io with Docker containerization
- **Authentication**: Flask-Login with password hashing

## Core Features

### User Authentication
- **Registration**: Email + password with confirmation
- **Login**: Email/password authentication with session management
- **User Isolation**: Complete data separation between users
- **Welcome Page**: Landing page for unauthenticated users
- **Session Management**: Secure login/logout with Flask-Login

### Golf Progress Tracking
- **9-hole Score Entry**: Real-time validation and total calculation
- **Level Progression**: Automatic advancement when shooting 36 or better
- **Progress Dashboard**: Current level, course info, and advancement status
- **Statistics Panel**: Comprehensive metrics and performance tracking
- **Rounds History**: Detailed hole-by-hole scores for recent rounds

### User Interface
- **Responsive Design**: Mobile-first with Tailwind CSS breakpoints
- **Dynamic Updates**: HTMX-powered interactions without page reloads
- **Real-time Feedback**: Client-side validation with visual error indicators
- **Progressive Enhancement**: Works without JavaScript as fallback

## Level Progression System
- **Level 1**: 225 yards total (25 yards per hole average)
- **Level 2**: 450 yards total (50 yards per hole average)
- **Level 3**: 900 yards total (100 yards per hole average)
- **Level 4**: 1,350 yards total (150 yards per hole average)
- **Level 5**: 1,800 yards total (200 yards per hole average)
- **Level 6**: 2,250 yards total (250 yards per hole average)

Players advance by shooting par (36) or better at their current level.

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### User Profiles Table
```sql
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    current_level INTEGER DEFAULT 1,
    total_rounds INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Rounds Table
```sql
CREATE TABLE rounds (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    level INTEGER NOT NULL,
    holes JSON NOT NULL, -- Array of 9 hole scores
    total INTEGER NOT NULL,
    leveled_up BOOLEAN DEFAULT FALSE,
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Performance Indexes
- `idx_rounds_user_id` on `rounds(user_id)`
- `idx_rounds_user_played` on `rounds(user_id, played_at DESC)`

## API Routes

### Authentication Routes
- `GET /` - Welcome page (unauthenticated) or dashboard (authenticated)
- `GET /login` - Login form
- `POST /login` - Process login
- `GET /register` - Registration form
- `POST /register` - Process registration
- `GET /logout` - Logout user

### Protected Routes (Login Required)
- `GET /` - User dashboard with progress overview
- `POST /score` - Submit round scores (returns HTML for HTMX)
- `GET /progress` - Progress section partial (HTMX)
- `GET /history` - Rounds history partial (HTMX)
- `GET /stats` - Statistics panel partial (HTMX)

## Validation & Error Handling

### Client-side Validation
- Real-time input validation with visual feedback
- Score range checking (1-10 strokes per hole)
- Form completion validation

### Server-side Validation
- Comprehensive error handling with user-friendly messages
- Email format validation for registration
- Password requirements (minimum 6 characters)
- Duplicate email prevention
- Score validation and business logic enforcement

## Development Environment

### Local Development Setup
```bash
# Database setup
python create_dev_db.py
python init_db.py init
python init_db.py test-user

# Run application
python app.py
```

### Environment Variables
```bash
# Local Development
DATABASE_URL=postgresql+psycopg://localhost:5432/learntogolf_dev
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development

# Production
DATABASE_URL=postgresql+psycopg://[supabase_connection_string]
SECRET_KEY=[secure_production_key]
FLASK_ENV=production
```

## Production Deployment

### Docker Configuration
- Python 3.11 slim base image
- Gunicorn WSGI server with 2 workers
- Non-root user for security
- Port 8080 exposure

### fly.io Configuration
- Primary region: San Jose (sjc)
- Auto-scaling with stop/start machines
- HTTPS enforcement
- 1GB memory, 1 shared CPU
- Static file serving at `/static/`

### Database
- **Development**: Local PostgreSQL
- **Production**: Supabase PostgreSQL
- Connection string compatibility handling for both environments

## Security Features
- **Password Hashing**: Werkzeug secure password hashing
- **Session Security**: Flask-Login session management
- **SQL Injection Prevention**: SQLAlchemy ORM usage
- **Input Validation**: Comprehensive client and server-side validation
- **User Data Isolation**: Complete separation of user data
- **HTTPS Enforcement**: Required in production
