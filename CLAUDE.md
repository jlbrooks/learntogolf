# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a complete web application for tracking progress in the Learn to Golf program. Players start at Level 1 (225 yards total course, 25 yards per hole) and advance levels by shooting 36 or better on 9-hole rounds. The course gets progressively longer with each level up to a maximum of Level 6.

## Technical Architecture

- **Backend**: Python with Flask framework
- **Frontend**: HTMX with Jinja2 templates for dynamic interactions
- **Styling**: Tailwind CSS via CDN for responsive design
- **Data Storage**: JSON file persistence with DataStore class
- **Testing**: Comprehensive unittest suite in `test_models.py`

## File Structure

```
├── app.py                      # Main Flask application
├── models.py                   # Data models (Player, Round, DataStore)
├── utils.py                    # Utility functions for calculations and validation
├── test_models.py              # Complete test suite
├── requirements.txt            # Python dependencies
├── templates/
│   ├── index.html             # Main page template
│   ├── progress_section.html  # Progress dashboard partial
│   ├── history_section.html   # Rounds history partial
│   └── stats_section.html     # Statistics panel partial
├── player_data.json           # Generated data file (gitignored)
└── venv/                      # Virtual environment (gitignored)
```

## Key Features Implemented

### Core Functionality
- **Score Entry**: 9-hole form with real-time validation and total calculation
- **Level Progression**: Automatic advancement when shooting 36 or better
- **Data Persistence**: JSON-based storage that survives server restarts
- **Progress Tracking**: Visual indicators and statistics

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

- `GET /` - Main dashboard with all components
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

# Run application
python app.py

# Run tests
python test_models.py
```

## Development Notes

- **Single Player**: No authentication required, one player per instance
- **HTMX Integration**: All form submissions and updates happen without page reloads
- **Responsive Design**: Works well on mobile devices with touch-friendly inputs
- **Error Handling**: Comprehensive validation on both client and server sides
- **Testing**: Full test coverage with 15 unit tests covering all core functionality
- **Data Safety**: Automatic data persistence with error recovery