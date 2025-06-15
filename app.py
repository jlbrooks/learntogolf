from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import DataStore
from utils import validate_round_scores, get_level_info

app = Flask(__name__)
data_store = DataStore()

@app.route('/')
def index():
    player = data_store.player
    level_info = get_level_info(player.current_level)
    recent_rounds = player.get_recent_rounds(5)
    
    return render_template('index.html', 
                         player=player, 
                         level_info=level_info,
                         recent_rounds=recent_rounds)

@app.route('/score', methods=['POST'])
def submit_score():
    try:
        # Extract hole scores from form data
        holes = []
        for i in range(1, 10):
            hole_score = request.form.get(f'hole{i}')
            if hole_score:
                holes.append(int(hole_score))
            else:
                return jsonify({'error': f'Missing score for hole {i}'}), 400
        
        # Validate the round
        is_valid, message = validate_round_scores(holes)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Add the round to the player's data
        round_obj = data_store.add_round(holes)
        
        # Check if this was a successful round (level up)
        if round_obj.leveled_up and data_store.player.current_level > round_obj.level:
            message = f'Congratulations! You shot {round_obj.total} and leveled up to Level {data_store.player.current_level}!'
        elif round_obj.total <= 36:
            message = f'Great round! You shot {round_obj.total} (Par or better).'
        else:
            message = f'Round completed with a score of {round_obj.total}. Keep practicing!'
        
        return jsonify({
            'success': True,
            'message': message,
            'total': round_obj.total,
            'leveled_up': round_obj.leveled_up,
            'new_level': data_store.player.current_level
        })
        
    except ValueError as e:
        return jsonify({'error': 'Invalid score values. Please enter numbers between 1 and 10.'}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing your round.'}), 500

if __name__ == '__main__':
    app.run(debug=True)