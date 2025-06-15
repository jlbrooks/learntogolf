def calculate_course_length(level: int) -> int:
    """Calculate total course length for a given level."""
    return 225 + (level - 1) * 25

def calculate_yards_per_hole(level: int) -> float:
    """Calculate yards per hole for a given level."""
    return calculate_course_length(level) / 9

def get_level_info(level: int) -> dict:
    """Get comprehensive level information."""
    total_yards = calculate_course_length(level)
    yards_per_hole = calculate_yards_per_hole(level)
    
    return {
        "level": level,
        "total_yards": total_yards,
        "yards_per_hole": yards_per_hole,
        "target_score": 36,
        "par_per_hole": 4
    }

def validate_hole_score(score: int) -> bool:
    """Validate that a hole score is reasonable (1-10 strokes)."""
    return isinstance(score, int) and 1 <= score <= 10

def validate_round_scores(holes: list) -> tuple[bool, str]:
    """Validate a complete round of 9 hole scores."""
    if len(holes) != 9:
        return False, "Must have exactly 9 hole scores"
    
    for i, score in enumerate(holes, 1):
        if not validate_hole_score(score):
            return False, f"Hole {i} score must be between 1 and 10"
    
    return True, "Valid round"