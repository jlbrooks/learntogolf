# Operation 36 Golf Tracker - Version 1 Specification

## Overview
A simple web application to track progress in the Operation 36 golf program, where players start at Level 1 (225 yards total course) and level up by shooting 36 or better on 9-hole rounds. The maximum level is 6.

## Technical Stack
- **Backend**: Python (Flask/FastAPI)
- **Frontend**: HTMX with HTML templates
- **Styling**: Tailwind CSS
- **Database**: SQLite for persistence
- **Storage**: Start with JSON file, migrate to SQLite

## Core Features

### 1. User Progress Tracking
- Track current level (determines course length)
- Record scores for each 9-hole round
- Display level-up progress (need 36 or better to advance)
- Calculate course length: 225 + (level - 1) * 25 yards
- The maximum level is 6.

### 2. Score Entry
- Simple form to input 9 individual hole scores
- Automatic calculation of total score
- Validation that each hole entry is reasonable (1-10 strokes)
- Submit button triggers HTMX request

### 3. Progress Dashboard
- Current level indicator with course length
- Recent rounds history (last 10 rounds)
- Key statistics:
  - Current level
  - Total rounds played
  - Average score
  - Best score
  - Rounds at current level

### 4. Level Management
- Automatic level progression when score ≤ 36
- Level display shows yards per hole (25 yards base + level adjustments)
- Visual progress indicator toward next level

## Key Components

### Backend Routes
- `GET /` - Main dashboard
- `POST /score` - Submit new round score
- `GET /history` - Rounds history (HTMX partial)
- `GET /stats` - Statistics partial

### Frontend Components
1. **LevelDisplay** - Current level and course details
2. **ScoreCard** - 9-hole score entry form
3. **ProgressIndicator** - Visual progress toward level-up
4. **RoundsHistory** - Scrollable list of previous rounds
5. **StatsPanel** - Key performance metrics

### Data Model
```python
Round = {
    "id": int,
    "date": datetime,
    "level": int,
    "holes": [int] * 9,  # Individual hole scores
    "total": int,
    "leveled_up": bool
}

Player = {
    "current_level": int,
    "total_rounds": int,
    "rounds": [Round]
}
```

## User Experience Flow
1. Player sees current level and course length
2. Player enters 9 hole scores in simple form
3. HTMX submits form without page reload
4. Dashboard updates with new total and level progression
5. If score ≤ 36, level automatically increases
6. History and stats update dynamically

## MVP Requirements
- Single player (no authentication)
- Score entry and validation
- Level progression logic
- Basic statistics display
- Responsive design with Tailwind
- Data persistence between sessions