from datetime import datetime
from typing import List, Dict, Any
import json
import os

class Round:
    def __init__(self, holes: List[int], level: int, round_id: int = None):
        self.id = round_id or int(datetime.now().timestamp())
        self.date = datetime.now()
        self.level = level
        self.holes = holes
        self.total = sum(holes)
        self.leveled_up = self.total <= 36
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "level": self.level,
            "holes": self.holes,
            "total": self.total,
            "leveled_up": self.leveled_up
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Round':
        round_obj = cls(data["holes"], data["level"], data["id"])
        round_obj.date = datetime.fromisoformat(data["date"])
        round_obj.total = data["total"]
        round_obj.leveled_up = data["leveled_up"]
        return round_obj

class Player:
    def __init__(self):
        self.current_level = 1
        self.total_rounds = 0
        self.rounds = []
    
    def add_round(self, holes: List[int]) -> Round:
        round_obj = Round(holes, self.current_level)
        self.rounds.append(round_obj)
        self.total_rounds += 1
        
        if round_obj.leveled_up and self.current_level < 6:
            self.current_level += 1
        
        return round_obj
    
    def get_recent_rounds(self, limit: int = 10) -> List[Round]:
        return self.rounds[-limit:]
    
    def get_average_score(self) -> float:
        if not self.rounds:
            return 0.0
        return sum(r.total for r in self.rounds) / len(self.rounds)
    
    def get_best_score(self) -> int:
        if not self.rounds:
            return 0
        return min(r.total for r in self.rounds)
    
    def get_rounds_at_current_level(self) -> int:
        return sum(1 for r in self.rounds if r.level == self.current_level)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "current_level": self.current_level,
            "total_rounds": self.total_rounds,
            "rounds": [r.to_dict() for r in self.rounds]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        player = cls()
        player.current_level = data["current_level"]
        player.total_rounds = data["total_rounds"]
        player.rounds = [Round.from_dict(r) for r in data["rounds"]]
        return player

class DataStore:
    def __init__(self, filename: str = "player_data.json"):
        self.filename = filename
        self.player = self.load_player()
    
    def load_player(self) -> Player:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                return Player.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                return Player()
        return Player()
    
    def save_player(self):
        with open(self.filename, 'w') as f:
            json.dump(self.player.to_dict(), f, indent=2)
    
    def add_round(self, holes: List[int]) -> Round:
        round_obj = self.player.add_round(holes)
        self.save_player()
        return round_obj