#!/usr/bin/env python3
"""Tests for the Operation 36 Golf Tracker models and logic."""

import unittest
import tempfile
import os
from datetime import datetime
from models import Player, Round, DataStore
from utils import get_level_info, validate_round_scores, calculate_course_length


class TestPlayer(unittest.TestCase):
    """Test Player class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.player = Player()
    
    def test_new_player_starts_at_level_1(self):
        """Test that a new player starts at level 1."""
        self.assertEqual(self.player.current_level, 1)
        self.assertEqual(self.player.total_rounds, 0)
        self.assertEqual(len(self.player.rounds), 0)
    
    def test_level_up_with_par_score(self):
        """Test leveling up with a score of exactly 36."""
        holes = [4, 4, 4, 4, 4, 4, 4, 4, 4]  # Perfect par
        round_obj = self.player.add_round(holes)
        
        self.assertEqual(round_obj.total, 36)
        self.assertTrue(round_obj.leveled_up)
        self.assertEqual(self.player.current_level, 2)
        self.assertEqual(self.player.total_rounds, 1)
    
    def test_level_up_with_under_par_score(self):
        """Test leveling up with a score under 36."""
        holes = [4, 4, 4, 3, 4, 4, 4, 4, 4]  # One under par = 35
        round_obj = self.player.add_round(holes)
        
        self.assertEqual(round_obj.total, 35)
        self.assertTrue(round_obj.leveled_up)
        self.assertEqual(self.player.current_level, 2)
    
    def test_no_level_up_with_over_par_score(self):
        """Test that scores over 36 don't level up."""
        holes = [4, 4, 4, 5, 4, 4, 4, 4, 4]  # One over par = 37
        round_obj = self.player.add_round(holes)
        
        self.assertEqual(round_obj.total, 37)
        self.assertFalse(round_obj.leveled_up)
        self.assertEqual(self.player.current_level, 1)
    
    def test_max_level_progression(self):
        """Test progression through all levels to max level 6."""
        # Level up through levels 1-6
        for expected_level in range(2, 7):  # 2 through 6
            holes = [4, 4, 4, 4, 4, 4, 4, 4, 4]  # Par score
            round_obj = self.player.add_round(holes)
            self.assertEqual(self.player.current_level, expected_level)
            if expected_level < 6:
                self.assertTrue(round_obj.leveled_up)
    
    def test_no_level_up_beyond_max_level(self):
        """Test that level 6 is the maximum level."""
        # Get to level 6
        for _ in range(5):  # 5 level-ups to reach level 6
            self.player.add_round([4, 4, 4, 4, 4, 4, 4, 4, 4])
        
        self.assertEqual(self.player.current_level, 6)
        
        # Try to level up beyond 6
        round_obj = self.player.add_round([4, 4, 4, 4, 4, 4, 4, 4, 4])
        self.assertEqual(self.player.current_level, 6)  # Should stay at 6
        # Note: round_obj.leveled_up might still be True based on score <= 36
    
    def test_statistics_methods(self):
        """Test player statistics calculation methods."""
        # Add some rounds with different scores
        self.player.add_round([4, 4, 4, 4, 4, 4, 4, 4, 4])  # 36
        self.player.add_round([3, 4, 5, 4, 4, 4, 4, 4, 4])  # 36
        self.player.add_round([5, 5, 5, 5, 5, 4, 4, 4, 4])  # 41
        
        # Test average score
        expected_average = (36 + 36 + 41) / 3
        self.assertEqual(self.player.get_average_score(), expected_average)
        
        # Test best score
        self.assertEqual(self.player.get_best_score(), 36)
        
        # Test rounds at current level
        rounds_at_level = self.player.get_rounds_at_current_level()
        self.assertEqual(rounds_at_level, 1)  # Only the last round at level 2


class TestRound(unittest.TestCase):
    """Test Round class functionality."""
    
    def test_round_creation(self):
        """Test creating a round with valid data."""
        holes = [4, 3, 5, 4, 4, 6, 4, 4, 4]
        round_obj = Round(holes, level=1)
        
        self.assertEqual(round_obj.holes, holes)
        self.assertEqual(round_obj.level, 1)
        self.assertEqual(round_obj.total, sum(holes))
        self.assertIsInstance(round_obj.date, datetime)
        self.assertIsInstance(round_obj.id, int)
    
    def test_round_leveled_up_flag(self):
        """Test the leveled_up flag is set correctly."""
        # Par round should level up
        par_holes = [4, 4, 4, 4, 4, 4, 4, 4, 4]
        par_round = Round(par_holes, level=1)
        self.assertTrue(par_round.leveled_up)
        
        # Over par round should not level up
        over_par_holes = [5, 5, 5, 5, 5, 5, 5, 5, 5]
        over_par_round = Round(over_par_holes, level=1)
        self.assertFalse(over_par_round.leveled_up)
    
    def test_round_serialization(self):
        """Test round to_dict and from_dict methods."""
        holes = [4, 3, 5, 4, 4, 6, 4, 4, 4]
        original_round = Round(holes, level=2)
        
        # Test serialization
        round_dict = original_round.to_dict()
        self.assertIn('id', round_dict)
        self.assertIn('date', round_dict)
        self.assertIn('holes', round_dict)
        self.assertIn('total', round_dict)
        self.assertIn('level', round_dict)
        self.assertIn('leveled_up', round_dict)
        
        # Test deserialization
        restored_round = Round.from_dict(round_dict)
        self.assertEqual(restored_round.holes, original_round.holes)
        self.assertEqual(restored_round.level, original_round.level)
        self.assertEqual(restored_round.total, original_round.total)
        self.assertEqual(restored_round.leveled_up, original_round.leveled_up)


class TestDataStore(unittest.TestCase):
    """Test DataStore functionality."""
    
    def setUp(self):
        """Set up test fixtures with temporary file."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.data_store = DataStore(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_new_datastore_creates_new_player(self):
        """Test that a new datastore creates a new player."""
        self.assertEqual(self.data_store.player.current_level, 1)
        self.assertEqual(self.data_store.player.total_rounds, 0)
    
    def test_datastore_persistence(self):
        """Test that data persists across DataStore instances."""
        # Add a round
        holes = [4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.data_store.add_round(holes)
        
        # Create new DataStore instance with same file
        new_data_store = DataStore(self.temp_file.name)
        
        # Verify data was loaded
        self.assertEqual(new_data_store.player.current_level, 2)
        self.assertEqual(new_data_store.player.total_rounds, 1)
        self.assertEqual(len(new_data_store.player.rounds), 1)


class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_calculate_course_length(self):
        """Test course length calculation."""
        self.assertEqual(calculate_course_length(1), 225)
        self.assertEqual(calculate_course_length(2), 450)
        self.assertEqual(calculate_course_length(3), 900)
        self.assertEqual(calculate_course_length(4), 1350)
        self.assertEqual(calculate_course_length(5), 1800)
        self.assertEqual(calculate_course_length(6), 2250)
    
    def test_get_level_info(self):
        """Test level info generation."""
        level_info = get_level_info(1)
        self.assertEqual(level_info['level'], 1)
        self.assertEqual(level_info['total_yards'], 225)
        self.assertEqual(level_info['yards_per_hole'], 25.0)
        self.assertEqual(level_info['target_score'], 36)
        self.assertEqual(level_info['par_per_hole'], 4)
        
        # Test level 2 with new progression
        level_info_2 = get_level_info(2)
        self.assertEqual(level_info_2['total_yards'], 450)
        self.assertEqual(level_info_2['yards_per_hole'], 50.0)
    
    def test_validate_round_scores(self):
        """Test round score validation."""
        # Valid scores
        valid_scores = [4, 4, 4, 4, 4, 4, 4, 4, 4]
        is_valid, message = validate_round_scores(valid_scores)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid round")
        
        # Invalid - wrong number of holes
        wrong_count = [4, 4, 4, 4, 4, 4, 4, 4]  # Only 8 holes
        is_valid, message = validate_round_scores(wrong_count)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Must have exactly 9 hole scores")
        
        # Invalid - score out of range
        out_of_range = [4, 4, 4, 4, 4, 4, 4, 4, 11]  # Score > 10
        is_valid, message = validate_round_scores(out_of_range)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Hole 9 score must be between 1 and 10")


if __name__ == '__main__':
    unittest.main()