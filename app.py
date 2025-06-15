import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from db_models import db, User, UserProfile, Round
from auth import init_auth
from utils import validate_round_scores, get_level_info

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'postgresql+psycopg://localhost:5432/learntogolf_dev'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
init_auth(app)

@app.route('/')
@login_required
def index():
    # Get or create user profile
    profile = current_user.profile
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    # Get data for dashboard
    level_info = get_level_info(profile.current_level)
    recent_rounds = profile.get_recent_rounds(5)
    
    return render_template('index.html', 
                         player=profile, 
                         level_info=level_info,
                         recent_rounds=recent_rounds)

@app.route('/score', methods=['POST'])
@login_required
def submit_score():
    try:
        # Extract hole scores from form data
        holes = []
        for i in range(1, 10):
            hole_score = request.form.get(f'hole{i}')
            if hole_score is None or hole_score.strip() == '':
                return '''
                <div class="p-4 rounded-lg bg-red-50 border-l-4 border-red-500">
                    <p class="font-semibold text-red-600">Missing score for hole {}</p>
                    <p class="text-sm text-red-500 mt-1">Please enter a score for all 9 holes.</p>
                </div>
                '''.format(i), 400
            
            try:
                score = int(hole_score)
                if score < 1 or score > 10:
                    return '''
                    <div class="p-4 rounded-lg bg-red-50 border-l-4 border-red-500">
                        <p class="font-semibold text-red-600">Invalid score for hole {}</p>
                        <p class="text-sm text-red-500 mt-1">Scores must be between 1 and 10 strokes.</p>
                    </div>
                    '''.format(i), 400
                holes.append(score)
            except ValueError:
                return '''
                <div class="p-4 rounded-lg bg-red-50 border-l-4 border-red-500">
                    <p class="font-semibold text-red-600">Invalid score for hole {}</p>
                    <p class="text-sm text-red-500 mt-1">Please enter a valid number between 1 and 10.</p>
                </div>
                '''.format(i), 400
        
        # Validate the round (additional validation)
        is_valid, message = validate_round_scores(holes)
        if not is_valid:
            return '''
            <div class="p-4 rounded-lg bg-red-50 border-l-4 border-red-500">
                <p class="font-semibold text-red-600">Invalid Round</p>
                <p class="text-sm text-red-500 mt-1">{}</p>
            </div>
            '''.format(message), 400
        
        # Get user profile
        profile = current_user.profile
        if not profile:
            return '''
            <div class="p-4 rounded-lg bg-red-50 border-l-4 border-red-500">
                <p class="font-semibold text-red-600">Profile Error</p>
                <p class="text-sm text-red-500 mt-1">User profile not found. Please contact support.</p>
            </div>
            ''', 500
        
        # Add the round to the user's profile
        round_obj = profile.add_round(holes)
        
        # Generate success message
        if round_obj.leveled_up and profile.current_level > round_obj.level:
            message = f'Congratulations! You shot {round_obj.total} and leveled up to Level {profile.current_level}!'
        elif round_obj.total <= 36:
            message = f'Great round! You shot {round_obj.total} (Par or better).'
        else:
            message = f'Round completed with a score of {round_obj.total}. Keep practicing!'
        
        # Return HTML response for HTMX
        success_class = "text-green-600" if round_obj.total <= 36 else "text-blue-600"
        level_up_badge = ""
        if round_obj.leveled_up and profile.current_level > round_obj.level:
            level_up_badge = f'<span class="inline-block bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full ml-2">Level Up!</span>'
        
        return f'''
        <div class="p-4 rounded-lg bg-gray-50 border-l-4 border-green-500">
            <p class="font-semibold {success_class}">{message}{level_up_badge}</p>
        </div>
        '''
        
    except Exception as e:
        # Log the actual error for debugging
        print(f"Error processing score submission: {e}")
        return '''
        <div class="p-4 rounded-lg bg-red-50 border-l-4 border-red-500">
            <p class="font-semibold text-red-600">Unexpected Error</p>
            <p class="text-sm text-red-500 mt-1">An error occurred while processing your round. Please try again.</p>
        </div>
        ''', 500

@app.route('/progress')
@login_required
def get_progress():
    profile = current_user.profile
    level_info = get_level_info(profile.current_level)
    recent_rounds = profile.get_recent_rounds(5)
    
    return render_template('progress_section.html', 
                         player=profile, 
                         level_info=level_info,
                         recent_rounds=recent_rounds)

@app.route('/history')
@login_required
def get_history():
    profile = current_user.profile
    recent_rounds = profile.get_recent_rounds(10)
    
    return render_template('history_section.html', 
                         player=profile,
                         recent_rounds=recent_rounds)

@app.route('/stats')
@login_required
def get_stats():
    profile = current_user.profile
    
    # Calculate statistics
    par_or_better_count = Round.query.filter_by(user_id=current_user.id).filter(Round.total <= 36).count()
    level_ups = Round.query.filter_by(user_id=current_user.id, leveled_up=True).count()
    
    stats = {
        'total_rounds': profile.total_rounds,
        'average_score': profile.get_average_score(),
        'best_score': profile.get_best_score(),
        'current_level': profile.current_level,
        'rounds_at_current_level': profile.get_rounds_at_current_level(),
        'par_or_better_count': par_or_better_count,
        'level_ups': level_ups
    }
    
    return render_template('stats_section.html', stats=stats)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please enter both email and password.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])  
def register():
    """User registration page."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not email or not password:
            flash('Please enter both email and password.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'error')
            return render_template('register.html')
        
        try:
            # Create new user
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            # Create user profile
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)
            db.session.commit()
            
            # Log in the user
            login_user(user)
            flash('Account created successfully! Welcome to Learn to Golf Tracker.', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)