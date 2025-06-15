# Learn to Golf Tracker - Specification

## Version 1 - Single Player (Completed)

### Overview
A simple web application to track progress in the Learn to Golf program, where players start at Level 1 (225 yards total course) and level up by shooting 36 or better on 9-hole rounds.

### Technical Stack
- **Backend**: Python Flask
- **Frontend**: HTMX with HTML templates
- **Styling**: Tailwind CSS
- **Storage**: JSON file persistence

### Core Features
- Single player score tracking
- 9-hole score entry with validation
- Automatic level progression (levels 1-6)
- Progress dashboard with statistics
- Responsive design for mobile/desktop

### Level Progression
- Level 1: 225 yards (25 yards/hole)
- Level 2: 450 yards (50 yards/hole)
- Level 3: 900 yards (100 yards/hole)
- Level 4: 1350 yards (150 yards/hole)
- Level 5: 1800 yards (200 yards/hole)
- Level 6: 2250 yards (250 yards/hole)

---

## Version 2 - Multi-User Cloud Deployment

### Overview
Extend the application for multi-user support with authentication and cloud database deployment. Each user tracks their own golf learning progress independently.

### Technical Stack
- **Backend**: Python Flask with Flask-Login and Flask-SQLAlchemy
- **Frontend**: HTMX with HTML templates (maintain existing UI)
- **Styling**: Tailwind CSS (unchanged)
- **Database**: PostgreSQL via Supabase (free tier: 500MB, 2 concurrent connections)
- **Deployment**: fly.io

### Database Choice: Supabase PostgreSQL
**Why Supabase:**
- **Free tier**: 500MB storage, 2 concurrent connections
- **PostgreSQL**: Mature, reliable, handles JSON data well
- **Simple setup**: Web dashboard, automatic backups
- **Scalable**: Easy upgrade path when needed
- **No server management**: Fully managed service

### New Features

#### 1. User Authentication
- **Registration**: Email + password (no email verification)
- **Login**: Simple email/password form
- **Session Management**: Flask-Login for session handling
- **User Isolation**: Each user sees only their own data

#### 2. Database Schema
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles (extends user data)
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    current_level INTEGER DEFAULT 1,
    total_rounds INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rounds table
CREATE TABLE rounds (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    level INTEGER NOT NULL,
    holes JSONB NOT NULL, -- Array of 9 hole scores
    total INTEGER NOT NULL,
    leveled_up BOOLEAN DEFAULT FALSE,
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_rounds_user_id ON rounds(user_id);
CREATE INDEX idx_rounds_played_at ON rounds(user_id, played_at DESC);
```

#### 3. Updated Routes
```python
# Authentication routes
GET /login          # Login form
POST /login         # Process login
GET /register       # Registration form  
POST /register      # Process registration
POST /logout        # Logout user

# Protected routes (require login)
GET /               # User dashboard (existing)
POST /score         # Submit score (existing, user-scoped)
GET /progress       # Progress partial (existing, user-scoped)
GET /history        # History partial (existing, user-scoped)
GET /stats          # Stats partial (existing, user-scoped)
```

#### 4. Data Migration Strategy
- No data migration is needed.

### Implementation Plan

#### Phase 1: Local Database Setup
1. Install PostgreSQL locally (via Homebrew/package manager)
2. Create local development database
3. Create database schema and migrations
4. Add SQLAlchemy models
5. Test database connectivity with local PostgreSQL

#### Phase 2: Authentication
1. Add Flask-Login and password hashing
2. Create registration/login forms
3. Implement session management
4. Add login_required decorators
5. Test authentication flow with local database

#### Phase 3: User Data Isolation
1. Update all routes to filter by user_id
2. Modify models to associate data with users
3. Update templates to show user-specific data
4. Test multi-user scenarios locally
5. Ensure complete data separation between users

#### Phase 4: Production Deployment
1. Set up Supabase PostgreSQL database
2. Configure environment variables for production
3. Set up fly.io deployment configuration
4. Deploy application to fly.io
5. Configure production database connection to Supabase
6. Test production deployment and database connectivity
7. Run production smoke tests

### Environment Variables

#### Local Development
```bash
# Database (local PostgreSQL)
DATABASE_URL=postgresql://localhost:5432/op36golf_dev

# Flask
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
```

#### Production (fly.io)
```bash
# Database (Supabase)
DATABASE_URL=postgresql://user:pass@host:port/db

# Flask
SECRET_KEY=your-secure-secret-key
FLASK_ENV=production

# Optional: Analytics
PLAUSIBLE_DOMAIN=yourdomain.com
```

### Deployment Platform: fly.io

#### Why fly.io:
- **Performance**: Edge deployment, fast global performance
- **Simplicity**: Single command deployment with flyctl
- **Cost-effective**: Generous free tier, pay-as-you-scale
- **Docker-based**: Flexible deployment options
- **PostgreSQL**: Easy integration with external databases like Supabase

#### Local Development Setup:
```bash
# Install PostgreSQL locally
brew install postgresql  # macOS
sudo apt-get install postgresql  # Ubuntu

# Create development database
createdb op36golf_dev

# Install Python dependencies
pip install flask flask-sqlalchemy flask-login psycopg2-binary
```

#### Production Deployment:
```bash
# Install flyctl
brew install flyctl  # macOS

# Login and deploy
flyctl auth login
flyctl launch
flyctl deploy
```

### Security Considerations
- **Password Hashing**: Use bcrypt/Argon2
- **Session Security**: Secure cookies, CSRF protection
- **SQL Injection**: Use SQLAlchemy ORM (prevents SQL injection)
- **Input Validation**: Maintain existing validation + email validation
- **Rate Limiting**: Basic rate limiting on auth endpoints
