"""SQLAlchemy database models for Learn to Golf Tracker."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    rounds = db.relationship('Round', backref='user', cascade='all, delete-orphan', 
                           order_by='Round.played_at.desc()')
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class UserProfile(db.Model):
    """User profile with golf-specific data."""
    
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    current_level = db.Column(db.Integer, default=1, nullable=False)
    total_rounds = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_rounds_at_current_level(self):
        """Get number of rounds played at current level."""
        return Round.query.filter_by(
            user_id=self.user_id, 
            level=self.current_level
        ).count()
    
    def get_recent_rounds(self, limit=10):
        """Get recent rounds for this user."""
        return Round.query.filter_by(user_id=self.user_id)\
                          .order_by(Round.played_at.desc())\
                          .limit(limit).all()
    
    def get_average_score(self):
        """Calculate average score across all rounds."""
        rounds = Round.query.filter_by(user_id=self.user_id).all()
        if not rounds:
            return 0.0
        return sum(r.total for r in rounds) / len(rounds)
    
    def get_best_score(self):
        """Get the best (lowest) score."""
        best_round = Round.query.filter_by(user_id=self.user_id)\
                                .order_by(Round.total.asc())\
                                .first()
        return best_round.total if best_round else 0
    
    def add_round(self, holes):
        """Add a new round and handle level progression."""
        total = sum(holes)
        leveled_up = total <= 36
        
        # Create the round
        round_obj = Round(
            user_id=self.user_id,
            level=self.current_level,
            holes=holes,
            total=total,
            leveled_up=leveled_up
        )
        
        db.session.add(round_obj)
        
        # Update user profile
        self.total_rounds += 1
        
        # Level up if eligible and not at max level
        if leveled_up and self.current_level < 6:
            self.current_level += 1
        
        db.session.commit()
        return round_obj
    
    def __repr__(self):
        return f'<UserProfile user_id={self.user_id} level={self.current_level}>'


class Round(db.Model):
    """Individual golf round data."""
    
    __tablename__ = 'rounds'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    level = db.Column(db.Integer, nullable=False)
    holes = db.Column(db.JSON, nullable=False)  # Array of 9 hole scores
    total = db.Column(db.Integer, nullable=False)
    leveled_up = db.Column(db.Boolean, default=False)
    played_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def get_holes_list(self):
        """Get holes as a Python list (in case stored as JSON string)."""
        if isinstance(self.holes, str):
            return json.loads(self.holes)
        return self.holes
    
    def __repr__(self):
        return f'<Round user_id={self.user_id} total={self.total} level={self.level}>'


def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Create indexes for performance
        try:
            # Index on rounds for user queries
            db.engine.execute(
                'CREATE INDEX IF NOT EXISTS idx_rounds_user_played '
                'ON rounds(user_id, played_at DESC)'
            )
        except Exception:
            # Index might already exist
            pass