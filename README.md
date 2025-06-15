# Learn to Golf Tracker

A progressive golf learning web application that helps players build skills systematically. Players start close to the hole and gradually work their way back through 6 levels, advancing only after demonstrating consistency at each distance.

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (for local development)
- Git

### Local Development Setup

1. **Clone and setup environment**
   ```bash
   git clone <repository-url>
   cd learntogolf
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database setup**
   ```bash
   # Create local PostgreSQL database
   python create_dev_db.py
   
   # Initialize tables and indexes
   python init_db.py init
   
   # Create test user (optional)
   python init_db.py test-user
   ```

3. **Run the application**
   ```bash
   python app.py
   ```
   
   Access at http://localhost:5000

### Test User
- **Email**: test@learntogolf.com
- **Password**: password123

## Architecture Overview

### Tech Stack
- **Backend**: Flask + SQLAlchemy + Flask-Login
- **Frontend**: HTMX + Tailwind CSS
- **Database**: PostgreSQL (local) / Supabase (production)
- **Deployment**: fly.io with Docker

### Key Components

```
app.py              # Main Flask app with routes
auth.py             # Flask-Login configuration
db_models.py        # SQLAlchemy models
utils.py            # Business logic utilities
templates/          # Jinja2 templates
├── welcome.html    # Landing page
├── login.html      # Authentication
├── register.html   
├── index.html      # Main dashboard
└── *_section.html  # HTMX partials
```

### Database Schema

- **users**: Authentication (email, password_hash)
- **user_profiles**: Golf progress (current_level, total_rounds)
- **rounds**: Individual games (holes array, total, level)

## Development Workflow

### Database Management

```bash
# Reset database (WARNING: deletes all data)
python init_db.py reset

# Create test user
python init_db.py test-user

# Check database status
python init_db.py init
```

### Testing

```bash
# Run all tests
python test_models.py

# Tests cover:
# - Level progression logic
# - Score validation
# - User authentication
# - Database operations
```

### Environment Variables

Create `.env` or set in your shell:

```bash
# Required
DATABASE_URL=postgresql+psycopg://localhost:5432/learntogolf_dev
SECRET_KEY=your-secret-key-here

# Optional
FLASK_ENV=development
```

## Production Deployment

### fly.io Deployment

1. **Setup fly.io**
   ```bash
   # Install flyctl
   brew install flyctl  # macOS
   # or download from https://fly.io/docs/flyctl/install/
   
   flyctl auth login
   ```

2. **Configure database**
   - Set up Supabase PostgreSQL database
   - Update `supabase-connection-string.txt` (gitignored)
   - Set `DATABASE_URL` environment variable

3. **Deploy**
   ```bash
   flyctl deploy
   ```

### Environment Configuration

Production requires:
- `DATABASE_URL`: Supabase PostgreSQL connection string
- `SECRET_KEY`: Secure random key for sessions

## How the Golf System Works

### Level Progression
- **Level 1**: 225 yards total (25 yards/hole average)
- **Level 2**: 450 yards total (50 yards/hole average)
- **Level 3**: 900 yards total (100 yards/hole average)
- **Level 4**: 1,350 yards total (150 yards/hole average)
- **Level 5**: 1,800 yards total (200 yards/hole average)
- **Level 6**: 2,250 yards total (250 yards/hole average)

### Advancement Rules
- Players must shoot **36 or better** (par) to advance
- Each level must be conquered before moving to the next
- Level 6 is the maximum level (no advancement beyond)

### Scoring
- 9-hole rounds only
- Each hole: 1-10 strokes allowed
- Par is 4 strokes per hole (36 total)

## API Reference

### Authentication Routes
- `GET /` - Welcome page (logged out) or dashboard (logged in)
- `GET /login` - Login form
- `POST /login` - Process login
- `GET /register` - Registration form
- `POST /register` - Create account
- `GET /logout` - Sign out

### Protected Routes (Login Required)
- `POST /score` - Submit round (returns HTMX HTML)
- `GET /progress` - Progress section partial
- `GET /history` - Recent rounds partial
- `GET /stats` - Statistics partial

## Common Development Tasks

### Adding New Features
1. Update database models in `db_models.py`
2. Add routes in `app.py`
3. Create/update templates in `templates/`
4. Add business logic to `utils.py`
5. Write tests in `test_models.py`

### Database Schema Changes
1. Modify models in `db_models.py`
2. Run `python init_db.py reset` (development only)
3. Run `python init_db.py init`
4. Update tests if needed

### Debugging
- Enable Flask debug mode: `FLASK_ENV=development`
- Check database connectivity: `python init_db.py init`
- Run tests: `python test_models.py`
- Check logs: `flyctl logs` (production)

## File Structure

```
learntogolf/
├── app.py                      # Main Flask application
├── auth.py                     # Authentication setup
├── db_models.py                # Database models
├── utils.py                    # Business logic
├── test_models.py              # Test suite
├── init_db.py                  # Database management
├── create_dev_db.py            # Local DB setup
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Production container
├── fly.toml                    # fly.io configuration
├── CLAUDE.md                   # AI assistant instructions
├── spec.md                     # Technical specification
└── templates/                  # HTML templates
    ├── welcome.html            # Landing page
    ├── login.html              # Authentication
    ├── register.html
    ├── index.html              # Dashboard
    └── *_section.html          # HTMX partials
```

## Security Notes

- Passwords are hashed with Werkzeug's secure methods
- Users can only access their own data (complete isolation)
- SQLAlchemy ORM prevents SQL injection
- HTTPS enforced in production
- Session management via Flask-Login

## Contributing

1. Create feature branch from `main`
2. Make changes with tests
3. Ensure all tests pass: `python test_models.py`
4. Test locally with fresh database
5. Submit pull request

## Troubleshooting

### Database Issues
```bash
# Can't connect to database
python create_dev_db.py  # Recreate local DB

# Tables don't exist
python init_db.py init   # Create tables

# Data issues
python init_db.py reset  # Nuclear option - deletes everything
python init_db.py init
python init_db.py test-user
```

### Import/Module Issues
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Production Deployment Issues
```bash
# Check deployment status
flyctl status

# View logs
flyctl logs

# Redeploy
flyctl deploy
```