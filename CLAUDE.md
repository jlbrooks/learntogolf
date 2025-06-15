# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a web application for tracking progress in the Operation 36 golf program. Players start at Level 1 (225 yards total course, 25 yards per hole) and advance levels by shooting 36 or better on 9-hole rounds. The course gets progressively longer with each level.

## Architecture

- **Backend**: Python with Flask/FastAPI
- **Frontend**: HTMX with HTML templates for dynamic interactions
- **Styling**: Tailwind CSS for responsive design
- **Database**: SQLite for data persistence
- **Data Flow**: HTMX requests update UI components without full page reloads

## Key Business Logic

- **Level Progression**: Players advance when they shoot 36 or better (Par 4 × 9 holes)
- **Course Length**: 225 + (level - 1) × 25 yards total
- **Score Validation**: Individual hole scores should be 1-10 strokes
- **Maximum Level**: 6 levels total

## Data Model

The application tracks:
- Player current level and total rounds played
- Individual rounds with 9 hole scores, total, date, and level-up status
- Statistics: average score, best score, rounds at current level

## Development Notes

- Single player application (no authentication required)
- HTMX handles dynamic updates for score submission and dashboard refresh
- Core routes: `/` (dashboard), `POST /score` (submit round), `/history` and `/stats` (HTMX partials)
- Focus on simple, responsive UI that works well on mobile devices